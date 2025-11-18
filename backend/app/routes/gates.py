from fastapi import APIRouter, HTTPException
from typing import List
from app.models.gate import Gate
from app.services.gate_service import gate_service

router = APIRouter(prefix="/api/gates", tags=["gates"])

@router.post("/", response_model=Gate)
async def create_gate(gate: Gate):
    """Create new gate"""
    return await gate_service.create_gate(gate)

@router.get("/", response_model=List[Gate])
async def get_gates():
    """Get all gates"""
    return await gate_service.get_all_gates()

@router.get("/{gate_id}", response_model=Gate)
async def get_gate(gate_id: str):
    """Get gate by ID"""
    gate = await gate_service.get_gate(gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found")
    return gate

@router.put("/{gate_id}", response_model=Gate)
async def update_gate(gate_id: str, gate_data: dict):
    """Update gate"""
    gate = await gate_service.update_gate(gate_id, gate_data)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found")
    return gate

@router.delete("/{gate_id}")
async def delete_gate(gate_id: str):
    """Delete gate"""
    success = await gate_service.delete_gate(gate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gate not found")
    return {"message": "Gate deleted successfully"}

@router.post("/{gate_id}/open")
async def open_gate(gate_id: str, duration: dict = None):
    """Open gate"""
    dur = duration.get("duration") if duration else None
    success = await gate_service.open_gate(gate_id, dur)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to open gate")
    return {"message": "Gate opened successfully"}

@router.post("/{gate_id}/test")
async def test_gate(gate_id: str):
    """Test gate operation"""
    success = await gate_service.test_gate(gate_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to test gate")
    return {"message": "Gate test successful"}