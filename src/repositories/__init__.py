# src/repositories/__init__.py

# Абстракции
from src.repositories.base import (
    UserRepository, MovieRepository, HallRepository,
    ScreeningRepository, BookingRepository
)

# InMemory реализации 
from src.repositories.in_memory import (
    InMemoryUserRepository, InMemoryMovieRepository,
    InMemoryHallRepository, InMemoryScreeningRepository,
    InMemoryBookingRepository
)

# SQLAlchemy реализации
from src.repositories.sqlalchemy_repo import (
    SQLAlchemyUserRepository, SQLAlchemyMovieRepository,
    SQLAlchemyHallRepository, SQLAlchemyScreeningRepository,
    SQLAlchemyBookingRepository
)

__all__ = [
    "UserRepository", "InMemoryUserRepository", "SQLAlchemyUserRepository",
    "MovieRepository", "InMemoryMovieRepository", "SQLAlchemyMovieRepository",
    "HallRepository", "InMemoryHallRepository", "SQLAlchemyHallRepository",
    "ScreeningRepository", "InMemoryScreeningRepository", "SQLAlchemyScreeningRepository",
    "BookingRepository", "InMemoryBookingRepository", "SQLAlchemyBookingRepository"
]
