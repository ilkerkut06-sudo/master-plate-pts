from fastapi import APIRouter, HTTPException
from typing import List
from app.models.site import Site
from app.services.site_service import site_service

router = APIRouter(prefix="/api/sites", tags=["sites"])

@router.post("/", response_model=Site)
async def create_site(site: Site):
    """Create new site"""
    return await site_service.create_site(site)

@router.get("/", response_model=List[Site])
async def get_sites():
    """Get all sites"""
    return await site_service.get_all_sites()

@router.get("/{site_id}", response_model=Site)
async def get_site(site_id: str):
    """Get site by ID"""
    site = await site_service.get_site(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.put("/{site_id}", response_model=Site)
async def update_site(site_id: str, site_data: dict):
    """Update site"""
    site = await site_service.update_site(site_id, site_data)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.delete("/{site_id}")
async def delete_site(site_id: str):
    """Delete site"""
    success = await site_service.delete_site(site_id)
    if not success:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"message": "Site deleted successfully"}