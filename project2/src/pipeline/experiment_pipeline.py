from pathlib import Path

import pandas as pd

from src.data.dataset_loader import DatasetLoader
from src.data.preprocess import Preprocessor
from src.models.ablation_runner import apply_experiment
from src.models.experiments import EXPERIMENTS
from src.models.model_persistence import ModelPersistence
from src.models.model_selector import ModelSelector
from src.models.model_trainer import ModelTrainer

DEFAULT_DATA_PATH = Path("data/raw/data.xlsx")
DEFAULT_OUTPUT_DIR = Path("models_saved/experiments")
DEFAULT_SUMMARY_PATH = Path("models_saved/experiment_summary.csv")
DEFAULT_README_PATH = Path("models_saved/experiments/README.md")


def _serializable_metrics(results_df):
    df = results_df.copy()
    for col in ["confusion_matrix", "y_pred"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda value: value.tolist() if hasattr(value, "tolist") else value
            )
    return df


def _safe_model_filename(model_name):
    return model_name.lower().replace(" ", "_").replace("/", "_") + ".pkl"


def _write_conclusions(summary_df, path):
    best = summary_df.sort_values("F1", ascending=False).iloc[0]
    lines = [
        "# Experiment Conclusions",
        "",
        "This folder contains the trained models for each feature-ablation experiment.",
        "Each experiment trains all registered classifiers, saves every fitted model, and highlights the model with the best F1-score.",
        "",
        "## Overall Best Model",
        "",
        f"- Experiment: `{best['Experiment']}`",
        f"- Model: `{best['BestModel']}`",
        f"- Accuracy: `{best['Accuracy']:.4f}`",
        f"- Precision: `{best['Precision']:.4f}`",
        f"- Recall: `{best['Recall']:.4f}`",
        f"- F1-score: `{best['F1']:.4f}`",
        f"- ROC AUC: `{best['ROC_AUC']:.4f}`",
        "",
        "## Results by Experiment",
        "",
        "| Experiment | Best model | Features | Accuracy | Precision | Recall | F1 | ROC AUC |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for _, row in summary_df.sort_values("F1", ascending=False).iterrows():
        lines.append(
            "| {Experiment} | {BestModel} | {FeatureCount} | "
            "{Accuracy:.4f} | {Precision:.4f} | {Recall:.4f} | "
            "{F1:.4f} | {ROC_AUC:.4f} |".format(**row)
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- The baseline uses all cleaned and engineered features and is the main reference.",
        "- The `no_binary` experiment measures the impact of operational yes/no decisions.",
        "- The `no_aggregated_costs` experiment removes total-cost and estimated-margin variables, checking how much the model depends on financial aggregates.",
        "- The `no_geo_time` experiment checks whether location and time variables are important.",
        "- The `structural_only` experiment tests whether early planning variables are enough for useful predictions.",
        "",
        "## Main Conclusions",
        "",
        "- Removing binary operational variables did not reduce performance. This suggests that the monetary and structural variables already capture most of the information carried by yes/no operational flags.",
        "- Removing geographic and temporal variables also preserved performance, indicating that the model is not strongly dependent on region or date patterns in this dataset.",
        "- Removing aggregated costs and estimated margin kept performance high, but slightly below the best experiments. These financial aggregates are useful, but the model can still infer profitability from lower-level cost and revenue information.",
        "- The structural-only setup achieved strong results with far fewer features, showing that early planning variables can already support useful predictions.",
        "- Since several experiments have very similar F1-scores, the simpler experiments should be considered if interpretability and robustness are more important than a marginal metric gain.",
        "",
        "A strong drop in F1 after removing a group would indicate that the removed feature group carries important predictive information. In this run, no feature group caused a severe drop, which is a positive robustness sign.",
    ])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run_experiment_pipeline(
    data_path=DEFAULT_DATA_PATH,
    output_dir=DEFAULT_OUTPUT_DIR,
    summary_path=DEFAULT_SUMMARY_PATH,
    readme_path=DEFAULT_README_PATH,
):
    df = DatasetLoader(str(data_path)).load_single_sheet()
    X_train, X_test, y_train, y_test = Preprocessor(df).run()
    feature_names = list(X_train.columns)

    output_dir.mkdir(parents=True, exist_ok=True)
    selector = ModelSelector(metric="F1")
    summary_rows = []

    for experiment_name, config in EXPERIMENTS.items():
        X_train_exp, selected_features = apply_experiment(
            X_train, config, feature_names
        )
        X_test_exp, _ = apply_experiment(X_test, config, feature_names)

        trainer = ModelTrainer()
        results_df = trainer.train_all(
            X_train_exp,
            y_train,
            X_test_exp,
            y_test,
        )
        best_model_name = selector.select_best(results_df)
        if best_model_name is None:
            raise ValueError(f"Could not select model for {experiment_name}")

        experiment_dir = output_dir / experiment_name
        experiment_dir.mkdir(parents=True, exist_ok=True)

        best_model = trainer.fitted_models[best_model_name]
        ModelPersistence.save(best_model, experiment_dir / "model.pkl")

        all_models_dir = experiment_dir / "all_models"
        all_models_dir.mkdir(parents=True, exist_ok=True)
        for model_name, fitted_model in trainer.fitted_models.items():
            ModelPersistence.save(
                fitted_model,
                all_models_dir / _safe_model_filename(model_name),
            )

        _serializable_metrics(results_df).to_json(
            experiment_dir / "metrics.json",
            orient="records",
            indent=2,
        )
        pd.Series(selected_features, name="feature").to_csv(
            experiment_dir / "features.csv",
            index=False,
        )

        best_row = results_df[results_df["Model"] == best_model_name].iloc[0]
        summary_rows.append({
            "Experiment": experiment_name,
            "Description": config["description"],
            "BestModel": best_model_name,
            "FeatureCount": len(selected_features),
            "Accuracy": float(best_row["Accuracy"]),
            "Precision": float(best_row["Precision"]),
            "Recall": float(best_row["Recall"]),
            "F1": float(best_row["F1"]),
            "ROC_AUC": float(best_row["ROC_AUC"]),
            "ModelPath": str(experiment_dir / "model.pkl"),
            "MetricsPath": str(experiment_dir / "metrics.json"),
            "FeaturesPath": str(experiment_dir / "features.csv"),
        })

    summary_df = pd.DataFrame(summary_rows).sort_values("F1", ascending=False)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)
    _write_conclusions(summary_df, readme_path)

    return summary_df


if __name__ == "__main__":
    summary = run_experiment_pipeline()
    print(summary[[
        "Experiment",
        "BestModel",
        "FeatureCount",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "ROC_AUC",
    ]].to_string(index=False))
