from models.user import User, UpdateUser
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from firebase_admin import db
from uuid import uuid4
from db_connector import default_app


users_ref = db.reference('/users')


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('')
async def add_user(user: User):
    try:
        _uuid = str(uuid4())
        temp_ref = users_ref.child(_uuid)
        temp_ref.set(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('')
async def get_all_users():
    try:
        return users_ref.get()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/{id}')
async def get_user(_uuid: str):
    try:
        temp_ref = users_ref.child(_uuid)
        user = temp_ref.get()
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        print(user)
        return user
    except Exception as e:
        raise e


@router.put('/{id}')
async def update_user(_uuid: str, updates: UpdateUser):
    try:
        temp_ref = users_ref.child(_uuid)
        user = temp_ref.get()
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        updates_dict = updates.model_dump()
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(status_code=400, detail="Empty update request. Likely incorrect field names.")
    except Exception as e:
        raise e
    try:
        updated_user = temp_ref.update(update)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update user: {str(e)}")


@router.delete('/{id}')
async def delete_user(_uuid: str):
    try:
        temp_ref = users_ref.child(_uuid)
        user = temp_ref.get()
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return temp_ref.delete()
    except Exception as e:
        raise e