import os


class Config:
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    API_TITLE = "Theater Recommendation API"
    API_VERSION = "1.0"

    MODEL_PATH = os.getenv("MODEL_PATH", "models_saved/model.pkl")

    METRICS_FILE = os.getenv("METRICS_FILE", "models_saved/metrics.json")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
