from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
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

@router.post("/", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate):
    try:
        # Insert appointment into Supabase
        response = supabase.table("appointments").insert(
            {
                "client_id": str(appointment.client_id),
                "date": appointment.date.isoformat(),
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
                "tattoo_size": appointment.tattoo_size,
                "tattoo_style": appointment.tattoo_style,
                "tattoo_placement": appointment.tattoo_placement,
                "description": appointment.description,
                "price": appointment.price,
                "deposit": appointment.deposit,
                "special_instructions": appointment.special_instructions,
                "reference_images": appointment.reference_images,
                "status": "pending",
            }
        ).execute()

        if not response.data:
            raise HTTPException(
                status_code=400,
                detail="Failed to create appointment",
            )

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
