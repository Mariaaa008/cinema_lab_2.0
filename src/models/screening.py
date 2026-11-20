# src/models/screening.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SeatStatus(Enum):
    """Статусы мест в зале."""
    FREE = "free"
    BOOKED = "booked"


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