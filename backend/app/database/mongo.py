from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.logger import logger

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)
        mongodb.db = mongodb.client[settings.MONGO_DB_NAME]
        # Test connection
        await mongodb.client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {settings.MONGO_DB_NAME}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("MongoDB connection closed")

async def get_database():
    """Get database instance"""
    return mongodb.db