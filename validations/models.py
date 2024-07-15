from pydantic import BaseModel


class TodoModel(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool


class ListTodoModel(BaseModel):
    id: int
    data: TodoModel
