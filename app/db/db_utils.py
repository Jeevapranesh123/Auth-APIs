from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.db.db import db


async def connect_to_mongodb() -> None:
    logger.info("Connect to the database...")
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
    )
    logger.info("Successfully connected to the database!")


async def close_mongo_connection():
    logger.info("Close database connection...")
    db.client.close()
    logger.info("The database connection is closed!")
