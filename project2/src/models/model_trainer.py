from sklearn.base import clone
import pandas as pd

from src.models.model_registry import get_model_registry
from src.models.model_evaluator import ModelEvaluator
from src.models.model_selector import ModelSelector
from src.models.model_persistence import ModelPersistence
from src.utils.logger import get_logger


class ModelTrainer:
    """
    Trains multiple ML models.
    """

    def __init__(self):
        self.registry = get_model_registry()
        self.fitted_models = {}
        self.results = []
        self.logger = get_logger(__name__)

    def _get_scores(self, model, X_test):
        """
        Return probability or decision scores when available.
        """

        if hasattr(model, "predict_proba"):
            return model.predict_proba(X_test)[:, 1]

        if hasattr(model, "decision_function"):
            return model.decision_function(X_test)

        return None

    def train_all(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
    ):
        self.results = []
        self.fitted_models = {}

        for name, model in self.registry.items():
            self.logger.info(f"Training {name}")

            estimator = clone(model)

            # KMeans is unsupervised
            if name == "KMeans":
                estimator.fit(X_train)
            else:
                estimator.fit(X_train, y_train)

            y_pred = estimator.predict(X_test)

            # Fix inverted cluster labels for KMeans
            if name == "KMeans":
                acc_normal = (y_pred == y_test).mean()
                acc_inverted = ((1 - y_pred) == y_test).mean()

                if acc_inverted > acc_normal:
                    y_pred = 1 - y_pred

            y_score = self._get_scores(
                estimator,
                X_test,
            )

            evaluator = ModelEvaluator()

            metrics = evaluator.evaluate(
                estimator,
                X_test,
                y_test,
                name=name,
            )
            metrics["Model"] = name

            self.results.append(metrics)
            self.fitted_models[name] = estimator

        return pd.DataFrame(self.results).sort_values(
            by="F1",
            ascending=False,
        )

    def get_best_model(self, results_df):
        selector = ModelSelector(metric="F1")

        best_name = selector.select_best(results_df)

        if best_name is None:
            return None

        return self.fitted_models[best_name]

    def save_best(self, model, path):
        ModelPersistence.save(model, path)
