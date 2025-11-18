from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.plate import Plate
from app.services.plate_service import plate_service

router = APIRouter(prefix="/api/plates", tags=["plates"])

@router.get("/", response_model=List[Plate])
async def get_plates(limit: int = Query(50, ge=1, le=500)):
    """Get recent plates"""
    return await plate_service.get_recent_plates(limit)

@router.get("/{plate_id}", response_model=Plate)
async def get_plate(plate_id: str):
    """Get plate by ID"""
    plate = await plate_service.get_plate(plate_id)
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate

@router.get("/camera/{camera_id}", response_model=List[Plate])
async def get_plates_by_camera(camera_id: str, limit: int = Query(50, ge=1, le=500)):
    """Get plates by camera"""
    return await plate_service.get_plates_by_camera(camera_id, limit)

@router.get("/search/{plate_number}", response_model=List[Plate])
async def search_plate(plate_number: str):
    """Search plates by plate number"""
    return await plate_service.search_plate(plate_number)

@router.get("/stats/summary")
async def get_plate_stats():
    """Get plate statistics"""
    return await plate_service.get_stats()