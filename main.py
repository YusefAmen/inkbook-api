from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.appointments import router as appointments_router
from routes.portfolio import router as portfolio_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="InkBook API",
    description="Backend API for InkBook - Tattoo Artist Management Platform",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "InkBook API is running"}


app.include_router(
    appointments_router,
    prefix="/appointments",
    tags=["appointments"],
)
app.include_router(
    portfolio_router,
    prefix="/portfolio",
    tags=["portfolio"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
