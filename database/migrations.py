from models import models
from .database import ENGINE


def create_database():
    models.BASE.metadata.create_all(bind=ENGINE)
