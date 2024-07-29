from models.todo import Todo, UpdateTodo
from models.user import User, UpdateUser
from fastapi import APIRouter, HTTPException

from db_connector import db

import utils.util as util


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

todos_ref = db.collection("todos")

# todo: add code to relate the users and todos


@router.post('')
async def add_todo(todo: Todo):
    try:
        temp_ref = todos_ref.document(str(todo.uuid))
        temp_ref.set(todo.model_dump())
        _todo = temp_ref.get()
        return _todo.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    

@router.get('')
async def get_all_todos():
    try:
        return [todo.to_dict() for todo in todos_ref.stream()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/{id}')
async def get_todo(_uuid: str):
    try:
        todo_ref = todos_ref.document(_uuid)
        todo = todo_ref.get()
        if not todo.exists:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        return todo.to_dict()
    except Exception as e:
        raise e


@router.put('/{id}')
async def update_todo(_uuid: str, updates: UpdateTodo):
    try:
        temp_ref = todos_ref.document(_uuid)
        todo = temp_ref.get()
        if not todo.exists:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        updates_dict = updates.model_dump()
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(status_code=400, detail="Empty update request. Likely incorrect field names.")
    except Exception as e:
        raise e
    try:
        temp_ref.update(update)
        todo_ref = todos_ref.document(_uuid)
        todo = todo_ref.get()
        return todo.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update user: {str(e)}")


@router.delete('/{id}')
async def delete_todo(_uuid: str):
    try:
        temp_ref = todos_ref.document(_uuid)
        todo = temp_ref.get()
        if not todo.exists:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        return temp_ref.delete()
    except Exception as e:
        raise e