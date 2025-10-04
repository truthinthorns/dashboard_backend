from beanie import init_beanie
import motor.motor_asyncio

from backend.models.user import MongoUser
from backend.models.todo import Todo


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        
    )
    await init_beanie(database=client["db"], document_models=[MongoUser, Todo])
