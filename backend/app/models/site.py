from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Site(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Merkez Kampüs",
                "address": "Maslak, İstanbul",
                "city": "İstanbul"
            }
        }