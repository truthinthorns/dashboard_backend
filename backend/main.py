from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from backend.routers.user_router import router as user_router
from backend.routers.weather_router import router as weather_router
from backend.routers.todo_router import router as todo_router
from backend.db_connector import init_db
from backend.models.token import Token
from backend.util.auth_util import authenticate_user, create_access_token
import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated
from datetime import timedelta


ACCESS_TOKEN_EXPIRE_MINUTES = 15


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "*"]

app.include_router(user_router)
app.include_router(weather_router)
app.include_router(todo_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
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
    return Token(access_token=access_token, token_type="bearer")


def start():
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)
