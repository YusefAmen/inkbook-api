from fastapi.testclient import TestClient
from datetime import datetime
from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "InkBook API is running"
    }


def test_create_appointment():
    appointment_data = {
        "client_name": "Test User",
        "email": "test@example.com",
        "date": datetime.now().isoformat(),
        "notes": "Test appointment"
    }
    response = client.post("/appointments/", json=appointment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data 