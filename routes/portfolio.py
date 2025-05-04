from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


class PortfolioUpload(BaseModel):
    title: str
    description: str
    style: str
    # Image handling will be implemented later


@router.post("/")
async def upload_portfolio_item(item: PortfolioUpload):
    """
    TODO: Implement portfolio upload functionality
    This endpoint will handle:
    1. Image upload to Supabase Storage
    2. Metadata storage in Supabase Database
    3. Image processing and optimization
    """
    raise HTTPException(
        status_code=501,
        detail="Portfolio upload functionality is not implemented yet"
    )
