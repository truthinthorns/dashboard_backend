from beanie import Document
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Todo(Document):
    user_id: str
    description: str
    title: str
    date_created: datetime = datetime.now()
    finish_by: Optional[datetime] = None
    status: Optional[str] = None
    resolution: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = 0


    class Settings:
        name = "todo_collection"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "5eb7cf5a86d9755df3a6c593",
                "description": "do x and y and z",
                "title": "tasks",
                "finish_by": datetime.now()
            }
        }


class UpdateTodo(BaseModel):
    description: Optional[str] = None
    title: Optional[str] = None
    finish_by: Optional[datetime] = None
    status: Optional[str] = None
    resolution: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = 0
