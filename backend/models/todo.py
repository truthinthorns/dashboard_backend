from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Todo(BaseModel):
    uuid: str
    user_id: str
    description: str
    title: str
    date_created: datetime = datetime.now()
    finish_by: Optional[datetime] = None
    status: Optional[str] = None
    resolution: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = 0


class UpdateTodo(BaseModel):
    description: Optional[str] = None
    title: Optional[str] = None
    finish_by: Optional[datetime] = None
    status: Optional[str] = None
    resolution: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = 0
