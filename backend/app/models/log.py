from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class SystemLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    log_type: Literal["plate_detected", "gate_opened", "camera_error", "system_error", "blacklist_alert"] = "plate_detected"
    message: str
    plate_id: Optional[str] = None
    camera_id: Optional[str] = None
    gate_id: Optional[str] = None
    severity: Literal["info", "warning", "error", "critical"] = "info"
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "log_type": "plate_detected",
                "message": "Plaka tespit edildi: 34ABC123",
                "severity": "info"
            }
        }