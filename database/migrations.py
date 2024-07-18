from .database import ENGINE
from models import users_model, todos_models


def create_database():
    users_model.BASE.metadata.create_all(bind=ENGINE)
    todos_models.BASE.metadata.create_all(bind=ENGINE)
