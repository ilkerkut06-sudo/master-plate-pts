from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime
import uuid

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    role: Literal["admin", "operator", "viewer"] = "operator"
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@evoplate.com",
                "full_name": "Sistem Yöneticisi",
                "role": "admin"
            }
        }