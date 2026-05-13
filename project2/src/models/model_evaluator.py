from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


class ModelEvaluator:
    """
    Evaluates classification models.
    """

    def __init__(self, average="weighted"):
        self.average = average

    def evaluate(self, model, X_test, y_test, name="Model"):
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average=self.average, zero_division=0)
        rec = recall_score(y_test, y_pred, average=self.average, zero_division=0)
        f1 = f1_score(y_test, y_pred, average=self.average, zero_division=0)

        roc_auc = None
        if hasattr(model, "predict_proba"):
            try:
                y_score = model.predict_proba(X_test)

                if y_score.shape[1] == 2:
                    roc_auc = roc_auc_score(y_test, y_score[:, 1])
                else:
                    roc_auc = roc_auc_score(
                        y_test, y_score, multi_class="ovr", average=self.average
                    )
            except:
                roc_auc = None

        cm = confusion_matrix(y_test, y_pred)

        return {
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1": f1,
            "ROC_AUC": roc_auc,
            "confusion_matrix": cm,
            "y_pred": y_pred,
        }
