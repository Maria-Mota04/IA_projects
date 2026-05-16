from pathlib import Path

from src.data.dataset_loader import DatasetLoader
from src.data.preprocess import Preprocessor
from src.utils.helpers import scale_splits

from src.models.model_trainer import ModelTrainer
from src.models.model_selector import ModelSelector
from src.models.model_persistence import ModelPersistence

DEFAULT_DATA_PATH = Path("data/raw/data.xlsx")
DEFAULT_MODEL_PATH = Path("models_saved/model.pkl")
DEFAULT_METRICS_PATH = Path("models_saved/metrics.json")


def run_pipeline(
    data_path: Path = DEFAULT_DATA_PATH,
    model_path: Path = DEFAULT_MODEL_PATH,
    metrics_path: Path = DEFAULT_METRICS_PATH,
):
    loader = DatasetLoader(str(data_path))
    df = loader.load_single_sheet()

    preprocessor = Preprocessor(df)
    X_train, X_test, y_train, y_test = preprocessor.run()

    X_train, X_test = scale_splits(X_train, X_test)

    trainer = ModelTrainer()

    results_df = trainer.train_all(
        X_train,
        y_train,
        X_test,
        y_test,
    )

    if results_df.empty:
        raise ValueError("No models were trained successfully")

    selector = ModelSelector(metric="F1")
    best_model_name = selector.select_best(results_df)

    if best_model_name is None:
        raise ValueError("Could not select best model")

    best_model = trainer.fitted_models[best_model_name]

    ModelPersistence.save(best_model, model_path)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    results_df.to_json(
        metrics_path,
        orient="records",
        indent=2,
    )

    return results_df


if __name__ == "__main__":
    results = run_pipeline()
    print("\n=== Resultados dos Modelos ===")
    print(results[["Model", "Accuracy", "Precision", "Recall", "F1", "ROC_AUC"]].to_string(index=False))
    print("\nMelhor modelo guardado em models_saved/model.pkl")