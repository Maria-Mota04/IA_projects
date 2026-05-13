import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.model_selector import ModelSelector
from src.models.model_evaluator import ModelEvaluator


def test_model_selector_returns_best_model():
    df = pd.DataFrame(
        {
            "Model": [
                "A",
                "B",
                "C",
            ],
            "F1": [
                0.70,
                0.91,
                0.82,
            ],
        }
    )

    selector = ModelSelector(metric="F1")

    best = selector.select_best(df)

    assert best == "B"


def test_model_selector_returns_none_for_empty_df():
    df = pd.DataFrame()

    selector = ModelSelector()

    result = selector.select_best(df)

    assert result is None


def test_model_evaluator_returns_metrics():
    import numpy as np
    from src.models.model_evaluator import ModelEvaluator
    from sklearn.linear_model import LogisticRegression

    X_test = np.array(
        [
            [0.1],
            [0.2],
            [0.3],
            [0.4],
        ]
    )

    y_test = [1, 0, 1, 1]

    model = LogisticRegression()
    model.fit(X_test, y_test)

    evaluator = ModelEvaluator()

    metrics = evaluator.evaluate(
        model,
        X_test,
        y_test,
        name="test_model",
    )

    assert "Accuracy" in metrics
    assert "Precision" in metrics
    assert "Recall" in metrics
    assert "F1" in metrics
    assert "ROC_AUC" in metrics
