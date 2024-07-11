from models.todo import Todo, UpdateTodo
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

# todo: add code to relate the users and todos


@router.post('')
async def add_todo(todo: Todo):
    try:
        new_todo = await todo.create()
        return new_todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('')
async def get_all_todos():
    try:
        todos = await Todo.find_all().to_list()
        return todos
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/{id}')
async def get_todo(id: PydanticObjectId):
    try:
        todo = await Todo.get(id)
        if todo == None:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        return todo
    except Exception as e:
        raise e


@router.put('/{id}')
async def update_todo(id: PydanticObjectId, updates: UpdateTodo):
    try:
        todo = await Todo.get(id)
        if todo == None:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        updates_dict = dict(updates)
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(status_code=400, detail="Empty update request. Likely incorrect field names.")
    except Exception as e:
        raise e
    try:
        updated_todo = await todo.update({"$set": update})
        return updated_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update todo: {str(e)}")


@router.delete('/{id}')
async def delete_todo(id: PydanticObjectId):
    try:
        todo = await Todo.get(id)
        if todo == None:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        await todo.delete()
        return {"message": "Todo deleted!"}
    except Exception as e:
        raise e