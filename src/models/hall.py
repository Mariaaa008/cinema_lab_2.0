# src/models/hall.py
from dataclasses import dataclass
from enum import Enum


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
class Hall:
    """Модель кинозала (шаблон геометрии)."""
    id: int | None
    name: str
    rows: int
    seats_per_row: int

    def get_seat_id(self, row: int, seat: int) -> str:
        """Генерирует уникальный ID места по координатам."""
        return f"{row}-{seat}"