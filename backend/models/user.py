from beanie import Document, Indexed, PydanticObjectId, Indexed
from pydantic import BaseModel, Field, EmailStr, ConfigDict, ConfigDict
from typing import Optional, List, Annotated, Annotated


class RecoveryQuestions(BaseModel):
    question: str = Field(
        example="What color is the sky?",
        description="The question the User picked",
        min_length=10,
        max_length=128,
    )
    answer: str = Field(
        example="blue",
        description="The HASHED answer the User entered for the question. Should NOT be the user's raw input!",
        min_length=1,
        max_length=128,
    )


# Common fields for creation
class BaseUser(BaseModel):
    id: PydanticObjectId = Field(default=None)
    username: Annotated[str, Indexed(unique=True)] = Field(
        description="The username for the User. This is case sensitive!",
        min_length=6,
        max_length=32,
        pattern="^[A-Za-z0-9_]+$",
    )
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(
        description="The email for the User. This is case sensitive!",
    )
    recovery_questions: Optional[List[RecoveryQuestions]] = Field(
        default=None,
        description="A list of recovery questions the User can use to recover their info.",
    )
    creation_method: Optional[str] = Field(
        default=None, description="The method used to create this User.",
    )


# BaseUser + validated, raw password, used for endpoint validation
class CreateUser(BaseUser):
    password: str = Field(
        description="The RAW password for the User! Should hashed before insert into MongoDB!",
        min_length=8,
        max_length=48
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "recovery_questions": [{"question": "Color?", "answer": "Blue"}],
                "creation_method": "Swagger",
                "password": "supersecret123",
            }
        }
    )


# BaseUser + hashed password, used to insert into MongoDB
class MongoUser(Document, BaseUser):
    password: str = Field(
        example="password",
        description="The HASHED password for the User. Should NOT be the user's raw input!",
    )
    

class UpdateUser(BaseModel):
    username: Optional[str] = Field(
        default=None,
        description="The username for the User. This is case sensitive!",
        min_length=6,
        max_length=32,
        pattern="^[A-Za-z0-9_]+$",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="The email for the User. This is case sensitive!",
    )
    password: Optional[str] = Field(
        default=None,
        description="The RAW password for the User! Should hashed before insert into MongoDB!",
        min_length=8,
        max_length=48,
    )
    recovery_questions: Optional[List[RecoveryQuestions]] = Field(
        default=None,
        description="A list of recovery questions the User can use to recover their info.",
    )

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "test@example.com",
                "password": "password",
                "recovery_questions": [{"question": "What color is the sky?", "answer": "Blue"}],
            }
        }
    )
