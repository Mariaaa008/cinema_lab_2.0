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
    
    # FIXME: Вот эта переменная должна быть в другом месте
    # Ее можно сделать отдельным классом, который бы ссылался на Hall и Screening
    seat_map: dict[str, SeatStatus] = field(default_factory=dict)
    
    """
    Например:
    from dataclasses import dataclass, field

    @dataclass
    class SeatsOfScreeningStatus:
        id: int
        screening: Screening
        hall: Hall
        
        _seat_map: dict[str, SeatStatus] = field(init=False, repr=False)

        def __post_init__(self) -> None:
            # Инициализируем карту мест по умолчанию — все FREE
            self._seat_map = {
                self.hall.get_seat_id(r, s): SeatStatus.FREE
                for r in range(1, self.hall.rows + 1)
                for s in range(1, self.hall.seats_per_row + 1)
            }

        @property
        def seat_map(self) -> dict[str, SeatStatus]:
            return self._seat_map

        @seat_map.setter
        def seat_map(self, value: dict[str, SeatStatus]) -> None:
            # Можно добавить валидацию, например: ключи должны совпадать с местами зала
            expected_ids = {
                self.hall.get_seat_id(r, s)
                for r in range(1, self.hall.rows + 1)
                for s in range(1, self.hall.seats_per_row + 1)
            }
            if set(value.keys()) != expected_ids:
                raise ValueError("Ключи seat_map не соответствуют местам зала")
            self._seat_map = value
    """
    


@dataclass
class Booking:
    """Модель бронирования (билета)."""
    id: int
    user_id: int # FIXME: user_id -> created_by
    screening_id: int
    
    # FIXME: лучше не list[str], а set[int]. 
    # Или лучше вообще создать класс Seat
    seats: list[str] 
    
    """
    Например:
    
    @dataclass
    class Seat:
        screening: SeatsOfScreeningStatus
        
        row: int
        number: int
        
        status: SeatStatus = SeatStatus.FREE
        
        
    @dataclass
    class Booking:
        id: int
        created_by: int
        screening_id: int
        seats: list[Seat] 
    """
    
    qr_code: str
    created_at: datetime = field(default_factory=datetime.now)