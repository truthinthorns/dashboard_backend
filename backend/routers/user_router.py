from models.user import User, UpdateUser
from fastapi import APIRouter, HTTPException

from db_connector import db
import utils.util as util

from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

users_ref = db.collection("users")




@router.post('')
async def add_user(user: User):
    try:
        temp_ref = users_ref.document(str(user.uuid))
        temp_ref.set(user.model_dump())
        _user = temp_ref.get()
        return _user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('')
async def get_all_users():
    try:
        return [user.to_dict() for user in users_ref.stream()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/{id}')
async def get_user(_uuid: str):
    try:
        user_ref = users_ref.document(_uuid)
        user = user_ref.get()
        if not user.exists:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return user.to_dict()
    except Exception as e:
        raise e


@router.put('/{id}')
async def update_user(_uuid: str, updates: UpdateUser):
    try:
        temp_ref = users_ref.document(_uuid)
        user = temp_ref.get()
        if not user.exists:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        updates_dict = updates.model_dump()
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(status_code=400, detail="Empty update request. Likely incorrect field names.")
    except Exception as e:
        raise e
    try:
        temp_ref.update(update)
        user_ref = users_ref.document(_uuid)
        user = user_ref.get()
        return user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update user: {str(e)}")


@router.delete('/{id}')
async def delete_user(_uuid: str):
    try:
        temp_ref = users_ref.document(_uuid)
        user = temp_ref.get()
        if not user.exists:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return temp_ref.delete()
    except Exception as e:
        raise e


@router.post("/login")
async def login(email: str, password: str):
    try:
        query_list = [user.to_dict() for user in users_ref.where(filter=FieldFilter("email", "==", email)).stream()]
        if len(query_list) != 1:
            raise HTTPException(status_code=500,detail="More than one user found with that email")
        else:
            user = query_list[0]
            if util.check_password(password, user['password']):
                print('matches!')
            else:
                raise HTTPException(status_code=403, detail="invalid email/password")
            return query_list[0]
    except Exception as e:
        raise e