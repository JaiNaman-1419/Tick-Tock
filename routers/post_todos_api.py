from models import Todos
from fastapi_utils.cbv import cbv
from .base_api import BaseApi, ROUTER
from fastapi import status, HTTPException
from validations import TodoModel, ListTodoModel


@cbv(ROUTER)
class PostTodoApi(BaseApi):

    @ROUTER.post(
        path="/create",
        response_model=ListTodoModel,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_todos_list(
        self,
        todo_request: TodoModel,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
    ):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed :("
            )

        todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
        
        db.add(todo_model)
        db.commit()

        return ListTodoModel(
            id=todo_model.id,
            data=todo_request
        )
