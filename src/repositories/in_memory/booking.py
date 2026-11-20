from typing import Optional, List
from src.models import Booking
from src.repositories.base import BookingRepository


class InMemoryBookingRepository(BookingRepository):
    """InMemory-реализация репозитория бронирований."""

    def __init__(self) -> None:
        self._bookings: dict[int, Booking] = {}
        self._next_id: int = 1

    def get(self, entity_id: int) -> Optional[Booking]:
        return self._bookings.get(entity_id)

    def get_all(self) -> List[Booking]:
        return list(self._bookings.values())

    def add(self, entity: Booking) -> Booking:
        entity.id = self._next_id
        self._next_id += 1
        self._bookings[entity.id] = entity
        return entity

    def update(self, entity_id: int, **kwargs) -> Optional[Booking]:
        booking = self._bookings.get(entity_id)
        if booking:
            for key, value in kwargs.items():
                setattr(booking, key, value)
        return booking

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._bookings:
            del self._bookings[entity_id]
            return True
        return False

    def get_by_user(self, user_id: int) -> List[Booking]:
        return [b for b in self._bookings.values() if b.user_id == user_id]