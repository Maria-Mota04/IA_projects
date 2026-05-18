from src.features.feature_utils import keep_columns, remove_columns
from src.models.experiments import EXPERIMENTS


def apply_experiment(X, experiment_config, feature_names):
    keep = experiment_config.get("keep")
    drop = experiment_config.get("drop", [])

    if keep is not None:
        return keep_columns(X, keep, feature_names)

    if drop:
        return remove_columns(X, drop, feature_names)

    return X.copy(), list(feature_names)


def run_ablation_experiments(
    trainer_factory, X_train, X_test, y_train, y_test, feature_names
):
    results = {}
    fitted_models = {}
    selected_features = {}

    for name, config in EXPERIMENTS.items():
        X_train_exp, features = apply_experiment(X_train, config, feature_names)
        X_test_exp, _ = apply_experiment(X_test, config, feature_names)

        trainer = trainer_factory()
        results[name] = trainer.train_all(
            X_train_exp,
            y_train,
            X_test_exp,
            y_test,
        )
        fitted_models[name] = trainer.fitted_models
        selected_features[name] = features

    return results, fitted_models, selected_features
