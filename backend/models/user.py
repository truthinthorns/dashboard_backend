from beanie import Document
from pydantic import BaseModel
from typing import Optional, List


class RecoveryQuestions(BaseModel):
    question: str
    answer: str


class User(Document):
    username: str
    email: str
    password: str
    recovery_questions: Optional[List[RecoveryQuestions]] = None
    creation_method: Optional[str] = None

    class Settings:
        name = "user_collection"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "email@host.com",
                "password": "password",
                "creation_method": "swagger"
            }
        }


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    recovery_questions: Optional[List[RecoveryQuestions]] = None
