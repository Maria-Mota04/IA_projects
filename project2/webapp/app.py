from flask import Flask, render_template, request, jsonify
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)


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


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
