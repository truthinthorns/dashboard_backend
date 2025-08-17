from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timedelta


class Todo(Document):
    user_id: PydanticObjectId = Field(
        description="The user id of the user that created this Todo",
    )
    description: str = Field(
        description="The description of the todo. Generally, some info about it and maybe a list of things necessary to complete it.",
        min_length=8,
        max_length=16384,
    )
    title: str = Field(
        description="The title of the todo",
        min_length=8,
        max_length=512,
    )
    date_created: datetime = Field(
        default_factory=datetime.now, description="The datetime this Todo was created."
    )
    finish_by: Optional[datetime] = Field(
        default=None,
        description="The datetime that this Todo should be completed by.",
    )
    status: Optional[str] = Field(
        default=None,
        description="The current status of the Todo",
        min_length=1,
        max_length=128,
    )
    resolution: Optional[str] = Field(
        default=None,
        description="Comment about how this was resolved",
        min_length=1,
        max_length=128,
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="A list of tags for the Todo. Could be used for grouping Todos, for example.",
    )
    priority: Optional[int] = Field(
        default=None,
        description="The priority level of the Todo.",
        ge=-10,
        le=10,
    )

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
        json_schema_extra={
            "example": {
                "user_id": str(PydanticObjectId()),
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "date_created": datetime.now(),
                "finish_by": (datetime.now() + timedelta(days=2)).isoformat(),
                "status": "done",
                "resolution": "went to store",
                "tags": ["groceries", "urgent"],
                "priority": 5,
            }
        },
    )


class UpdateTodo(BaseModel):
    description: Optional[str] = Field(
        default=None,
        description="The description of the todo. Generally, some info about it and maybe a list of things necessary to complete it.",
        min_length=8,
        max_length=16384,
    )
    title: Optional[str] = Field(
        default=None,
        description="The title of the todo",
        min_length=8,
        max_length=512,
    )
    finish_by: Optional[datetime] = Field(
        default=None,
        description="The datetime that this Todo should be completed by.",
    )
    status: Optional[str] = Field(
        default=None,
        description="The current status of the Todo",
        min_length=1,
        max_length=128,
    )
    resolution: Optional[str] = Field(
        default=None,
        description="Comment about how this was resolved",
        min_length=1,
        max_length=128,
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="A list of tags for the Todo. Could be used for grouping Todos.",
    )
    priority: Optional[int] = Field(
        default=None,
        description="The priority level of the Todo.",
        ge=-10,
        le=10,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries (updated)",
                "description": "Need to buy milk, bread, eggs, and butter",
                "finish_by": (datetime.now() + timedelta(days=5)).isoformat(),
                "status": "in progress",
                "resolution": None,
                "tags": ["groceries", "weekly"],
                "priority": 4,
            }
        }
    )
