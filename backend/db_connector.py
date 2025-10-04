from beanie import init_beanie
import motor.motor_asyncio

from backend.models.user import MongoUser
from backend.models.todo import Todo


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb+srv://user:2jMhJsFvIAfQcMn2@kanboard.aw9zrws.mongodb.net/"
    )
    await init_beanie(database=client["db"], document_models=[MongoUser, Todo])
