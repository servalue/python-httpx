"""Модели для API запросов."""

from os import name
from pydantic import BaseModel

class CreateUser(BaseModel):
    """Модель для создания пользователя."""
    name: str
    job: str