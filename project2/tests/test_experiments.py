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
        "a",
        "b",
        "c",
        "d",
        "e",
        "tem_portagens",
        "precisa_carrinha",
        "custo_total_eur",
        "local_evento",
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
