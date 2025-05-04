from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from db.supabase_client import supabase


router = APIRouter()


class AppointmentCreate(BaseModel):
    client_name: str
    email: str
    date: datetime
    notes: str | None = None


@router.post("/")
async def create_appointment(appointment: AppointmentCreate):
    try:
        # Insert appointment into Supabase
        response = supabase.table("appointments").insert({
            "client_name": appointment.client_name,
            "email": appointment.email,
            "date": appointment.date.isoformat(),
            "notes": appointment.notes,
            "status": "pending"
        }).execute()

        if not response.data:
            raise HTTPException(
                status_code=400,
                detail="Failed to create appointment"
            )

        return {
            "status": "success",
            "message": "Appointment created successfully",
            "data": response.data[0]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 