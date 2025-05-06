"""
Golden Path API Test for InkBook MVP:
1. Create a client (POST /appointments/clients/)
2. Create an appointment for that client (POST /appointments/appointments)
All Supabase calls are mocked.
"""

import os
os.environ["SUPABASE_URL"] = "http://dummy"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "dummy"

from unittest.mock import MagicMock, patch
import atexit
from datetime import datetime
from fastapi.testclient import TestClient
from uuid import uuid4

# Patch get_supabase_client globally before importing app
mock_client = MagicMock()
mock_table_client = MagicMock()
mock_table_appointment = MagicMock()

mock_table_client.insert.return_value.execute.return_value.data = [{
    "id": str(uuid4()),
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "created_at": datetime.now().isoformat()
}]
mock_table_client.select.return_value.eq.return_value.execute.return_value.data = [{
    "id": str(uuid4()),
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "created_at": datetime.now().isoformat()
}]

def appointment_insert_side_effect(data):
    return MagicMock(
        execute=MagicMock(
            return_value=MagicMock(
                data=[{
                    "id": str(uuid4()),
                    "client_id": data["client_id"],
                    "date": data["date"],
                    "start_time": data["start_time"],
                    "end_time": data["end_time"],
                    "tattoo_size": data["tattoo_size"],
                    "tattoo_style": data["tattoo_style"],
                    "tattoo_placement": data["tattoo_placement"],
                    "description": data["description"],
                    "price": data["price"],
                    "deposit": data["deposit"],
                    "special_instructions": data.get("special_instructions"),
                    "created_at": datetime.now().isoformat(),
                    "status": "scheduled"
                }]
            )
        )
    )

mock_table_appointment.insert.side_effect = appointment_insert_side_effect
mock_table_appointment.select.return_value.eq.return_value.execute.return_value.data = [{
    "id": str(uuid4()),
    "client_id": str(uuid4()),
    "date": datetime.now().isoformat(),
    "start_time": "10:00",
    "end_time": "12:00",
    "tattoo_size": "medium",
    "tattoo_style": "traditional",
    "tattoo_placement": "arm",
    "description": "Test appointment",
    "price": "100",
    "deposit": "50",
    "special_instructions": "Test instructions",
    "created_at": datetime.now().isoformat(),
    "status": "scheduled"
}]

def table_side_effect(table_name):
    if table_name == "clients":
        return mock_table_client
    elif table_name == "appointments":
        return mock_table_appointment
    else:
        raise ValueError(f"Unknown table: {table_name}")

mock_client.table.side_effect = table_side_effect

def mock_supabase_gen():
    yield mock_client

patcher = patch("db.supabase_client.get_supabase_client", mock_supabase_gen)
patcher.start()
atexit.register(patcher.stop)

from main import app

client = TestClient(app)

def test_create_client_and_appointment():
    # 1. Create client
    client_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    client_response = client.post("/appointments/clients/", json=client_data)
    if client_response.status_code != 200:
        print("Client creation error:", client_response.json())
    assert client_response.status_code == 200
    client_id = client_response.json()["id"]

    # 2. Create appointment
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
    if response.status_code != 201:
        print("Appointment creation error:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "scheduled"
    assert data["client_id"] == client_id
    assert data["description"] == "Test appointment"

def test_debug_client():
    debug_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    response = client.post("/appointments/debug-client/", json=debug_data)
    print("Debug client response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["ok"] is True
