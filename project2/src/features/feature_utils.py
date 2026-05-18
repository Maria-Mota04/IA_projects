def remove_columns(X, columns_to_remove, feature_names):
    idx_keep = [i for i, c in enumerate(feature_names) if c not in columns_to_remove]
    new_names = [feature_names[i] for i in idx_keep]

    if hasattr(X, "iloc"):
        return X.iloc[:, idx_keep], new_names

    return X[:, idx_keep], new_names
