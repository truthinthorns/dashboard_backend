from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta


class Todo(Document):
    user_id: PydanticObjectId = Field(
        default=PydanticObjectId(),
        description="The user id of the user that created this Todo",
    )
    description: str = Field(
        default="This is the description of the todo",
        description="The description of the todo. Generally, some info about it and maybe a list of things necessary to complete it.",
        min_length=8,
        max_length=16384,
    )
    title: str = Field(
        default="This is the title of the todo",
        description="The title of the todo",
        min_length=8,
        max_length=512,
    )
    date_created: datetime = Field(
        default=datetime.now(), description="The datetime this Todo was created."
    )
    finish_by: Optional[datetime] = Field(
        default=datetime.now() + timedelta(days=7),
        description="The datetime that this Todo should be completed by.",
    )
    status: Optional[str] = Field(
        default="Done", description="I don't remember", min_length=1, max_length=128
    )
    resolution: Optional[str] = Field(
        default="Done",
        description="I don't remember this one either",
        min_length=1,
        max_length=128,
    )
    tags: Optional[List[str]] = Field(
        default=["Groceries", "Urgent"],
        description="A list of tags for the Todo. Could be used for grouping Todos, for example.",
    )
    priority: Optional[int] = Field(
        default=0, description="The priority level of the Todo.", ge=-10, le=10
    )


class UpdateTodo(BaseModel):
    description: str = Field(
        default="This is the description of the todo",
        description="The description of the todo. Generally, some info about it and maybe a list of things necessary to complete it.",
        min_length=8,
        max_length=16384,
    )
    title: str = Field(
        default="This is the title of the todo",
        description="The title of the todo",
        min_length=8,
        max_length=512,
    )
    finish_by: Optional[datetime] = Field(
        default=datetime.now() + timedelta(days=7),
        description="The datetime that this Todo should be completed by.",
    )
    status: Optional[str] = Field(
        default="Done", description="I don't remember", min_length=1, max_length=128
    )
    resolution: Optional[str] = Field(
        default="Done",
        description="I don't remember this one either",
        min_length=1,
        max_length=128,
    )
    tags: Optional[List[str]] = Field(
        default=["Groceries", "Urgent"],
        description="A list of tags for the Todo. Could be used for grouping Todos.",
    )
    priority: Optional[int] = Field(
        default=0, description="The priority level of the Todo.", ge=-10, le=10
    )
