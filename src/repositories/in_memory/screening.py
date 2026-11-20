from typing import Optional, List
from src.models import Screening
from src.repositories.base import ScreeningRepository


class InMemoryScreeningRepository(ScreeningRepository):
    """InMemory-реализация репозитория сеансов."""

    def __init__(self) -> None:
        self._screenings: dict[int, Screening] = {}
        self._next_id: int = 1

    def get(self, entity_id: int) -> Optional[Screening]:
        return self._screenings.get(entity_id)

    def get_all(self) -> List[Screening]:
        return list(self._screenings.values())

    def add(self, entity: Screening) -> Screening:
        entity.id = self._next_id
        self._next_id += 1
        self._screenings[entity.id] = entity
        return entity

    def update(self, entity_id: int, **kwargs) -> Optional[Screening]:
        screening = self._screenings.get(entity_id)
        if screening:
            for key, value in kwargs.items():
                setattr(screening, key, value)
        return screening

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._screenings:
            del self._screenings[entity_id]
            return True
        return False

    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        return [s for s in self._screenings.values() if s.movie_id == movie_id]