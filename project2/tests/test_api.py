import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webapp.app import app, build_feature_vector, load_experiment_data, load_model


def test_home_route():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_result_route():
    client = app.test_client()

    response = client.get("/result?value=test")

    assert response.status_code == 200


def test_comparison_route():
    client = app.test_client()

    response = client.get("/comparison")

    assert response.status_code == 200


def test_experiments_route():
    client = app.test_client()

    response = client.get("/experiments")

    assert response.status_code == 200


def test_load_experiment_data_returns_summary_rows():
    rows = load_experiment_data()

    assert len(rows) >= 5
    assert {"Experiment", "BestModel", "F1"}.issubset(rows[0])


def test_predict_route_distinguishes_profit_and_loss_cases():
    client = app.test_client()

    profitable_case = {
        "distancia_km": 10,
        "n_atores_total": 2,
        "n_atores_residentes": 2,
        "n_tecnicos": 1,
        "receita_esperada": 10000,
        "lotacao_espaco": 500,
        "peso_cenario_kg": 10,
        "n_figurinos": 2,
        "dias_deslocacao": 0,
        "percentagem_imprevistos": 5,
        "tem_sistema_proprio": 1,
        "catering_pago_pelo_cliente": 1,
        "alojamento_pago_pelo_cliente": 1,
        "marketing_pago_pelo_espaco": 1,
    }
    loss_case = {
        "distancia_km": 800,
        "n_atores_total": 20,
        "n_atores_residentes": 0,
        "n_tecnicos": 10,
        "receita_esperada": 0,
        "lotacao_espaco": 50,
        "peso_cenario_kg": 2000,
        "n_figurinos": 80,
        "dias_deslocacao": 10,
        "percentagem_imprevistos": 50,
        "tem_portagens": 1,
        "precisa_carrinha": 1,
        "precisa_autocarro_privado": 1,
        "tem_cenario_grande": 1,
        "tem_costureira": 1,
        "tem_maquilhagem": 1,
    }

    profitable_response = client.post("/predict", json=profitable_case)
    loss_response = client.post("/predict", json=loss_case)

    assert profitable_response.status_code == 200
    assert loss_response.status_code == 200
    assert profitable_response.json["profitable"] is True
    assert loss_response.json["profitable"] is False


def test_predict_route_rejects_empty_json():
    client = app.test_client()

    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert response.json["error"] == "No input fields provided."


def test_predict_route_rejects_invalid_field_type():
    client = app.test_client()

    response = client.post("/predict", json={"distancia_km": "abc"})

    assert response.status_code == 400
    assert response.json["error"] == "distancia_km must be a valid number"


def test_predict_route_rejects_numeric_overflow_values():
    client = app.test_client()

    response = client.post("/predict", json={"receita_esperada": 10**12})

    assert response.status_code == 400
    assert response.json["error"] == "receita_esperada must be between 0 and 1000000"


def test_predict_route_rejects_inconsistent_actor_counts():
    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "n_atores_total": 2,
            "n_atores_residentes": 3,
        },
    )

    assert response.status_code == 400
    assert response.json["error"] == "n_atores_residentes cannot exceed n_atores_total"


def test_predict_route_rejects_invalid_boolean_values():
    client = app.test_client()

    response = client.post("/predict", json={"tem_portagens": 3})

    assert response.status_code == 400
    assert response.json["error"] == "tem_portagens must be 0 or 1"


def test_feature_vector_matches_saved_model_features():
    model = load_model()
    feature_row = build_feature_vector({})

    assert model is not None
    assert set(feature_row) == set(model.feature_names_in_)


def test_feature_vector_only_charges_lodging_when_needed_and_not_paid_by_client():
    base = {
        "n_atores_total": 4,
        "n_atores_residentes": 4,
        "n_tecnicos": 2,
        "dias_deslocacao": 3,
    }

    no_lodging = build_feature_vector({
        **base,
        "precisa_alojamento": 0,
        "alojamento_pago_pelo_cliente": 0,
    })
    paid_by_client = build_feature_vector({
        **base,
        "precisa_alojamento": 1,
        "alojamento_pago_pelo_cliente": 1,
    })
    paid_by_company = build_feature_vector({
        **base,
        "precisa_alojamento": 1,
        "alojamento_pago_pelo_cliente": 0,
    })

    assert no_lodging["custo_alojamento_eur"] == 0
    assert paid_by_client["custo_alojamento_eur"] == 0
    assert paid_by_company["custo_alojamento_eur"] > 0


def test_feature_vector_derives_region_from_location():
    feature_row = build_feature_vector({
        "local_evento": "Porto",
        "regiao_geografica": "Algarve",
    })

    assert feature_row["regiao_geografica_Norte"] == 1
    assert feature_row["regiao_geografica_Algarve"] == 0
