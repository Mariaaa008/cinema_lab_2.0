from typing import Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.repositories.base import (
    MovieRepository, HallRepository, ScreeningRepository,
    UserRepository, BookingRepository
)
from db.models import User, Movie, Hall, Screening, Booking


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[User]:
        return self.session.get(User, entity_id)

    def get_all(self) -> List[User]:
        return list(self.session.scalars(select(User)).all())

    def add(self, entity: User) -> User:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> Optional[User]:
        user = self.session.get(User, entity_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete(self, entity_id: int) -> bool:
        user = self.session.get(User, entity_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.scalar(
            select(User).where(User.email == email)
        )


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Movie]:
        return self.session.get(Movie, entity_id)

    def get_all(self) -> List[Movie]:
        return list(self.session.scalars(select(Movie)).all())

    def add(self, entity: Movie) -> Movie:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> Optional[Movie]:
        movie = self.session.get(Movie, entity_id)
        if movie:
            for key, value in kwargs.items():
                setattr(movie, key, value)
            self.session.commit()
            self.session.refresh(movie)
        return movie

    def delete(self, entity_id: int) -> bool:
        movie = self.session.get(Movie, entity_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()
            return True
        return False

    def get_active_movies(self) -> List[Movie]:
        return list(
            self.session.scalars(
                select(Movie).where(Movie.is_active == True)
            ).all()
        )


class SQLAlchemyHallRepository(HallRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Hall]:
        return self.session.get(Hall, entity_id)

    def get_all(self) -> List[Hall]:
        return list(self.session.scalars(select(Hall)).all())

    def add(self, entity: Hall) -> Hall:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> Optional[Hall]:
        hall = self.session.get(Hall, entity_id)
        if hall:
            for key, value in kwargs.items():
                setattr(hall, key, value)
            self.session.commit()
            self.session.refresh(hall)
        return hall

    def delete(self, entity_id: int) -> bool:
        hall = self.session.get(Hall, entity_id)
        if hall:
            self.session.delete(hall)
            self.session.commit()
            return True
        return False


class SQLAlchemyScreeningRepository(ScreeningRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Screening]:
        return self.session.get(Screening, entity_id)

    def get_all(self) -> List[Screening]:
        return list(self.session.scalars(select(Screening)).all())

    def add(self, entity: Screening) -> Screening:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> Optional[Screening]:
        screening = self.session.get(Screening, entity_id)
        if screening:
            for key, value in kwargs.items():
                setattr(screening, key, value)
            self.session.commit()
            self.session.refresh(screening)
        return screening

    def delete(self, entity_id: int) -> bool:
        screening = self.session.get(Screening, entity_id)
        if screening:
            self.session.delete(screening)
            self.session.commit()
            return True
        return False

    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        return list(
            self.session.scalars(
                select(Screening).where(Screening.movie_id == movie_id)
            ).all()
        )


class SQLAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Booking]:
        return self.session.get(Booking, entity_id)

    def get_all(self) -> List[Booking]:
        return list(self.session.scalars(select(Booking)).all())

    def add(self, entity: Booking) -> Booking:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity_id: int, **kwargs: Any) -> Optional[Booking]:
        booking = self.session.get(Booking, entity_id)
        if booking:
            for key, value in kwargs.items():
                setattr(booking, key, value)
            self.session.commit()
            self.session.refresh(booking)
        return booking

    def delete(self, entity_id: int) -> bool:
        booking = self.session.get(Booking, entity_id)
        if booking:
            self.session.delete(booking)
            self.session.commit()
            return True
        return False

    def get_by_user(self, user_id: int) -> List[Booking]:
        return list(
            self.session.scalars(
                select(Booking).where(Booking.user_id == user_id)
            ).all()
        )