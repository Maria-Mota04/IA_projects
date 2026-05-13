from src.features.feature_utils import remove_columns


def run_ablation_experiments(
    model, X_train, X_test, y_train, y_test, feature_names, evaluator
):
    results = {}

    for name, cols in EXPERIMENTS.items():
        print(f"\nExperiment: {name}")

        if len(cols) == 0:
            X_train_r, feats = X_train, feature_names
            X_test_r = X_test
        else:
            X_train_r, feats = remove_columns(X_train, cols, feature_names)
            X_test_r, _ = remove_columns(X_test, cols, feature_names)

        m = clone(model)
        m.fit(X_train_r, y_train)

        results[name] = evaluator(m, X_test_r, y_test, nome_modelo=name)

    return results
