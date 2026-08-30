import json
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_api_fields():
    response = client.get("/fields")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_api_recommend():
    with open("data/synthetic/students.json") as f:
        student = json.load(f)[0]
    response = client.post("/recommend?top_k=5", json=student)
    assert response.status_code == 200
    assert len(response.json()["recommendations"]) > 0

def test_api_bias_audit():
    response = client.get("/audit/bias")
    assert response.status_code == 200
    assert response.json()["total_profiles_audited"] == 100
