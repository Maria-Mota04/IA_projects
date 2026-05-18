from sklearn.base import clone
import numpy as np
from src.features.feature_utils import remove_columns
from src.models.experiments import EXPERIMENTS


def _to_array(X):
    if hasattr(X, "values"):
        return X.values
    return np.asarray(X)


def run_ablation_experiments(
    model, X_train, X_test, y_train, y_test, feature_names, evaluator
):
    results = {}

    for name, cols in EXPERIMENTS.items():
        if len(cols) == 0:
            X_train_r = X_train
            X_test_r = X_test
            feats = feature_names
        else:
            X_train_r, feats = remove_columns(X_train, cols, feature_names)
            X_test_r, _ = remove_columns(X_test, cols, feature_names)

        X_train_r = _to_array(X_train_r)
        X_test_r = _to_array(X_test_r)

        m = clone(model)
        m.fit(X_train_r, y_train)

        if hasattr(evaluator, "evaluate"):
            results[name] = evaluator.evaluate(m, X_test_r, y_test, name=name)
        else:
            results[name] = evaluator(m, X_test_r, y_test, name=name)

    return results
