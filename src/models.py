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
    """Модель места в кинотеатре (заготовка для будущего рефакторинга)."""
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
    id: int | None
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
    """Отдельный класс для хранения карты мест (заготовка для будущего рефакторинга)."""
    screening_id: int | None
    hall_id: int | None
    seat_statuses: dict[str, SeatStatus] = field(default_factory=dict)

@dataclass
class Screening:
    """Модель сеанса. Хранит карту мест как словарь для совместимости с текущими сервисами."""
    id: int | None
    movie_id: int
    hall_id: int
    start_time: datetime
    # Словарь { "1-1": SeatStatus.FREE, ... } — именно этот формат ожидают текущие сервисы
    seat_map: dict[str, SeatStatus] = field(default_factory=dict)

@dataclass
class Booking:
    """Модель бронирования (билета). Синхронизирована с текущим BookingService."""
    id: int | None
    
    # user_id используется в текущем BookingService (cancel_booking, book_seats)
    user_id: int 
    
    screening_id: int
    
    # list[str] — список ID мест в формате "1-1", "2-3". 
    # Именно этот тип передаётся из CLI и обрабатывается в сервисах
    seats: list[str] 
    
    qr_code: str
    created_at: datetime = field(default_factory=datetime.now)
