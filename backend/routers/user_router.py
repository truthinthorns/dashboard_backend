from models.user import User, UpdateUser
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Path
from typing import List


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

UserNotFound = {
    "description": "User not found",
    "content": {
        "application/json": {"example": {"detail": "No user found with that id!"}}
    },
}


@router.post(
    path="",
    summary="Create a new User",
    description="This endpoint will create a new User using the info that is passed in and then return it.",
    response_model=User,
    status_code=200,
)
async def add_user(user: User):
    try:
        new_user = await user.create()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="",
    summary="Get all Users",
    description="This endpoint will return a list of all Users. This should not be used except for testing!",
    response_model=List[User],
    status_code=200,
)
async def get_all_users():
    try:
        return await User.find_all().to_list()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="/{id}",
    summary="Get User by id",
    description="This endpoint will return the User dictionary, if found, based on the passed in id",
    response_model=User,
    status_code=200,
    responses={404: UserNotFound},
)
async def get_user(id: PydanticObjectId = Path(example=str(PydanticObjectId()))):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return user
    except Exception as e:
        raise e


@router.put(
    path="/{id}",
    summary="Update User by id",
    description="This endpoint will try to find a User with the passed in id, then update and return the updated dictionary.",
    response_model=User,
    status_code=200,
    responses={404: UserNotFound},
)
async def update_user(
    updates: UpdateUser, id: PydanticObjectId = Path(example=str(PydanticObjectId()))
):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        updates_dict = dict(updates)
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(
                status_code=400,
                detail="Empty update request. Likely incorrect field names.",
            )
    except Exception as e:
        raise e
    try:
        updated_user = await user.update({"$set": update})
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update user: {str(e)}")


@router.delete(
    path="/{id}",
    summary="Delete User by id",
    description="This endpoint will delete the User, if found, based on the id",
    response_model=dict,
    status_code=200,
    responses={404: UserNotFound},
)
async def delete_user(id: PydanticObjectId = Path(example=str(PydanticObjectId()))):
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        await user.delete()
        return {"message": "User deleted!"}
    except Exception as e:
        raise e
