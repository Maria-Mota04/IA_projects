import pickle
from pathlib import Path


class ModelPersistence:
    """
    Save and load trained models.
    """

    @staticmethod
    def save(model, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump(model, f)

    @staticmethod
    def load(path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Model not found: {path}")

        with open(path, "rb") as f:
            return pickle.load(f)
