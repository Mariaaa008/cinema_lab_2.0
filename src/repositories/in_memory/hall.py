from typing import Optional, List
from src.models import Hall
from src.repositories.base import HallRepository


class InMemoryHallRepository(HallRepository):
    """InMemory-реализация репозитория залов."""

    def __init__(self) -> None:
        self._halls: dict[int, Hall] = {}
        self._next_id: int = 1

    def get(self, entity_id: int) -> Optional[Hall]:
        return self._halls.get(entity_id)

    def get_all(self) -> List[Hall]:
        return list(self._halls.values())

    def add(self, entity: Hall) -> Hall:
        entity.id = self._next_id
        self._next_id += 1
        self._halls[entity.id] = entity
        return entity

    def update(self, entity_id: int, **kwargs) -> Optional[Hall]:
        hall = self._halls.get(entity_id)
        if hall:
            for key, value in kwargs.items():
                setattr(hall, key, value)
        return hall

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._halls:
            del self._halls[entity_id]
            return True
        return False