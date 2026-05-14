from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from backend.models.user import BaseUser
from backend.util.auth_util import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from backend.util.util import get_todo


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


ACCESS_TOKEN_EXPIRE_MINUTES = 15


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> dict:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # JS cannot access
        secure=True,  # HTTP local dev
        samesite="None",
        max_age=3600,
        path="/",
    )

    return {"message": "Login successful", "user": user}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Successfully logged out"}


@router.get("/me")
async def read_users_me(current_user: BaseUser = Depends(get_current_user)):
    print(current_user)
    return {"username": current_user.username}
