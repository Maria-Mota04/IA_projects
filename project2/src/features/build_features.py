import pandas as pd


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create additional meaningful features to improve model performance.

    This method generates new derived variables from existing data in order
    to better capture business relationships that are not explicitly represented
    in the raw dataset.

    Feature engineering helps machine learning models by:
    - exposing hidden patterns
    - improving predictive power
    - reducing reliance on raw noisy variables
    """

    df = df.copy()

    if "custo_total_transporte_eur" in df.columns and "n_atores_total" in df.columns:
        df["custo_transporte_por_ator"] = df["custo_total_transporte_eur"] / (
            df["n_atores_total"] + 1
        )

    if "total_pessoas_equipa" in df.columns and "custo_total_tecnica_eur" in df.columns:
        df["custo_tecnico_por_pessoa"] = df["custo_total_tecnica_eur"] / (
            df["total_pessoas_equipa"] + 1
        )

    if "distancia_km" in df.columns:
        df["custo_km_estimado"] = df["distancia_km"] * df.get(
            "custo_combustivel_eur", 1
        )

    return df
