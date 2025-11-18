from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # MongoDB
    MONGO_URL: str = "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = "evoplate_db"
    
    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "evoplate_secret_key_change_in_production_2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OCR
    DEFAULT_OCR_ENGINE: str = "hybrid"
    OCR_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Camera
    DEFAULT_STREAM_FPS: int = 25
    OCR_PROCESS_FPS: int = 5
    MOTION_THRESHOLD: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()