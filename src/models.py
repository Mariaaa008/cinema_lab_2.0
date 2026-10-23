from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    """Роли пользователей системы."""
    CLIENT = "client"
    ADMIN = "admin"


class SeatStatus(Enum):
    """Статусы мест в зале."""
    FREE = "free"
    BOOKED = "booked"


@dataclass
class Seat:
    """Модель места в кинотеатре."""
    row: int
    number: int
    status: SeatStatus = SeatStatus.FREE

    @property
    def seat_id(self) -> str:
        """Генерирует уникальный ID места (например, '1-5')."""
        return f"{self.row}-{self.number}"


@dataclass
class User:
    """Модель пользователя."""
    id: int | None  # Используем современный синтаксис вместо Optional
    email: str
    password: str
    role: UserRole = UserRole.CLIENT


@dataclass
class Movie:
    """Модель фильма."""
    id: int | None
    title: str
    description: str
    duration_min: int
    age_limit: int
    is_active: bool = True


@dataclass
class Hall:
    """Модель кинозала (шаблон геометрии)."""
    id: int | None
    name: str
    rows: int
    seats_per_row: int

    def get_seat_id(self, row: int, seat: int) -> str:
        """Генерирует уникальный ID места по координатам."""
        return f"{row}-{seat}"


@dataclass
class ScreeningSeatMap:
    """Отдельный класс для хранения карты мест конкретного сеанса."""
    screening_id: int | None
    hall_id: int | None
    # Хранит статусы мест в формате { "1-1": SeatStatus.FREE, ... }
    seat_statuses: dict[str, SeatStatus] = field(default_factory=dict)


@dataclass
class Screening:
    """Модель сеанса."""
    id: int | None
    movie_id: int
    hall_id: int
    start_time: datetime
    # Теперь сеанс ссылается на отдельный класс карты мест, а не хранит словарь внутри себя
    seat_map: ScreeningSeatMap | None = None


@dataclass
class Booking:
    """Модель бронирования (билета)."""
    id: int | None
    
    created_by: int 
    
    screening_id: int
    
    seats: list[Seat] 
    
    qr_code: str
    created_at: datetime = field(default_factory=datetime.now)
