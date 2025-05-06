import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_supabase():
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_table.insert.return_value.execute.return_value.data = [{"id": "test-client-id"}]
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [{"id": "test-client-id"}]
    mock_client.table.return_value = mock_table

    patcher = patch("db.supabase_client.get_supabase_client", return_value=mock_client)
    patcher.start()
    yield mock_client
    patcher.stop()

from datetime import datetime
from uuid import UUID

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "InkBook API is running",
    }


def test_create_appointment(mock_supabase):
    # First create a client
    client_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    client_response = client.post("/appointments/clients/", json=client_data)
    assert client_response.status_code == 200
    client_id = client_response.json()["id"]

    # Then create an appointment
    appointment_data = {
        "client_id": client_id,
        "date": datetime.now().isoformat(),
        "start_time": "10:00",
        "end_time": "12:00",
        "tattoo_size": "medium",
        "tattoo_style": "traditional",
        "tattoo_placement": "arm",
        "description": "Test appointment",
        "price": "100",
        "deposit": "50",
        "special_instructions": "Test instructions"
    }
    response = client.post("/appointments/appointments", json=appointment_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
