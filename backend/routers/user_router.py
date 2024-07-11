from models.user import User, UpdateUser
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('')
async def add_user(user: User):
    try:
        new_user = await user.create()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('')
async def get_all_users():
    try:
        users = await User.find_all().to_list()
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/{id}')
async def get_user(id: PydanticObjectId):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return user
    except Exception as e:
        raise e


@router.put('/{id}')
async def update_user(id: PydanticObjectId, updates: UpdateUser):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        updates_dict = dict(updates)
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(status_code=400, detail="Empty update request. Likely incorrect field names.")
    except Exception as e:
        raise e
    try:
        updated_user = await user.update({"$set": update})
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update user: {str(e)}")


@router.delete('/{id}')
async def delete_user(id: PydanticObjectId):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        await user.delete()
        return {"message": "User deleted!"}
    except Exception as e:
        raise e