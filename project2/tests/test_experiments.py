import numpy as np
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier

from src.models.ablation_runner import run_ablation_experiments
from src.models.experiment_results import summarize_results
from src.models.experiments import EXPERIMENTS
from src.features.feature_utils import remove_columns
from src.models.model_evaluator import ModelEvaluator

@pytest.fixture
def sample_data():
    feature_names = [
        "a", "b", "c", "d", "e",
        # no_binary
        "tem_portagens", "precisa_carrinha", "precisa_autocarro_privado",
        "tem_cenario_grande", "tem_costureira", "tem_maquilhagem",
        "catering_pago_pelo_cliente", "alojamento_pago_pelo_cliente",
        "tem_sistema_proprio", "marketing_pago_pelo_espaco",
        # no_aggregated_costs
        "custo_total_transporte_eur", "custo_total_cenario_eur",
        "custo_total_figurinos_eur", "custo_total_tecnica_eur",
        "custo_total_alimentacao_alojamento_eur", "custo_total_eur",
        # no_geo_time
        "data_espetaculo", "regiao_geografica", "local_evento",
    ]

    X = np.random.rand(10, len(feature_names))
    y = np.random.randint(0, 2, 10)

    return X, y, feature_names


def test_experiments_defined():
    assert isinstance(EXPERIMENTS, dict)
    assert "baseline" in EXPERIMENTS
    assert isinstance(EXPERIMENTS["baseline"], list)


def test_remove_columns_shape(sample_data):
    X, y, feature_names = sample_data

    X_new, new_names = remove_columns(
        X, ["tem_portagens", "custo_total_eur"], feature_names
    )

    assert X_new.shape[1] == len(new_names)
    assert "tem_portagens" not in new_names
    assert "custo_total_eur" not in new_names


def test_remove_columns_accepts_dataframes(sample_data):
    X, _, feature_names = sample_data
    X_df = pd.DataFrame(X, columns=feature_names)

    X_new, new_names = remove_columns(
        X_df, ["tem_portagens", "custo_total_eur"], feature_names
    )

    assert isinstance(X_new, pd.DataFrame)
    assert X_new.shape[1] == len(new_names)
    assert "tem_portagens" not in X_new.columns
    assert "custo_total_eur" not in X_new.columns


def test_baseline_identity(sample_data):
    X, y, feature_names = sample_data

    X_new, new_names = remove_columns(X, EXPERIMENTS["baseline"], feature_names)

    assert X.shape == X_new.shape
    assert feature_names == new_names


def test_all_experiment_columns_valid(sample_data):
    _, _, feature_names = sample_data

    all_features = set(feature_names)

    for exp, cols in EXPERIMENTS.items():
        for c in cols:
            assert c in all_features, f"{c} not in dataset for experiment {exp}"


def test_no_duplicate_columns(sample_data):
    X, _, feature_names = sample_data

    for exp, cols in EXPERIMENTS.items():
        _, new_names = remove_columns(X, cols, feature_names)

        assert len(new_names) == len(set(new_names))

def test_run_ablation_experiments_returns_metrics(sample_data):
    X, y, feature_names = sample_data

    results = run_ablation_experiments(
        DecisionTreeClassifier(random_state=42),
        X,
        X,
        y,
        y,
        feature_names,
        ModelEvaluator(),
    )

    assert set(results) == set(EXPERIMENTS)
    assert all("F1" in metrics for metrics in results.values())


def test_summarize_results_writes_csv_without_predictions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    results = {
        "baseline": {
            "Accuracy": 0.8,
            "F1": 0.75,
            "y_pred": np.array([0, 1, 1]),
        }
    }

    df = summarize_results(results)
    output_path = tmp_path / "outputs" / "experiments" / "results.csv"

    assert output_path.exists()
    assert df.loc[0, "experiment"] == "baseline"
    assert "y_pred" not in df.columns
