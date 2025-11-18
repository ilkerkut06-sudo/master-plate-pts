from fastapi import APIRouter, Query
from typing import List
from app.models.log import SystemLog
from app.services.log_service import log_service

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.get("/", response_model=List[SystemLog])
async def get_logs(limit: int = Query(100, ge=1, le=500)):
    """Get recent logs"""
    return await log_service.get_recent_logs(limit)

@router.get("/type/{log_type}", response_model=List[SystemLog])
async def get_logs_by_type(log_type: str, limit: int = Query(100, ge=1, le=500)):
    """Get logs by type"""
    return await log_service.get_logs_by_type(log_type, limit)

@router.get("/severity/{severity}", response_model=List[SystemLog])
async def get_logs_by_severity(severity: str, limit: int = Query(100, ge=1, le=500)):
    """Get logs by severity"""
    return await log_service.get_logs_by_severity(severity, limit)

@router.delete("/clean")
async def clean_old_logs(days: int = Query(30, ge=1)):
    """Clean logs older than specified days"""
    deleted_count = await log_service.clean_old_logs(days)
    return {"message": f"Cleaned {deleted_count} old logs"}