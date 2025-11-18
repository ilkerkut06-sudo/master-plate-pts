from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.mongo import connect_to_mongo, close_mongo_connection
from app.utils.logger import logger
from app.routes import cameras, plates, gates, sites, logs, settings, system
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting EvoPlate Enterprise Edition...")
    await connect_to_mongo()
    logger.info("EvoPlate system ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down EvoPlate...")
    await close_mongo_connection()
    logger.info("EvoPlate shutdown complete")

app = FastAPI(
    title="EvoPlate Enterprise API",
    description="Turkish License Plate Recognition System with Dual Pipeline & Hybrid OCR",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cameras.router)
app.include_router(plates.router)
app.include_router(gates.router)
app.include_router(sites.router)
app.include_router(logs.router)
app.include_router(settings.router)
app.include_router(system.router)

@app.get("/")
async def root():
    return {
        "message": "EvoPlate Enterprise Edition API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )