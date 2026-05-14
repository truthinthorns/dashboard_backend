from backend.models.todo import Todo, UpdateTodo
from backend.models.user import MongoUser as User
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from backend.util.util import get_todo
from backend.util.auth_util import get_current_user


router = APIRouter(
    prefix="/todo",
    tags=["Todo"],
)

TodoNotFound = {
    "description": "Todo not found",
    "content": {
        "application/json": {"example": {"detail": "No todo found with that id!"}}
    },
}

# todo: add code to relate the users and todos


@router.post(
    path="",
    summary="Create a new Todo",
    description="This endpoint will create a new Todo using the info that is passed in and then return it.",
    response_model=Todo,
    status_code=200,
)
async def add_todo(todo: Todo, _: Annotated[User, Depends(get_current_user)]):
    try:
        new_todo = await todo.create()
        return new_todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="/all",
    summary="Get all Todos",
    description="This endpoint will return a list of all Todos for the current User.",
    response_model=list[Todo],
    status_code=200,
)
async def get_all_todos(user: Annotated[User, Depends(get_current_user)]):
    try:
        todos = await Todo.find(Todo.user_id == user.id).to_list()
        return todos
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.delete(
    path="/all",
    summary="Delete all Todos",
    description="This endpoint will DELETE ALL Todos. This should not be used except for testing!",
    response_model=dict,
    status_code=200,
)
async def delete_all_todos(_: Annotated[User, Depends(get_current_user)]):
    try:
        await Todo.find_all().delete()
        return {"message": "Deleted ALL Todos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get(
    path="/{id}",
    summary="Get Todo by id",
    description="This endpoint will return the Todo dictionary, if found, based on the passed in id",
    response_model=Todo,
    status_code=200,
    responses={404: TodoNotFound},
)
async def get_todo(
    _: Annotated[User, Depends(get_current_user)],
    todo: Todo = Depends(get_todo),
):
    return todo


@router.put(
    path="/{id}",
    summary="Update Todo by id",
    description="This endpoint will try to find a Todo with the passed in id, then update and return the updated dictionary.",
    response_model=Todo,
    status_code=200,
    responses={404: TodoNotFound},
)
async def update_todo(
    updates: UpdateTodo,
    _: Annotated[User, Depends(get_current_user)],
    todo: Todo = Depends(get_todo),
):
    try:
        updates_dict = dict(updates)
        update = {k: v for k, v in updates_dict.items() if v is not None}
        if update == {}:
            raise HTTPException(
                status_code=400,
                detail="Empty update request. Likely incorrect field names.",
            )
    except Exception as e:
        raise e
    try:
        updated_todo = await todo.update({"$set": update})
        return updated_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to update todo: {str(e)}")


@router.delete(
    path="/{id}",
    summary="Delete Todo by id",
    description="This endpoint will delete the Todo, if found, based on the id",
    response_model=dict,
    status_code=200,
    responses={404: TodoNotFound},
)
async def delete_todo(
    _: Annotated[User, Depends(get_current_user)],
    todo: Todo = Depends(get_todo),
):
    try:
        await todo.delete()
        return {"message": "Todo deleted!"}
    except Exception as e:
        raise e
