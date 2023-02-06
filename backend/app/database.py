"""Module contains database connection."""
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(settings.DATABASE_URL)
print("Connected to MongoDB...")

db = client[settings.MONGO_INITDB_DATABASE]

User = db.users
