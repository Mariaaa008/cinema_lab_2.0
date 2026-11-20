from typing import Optional, List
from src.models import Movie, Hall
from src.repositories import MovieRepository, HallRepository, InMemoryMovieRepository, InMemoryHallRepository


class CatalogService:
    """Сервис управления фильмами и залами."""

    def __init__(
        self,
        movie_repository: Optional[MovieRepository] = None,
        hall_repository: Optional[HallRepository] = None
    ) -> None:
        self.movie_repository = movie_repository or InMemoryMovieRepository()
        self.hall_repository = hall_repository or InMemoryHallRepository()

    def add_movie(self, title: str, description: str, duration_min: int, age_limit: int) -> Movie:
        movie = Movie(id=None, title=title, description=description, duration_min=duration_min, age_limit=age_limit)
        return self.movie_repository.add(movie)

    def get_movies(self) -> List[Movie]:
        return self.movie_repository.get_active_movies()

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.movie_repository.get(movie_id)

    def add_hall(self, name: str, rows: int, seats_per_row: int) -> Hall:
        hall = Hall(id=None, name=name, rows=rows, seats_per_row=seats_per_row)
        return self.hall_repository.add(hall)

    def get_halls(self) -> List[Hall]:
        return self.hall_repository.get_all()

    def get_hall(self, hall_id: int) -> Optional[Hall]:
        return self.hall_repository.get(hall_id)