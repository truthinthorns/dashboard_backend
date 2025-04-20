from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class RecoveryQuestions(BaseModel):
    question: str = Field(default="What color is the sky?", min_length=10, max_length=128)
    answer: str = Field(default="blue", min_length=1, max_length=128, description="This is case sensitive!")


class User(Document):
    username: str = Field(default="username", description="This is case sensitive!", min_length=6, max_length=32, pattern="^[A-Za-z0-9_]+$")
    email: EmailStr = Field(default="test@example.com", description="This is case sensitive!")
    password: str
    recovery_questions: Optional[List[RecoveryQuestions]] = None
    creation_method: Optional[str] = None


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    recovery_questions: Optional[List[RecoveryQuestions]] = None
