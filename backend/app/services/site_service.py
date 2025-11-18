from typing import List, Optional
from app.database.mongo import get_database
from app.models.site import Site

class SiteService:
    """Service for managing sites"""
    
    async def create_site(self, site: Site) -> Site:
        """Create new site"""
        db = await get_database()
        site_dict = site.model_dump()
        
        result = await db.sites.insert_one(site_dict)
        site_dict["_id"] = str(result.inserted_id)
        
        return Site(**site_dict)
    
    async def get_site(self, site_id: str) -> Optional[Site]:
        """Get site by ID"""
        db = await get_database()
        site_dict = await db.sites.find_one({"id": site_id})
        
        if site_dict:
            return Site(**site_dict)
        return None
    
    async def get_all_sites(self) -> List[Site]:
        """Get all sites"""
        db = await get_database()
        sites = []
        
        async for site_dict in db.sites.find():
            sites.append(Site(**site_dict))
        
        return sites
    
    async def update_site(self, site_id: str, site_data: dict) -> Optional[Site]:
        """Update site"""
        db = await get_database()
        
        result = await db.sites.update_one(
            {"id": site_id},
            {"$set": site_data}
        )
        
        if result.modified_count > 0:
            return await self.get_site(site_id)
        return None
    
    async def delete_site(self, site_id: str) -> bool:
        """Delete site"""
        db = await get_database()
        result = await db.sites.delete_one({"id": site_id})
        
        return result.deleted_count > 0

# Global site service
site_service = SiteService()