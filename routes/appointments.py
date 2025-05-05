from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from db.supabase_client import get_supabase_client

router = APIRouter()

# Models
class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    client_id: UUID
    date: datetime
    start_time: str
    end_time: str
    tattoo_size: str
    tattoo_style: str
    tattoo_placement: str
    description: str
    price: str
    deposit: str
    special_instructions: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: UUID
    created_at: datetime
    status: str = "scheduled"

    class Config:
        from_attributes = True

# Endpoints
@router.post("/clients/", response_model=Client)
async def create_client(client: ClientCreate, supabase=Depends(get_supabase_client)):
    try:
        response = supabase.table("clients").insert(client.model_dump()).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create client")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients/", response_model=List[Client])
async def get_clients(supabase=Depends(get_supabase_client)):
    try:
        response = supabase.table("clients").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: UUID, supabase=Depends(get_supabase_client)):
    try:
        response = supabase.table("clients").select("*").eq("id", str(client_id)).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Client not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate, supabase=Depends(get_supabase_client)):
    try:
        # Verify client exists
        client_response = supabase.table("clients").select("*").eq("id", str(appointment.client_id)).execute()
        if not client_response.data:
            raise HTTPException(status_code=404, detail="Client not found")

        # Create appointment
        response = supabase.table("appointments").insert(appointment.model_dump()).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create appointment")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointments/", response_model=List[Appointment])
async def get_appointments(supabase=Depends(get_supabase_client)):
    try:
        response = supabase.table("appointments").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: UUID, supabase=Depends(get_supabase_client)):
    try:
        response = supabase.table("appointments").select("*").eq("id", str(appointment_id)).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
