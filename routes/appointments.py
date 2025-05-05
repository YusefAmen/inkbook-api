from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
import logging

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr

from db.supabase_client import supabase

router = APIRouter()

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
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
    reference_images: Optional[List[str]] = None

class AppointmentCreate(AppointmentBase):
    client_id: UUID

class Appointment(AppointmentBase):
    id: UUID
    client_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/clients/", response_model=Client)
async def create_client(client: ClientCreate):
    try:
        # Insert client into Supabase
        response = supabase.table("clients").insert(
            {
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
            }
        ).execute()

        if not response.data:
            raise HTTPException(
                status_code=400,
                detail="Failed to create client",
            )

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/appointments", status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate):
    try:
        data = appointment.dict()
        response = supabase.table("appointments").insert(data).execute()
        if response.error:
            logging.error(f"Supabase error: {response.error}")
            raise HTTPException(status_code=500, detail="Failed to create appointment")
        return {"status": "success", "data": response.data}
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: UUID):
    try:
        response = supabase.table("clients").select("*").eq("id", str(client_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Client not found",
            )
            
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients/{client_id}/appointments", response_model=List[Appointment])
async def get_client_appointments(client_id: UUID):
    try:
        response = supabase.table("appointments").select("*").eq("client_id", str(client_id)).execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointments", response_model=List[Appointment])
async def get_appointments():
    try:
        response = supabase.table("appointments").select("*").execute()
        if response.error:
            logging.error(f"Supabase error: {response.error}")
            raise HTTPException(status_code=500, detail="Failed to fetch appointments")
        return response.data
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    try:
        response = supabase.table("appointments").select("*").eq("id", appointment_id).single().execute()
        if response.error:
            logging.error(f"Supabase error: {response.error}")
            raise HTTPException(status_code=404, detail="Appointment not found")
        return response.data
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str):
    try:
        response = supabase.table("appointments").delete().eq("id", appointment_id).execute()
        if response.error:
            logging.error(f"Supabase error: {response.error}")
            raise HTTPException(status_code=404, detail="Appointment not found")
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
