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
        """
        Remove irrelevant + leakage columns.
        """

        cols_to_drop = [
            "id",
            "companhia",
            "espetaculo",
            "lucro_prejuizo",
            "margem_pct",
            "receita_real",
        ]

        self.df = self.df.drop(
            columns=[c for c in cols_to_drop if c in self.df.columns], errors="ignore"
        )

        return self

    def create_target(self):
        """
        Create the classification target variable for the model.

        This method generates a binary target column called `teve_lucro`,
        which indicates whether a given event (performance) was profitable or not.

        The target is derived from the column `lucro_prejuizo`:
            - 1 (True)  → if profit > 0 (the event made a profit)
            - 0 (False) → if profit <= 0 (the event did not make a profit)

        This transformation converts a continuous financial outcome into a
        classification problem, enabling the use of supervised learning
        algorithms for binary classification.

        Returns:
            self: The updated Preprocessor instance with the target column added.
        """

        self.df["teve_lucro"] = (self.df["lucro_prejuizo"] > 0).astype(int)

        return self

    def handle_missing(self):
        """
        Handle missing values in the dataset.

        This method ensures that the dataset contains no missing values,
        which is required by most machine learning algorithms.

        Strategy:
        - Numerical features: missing values are replaced with the median
        of each column, as it is robust to outliers and skewed distributions.
        - Categorical and boolean features: missing values are replaced
        with the string "Unknown", preserving them as a separate category
        instead of discarding information.

        This approach maintains dataset integrity while avoiding data loss,
        ensuring compatibility with downstream machine learning models.

        Returns:
            self: The updated Preprocessor instance with no missing values.
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
        Convert boolean columns to integer format.

        This method ensures that all boolean features in the dataset
        are converted into a numerical representation (0 and 1),
        which is required by most machine learning algorithms.

        Returns:
            self: The updated Preprocessor instance with standardized data types.
        """

        bool_cols = self.df.select_dtypes(include=["bool"]).columns

        for col in bool_cols:
            self.df[col] = self.df[col].astype(int)

        return self

    def feature_engineering(self):
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

        self.df = add_engineered_features(self.df)

        return self

    def encode(self):
        """
        Convert categorical variables into numerical format using one-hot encoding.

        This step transforms text-based categorical features into binary indicator
        columns so that machine learning models can interpret them.

        We use drop_first=True to avoid multicollinearity (dummy variable trap).
        """

        cat_cols = self.df.select_dtypes(include=["object"]).columns  # object = text

        self.df = pd.get_dummies(
            self.df, columns=cat_cols, drop_first=True
        )  # to avoid redundancy

        return self

    def split(self):
        """
        Split dataset into features (X) and target (y),
        then create training and testing sets.

        The target variable is 'teve_lucro', which indicates
        whether an event was profitable or not.
        """

        X = self.df.drop(columns=["teve_lucro"])

        y = self.df["teve_lucro"]

        return train_test_split(
            X,
            y,
            test_size=0.2,  # 80% train, 20% test
            random_state=42,  # guarantees always the same split
            stratify=y,  # guarantees that the train and test data maintain class distribuition, according to target
        )

    def run(self):
        """
        Execute the full preprocessing pipeline in the correct order.

        Steps:
        1. Clean dataset
        2. Handle missing values
        3. Convert data types
        4. Create new features
        5. Encode categorical variables
        6. Split into train/test sets

        Returns:
            Train and test sets ready for machine learning.
        """

        self.clean()
        self.handle_missing()
        self.convert_types()
        self.feature_engineering()
        self.encode()

        return self.split()
