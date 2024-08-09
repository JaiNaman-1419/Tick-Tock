from typing import List
from models import Todos
from .base_api import BaseApi
from fastapi_utils.cbv import cbv
from validations import TodoModel, ListTodoModel

from fastapi import (
    Path, status, 
    APIRouter, HTTPException
)


ROUTER = APIRouter(prefix='/todos', tags=["TODO"])


@cbv(ROUTER)
class GetTodoApi(BaseApi):

    @ROUTER.get(
        path='/list',
        status_code=status.HTTP_200_OK,
        response_model=List[ListTodoModel],
    )
    async def get_todos_list(
        self,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY
    ):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed :("
            )

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return [
            ListTodoModel(
                id=todo.id,
                data=TodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                )
            )
            for todo in todos
        ]

    @ROUTER.get(
        path='/list/{todo_id}',
        response_model=ListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def get_todo_by_id(
        self,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
        todo_id: int = Path(gt=0)
    ):

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed :("
            )

        todo = db.query(Todos).filter(
            Todos.id == todo_id
        ).filter(
            Todos.owner_id == user.get("id")
        ).first()

        if todo is not None:
            return ListTodoModel(
                id=todo.id,
                data=TodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                )
            )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )
