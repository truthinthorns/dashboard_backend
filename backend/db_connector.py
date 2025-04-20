from beanie import init_beanie
import motor.motor_asyncio

from models.user import User
from models.todo import Todo


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://user:password@localhost:27017"
    )
    await init_beanie(database=client["db"], document_models=[User, Todo])
