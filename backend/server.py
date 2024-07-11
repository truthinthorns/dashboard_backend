from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db_connector import init_db
from routers.user_router import router as user_router
from routers.weather_router import router as weather_router
from routers.todo_router import router as todo_router

app = FastAPI()

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

@app.on_event("startup")
async def startup_event():
    await init_db()
