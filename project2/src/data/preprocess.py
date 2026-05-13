import pandas as pd
from sklearn.model_selection import train_test_split

from src.features.build_features import add_engineered_features


class Preprocessor:
    """
    Handles full preprocessing pipeline:
    - cleaning
    - feature engineering
    - encoding
    - split
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean(self):
        cols_to_drop = [
            "id",
            "companhia",
            "espetaculo",
            "margem_pct",
            "receita_real",
        ]

        self.df = self.df.drop(
            columns=[c for c in cols_to_drop if c in self.df.columns],
            errors="ignore",
        )

        return self

    def create_target(self):
        """
        Create binary classification target.
        """

        self.df["teve_lucro"] = (self.df["lucro_prejuizo"] > 0).astype(int)

        return self

    def handle_missing(self):
        """
        Handle missing values.
        """

        num_cols = self.df.select_dtypes(include=["int64", "float64"]).columns

        cat_cols = self.df.select_dtypes(include=["object", "bool"]).columns

        for col in num_cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())

        for col in cat_cols:
            self.df[col] = self.df[col].fillna("Unknown")

        return self

    def convert_types(self):
        """
        Convert boolean columns to integers.
        """

        bool_cols = self.df.select_dtypes(include=["bool"]).columns

        for col in bool_cols:
            self.df[col] = self.df[col].astype(int)

        return self

    def feature_engineering(self):
        """
        Apply engineered features.
        """

        self.df = add_engineered_features(self.df)

        return self

    def encode(self):
        """
        One-hot encode categorical features.
        """

        cat_cols = self.df.select_dtypes(include=["object"]).columns

        self.df = pd.get_dummies(
            self.df,
            columns=cat_cols,
            drop_first=True,
        )

        return self

    def split(self):
        """
        Split dataset into train and test sets.
        """

        X = self.df.drop(columns=["teve_lucro"])
        y = self.df["teve_lucro"]

        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

    def run(self):
        self.create_target()
        self.clean()
        self.handle_missing()
        self.convert_types()
        self.feature_engineering()
        self.encode()

        if "teve_lucro" not in self.df.columns:
            raise ValueError("Target column missing after preprocessing")

        return self.split()
