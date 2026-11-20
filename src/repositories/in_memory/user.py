from typing import Optional, List
from src.models import User
from src.repositories.base import UserRepository


class InMemoryUserRepository(UserRepository):
    """InMemory-реализация репозитория пользователей."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id: int = 1

    def get(self, entity_id: int) -> Optional[User]:
        return self._users.get(entity_id)

    def get_all(self) -> List[User]:
        return list(self._users.values())

    def add(self, entity: User) -> User:
        entity.id = self._next_id
        self._next_id += 1
        self._users[entity.id] = entity
        return entity

    def update(self, entity_id: int, **kwargs) -> Optional[User]:
        user = self._users.get(entity_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
        return user

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._users:
            del self._users[entity_id]
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None