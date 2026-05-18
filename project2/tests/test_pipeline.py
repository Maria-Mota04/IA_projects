from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.model_persistence import ModelPersistence
from src.pipeline.training_pipeline import run_pipeline


def test_run_pipeline_saves_model_and_metrics(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "raw" / "data.xlsx"
    model_path = tmp_path / "model.pkl"
    metrics_path = tmp_path / "metrics.json"

    results = run_pipeline(
        data_path=data_path,
        model_path=model_path,
        metrics_path=metrics_path,
    )
    model = ModelPersistence.load(model_path)

    assert model_path.exists()
    assert metrics_path.exists()
    assert not results.empty
    assert isinstance(model, Pipeline)
    assert isinstance(model.steps[0][1], StandardScaler)
