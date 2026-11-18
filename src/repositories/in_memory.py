from typing import Optional, List, Dict, Any

from src.models import Movie, Hall, Screening, User, Booking, UserRole, SeatStatus
from src.repositories.base import (
    BaseRepository, MovieRepository, HallRepository,
    ScreeningRepository, UserRepository, BookingRepository
)


class InMemoryMovieRepository(MovieRepository):
    """InMemory репозиторий для фильмов."""
    
    def __init__(self) -> None:
        self._storage: Dict[int, Movie] = {}
        self._counter: int = 0
    
    def get(self, entity_id: int) -> Optional[Movie]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[Movie]:
        return list(self._storage.values())
    
    def add(self, entity: Movie) -> Movie:
        self._counter += 1
        if entity.id is None:
            entity.id = self._counter
        self._storage[entity.id] = entity
        return entity
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[Movie]:
        entity = self._storage.get(entity_id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._storage[entity_id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def get_active_movies(self) -> List[Movie]:
        return [m for m in self._storage.values() if m.is_active]


class InMemoryHallRepository(HallRepository):
    """InMemory репозиторий для залов."""
    
    def __init__(self) -> None:
        self._storage: Dict[int, Hall] = {}
        self._counter: int = 0
    
    def get(self, entity_id: int) -> Optional[Hall]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[Hall]:
        return list(self._storage.values())
    
    def add(self, entity: Hall) -> Hall:
        self._counter += 1
        if entity.id is None:
            entity.id = self._counter
        self._storage[entity.id] = entity
        return entity
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[Hall]:
        entity = self._storage.get(entity_id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._storage[entity_id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False


class InMemoryScreeningRepository(ScreeningRepository):
    """InMemory репозиторий для сеансов."""
    
    def __init__(self) -> None:
        self._storage: Dict[int, Screening] = {}
        self._counter: int = 0
    
    def get(self, entity_id: int) -> Optional[Screening]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[Screening]:
        return list(self._storage.values())
    
    def add(self, entity: Screening) -> Screening:
        self._counter += 1
        if entity.id is None:
            entity.id = self._counter
        self._storage[entity.id] = entity
        return entity
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[Screening]:
        entity = self._storage.get(entity_id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._storage[entity_id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        return [s for s in self._storage.values() if s.movie_id == movie_id]


class InMemoryUserRepository(UserRepository):
    """InMemory репозиторий для пользователей."""
    
    def __init__(self) -> None:
        self._storage: Dict[int, User] = {}
        self._counter: int = 0
    
    def get(self, entity_id: int) -> Optional[User]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[User]:
        return list(self._storage.values())
    
    def add(self, entity: User) -> User:
        self._counter += 1
        if entity.id is None:
            entity.id = self._counter
        self._storage[entity.id] = entity
        return entity
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[User]:
        entity = self._storage.get(entity_id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._storage[entity_id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._storage.values():
            if user.email == email:
                return user
        return None


class InMemoryBookingRepository(BookingRepository):
    """InMemory репозиторий для бронирований."""
    
    def __init__(self) -> None:
        self._storage: Dict[int, Booking] = {}
        self._counter: int = 0
    
    def get(self, entity_id: int) -> Optional[Booking]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[Booking]:
        return list(self._storage.values())
    
    def add(self, entity: Booking) -> Booking:
        self._counter += 1
        if entity.id is None:
            entity.id = self._counter
        self._storage[entity.id] = entity
        return entity
    
    def update(self, entity_id: int, **kwargs: Any) -> Optional[Booking]:
        entity = self._storage.get(entity_id)
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            self._storage[entity_id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def get_by_user(self, user_id: int) -> List[Booking]:
        return [b for b in self._storage.values() if b.user_id == user_id]