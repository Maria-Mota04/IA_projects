from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
import os
import pandas as pd

from webapp.settings import Config

from src.models.model_persistence import ModelPersistence

app = Flask(__name__)
app.config.from_object(Config)

model = None


def load_model():
    global model

    if model is None:
        model_path = Path(app.config["MODEL_PATH"])

        if model_path.exists():
            model = ModelPersistence.load(model_path)

    return model


def load_models_data():
    try:
        metrics_file = Path(app.config.get("METRICS_FILE"))
        if metrics_file.exists():
            with open(metrics_file, "r") as f:
                return json.load(f)

    except Exception as e:
        print(f"Error loading models data: {e}")

    return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        model = load_model()

        if model is None:
            return jsonify({"error": "Model not found. Train the model first."}), 500

        input_df = pd.DataFrame([data])

        prediction = model.predict(input_df)[0]

        probability = None

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(input_df)[0][1])

        result = {
            "prediction": int(prediction),
            "profitable": bool(prediction),
            "probability_profit": probability,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/result")
def result():
    value = request.args.get("value")

    return render_template(
        "result.html",
        result=value,
    )


@app.route("/comparison")
def comparison():
    models_data = load_models_data()

    return render_template(
        "comparison.html",
        models=models_data,
    )


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
