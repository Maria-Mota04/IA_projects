from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.model_persistence import ModelPersistence
from src.pipeline.experiment_pipeline import run_experiment_pipeline
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


def test_run_experiment_pipeline_saves_experiment_artifacts(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "raw" / "data.xlsx"
    output_dir = tmp_path / "experiments"
    summary_path = tmp_path / "summary.csv"
    readme_path = output_dir / "README.md"

    summary = run_experiment_pipeline(
        data_path=data_path,
        output_dir=output_dir,
        summary_path=summary_path,
        readme_path=readme_path,
    )

    assert summary_path.exists()
    assert readme_path.exists()
    assert set(summary["Experiment"]) == {
        "baseline",
        "no_binary",
        "no_aggregated_costs",
        "no_geo_time",
        "structural_only",
    }

    for experiment in summary["Experiment"]:
        experiment_dir = output_dir / experiment
        assert (experiment_dir / "model.pkl").exists()
        assert (experiment_dir / "metrics.json").exists()
        assert (experiment_dir / "features.csv").exists()
        assert (experiment_dir / "all_models").exists()
        assert len(list((experiment_dir / "all_models").glob("*.pkl"))) == 6
