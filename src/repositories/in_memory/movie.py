from typing import Optional, List
from src.models import Movie
from src.repositories.base import MovieRepository


class InMemoryMovieRepository(MovieRepository):
    """InMemory-реализация репозитория фильмов."""

    def __init__(self) -> None:
        self._movies: dict[int, Movie] = {}
        self._next_id: int = 1

    def get(self, entity_id: int) -> Optional[Movie]:
        return self._movies.get(entity_id)

    def get_all(self) -> List[Movie]:
        return list(self._movies.values())

    def add(self, entity: Movie) -> Movie:
        entity.id = self._next_id
        self._next_id += 1
        self._movies[entity.id] = entity
        return entity

    def update(self, entity_id: int, **kwargs) -> Optional[Movie]:
        movie = self._movies.get(entity_id)
        if movie:
            for key, value in kwargs.items():
                setattr(movie, key, value)
        return movie

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._movies:
            del self._movies[entity_id]
            return True
        return False

    def get_active_movies(self) -> List[Movie]:
        return [m for m in self._movies.values() if m.is_active]