from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class Camera(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    camera_type: Literal["rtsp", "onvif", "webcam"] = "rtsp"
    stream_url: Optional[str] = None  # RTSP URL or webcam index
    webcam_index: Optional[int] = None  # For webcam: 0, 1, 2...
    onvif_host: Optional[str] = None
    onvif_port: Optional[int] = 2000
    onvif_username: Optional[str] = None
    onvif_password: Optional[str] = None
    fps: int = 25
    resolution: str = "1920x1080"
    gate_id: Optional[str] = None
    site_id: Optional[str] = None
    is_active: bool = True
    enable_ocr: bool = True
    enable_motion_detection: bool = True
    roi_enabled: bool = True
    roi_coordinates: Optional[dict] = None  # {"x1": 0, "y1": 0, "x2": 100, "y2": 100}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ana Giriş Kamerası",
                "camera_type": "rtsp",
                "stream_url": "rtsp://admin:12345@192.168.1.100:554/stream1",
                "fps": 25,
                "gate_id": "gate-001"
            }
        }