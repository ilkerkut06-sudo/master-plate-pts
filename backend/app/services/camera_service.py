from typing import List, Optional, Dict
from app.database.mongo import get_database
from app.models.camera import Camera
from app.utils.video_pipeline_live import LiveVideoPipeline
from app.utils.video_pipeline_ocr import OCRVideoPipeline
import asyncio

class CameraService:
    """Service for managing cameras and video pipelines"""
    
    def __init__(self):
        # Active pipelines: {camera_id: {"live": LiveVideoPipeline, "ocr": OCRVideoPipeline}}
        self.active_pipelines: Dict[str, Dict] = {}
    
    async def create_camera(self, camera: Camera) -> Camera:
        """Create new camera"""
        db = await get_database()
        camera_dict = camera.model_dump()
        
        result = await db.cameras.insert_one(camera_dict)
        camera_dict["_id"] = str(result.inserted_id)
        
        return Camera(**camera_dict)
    
    async def get_camera(self, camera_id: str) -> Optional[Camera]:
        """Get camera by ID"""
        db = await get_database()
        camera_dict = await db.cameras.find_one({"id": camera_id})
        
        if camera_dict:
            return Camera(**camera_dict)
        return None
    
    async def get_all_cameras(self) -> List[Camera]:
        """Get all cameras"""
        db = await get_database()
        cameras = []
        
        async for camera_dict in db.cameras.find():
            cameras.append(Camera(**camera_dict))
        
        return cameras
    
    async def update_camera(self, camera_id: str, camera_data: dict) -> Optional[Camera]:
        """Update camera"""
        db = await get_database()
        
        result = await db.cameras.update_one(
            {"id": camera_id},
            {"$set": camera_data}
        )
        
        if result.modified_count > 0:
            return await self.get_camera(camera_id)
        return None
    
    async def delete_camera(self, camera_id: str) -> bool:
        """Delete camera"""
        # Stop pipelines first
        await self.stop_camera_pipelines(camera_id)
        
        db = await get_database()
        result = await db.cameras.delete_one({"id": camera_id})
        
        return result.deleted_count > 0
    
    def start_camera_pipelines(self, camera: Camera, ocr_callback=None):
        """Start both pipelines for a camera"""
        if camera.id in self.active_pipelines:
            print(f"Pipelines already running for camera {camera.id}")
            return
        
        # Determine stream source
        if camera.camera_type == "webcam":
            stream_source = str(camera.webcam_index)
        else:
            stream_source = camera.stream_url
        
        if not stream_source:
            print(f"No stream source for camera {camera.id}")
            return
        
        # Start Pipeline A (Live streaming)
        live_pipeline = LiveVideoPipeline(
            camera_id=camera.id,
            stream_source=stream_source,
            fps=camera.fps
        )
        live_pipeline.start()
        
        # Start Pipeline B (OCR processing) if enabled
        ocr_pipeline = None
        if camera.enable_ocr:
            ocr_pipeline = OCRVideoPipeline(
                camera_id=camera.id,
                stream_source=stream_source,
                ocr_fps=2,  # Lower FPS for OCR
                enable_motion_detection=camera.enable_motion_detection,
                enable_roi=camera.roi_enabled,
                roi_coords=camera.roi_coordinates,
                ocr_callback=ocr_callback
            )
            ocr_pipeline.start()
        
        self.active_pipelines[camera.id] = {
            "live": live_pipeline,
            "ocr": ocr_pipeline
        }
        
        print(f"Started pipelines for camera {camera.id}")
    
    async def stop_camera_pipelines(self, camera_id: str):
        """Stop both pipelines for a camera"""
        if camera_id not in self.active_pipelines:
            return
        
        pipelines = self.active_pipelines[camera_id]
        
        if pipelines["live"]:
            pipelines["live"].stop()
        
        if pipelines["ocr"]:
            pipelines["ocr"].stop()
        
        del self.active_pipelines[camera_id]
        print(f"Stopped pipelines for camera {camera_id}")
    
    def get_live_frame(self, camera_id: str) -> Optional[bytes]:
        """Get current live frame as JPEG"""
        if camera_id not in self.active_pipelines:
            return None
        
        live_pipeline = self.active_pipelines[camera_id].get("live")
        if live_pipeline:
            return live_pipeline.get_frame_jpeg()
        
        return None
    
    def get_pipeline_stats(self, camera_id: str) -> Dict:
        """Get pipeline statistics"""
        if camera_id not in self.active_pipelines:
            return {"error": "Pipelines not running"}
        
        pipelines = self.active_pipelines[camera_id]
        
        stats = {}
        if pipelines["live"]:
            stats["live"] = pipelines["live"].get_stats()
        
        if pipelines["ocr"]:
            stats["ocr"] = pipelines["ocr"].get_stats()
        
        return stats
    
    def set_ocr_engine(self, camera_id: str, engine: str) -> bool:
        """Change OCR engine for a camera"""
        if camera_id not in self.active_pipelines:
            return False
        
        ocr_pipeline = self.active_pipelines[camera_id].get("ocr")
        if ocr_pipeline:
            return ocr_pipeline.set_ocr_engine(engine)
        
        return False

# Global camera service
camera_service = CameraService()