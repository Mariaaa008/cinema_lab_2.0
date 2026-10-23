from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Абстрактный базовый репозиторий."""
    
    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        """Получить сущность по ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Получить все сущности."""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Добавить сущность."""
        pass
    
    @abstractmethod
    def update(self, entity_id: int, **kwargs: Any) -> Optional[T]:
        """Обновить сущность."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Удалить сущность."""
        pass


class MovieRepository(BaseRepository, ABC):
    """Абстрактный репозиторий для фильмов."""
    
    @abstractmethod
    def get_active_movies(self) -> List[Any]:
        """Получить активные фильмы."""
        pass


class HallRepository(BaseRepository, ABC):
    """Абстрактный репозиторий для залов."""
    pass


class ScreeningRepository(BaseRepository, ABC):
    """Абстрактный репозиторий для сеансов."""
    
    @abstractmethod
    def get_screenings_by_movie(self, movie_id: int) -> List[Any]:
        """Получить все сеансы фильма."""
        pass


class UserRepository(BaseRepository, ABC):
    """Абстрактный репозиторий для пользователей."""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]:
        """Найти пользователя по email."""
        pass


class BookingRepository(BaseRepository, ABC):
    """Абстрактный репозиторий для бронирований."""
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Any]:
        """Получить бронирования пользователя."""
        pass