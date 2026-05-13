import numpy as np

def remove_columns(X, columns_to_remove, feature_names):
    idx_keep = [i for i, c in enumerate(feature_names) if c not in columns_to_remove]
    return X[:, idx_keep], [feature_names[i] for i in idx_keep]
