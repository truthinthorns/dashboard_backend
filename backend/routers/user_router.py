from backend.models.user import CreateUser, MongoUser, UpdateUser
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from backend.util.util import get_user
from backend.util.auth_util import get_password_hash, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    response_model=MongoUser,
    status_code=200,
)
async def add_user(user: CreateUser):
    try:
        user.password = get_password_hash(user.password)
        mongo_user = MongoUser(**user.model_dump())
        new_user = await mongo_user.create()
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="/all",
    summary="Get all Users",
    description="This endpoint will return a list of all Users. This should not be used except for testing!",
    response_model=list[MongoUser],
    status_code=200,
)
async def get_all_users(_: Annotated[MongoUser, Depends(get_current_user)]):
    try:
        return await MongoUser.find_all().to_list()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.delete(
    path="/all",
    summary="Delete all Users",
    description="This endpoint will DELETE ALL Users. This should not be used except for testing!",
    response_model=dict,
    status_code=200,
)
async def delete_all_users(_: Annotated[MongoUser, Depends(get_current_user)]):
    try:
        await MongoUser.find_all().delete()
        return {"message": "Deleted ALL Users"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="/{id}",
    summary="Get User by id",
    description="This endpoint will return the User dictionary, if found, based on the passed in id",
    response_model=MongoUser,
    status_code=200,
    responses={404: UserNotFound},
)
async def get_user(
    _: Annotated[MongoUser, Depends(get_current_user)],
    user: MongoUser = Depends(get_user),
):
    return user


@router.put(
    path="/{id}",
    summary="Update User by id",
    description="This endpoint will try to find a User with the passed in id, then update and return the updated dictionary.",
    response_model=MongoUser,
    status_code=200,
    responses={404: UserNotFound},
)
async def update_user(
    updates: UpdateUser,
    _: Annotated[MongoUser, Depends(get_current_user)],
    user: MongoUser = Depends(get_user),
):
    try:
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
async def delete_user(
    _: Annotated[MongoUser, Depends(get_current_user)],
    user: MongoUser = Depends(get_user),
):
    try:
        await user.delete()
        return {"message": "User deleted!"}
    except Exception as e:
        raise e
