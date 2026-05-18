def _matches_any(feature_name, patterns):
    return any(
        feature_name == pattern or feature_name.startswith(pattern)
        for pattern in patterns
    )


def remove_columns(X, columns_to_remove, feature_names):
    idx_keep = [
        i for i, c in enumerate(feature_names)
        if not _matches_any(c, columns_to_remove)
    ]
    return select_columns(X, idx_keep, feature_names)


def keep_columns(X, columns_to_keep, feature_names):
    idx_keep = [
        i for i, c in enumerate(feature_names)
        if _matches_any(c, columns_to_keep)
    ]
    return select_columns(X, idx_keep, feature_names)


def select_columns(X, idx_keep, feature_names):
    new_names = [feature_names[i] for i in idx_keep]

    if hasattr(X, "iloc"):
        return X.iloc[:, idx_keep], new_names

    return X[:, idx_keep], new_names
