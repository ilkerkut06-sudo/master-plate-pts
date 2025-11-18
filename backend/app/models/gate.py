from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class Gate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    gate_type: Literal["entry", "exit", "both"] = "entry"
    site_id: str
    nodemcu_id: Optional[str] = None  # NodeMCU/Arduino ID
    relay_pin: Optional[int] = None
    auto_open: bool = False
    open_duration: int = 5  # seconds
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ana Giriş Kapısı",
                "gate_type": "entry",
                "site_id": "site-001",
                "nodemcu_id": "NODE_001",
                "relay_pin": 2
            }
        }