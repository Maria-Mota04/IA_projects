import numpy as np
import pandas as pd
import pytest

from src.features.feature_utils import keep_columns, remove_columns
from src.models.ablation_runner import apply_experiment, run_ablation_experiments
from src.models.experiment_results import summarize_results
from src.models.experiments import EXPERIMENTS
from src.models.model_trainer import ModelTrainer


@pytest.fixture
def sample_data():
    feature_names = [
        "distancia_km",
        "n_atores_total",
        "n_atores_residentes",
        "n_atores_externos",
        "n_tecnicos",
        "total_pessoas_equipa",
        "peso_cenario_kg",
        "n_figurinos",
        "dias_deslocacao",
        "lotacao_espaco",
        "receita_esperada",
        "percentagem_imprevistos",
        "tem_portagens",
        "precisa_carrinha",
        "precisa_autocarro_privado",
        "tem_cenario_grande",
        "tem_costureira",
        "tem_maquilhagem",
        "catering_pago_pelo_cliente",
        "alojamento_pago_pelo_cliente",
        "precisa_alojamento",
        "tem_sistema_proprio",
        "marketing_pago_pelo_espaco",
        "custo_total_transporte_eur",
        "custo_total_cenario_eur",
        "custo_total_figurinos_eur",
        "custo_total_tecnica_eur",
        "custo_total_alimentacao_alojamento_eur",
        "custo_total_eur",
        "lucro_estimado_eur",
        "mes_espetaculo",
        "dia_semana_espetaculo",
        "ano_espetaculo",
        "local_evento_Porto",
        "regiao_geografica_Norte",
        "tipo_espetaculo_musical",
        "tipo_contrato_misto",
        "tipo_local_festival",
    ]
    X = pd.DataFrame(np.random.rand(30, len(feature_names)), columns=feature_names)
    y = pd.Series([0, 1] * 15)

    return X, y, feature_names


def test_experiments_defined():
    assert isinstance(EXPERIMENTS, dict)
    assert set(EXPERIMENTS) == {
        "baseline",
        "no_binary",
        "no_aggregated_costs",
        "no_geo_time",
        "structural_only",
    }
    assert EXPERIMENTS["baseline"]["drop"] == []
    assert EXPERIMENTS["baseline"]["keep"] is None


def test_remove_columns_accepts_prefixes_and_dataframes(sample_data):
    X, _, feature_names = sample_data

    X_new, new_names = remove_columns(
        X,
        ["tem_portagens", "local_evento_"],
        feature_names,
    )

    assert isinstance(X_new, pd.DataFrame)
    assert X_new.shape[1] == len(new_names)
    assert "tem_portagens" not in new_names
    assert "local_evento_Porto" not in new_names


def test_keep_columns_accepts_prefixes(sample_data):
    X, _, feature_names = sample_data

    X_new, new_names = keep_columns(
        X,
        ["distancia_km", "tipo_espetaculo_"],
        feature_names,
    )

    assert list(X_new.columns) == ["distancia_km", "tipo_espetaculo_musical"]
    assert new_names == ["distancia_km", "tipo_espetaculo_musical"]


def test_apply_experiment_baseline_keeps_all_features(sample_data):
    X, _, feature_names = sample_data

    X_new, new_names = apply_experiment(
        X,
        EXPERIMENTS["baseline"],
        feature_names,
    )

    assert X_new.shape == X.shape
    assert new_names == feature_names


def test_apply_experiment_removes_aggregated_costs(sample_data):
    X, _, feature_names = sample_data

    _, new_names = apply_experiment(
        X,
        EXPERIMENTS["no_aggregated_costs"],
        feature_names,
    )

    assert "custo_total_eur" not in new_names
    assert "lucro_estimado_eur" not in new_names


def test_apply_experiment_structural_only_removes_cost_outputs(sample_data):
    X, _, feature_names = sample_data

    _, new_names = apply_experiment(
        X,
        EXPERIMENTS["structural_only"],
        feature_names,
    )

    assert "distancia_km" in new_names
    assert "tipo_contrato_misto" in new_names
    assert "custo_total_eur" not in new_names
    assert "tem_portagens" not in new_names


def test_run_ablation_experiments_returns_results_for_each_experiment(sample_data):
    X, y, feature_names = sample_data

    results, fitted_models, selected_features = run_ablation_experiments(
        ModelTrainer,
        X,
        X,
        y,
        y,
        feature_names,
    )

    assert set(results) == set(EXPERIMENTS)
    assert set(fitted_models) == set(EXPERIMENTS)
    assert set(selected_features) == set(EXPERIMENTS)
    assert all("F1" in df.columns for df in results.values())


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
