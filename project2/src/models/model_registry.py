from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
from sklearn.svm import SVC


def get_model_registry():
    return {
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000), 
        ),
        "Decision Tree": make_pipeline(
            StandardScaler(),
            DecisionTreeClassifier(random_state=42),
        ),
        "Random Forest": make_pipeline(
            StandardScaler(),
            RandomForestClassifier(n_estimators=200, random_state=42),
        ),
        "SVM": make_pipeline(
            StandardScaler(),
            SVC(probability=True, random_state=42),
        ),
        "Gradient Boosting": make_pipeline(
            StandardScaler(),
            GradientBoostingClassifier(random_state=42),
        ),
        "AdaBoost": make_pipeline(
            StandardScaler(),
            AdaBoostClassifier(random_state=42),
        ),
    }
