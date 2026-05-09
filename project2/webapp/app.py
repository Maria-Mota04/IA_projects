from flask import Flask, render_template, request, jsonify
from settings import Config
import json
import os

app = Flask(__name__)
app.config.from_object(Config)


def load_models_data():
    """Load models data from JSON file, return empty list if file doesn't exist"""
    try:
        metrics_file = app.config.get("METRICS_FILE")
        if metrics_file and os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                data = json.load(f)
                return data.get("models", [])
    except Exception as e:
        print(f"Error loading models data: {e}")
    return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    score = float(data["genre"]) + float(data["budget"])

    return jsonify({"recommendation": f"Theater Show #{int(score) % 5 + 1}"})


@app.route("/result")
def result():
    value = request.args.get("value")
    return render_template("result.html", result=value)


@app.route("/comparison")
def comparison():
    models_data = load_models_data()
    return render_template("comparison.html", models=models_data)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
