from typing import Optional, List
from datetime import datetime
from src.models import Screening, SeatStatus
from src.repositories import ScreeningRepository, InMemoryScreeningRepository


class ScheduleService:
    """Сервис управления расписанием сеансов."""

    def __init__(
        self,
        catalog,  # CatalogService — чтобы избежать циклического импорта
        screening_repository: Optional[ScreeningRepository] = None
    ) -> None:
        self.catalog = catalog
        self.screening_repository = screening_repository or InMemoryScreeningRepository()

    def create_screening(self, movie_id: int, hall_id: int, start_time_str: str) -> Optional[Screening]:
        movie = self.catalog.get_movie(movie_id)
        hall = self.catalog.get_hall(hall_id)
        if not movie or not hall:
            return None
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        screening = Screening(id=None, movie_id=movie_id, hall_id=hall_id, start_time=start_time, seat_map={})
        # Инициализируем карту мест
        for row in range(1, hall.rows + 1):
            for seat in range(1, hall.seats_per_row + 1):
                seat_id = hall.get_seat_id(row, seat)
                screening.seat_map[seat_id] = SeatStatus.FREE
        return self.screening_repository.add(screening)

    def get_screenings(self) -> List[Screening]:
        return self.screening_repository.get_all()

    def get_screening(self, screening_id: int) -> Optional[Screening]:
        return self.screening_repository.get(screening_id)

    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        return self.screening_repository.get_screenings_by_movie(movie_id)