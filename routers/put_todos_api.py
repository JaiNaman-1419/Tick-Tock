from models import Todos
from fastapi_utils.cbv import cbv
from .get_todos_api import GetTodoApi
from .base_api import BaseApi, ROUTER
from fastapi import Path, status, HTTPException
from validations import TodoModel, ListTodoModel


@cbv(ROUTER)
class PutTodoApi(BaseApi):

    @ROUTER.put(
        path="/edit/{todo_id}",
        response_model=ListTodoModel,
        status_code=status.HTTP_200_OK,
    )
    async def edit_todos_list(
        self,
        todo_request: TodoModel,
        db: BaseApi._DB_DEPENDENCY,
        user: BaseApi._OAUTH_DEPENDENCY,
        todo_id: int = Path(gt=0),
    ):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed :("
            )

        todo_model = db.query(Todos).filter(
            Todos.id == todo_id
        ).filter(
            Todos.owner_id == user.get("id")
        ).first()

        if todo_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found :("
            )
        
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

        return await GetTodoApi().get_todo_by_id(db, todo_id=todo_id, user=user)
