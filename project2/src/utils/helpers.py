from sklearn.preprocessing import StandardScaler
import pandas as pd


class ScalerBundle:
    def __init__(self):
        self.scaler = StandardScaler()

    def fit(self, X_train):
        self.scaler.fit(X_train)
        return self

    def transform(self, X):
        return pd.DataFrame(
            self.scaler.transform(X),
            columns=X.columns,
            index=X.index,
        )

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
