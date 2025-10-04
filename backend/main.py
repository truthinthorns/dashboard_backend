from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth_router, todo_router, user_router, weather_router
from backend.db_connector import init_db
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)
app.include_router(weather_router.router)

origins = ["https://9000-firebase-dashboard2-1751145094776.cluster-f4iwdviaqvc2ct6pgytzw4xqy4.cloudworkstations.dev"]#,""http://localhost:5173", "https://5173-firebase-dashboard2-1751145094776.cluster-f4iwdviaqvc2ct6pgytzw4xqy4.cloudworkstations.dev/", "https://9000-firebase-dashboard2-1751145094776.cluster-f4iwdviaqvc2ct6pgytzw4xqy4.cloudworkstations.dev/", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)
