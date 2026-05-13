import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.features.build_features import add_engineered_features


def test_add_engineered_features_creates_transport_feature():
    df = pd.DataFrame(
        {
            "custo_total_transporte_eur": [120.0, 60.0],
            "n_atores_total": [2, 1],
        }
    )

    result = add_engineered_features(df)

    assert "custo_transporte_por_ator" in result.columns
    assert result.loc[0, "custo_transporte_por_ator"] == 120.0 / 3


def test_add_engineered_features_creates_technical_feature():
    df = pd.DataFrame(
        {
            "total_pessoas_equipa": [4, 1],
            "custo_total_tecnica_eur": [100.0, 20.0],
        }
    )

    result = add_engineered_features(df)

    assert "custo_tecnico_por_pessoa" in result.columns
    assert result.loc[0, "custo_tecnico_por_pessoa"] == 100.0 / 5


def test_add_engineered_features_uses_default_fuel_cost_when_missing():
    df = pd.DataFrame({"distancia_km": [10.0, 15.0]})

    result = add_engineered_features(df)

    assert "custo_km_estimado" in result.columns
    assert result.loc[0, "custo_km_estimado"] == 10.0
    assert result.loc[1, "custo_km_estimado"] == 15.0


def test_add_engineered_features_preserves_original_df():
    df = pd.DataFrame(
        {
            "distancia_km": [10.0],
            "custo_combustivel_eur": [2.0],
        }
    )

    result = add_engineered_features(df)

    assert "custo_km_estimado" not in df.columns
    assert "custo_km_estimado" in result.columns
    assert result.loc[0, "custo_km_estimado"] == 20.0
