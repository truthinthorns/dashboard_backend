# from beanie import init_beanie
# import motor.motor_asyncio

# from models.user import User
# from models.todo import Todo


# async def init_db():
#     client = motor.motor_asyncio.AsyncIOMotorClient(
#         "mongodb://127.0.0.1:27017/db"
#     )

#     await init_beanie(database=client.db_name, document_models=[User, Todo])

import firebase_admin
from firebase_admin import firestore

cred_obj = firebase_admin.credentials.Certificate('../firebase_credentials.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred_obj)
    db = firestore.client()
