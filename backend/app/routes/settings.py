from fastapi import APIRouter
from app.utils.ocr_engines.ocr_manager import ocr_manager
from app.services.camera_service import camera_service

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/ocr-engines")
async def get_available_ocr_engines():
    """Get available OCR engines"""
    available = ocr_manager.get_available_engines()
    current = ocr_manager.get_current_engine()
    
    return {
        "available_engines": available,
        "current_engine": current,
        "engines": [
            {"id": "paddle", "name": "PaddleOCR", "description": "Fast and accurate for Asian languages"},
            {"id": "easy", "name": "EasyOCR", "description": "Good Turkish character support"},
            {"id": "tesseract", "name": "Tesseract", "description": "Open source OCR engine"},
            {"id": "yolo", "name": "YOLO", "description": "Plate detection only"},
            {"id": "hybrid", "name": "Hybrid", "description": "Best result from all engines"}
        ]
    }

@router.post("/ocr-engine")
async def set_global_ocr_engine(data: dict):
    """Set global OCR engine"""
    engine = data.get("engine")
    if not engine:
        return {"error": "Engine name required"}
    
    success = ocr_manager.set_engine(engine)
    
    if success:
        return {"message": f"OCR engine set to {engine}"}
    else:
        return {"error": f"Failed to set engine to {engine}"}

@router.get("/system-info")
async def get_system_info():
    """Get system information"""
    return {
        "version": "1.0.0",
        "name": "EvoPlate Enterprise Edition",
        "active_cameras": len(camera_service.active_pipelines),
        "ocr_engine": ocr_manager.get_current_engine()
    }