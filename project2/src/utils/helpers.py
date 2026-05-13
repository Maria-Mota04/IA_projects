from sklearn.preprocessing import StandardScaler
import pandas as pd


def scale_splits(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index),
        pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index),
    )
