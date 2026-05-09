import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.preprocess import Preprocessor


def _base_df(rows=20):
    data = {
        "id": list(range(1, rows + 1)),
        "companhia": ["CompA"] * rows,
        "espetaculo": ["ShowA"] * rows,
        "lucro_prejuizo": [100 if i % 2 == 0 else -50 for i in range(rows)],
        "margem_pct": [0.1] * rows,
        "receita_real": [1000] * rows,
        "custo_total_transporte_eur": [200.0 + i for i in range(rows)],
        "n_atores_total": [4] * rows,
        "total_pessoas_equipa": [8] * rows,
        "custo_total_tecnica_eur": [400.0 + i for i in range(rows)],
        "distancia_km": [10.0 + i for i in range(rows)],
        "custo_combustivel_eur": [1.5] * rows,
        "cidade": ["Porto" if i % 2 == 0 else None for i in range(rows)],
        "fez_publicidade": [True if i % 2 == 0 else False for i in range(rows)],
    }
    return pd.DataFrame(data)


def test_clean_drops_leakage_columns():
    df = _base_df()
    pre = Preprocessor(df)

    pre.clean()

    assert "id" not in pre.df.columns
    assert "companhia" not in pre.df.columns
    assert "espetaculo" not in pre.df.columns
    assert "lucro_prejuizo" not in pre.df.columns
    assert "margem_pct" not in pre.df.columns
    assert "receita_real" not in pre.df.columns


def test_create_target_from_lucro_prejuizo():
    df = _base_df()
    pre = Preprocessor(df)

    pre.create_target()

    assert "teve_lucro" in pre.df.columns
    assert set(pre.df["teve_lucro"].unique()) == {0, 1}
    assert pre.df.loc[0, "teve_lucro"] == 1
    assert pre.df.loc[1, "teve_lucro"] == 0


def test_handle_missing_fills_numeric_and_categorical():
    df = _base_df()
    df.loc[0, "custo_total_transporte_eur"] = None
    df.loc[1, "cidade"] = None

    pre = Preprocessor(df)
    pre.handle_missing()

    assert pre.df["custo_total_transporte_eur"].isna().sum() == 0
    assert pre.df["cidade"].isna().sum() == 0
    assert "Unknown" in set(pre.df["cidade"].unique())


def test_convert_types_boolean_to_int():
    df = _base_df()
    pre = Preprocessor(df)

    pre.convert_types()

    assert str(pre.df["fez_publicidade"].dtype) in {"int64", "int32", "int"}
    assert set(pre.df["fez_publicidade"].unique()) == {0, 1}


def test_feature_engineering_creates_expected_columns():
    df = _base_df()
    pre = Preprocessor(df)

    pre.feature_engineering()

    assert "custo_transporte_por_ator" in pre.df.columns
    assert "custo_tecnico_por_pessoa" in pre.df.columns
    assert "custo_km_estimado" in pre.df.columns


def test_encode_applies_one_hot_drop_first():
    df = _base_df()
    df["cidade"] = ["Porto" if i % 2 == 0 else "Lisboa" for i in range(len(df))]
    pre = Preprocessor(df)

    pre.encode()

    assert "cidade" not in pre.df.columns
    encoded_city_cols = [c for c in pre.df.columns if c.startswith("cidade_")]
    assert len(encoded_city_cols) >= 1


def test_split_returns_stratified_partitions():
    df = _base_df()
    pre = Preprocessor(df)
    pre.create_target()
    pre.clean()
    pre.handle_missing()
    pre.convert_types()
    pre.feature_engineering()
    pre.encode()

    X_train, X_test, y_train, y_test = pre.split()

    assert len(X_train) == 16
    assert len(X_test) == 4
    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}


def test_run_executes_pipeline_and_splits_when_target_exists():
    df = _base_df()
    df["teve_lucro"] = (df["lucro_prejuizo"] > 0).astype(int)

    pre = Preprocessor(df)
    X_train, X_test, y_train, y_test = pre.run()

    assert len(X_train) == 16
    assert len(X_test) == 4
    assert len(y_train) == 16
    assert len(y_test) == 4
