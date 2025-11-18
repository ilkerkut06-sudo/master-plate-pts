from typing import List, Optional
from datetime import datetime, timedelta
from app.database.mongo import get_database
from app.models.log import SystemLog

class LogService:
    """Service for managing system logs"""
    
    async def create_log(self, log: SystemLog) -> SystemLog:
        """Create new log entry"""
        db = await get_database()
        log_dict = log.model_dump()
        
        result = await db.logs.insert_one(log_dict)
        log_dict["_id"] = str(result.inserted_id)
        
        return SystemLog(**log_dict)
    
    async def get_recent_logs(self, limit: int = 100) -> List[SystemLog]:
        """Get recent logs"""
        db = await get_database()
        logs = []
        
        cursor = db.logs.find().sort("created_at", -1).limit(limit)
        
        async for log_dict in cursor:
            logs.append(SystemLog(**log_dict))
        
        return logs
    
    async def get_logs_by_type(self, log_type: str, limit: int = 100) -> List[SystemLog]:
        """Get logs by type"""
        db = await get_database()
        logs = []
        
        cursor = db.logs.find({"log_type": log_type}).sort("created_at", -1).limit(limit)
        
        async for log_dict in cursor:
            logs.append(SystemLog(**log_dict))
        
        return logs
    
    async def get_logs_by_severity(self, severity: str, limit: int = 100) -> List[SystemLog]:
        """Get logs by severity"""
        db = await get_database()
        logs = []
        
        cursor = db.logs.find({"severity": severity}).sort("created_at", -1).limit(limit)
        
        async for log_dict in cursor:
            logs.append(SystemLog(**log_dict))
        
        return logs
    
    async def clean_old_logs(self, days: int = 30) -> int:
        """Clean logs older than specified days"""
        db = await get_database()
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await db.logs.delete_many({"created_at": {"$lt": cutoff_date}})
        
        return result.deleted_count

# Global log service
log_service = LogService()