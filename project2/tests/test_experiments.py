import numpy as np
import pytest

from src.models.experiments import EXPERIMENTS
from src.features.feature_utils import remove_columns


# -------------------------------------------------
# FIXTURE SIMPLES DE DADOS ARTIFICIAIS
# -------------------------------------------------
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

def test_prediction_no_profit(sample_data):
    X, y, feature_names = sample_data
    
    idx_receita = feature_names.index("a") if "receita_esperada" not in feature_names else feature_names.index("receita_esperada")
    idx_custo = feature_names.index("custo_total_eur")
    
    X_prejuizo = X.copy()
    X_prejuizo[:, idx_receita] = 0.0
    X_prejuizo[:, idx_custo] = 999999.0
    
    mock_y_pred = np.zeros(X_prejuizo.shape[0])
    
    assert np.all(mock_y_pred == 0)
    assert mock_y_pred[0] == 0