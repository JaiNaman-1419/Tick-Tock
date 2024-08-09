from models import Todos
from typing import Annotated
from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session
from .base_api import BaseApi, ROUTER
from validations import AdminTodoModel, AdminListTodoModel

from fastapi import (
    status, Depends,
    APIRouter, HTTPException
)


@cbv(ROUTER)
class PostTodoApi(BaseApi):

    @ROUTER.post(
        path="/create",
        response_model=AdminListTodoModel,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_todos_list(
        self,
        todo_request: AdminTodoModel,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
    ):

        if user.get("role").lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden access."
            )

        todo = Todos(**todo_request.model_dump())

        db.add(todo)
        db.commit()

        return AdminListTodoModel(
            id=todo.id,
            data=todo_request
        )
