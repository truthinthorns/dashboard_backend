from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router import router as user_router
from routers.weather_router import router as weather_router
from routers.todo_router import router as todo_router
from models.user import User

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "fakehashedsecret"
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "password": "fakehashedsecret2"
    },
}


app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:5173",
    "*"
]

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

def fake_decode_token(token):
    return User(username=token+"_fake_decoded", email="test@example.com")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/")
async def test(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user}

# to run, uvicorn server:app --port 5000 --reload