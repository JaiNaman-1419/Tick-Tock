from pydantic import Field,BaseModel


class TodoModel(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=255)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class ListTodoModel(BaseModel):
    id: int
    data: TodoModel
