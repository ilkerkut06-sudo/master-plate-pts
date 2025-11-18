from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from app.models.camera import Camera
from app.services.camera_service import camera_service
from app.services.websocket_manager import ws_manager
from app.services.plate_service import plate_service
from app.models.plate import Plate
import asyncio

router = APIRouter(prefix="/api/cameras", tags=["cameras"])

@router.post("/", response_model=Camera)
async def create_camera(camera: Camera):
    """Create new camera"""
    return await camera_service.create_camera(camera)

@router.get("/", response_model=List[Camera])
async def get_cameras():
    """Get all cameras"""
    return await camera_service.get_all_cameras()

@router.get("/{camera_id}", response_model=Camera)
async def get_camera(camera_id: str):
    """Get camera by ID"""
    camera = await camera_service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.put("/{camera_id}", response_model=Camera)
async def update_camera(camera_id: str, camera_data: dict):
    """Update camera"""
    camera = await camera_service.update_camera(camera_id, camera_data)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.delete("/{camera_id}")
async def delete_camera(camera_id: str):
    """Delete camera"""
    success = await camera_service.delete_camera(camera_id)
    if not success:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"message": "Camera deleted successfully"}

@router.post("/{camera_id}/start")
async def start_camera(camera_id: str):
    """Start camera pipelines"""
    camera = await camera_service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    # OCR callback to save detected plates
    async def ocr_callback(detection):
        plate = Plate(
            plate_number=detection["plate"],
            camera_id=detection["camera_id"],
            confidence=detection["confidence"],
            ocr_engine=detection["engine"]
        )
        await plate_service.create_plate_record(plate)
    
    # Start pipelines with callback
    def callback_wrapper(detection):
        asyncio.create_task(ocr_callback(detection))
    
    camera_service.start_camera_pipelines(camera, callback_wrapper)
    
    return {"message": f"Camera {camera_id} started"}

@router.post("/{camera_id}/stop")
async def stop_camera(camera_id: str):
    """Stop camera pipelines"""
    await camera_service.stop_camera_pipelines(camera_id)
    return {"message": f"Camera {camera_id} stopped"}

@router.get("/{camera_id}/stats")
async def get_camera_stats(camera_id: str):
    """Get camera pipeline statistics"""
    return camera_service.get_pipeline_stats(camera_id)

@router.post("/{camera_id}/ocr-engine")
async def set_ocr_engine(camera_id: str, engine: dict):
    """Change OCR engine for camera"""
    engine_name = engine.get("engine")
    if not engine_name:
        raise HTTPException(status_code=400, detail="Engine name required")
    
    success = camera_service.set_ocr_engine(camera_id, engine_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set OCR engine")
    
    return {"message": f"OCR engine set to {engine_name}"}

@router.websocket("/ws/{camera_id}")
async def camera_websocket(websocket: WebSocket, camera_id: str):
    """WebSocket endpoint for live camera stream"""
    await ws_manager.connect_camera(websocket, camera_id)
    
    try:
        while True:
            # Get frame from live pipeline
            frame_data = camera_service.get_live_frame(camera_id)
            
            if frame_data:
                await websocket.send_bytes(frame_data)
            
            await asyncio.sleep(0.033)  # ~30 FPS
    
    except WebSocketDisconnect:
        ws_manager.disconnect_camera(websocket, camera_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect_camera(websocket, camera_id)