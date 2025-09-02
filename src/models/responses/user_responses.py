"""Модели для API ответов."""

from pydantic import BaseModel
from typing import List


class Support(BaseModel):    
    """Модель поддержки."""
    url: str
    text: str

class User(BaseModel):
    """Модель пользователя."""
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class SingleUserResponse(BaseModel):
    """Модель ответа для получения одного пользователя."""
    data: User
    support: Support
    
class ListUsersResponse(BaseModel):
    """Модель ответа для получения списка пользователей."""
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[User]
    support: Support

