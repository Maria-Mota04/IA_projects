import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from webapp.app import app


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
