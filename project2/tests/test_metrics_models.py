import os
import sys
import tempfile

import numpy as np
import pandas as pd
import pytest
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.model_evaluator import ModelEvaluator
from src.models.model_selector import ModelSelector
from src.models.model_trainer import ModelTrainer
from src.models.model_registry import get_model_registry
from src.models.model_persistence import ModelPersistence


# ------------------------------------------------------------------
# FIXTURES
# ------------------------------------------------------------------

@pytest.fixture
def binary_dataset():
    """Simple separable binary classification dataset."""
    X, y = make_classification(
        n_samples=100,
        n_features=5,
        n_informative=3,
        n_redundant=1,
        random_state=42,
    )
    split = 80
    return (
        pd.DataFrame(X[:split], columns=[f"f{i}" for i in range(5)]),
        pd.DataFrame(X[split:], columns=[f"f{i}" for i in range(5)]),
        pd.Series(y[:split]),
        pd.Series(y[split:]),
    )


@pytest.fixture
def perfect_model():
    """Model trained on linearly separable data — should score ~1.0."""
    X_train = np.array([[0], [1], [2], [3], [4], [5]])
    y_train = np.array([0, 0, 0, 1, 1, 1])
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model, np.array([[0.5], [1.5], [3.5], [4.5]]), np.array([0, 0, 1, 1])


@pytest.fixture
def results_df():
    return pd.DataFrame({
        "Model": ["Logistic Regression", "Decision Tree", "Random Forest", "SVM", "Gradient Boosting", "AdaBoost"],
        "Accuracy": [0.85, 0.80, 0.92, 0.88, 0.90, 0.87],
        "Precision": [0.84, 0.79, 0.91, 0.87, 0.89, 0.86],
        "Recall":    [0.85, 0.80, 0.92, 0.88, 0.90, 0.87],
        "F1":        [0.84, 0.79, 0.91, 0.87, 0.89, 0.86],
        "ROC_AUC":   [0.91, 0.85, 0.97, 0.93, 0.95, 0.92],
    })


# ------------------------------------------------------------------
# ModelEvaluator — metric values
# ------------------------------------------------------------------

class TestModelEvaluatorMetricValues:

    def test_perfect_predictions_give_accuracy_one(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert metrics["Accuracy"] == pytest.approx(1.0)

    def test_perfect_predictions_give_f1_one(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert metrics["F1"] == pytest.approx(1.0)

    def test_metrics_are_between_zero_and_one(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        for key in ["Accuracy", "Precision", "Recall", "F1"]:
            assert 0.0 <= metrics[key] <= 1.0, f"{key} out of range"

    def test_roc_auc_returned_for_model_with_predict_proba(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert metrics["ROC_AUC"] is not None
        assert 0.0 <= metrics["ROC_AUC"] <= 1.0

    def test_confusion_matrix_shape_is_2x2(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert metrics["confusion_matrix"].shape == (2, 2)

    def test_confusion_matrix_sum_equals_n_samples(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert metrics["confusion_matrix"].sum() == len(y_test)

    def test_y_pred_length_matches_test_set(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert len(metrics["y_pred"]) == len(y_test)

    def test_model_name_stored_in_metrics(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test, name="MyModel")
        assert metrics["Model"] == "MyModel"

    def test_weighted_average_used_by_default(self):
        evaluator = ModelEvaluator()
        assert evaluator.average == "weighted"

    def test_custom_average_accepted(self):
        evaluator = ModelEvaluator(average="macro")
        assert evaluator.average == "macro"

    def test_all_required_keys_present(self, perfect_model):
        model, X_test, y_test = perfect_model
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X_test, y_test)
        for key in ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC_AUC", "confusion_matrix", "y_pred"]:
            assert key in metrics, f"Missing key: {key}"


# ------------------------------------------------------------------
# ModelEvaluator — edge cases
# ------------------------------------------------------------------

class TestModelEvaluatorEdgeCases:

    @pytest.mark.filterwarnings(
        "ignore:Only one class is present in y_true:sklearn.exceptions.UndefinedMetricWarning"
    )
    def test_roc_auc_is_none_or_nan_when_only_one_class_in_test(self):
        """ROC AUC is undefined when test set has a single class — returns None or NaN."""
        X = np.array([[0], [1], [2], [3]])
        y_train = np.array([0, 0, 1, 1])
        y_test_single_class = np.array([0, 0, 0, 0])

        model = LogisticRegression()
        model.fit(X, y_train)

        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate(model, X, y_test_single_class)
        # ROC AUC is either None or NaN when only one class is present
        roc = metrics["ROC_AUC"]
        assert roc is None or (isinstance(roc, float) and np.isnan(roc))

    def test_zero_division_does_not_raise(self):
        """Precision/Recall should not raise even if a class is never predicted."""
        # Use a model trained on two classes but that always predicts one class
        X_train = np.array([[0], [1], [2], [3], [10], [11]])
        y_train = np.array([0, 0, 0, 1, 1, 1])
        X_test = np.array([[0], [1]])
        y_test = np.array([0, 1])

        model = DecisionTreeClassifier(max_depth=1, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator()
        # should not raise
        metrics = evaluator.evaluate(model, X_test, y_test)
        assert "Precision" in metrics

    def test_roc_auc_uses_decision_function_when_probabilities_unavailable(self):
        X_train = np.array([[0], [1], [2], [3], [4], [5]])
        y_train = np.array([0, 0, 0, 1, 1, 1])
        X_test = np.array([[0.5], [1.5], [3.5], [4.5]])
        y_test = np.array([0, 0, 1, 1])

        model = LinearSVC(random_state=42)
        model.fit(X_train, y_train)

        metrics = ModelEvaluator().evaluate(model, X_test, y_test)

        assert metrics["ROC_AUC"] == pytest.approx(1.0)


# ------------------------------------------------------------------
# ModelSelector
# ------------------------------------------------------------------

class TestModelSelector:

    def test_selects_model_with_highest_f1(self, results_df):
        selector = ModelSelector(metric="F1")
        best = selector.select_best(results_df)
        assert best == "Random Forest"

    def test_selects_model_with_highest_accuracy(self, results_df):
        selector = ModelSelector(metric="Accuracy")
        best = selector.select_best(results_df)
        assert best == "Random Forest"

    def test_selects_model_with_highest_roc_auc(self, results_df):
        selector = ModelSelector(metric="ROC_AUC")
        best = selector.select_best(results_df)
        assert best == "Random Forest"

    def test_returns_none_for_empty_dataframe(self):
        selector = ModelSelector()
        assert selector.select_best(pd.DataFrame()) is None

    def test_returns_none_when_metric_column_missing(self, results_df):
        selector = ModelSelector(metric="NonExistentMetric")
        assert selector.select_best(results_df) is None

    def test_returns_none_when_all_metric_values_are_nan(self):
        df = pd.DataFrame({"Model": ["A", "B"], "F1": [float("nan"), float("nan")]})
        selector = ModelSelector(metric="F1")
        assert selector.select_best(df) is None

    def test_handles_single_model(self):
        df = pd.DataFrame({"Model": ["OnlyModel"], "F1": [0.75]})
        selector = ModelSelector(metric="F1")
        assert selector.select_best(df) == "OnlyModel"

    def test_default_metric_is_f1(self):
        selector = ModelSelector()
        assert selector.metric == "F1"

    def test_tied_f1_returns_a_valid_model(self, results_df):
        """When two models tie, one of them should still be returned."""
        df = pd.DataFrame({"Model": ["A", "B"], "F1": [0.90, 0.90]})
        selector = ModelSelector(metric="F1")
        result = selector.select_best(df)
        assert result in ["A", "B"]


# ------------------------------------------------------------------
# ModelRegistry
# ------------------------------------------------------------------

class TestModelRegistry:

    def test_registry_returns_dict(self):
        registry = get_model_registry()
        assert isinstance(registry, dict)

    def test_registry_has_expected_models(self):
        registry = get_model_registry()
        expected = {
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "SVM",
            "Gradient Boosting",
            "AdaBoost",
        }
        assert set(registry.keys()) == expected

    def test_registry_does_not_contain_kmeans(self):
        from sklearn.cluster import KMeans
        registry = get_model_registry()
        for model in registry.values():
            assert not isinstance(model, KMeans), "KMeans should not be in the registry"

    def test_all_models_are_classifiers(self):
        from sklearn.base import is_classifier
        registry = get_model_registry()
        for name, model in registry.items():
            assert is_classifier(model), f"{name} is not a classifier"

    def test_all_models_have_fit_and_predict(self):
        registry = get_model_registry()
        for name, model in registry.items():
            assert hasattr(model, "fit"), f"{name} missing fit()"
            assert hasattr(model, "predict"), f"{name} missing predict()"

    def test_all_models_support_predict_proba(self):
        registry = get_model_registry()
        for name, model in registry.items():
            assert hasattr(model, "predict_proba"), f"{name} missing predict_proba()"

    def test_all_models_include_scaler_in_pipeline(self):
        registry = get_model_registry()
        for name, model in registry.items():
            assert isinstance(model, Pipeline), f"{name} is not a Pipeline"
            assert isinstance(model.steps[0][1], StandardScaler)

    def test_registry_returns_new_instances_each_call(self):
        r1 = get_model_registry()
        r2 = get_model_registry()
        assert r1["Random Forest"] is not r2["Random Forest"]


# ------------------------------------------------------------------
# ModelTrainer
# ------------------------------------------------------------------

class TestModelTrainer:

    def test_train_all_returns_dataframe(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        assert isinstance(results, pd.DataFrame)

    def test_train_all_has_one_row_per_model(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        assert len(results) == len(get_model_registry())

    def test_train_all_sorted_by_f1_descending(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        f1_values = results["F1"].tolist()
        assert f1_values == sorted(f1_values, reverse=True)

    def test_train_all_results_contain_required_columns(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        for col in ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC_AUC"]:
            assert col in results.columns, f"Missing column: {col}"

    def test_fitted_models_stored_after_training(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        trainer.train_all(X_train, y_train, X_test, y_test)
        assert len(trainer.fitted_models) == len(get_model_registry())

    def test_fitted_models_can_predict(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        trainer.train_all(X_train, y_train, X_test, y_test)
        for name, model in trainer.fitted_models.items():
            preds = model.predict(X_test)
            assert len(preds) == len(y_test), f"{name} prediction length mismatch"

    def test_get_best_model_returns_fitted_model(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        best = trainer.get_best_model(results)
        assert best is not None
        assert hasattr(best, "predict")

    def test_get_best_model_returns_none_for_empty_results(self):
        trainer = ModelTrainer()
        result = trainer.get_best_model(pd.DataFrame())
        assert result is None

    def test_accuracy_values_between_zero_and_one(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        results = trainer.train_all(X_train, y_train, X_test, y_test)
        assert (results["Accuracy"] >= 0).all()
        assert (results["Accuracy"] <= 1).all()

    def test_train_all_resets_state_on_second_call(self, binary_dataset):
        X_train, X_test, y_train, y_test = binary_dataset
        trainer = ModelTrainer()
        trainer.train_all(X_train, y_train, X_test, y_test)
        results2 = trainer.train_all(X_train, y_train, X_test, y_test)
        assert len(results2) == len(get_model_registry())


# ------------------------------------------------------------------
# ModelPersistence
# ------------------------------------------------------------------

class TestModelPersistence:

    def test_save_and_load_returns_same_model_type(self):
        model = LogisticRegression()
        model.fit([[0], [1]], [0, 1])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.pkl"
            ModelPersistence.save(model, path)
            loaded = ModelPersistence.load(path)
            assert type(loaded) == type(model)

    def test_loaded_model_makes_same_predictions(self):
        X = np.array([[0], [1], [2], [3]])
        y = np.array([0, 0, 1, 1])
        model = LogisticRegression()
        model.fit(X, y)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.pkl"
            ModelPersistence.save(model, path)
            loaded = ModelPersistence.load(path)
            np.testing.assert_array_equal(model.predict(X), loaded.predict(X))

    def test_save_creates_parent_directories(self):
        model = LogisticRegression()
        model.fit([[0], [1]], [0, 1])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nested" / "dir" / "model.pkl"
            ModelPersistence.save(model, path)
            assert path.exists()

    def test_load_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            ModelPersistence.load(Path("nonexistent/model.pkl"))
