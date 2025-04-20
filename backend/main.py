from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.user_router import router as user_router
from backend.routers.weather_router import router as weather_router
from backend.routers.todo_router import router as todo_router
from backend.db_connector import init_db

import uvicorn

from contextlib import asynccontextmanager


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


def start():
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)
