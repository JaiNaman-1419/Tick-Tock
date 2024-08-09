from typing import List
from models import Todos
from fastapi_utils.cbv import cbv
from .base_api import BaseApi, ROUTER
from validations import AdminTodoModel, AdminListTodoModel

from fastapi import (
    status, Path,
    APIRouter, HTTPException
)


@cbv(ROUTER)
class GetTodoApi(BaseApi):

    @ROUTER.get(
        path="/list",
        status_code=status.HTTP_200_OK,
        response_model=List[AdminListTodoModel],
    )
    async def get_todos_list(
        self,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY
    ):
        if user.get("role").lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden access."
            )

        todos = db.query(Todos).all()

        return [
            AdminListTodoModel(
                id=todo.id,
                data=AdminTodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                    owner_id=todo.owner_id,
                )
            )
            for todo in todos
        ]

    @ROUTER.get(
        path="/list/{todo_id}",
        response_model=AdminListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def get_todo_by_id(
        self,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
        todo_id: int = Path(gt=0)
    ):
        if user.get("role").lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden access."
            )
        
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if todo is not None:
            return AdminListTodoModel(
                id=todo.id,
                data=AdminTodoModel(
                    title=todo.title,
                    description=todo.description,
                    priority=todo.priority,
                    complete=todo.complete,
                    owner_id=todo.owner_id
                )
            )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
