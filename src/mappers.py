# src/mappers.py
"""Конвертеры между доменными моделями и SQLAlchemy-моделями."""

from src.models import User, Movie, Hall, Screening, Booking, UserRole, SeatStatus
from db.models import (
    User as DBUser, Movie as DBMovie, Hall as DBHall,
    Screening as DBScreening, Booking as DBBooking
)


class UserMapper:
    """Конвертер между User (domain) и DBUser (SQLAlchemy)."""

    @staticmethod
    def to_domain(db_user: DBUser) -> User:
        """SQLAlchemy-модель → доменная модель."""
        return User(
            id=db_user.id,
            email=db_user.email,
            password=db_user.password,
            role=UserRole(db_user.role)
        )

    @staticmethod
    def to_db(user: User) -> DBUser:
        """Доменная модель → SQLAlchemy-модель."""
        return DBUser(
            id=user.id,
            email=user.email,
            password=user.password,
            role=user.role.value  # Enum → строка
        )


class MovieMapper:
    @staticmethod
    def to_domain(db_movie: DBMovie) -> Movie:
        return Movie(
            id=db_movie.id,
            title=db_movie.title,
            description=db_movie.description,
            duration_min=db_movie.duration_min,
            age_limit=db_movie.age_limit,
            is_active=db_movie.is_active
        )

    @staticmethod
    def to_db(movie: Movie) -> DBMovie:
        return DBMovie(
            id=movie.id,
            title=movie.title,
            description=movie.description,
            duration_min=movie.duration_min,
            age_limit=movie.age_limit,
            is_active=movie.is_active
        )


class HallMapper:
    @staticmethod
    def to_domain(db_hall: DBHall) -> Hall:
        return Hall(
            id=db_hall.id,
            name=db_hall.name,
            rows=db_hall.rows,
            seats_per_row=db_hall.seats_per_row
        )

    @staticmethod
    def to_db(hall: Hall) -> DBHall:
        return DBHall(
            id=hall.id,
            name=hall.name,
            rows=hall.rows,
            seats_per_row=hall.seats_per_row
        )


class ScreeningMapper:
    @staticmethod
    def to_domain(db_screening: DBScreening) -> Screening:
        # Преобразуем seat_map: строковые значения → Enum SeatStatus
        seat_map = {
            seat_id: SeatStatus(status)
            for seat_id, status in (db_screening.seat_map or {}).items()
        }
        return Screening(
            id=db_screening.id,
            movie_id=db_screening.movie_id,
            hall_id=db_screening.hall_id,
            start_time=db_screening.start_time,
            seat_map=seat_map
        )

    @staticmethod
    def to_db(screening: Screening) -> DBScreening:
        # Преобразуем SeatStatus → строки для JSON
        seat_map = {
            seat_id: status.value
            for seat_id, status in screening.seat_map.items()
        }
        return DBScreening(
            id=screening.id,
            movie_id=screening.movie_id,
            hall_id=screening.hall_id,
            start_time=screening.start_time,
            seat_map=seat_map
        )


class BookingMapper:
    @staticmethod
    def to_domain(db_booking: DBBooking) -> Booking:
        return Booking(
            id=db_booking.id,
            user_id=db_booking.user_id,
            screening_id=db_booking.screening_id,
            seats=db_booking.seats,
            qr_code=db_booking.qr_code,
            created_at=db_booking.created_at
        )

    @staticmethod
    def to_db(booking: Booking) -> DBBooking:
        return DBBooking(
            id=booking.id,
            user_id=booking.user_id,
            screening_id=booking.screening_id,
            seats=booking.seats,
            qr_code=booking.qr_code,
            created_at=booking.created_at
        )