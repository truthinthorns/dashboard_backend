from beanie import Document, Indexed
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Annotated


class RecoveryQuestions(BaseModel):
    question: str = Field(
        default="What color is the sky?",
        description="The question the User picked",
        min_length=10,
        max_length=128,
    )
    answer: str = Field(
        default="blue",
        description="The HASHED answer the User entered for the question. Should NOT be the user's raw input!",
        min_length=1,
        max_length=128,
    )


class User(Document):
    username: Annotated[str, Indexed(unique=True)] = Field(
        default="username",
        description="The username for the User. This is case sensitive!",
        min_length=6,
        max_length=32,
        pattern="^[A-Za-z0-9_]+$",
    )
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(
        default="test@example.com",
        description="The email for the User. This is case sensitive!",
    )
    password: str = Field(
        default="password",
        description="The HASHED password for the User. Should NOT be the user's raw input!",
    )
    recovery_questions: Optional[List[RecoveryQuestions]] = Field(
        default=[{"question": "What color is the sky?", "answer": "Blue"}],
        description="A list of recovery questions the User can use to recover their info.",
    )
    creation_method: Optional[str] = Field(
        default="IDK", description="The method used to create this User."
    )
    

class UpdateUser(BaseModel):
    username: str = Field(
        default="username",
        description="The username for the User. This is case sensitive!",
        min_length=6,
        max_length=32,
        pattern="^[A-Za-z0-9_]+$",
    )
    email: EmailStr = Field(
        default="test@example.com",
        description="The email for the User. This is case sensitive!",
    )
    password: str = Field(
        default="password",
        description="The HASHED password for the User. Should NOT be the user's raw input!",
    )
    recovery_questions: Optional[List[RecoveryQuestions]] = Field(
        default=[{"question": "What color is the sky?", "answer": "Blue"}],
        description="A list of recovery questions the User can use to recover their info.",
    )
