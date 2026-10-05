from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(Enum):
    """Роли пользователей системы."""
    CLIENT = "client"
    ADMIN = "admin"


class SeatStatus(Enum):
    """Статусы мест в зале."""
    FREE = "free"
    BOOKED = "booked"


@dataclass
class User:
    """Модель пользователя."""
    id: int
    email: str
    password: str
    role: UserRole = UserRole.CLIENT


@dataclass
class Movie:
    """Модель фильма."""
    id: int
    title: str
    description: str
    duration_min: int
    age_limit: int
    is_active: bool = True


@dataclass
class Hall:
    """Модель кинозала (шаблон геометрии)."""
    id: int
    name: str
    rows: int
    seats_per_row: int

    def get_seat_id(self, row: int, seat: int) -> str:
        """Генерирует уникальный ID места."""
        return f"{row}-{seat}"


@dataclass
class Screening:
    """Модель сеанса. Хранит собственную карту мест."""
    id: int
    movie_id: int
    hall_id: int
    start_time: datetime
    seat_map: dict[str, SeatStatus] = field(default_factory=dict)


@dataclass
class Booking:
    """Модель бронирования (билета)."""
    id: int
    user_id: int
    screening_id: int
    seats: list[str]
    qr_code: str
    created_at: datetime = field(default_factory=datetime.now)