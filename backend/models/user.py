from beanie import Document
from pydantic import BaseModel
from typing import Optional


class User(Document):
    username: str
    email: str
    password: str

    class Settings:
        name = "user_collection"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "email@host.com",
                "password": "password"
            }
        }


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None