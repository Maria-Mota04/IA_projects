from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
import pandas as pd

from webapp.settings import Config
from src.models.model_persistence import ModelPersistence

app = Flask(__name__)
app.config.from_object(Config)

model = None

NUMERIC_LIMITS = {
    "distancia_km": (0, 5000),
    "dias_deslocacao": (0, 30),
    "n_atores_total": (1, 100),
    "n_atores_residentes": (0, 100),
    "n_tecnicos": (0, 100),
    "peso_cenario_kg": (0, 10000),
    "n_figurinos": (0, 500),
    "receita_esperada": (0, 1_000_000),
    "lotacao_espaco": (1, 100_000),
    "percentagem_imprevistos": (0, 100),
    "mes_espetaculo": (1, 12),
    "dia_semana_espetaculo": (0, 6),
    "ano_espetaculo": (2000, 2100),
}

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
        app.logger.warning("Error loading models data: %s", e)
    return []


def _read_number(form, field, default, as_int=False):
    value = form.get(field, default)
    try:
        number = int(value) if as_int else float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be a valid number")

    min_value, max_value = NUMERIC_LIMITS[field]
    if number < min_value or number > max_value:
        raise ValueError(f"{field} must be between {min_value} and {max_value}")

    return number


def _read_bool(form, field):
    try:
        value = int(form.get(field, 0))
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be 0 or 1")

    if value not in (0, 1):
        raise ValueError(f"{field} must be 0 or 1")
    return value


def build_feature_vector(form):
    """
    Receives simplified form input and builds the full feature vector
    expected by the trained model.
    """

    # --- core inputs from form ---
    distancia_km              = _read_number(form, "distancia_km", 0)
    n_atores_total            = _read_number(form, "n_atores_total", 1, as_int=True)
    n_atores_residentes       = _read_number(form, "n_atores_residentes", 1, as_int=True)
    n_tecnicos                = _read_number(form, "n_tecnicos", 1, as_int=True)
    receita_esperada          = _read_number(form, "receita_esperada", 0)
    lotacao_espaco            = _read_number(form, "lotacao_espaco", 100, as_int=True)
    peso_cenario_kg           = _read_number(form, "peso_cenario_kg", 0)
    n_figurinos               = _read_number(form, "n_figurinos", 0, as_int=True)
    dias_deslocacao           = _read_number(form, "dias_deslocacao", 0, as_int=True)
    percentagem_imprevistos   = _read_number(form, "percentagem_imprevistos", 10)

    if n_atores_residentes > n_atores_total:
        raise ValueError("n_atores_residentes cannot exceed n_atores_total")

    # boolean flags
    tem_portagens             = _read_bool(form, "tem_portagens")
    precisa_carrinha          = _read_bool(form, "precisa_carrinha")
    precisa_autocarro_privado = _read_bool(form, "precisa_autocarro_privado")
    tem_cenario_grande        = _read_bool(form, "tem_cenario_grande")
    tem_costureira            = _read_bool(form, "tem_costureira")
    tem_maquilhagem           = _read_bool(form, "tem_maquilhagem")
    catering_pago_pelo_cliente    = _read_bool(form, "catering_pago_pelo_cliente")
    alojamento_pago_pelo_cliente  = _read_bool(form, "alojamento_pago_pelo_cliente")
    precisa_alojamento        = _read_bool(form, "precisa_alojamento")
    tem_sistema_proprio       = _read_bool(form, "tem_sistema_proprio")
    marketing_pago_pelo_espaco    = _read_bool(form, "marketing_pago_pelo_espaco")

    # categorical
    tipo_espetaculo = form.get("tipo_espetaculo", "teatro_adulto")
    local_evento    = form.get("local_evento", "Porto")
    regiao          = form.get("regiao_geografica", "Norte")
    tipo_local      = form.get("tipo_local", "teatro_municipal")
    tipo_contrato   = form.get("tipo_contrato", "fixo")

    # date
    mes              = _read_number(form, "mes_espetaculo", 6, as_int=True)
    dia_semana       = _read_number(form, "dia_semana_espetaculo", 5, as_int=True)
    ano              = _read_number(form, "ano_espetaculo", 2025, as_int=True)

    # --- derived cost estimates ---
    custo_combustivel_eur        = distancia_km * 0.15
    custo_portagens_eur          = distancia_km * 0.08 if tem_portagens else 0
    custo_aluguer_carrinha_eur   = 80 if precisa_carrinha else 0
    n_carros_extra               = 1 if precisa_autocarro_privado else 0
    custo_total_transporte_eur   = (custo_combustivel_eur + custo_portagens_eur
                                    + custo_aluguer_carrinha_eur)

    n_atores_externos            = max(0, n_atores_total - n_atores_residentes)
    total_pessoas_equipa         = n_atores_total + n_tecnicos
    custo_cachets_eur            = n_atores_externos * 150

    custo_construcao_cenario_eur = peso_cenario_kg * 2
    custo_cenografo_eur          = 200 if tem_cenario_grande else 0
    custo_aluguer_cenico_eur     = 100 if tem_cenario_grande else 0
    custo_adereccos_eur          = 50
    custo_total_cenario_eur      = (custo_construcao_cenario_eur
                                    + custo_cenografo_eur
                                    + custo_aluguer_cenico_eur
                                    + custo_adereccos_eur)

    custo_figurinos_eur          = n_figurinos * 30
    custo_costureira_eur         = 100 if tem_costureira else 0
    custo_maquilhagem_eur        = 50 if tem_maquilhagem else 0
    custo_total_figurinos_eur    = (custo_figurinos_eur + custo_costureira_eur
                                    + custo_maquilhagem_eur)

    custo_catering_eur           = 0 if catering_pago_pelo_cliente else total_pessoas_equipa * 15 * max(1, dias_deslocacao)
    custo_alojamento_eur         = 0 if (
        not precisa_alojamento or alojamento_pago_pelo_cliente
    ) else total_pessoas_equipa * 50 * max(0, dias_deslocacao - 1)
    custo_total_alimentacao_alojamento_eur = custo_catering_eur + custo_alojamento_eur

    custo_aluguer_luz_eur        = 0 if tem_sistema_proprio else 150
    custo_aluguer_som_eur        = 0 if tem_sistema_proprio else 100
    custo_tecnico_luz_eur        = 80
    custo_tecnico_som_eur        = 80
    custo_tecnicos_palco_eur     = n_tecnicos * 60
    custo_total_tecnica_eur      = (custo_aluguer_luz_eur + custo_aluguer_som_eur
                                    + custo_tecnico_luz_eur + custo_tecnico_som_eur
                                    + custo_tecnicos_palco_eur)

    custo_licencas_aavp_eur      = 50
    custo_marketing_eur          = 0 if marketing_pago_pelo_espaco else 100

    custo_total_sem_imprevistos  = (custo_total_transporte_eur + custo_cachets_eur
                                    + custo_total_cenario_eur + custo_total_figurinos_eur
                                    + custo_total_alimentacao_alojamento_eur
                                    + custo_total_tecnica_eur + custo_licencas_aavp_eur
                                    + custo_marketing_eur)

    custo_imprevistos_eur        = custo_total_sem_imprevistos * (percentagem_imprevistos / 100)
    custo_total_eur              = custo_total_sem_imprevistos + custo_imprevistos_eur

    # engineered features
    custo_transporte_por_ator    = custo_total_transporte_eur / (n_atores_total + 1)
    custo_tecnico_por_pessoa     = custo_total_tecnica_eur / (total_pessoas_equipa + 1)
    custo_km_estimado            = distancia_km * custo_combustivel_eur
    lucro_estimado_eur           = receita_esperada - custo_total_eur

    # --- one-hot encoding ---
    tipos = ["musical", "performance_dança", "teatro_adulto", "teatro_de_rua",
             "teatro_experimental", "teatro_infantil"]
    locais = ["Braga", "Bragança", "Castelo Branco", "Coimbra", "Faro", "Guarda",
              "Leiria", "Lisboa", "Porto", "Santarém", "Setúbal",
              "Viana do Castelo", "Viseu", "Évora"]
    regioes = ["Algarve", "Centro", "Lisboa", "Norte"]
    tipo_locais = ["câmara_municipal", "escola", "espaço_exterior",
                   "espaço_privado", "festival", "teatro_municipal"]
    contratos = ["misto", "percentagem_receita"]

    row = {
        "distancia_km": distancia_km,
        "tem_portagens": tem_portagens,
        "precisa_carrinha": precisa_carrinha,
        "precisa_autocarro_privado": precisa_autocarro_privado,
        "n_carros_extra": n_carros_extra,
        "custo_combustivel_eur": custo_combustivel_eur,
        "custo_portagens_eur": custo_portagens_eur,
        "custo_aluguer_carrinha_eur": custo_aluguer_carrinha_eur,
        "custo_total_transporte_eur": custo_total_transporte_eur,
        "n_atores_total": n_atores_total,
        "n_atores_residentes": n_atores_residentes,
        "n_atores_externos": n_atores_externos,
        "n_tecnicos": n_tecnicos,
        "total_pessoas_equipa": total_pessoas_equipa,
        "custo_cachets_eur": custo_cachets_eur,
        "peso_cenario_kg": peso_cenario_kg,
        "tem_cenario_grande": tem_cenario_grande,
        "custo_construcao_cenario_eur": custo_construcao_cenario_eur,
        "custo_cenografo_eur": custo_cenografo_eur,
        "custo_aluguer_cenico_eur": custo_aluguer_cenico_eur,
        "custo_adereccos_eur": custo_adereccos_eur,
        "custo_total_cenario_eur": custo_total_cenario_eur,
        "n_figurinos": n_figurinos,
        "tem_costureira": tem_costureira,
        "tem_maquilhagem": tem_maquilhagem,
        "custo_figurinos_eur": custo_figurinos_eur,
        "custo_costureira_eur": custo_costureira_eur,
        "custo_maquilhagem_eur": custo_maquilhagem_eur,
        "custo_total_figurinos_eur": custo_total_figurinos_eur,
        "dias_deslocacao": dias_deslocacao,
        "catering_pago_pelo_cliente": catering_pago_pelo_cliente,
        "alojamento_pago_pelo_cliente": alojamento_pago_pelo_cliente,
        "precisa_alojamento": precisa_alojamento,
        "custo_catering_eur": custo_catering_eur,
        "custo_alojamento_eur": custo_alojamento_eur,
        "custo_total_alimentacao_alojamento_eur": custo_total_alimentacao_alojamento_eur,
        "tem_sistema_proprio": tem_sistema_proprio,
        "custo_aluguer_luz_eur": custo_aluguer_luz_eur,
        "custo_aluguer_som_eur": custo_aluguer_som_eur,
        "custo_tecnico_luz_eur": custo_tecnico_luz_eur,
        "custo_tecnico_som_eur": custo_tecnico_som_eur,
        "custo_tecnicos_palco_eur": custo_tecnicos_palco_eur,
        "custo_total_tecnica_eur": custo_total_tecnica_eur,
        "custo_licencas_aavp_eur": custo_licencas_aavp_eur,
        "marketing_pago_pelo_espaco": marketing_pago_pelo_espaco,
        "custo_marketing_eur": custo_marketing_eur,
        "percentagem_imprevistos": percentagem_imprevistos,
        "custo_imprevistos_eur": custo_imprevistos_eur,
        "custo_total_eur": custo_total_eur,
        "lotacao_espaco": lotacao_espaco,
        "receita_esperada": receita_esperada,
        "mes_espetaculo": mes,
        "dia_semana_espetaculo": dia_semana,
        "ano_espetaculo": ano,
        "custo_transporte_por_ator": custo_transporte_por_ator,
        "custo_tecnico_por_pessoa": custo_tecnico_por_pessoa,
        "custo_km_estimado": custo_km_estimado,
        "lucro_estimado_eur": lucro_estimado_eur,
        # one-hot tipo_espetaculo (drop_first removes "circo" baseline)
        **{f"tipo_espetaculo_{t}": int(tipo_espetaculo == t) for t in tipos},
        # one-hot local_evento (drop_first removes "Aveiro" baseline)
        **{f"local_evento_{l}": int(local_evento == l) for l in locais},
        # one-hot regiao_geografica (drop_first removes "Alentejo" baseline)
        **{f"regiao_geografica_{r}": int(regiao == r) for r in regioes},
        # one-hot tipo_local (drop_first removes "auditório" baseline)
        **{f"tipo_local_{tl}": int(tipo_local == tl) for tl in tipo_locais},
        # one-hot tipo_contrato (drop_first removes "fixo" baseline)
        **{f"tipo_contrato_{c}": int(tipo_contrato == c) for c in contratos},
    }

    return row


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if data is None or not isinstance(data, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        if len(data) == 0:
            return jsonify({"error": "No input fields provided."}), 400

        m = load_model()

        if m is None:
            return jsonify({"error": "Model not found. Train the model first."}), 500

        feature_row = build_feature_vector(data)
        input_df = pd.DataFrame([feature_row])

        # ensure column order matches training
        input_df = input_df[m.feature_names_in_]

        prediction = m.predict(input_df)[0]
        probability = None
        if hasattr(m, "predict_proba"):
            probability = float(m.predict_proba(input_df)[0][1])

        return jsonify({
            "prediction": int(prediction),
            "profitable": bool(prediction),
            "probability_profit": probability,
            "custo_total_estimado": round(feature_row["custo_total_eur"], 2),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/result")
def result():
    value = request.args.get("value")
    probability = request.args.get("probability")
    custo = request.args.get("custo")
    return render_template("result.html", result=value, probability=probability, custo=custo)


@app.route("/comparison")
def comparison():
    models_data = load_models_data()
    return render_template("comparison.html", models=models_data)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
