import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_execute_sum(client):
    response = client.post("/execute", json={"task": "sum 2 3"})
    assert response.status_code == 200
    assert response.json["result"]["result"] == 5
