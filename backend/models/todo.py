from beanie import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Todo(Document):
    user_id: str
    content: str
    title: str
    date_created: datetime
    finish_by: Optional[datetime] = None


    class Settings:
        name = "todo_collection"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "5eb7cf5a86d9755df3a6c593",
                "content": "do x and y and z",
                "title": "tasks",
                "date_created": datetime.now(),
                "finish_by": datetime.now()
            }
        }


class UpdateTodo(BaseModel):
    content: Optional[str] = ""
    title: Optional[str] = ""
    finish_by: Optional[datetime] = None