from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Plate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    plate_number: str
    camera_id: str
    gate_id: Optional[str] = None
    site_id: Optional[str] = None
    confidence: float
    ocr_engine: str  # "paddle", "easy", "tesseract", "yolo", "hybrid"
    image_path: Optional[str] = None
    direction: Literal["in", "out"] = "in"
    is_blacklisted: bool = False
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "plate_number": "34ABC123",
                "camera_id": "cam-001",
                "confidence": 0.95,
                "ocr_engine": "hybrid"
            }
        }

from typing import Literal