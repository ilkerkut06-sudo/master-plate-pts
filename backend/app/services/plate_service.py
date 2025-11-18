from typing import List, Optional
from datetime import datetime
from app.database.mongo import get_database
from app.models.plate import Plate
from app.services.websocket_manager import ws_manager

class PlateService:
    """Service for managing detected plates"""
    
    async def create_plate_record(self, plate: Plate) -> Plate:
        """Create new plate detection record"""
        db = await get_database()
        plate_dict = plate.model_dump()
        
        result = await db.plates.insert_one(plate_dict)
        plate_dict["_id"] = str(result.inserted_id)
        
        # Broadcast event
        await ws_manager.broadcast_event("plate_detected", {
            "plate": plate.plate_number,
            "camera_id": plate.camera_id,
            "confidence": plate.confidence,
            "timestamp": plate.detected_at.isoformat()
        })
        
        return Plate(**plate_dict)
    
    async def get_plate(self, plate_id: str) -> Optional[Plate]:
        """Get plate by ID"""
        db = await get_database()
        plate_dict = await db.plates.find_one({"id": plate_id})
        
        if plate_dict:
            return Plate(**plate_dict)
        return None
    
    async def get_recent_plates(self, limit: int = 50) -> List[Plate]:
        """Get recent plate detections"""
        db = await get_database()
        plates = []
        
        cursor = db.plates.find().sort("detected_at", -1).limit(limit)
        
        async for plate_dict in cursor:
            plates.append(Plate(**plate_dict))
        
        return plates
    
    async def get_plates_by_camera(self, camera_id: str, limit: int = 50) -> List[Plate]:
        """Get plates detected by specific camera"""
        db = await get_database()
        plates = []
        
        cursor = db.plates.find({"camera_id": camera_id}).sort("detected_at", -1).limit(limit)
        
        async for plate_dict in cursor:
            plates.append(Plate(**plate_dict))
        
        return plates
    
    async def search_plate(self, plate_number: str) -> List[Plate]:
        """Search for plates by plate number"""
        db = await get_database()
        plates = []
        
        cursor = db.plates.find({"plate_number": {"$regex": plate_number, "$options": "i"}})
        
        async for plate_dict in cursor:
            plates.append(Plate(**plate_dict))
        
        return plates
    
    async def get_stats(self) -> dict:
        """Get plate detection statistics"""
        db = await get_database()
        
        total_plates = await db.plates.count_documents({})
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_plates = await db.plates.count_documents({"detected_at": {"$gte": today_start}})
        
        return {
            "total_plates": total_plates,
            "today_plates": today_plates
        }

# Global plate service
plate_service = PlateService()