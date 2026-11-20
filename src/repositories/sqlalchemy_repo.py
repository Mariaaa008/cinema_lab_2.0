# src/repositories/sqlalchemy_repo.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.repositories.base import (
    UserRepository, MovieRepository, HallRepository,
    ScreeningRepository, BookingRepository
)
from src.models import User, Movie, Hall, Screening, Booking
from src.mappers import (
    UserMapper, MovieMapper, HallMapper,
    ScreeningMapper, BookingMapper
)
from db.models import (
    User as DBUser, Movie as DBMovie, Hall as DBHall,
    Screening as DBScreening, Booking as DBBooking
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[User]:
        db_user = self.session.get(DBUser, entity_id)
        return UserMapper.to_domain(db_user) if db_user else None

    def get_all(self) -> List[User]:
        db_users = self.session.scalars(select(DBUser)).all()
        return [UserMapper.to_domain(u) for u in db_users]

    def add(self, entity: User) -> User:
        db_user = UserMapper.to_db(entity)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserMapper.to_domain(db_user)

    def update(self, entity_id: int, **kwargs) -> Optional[User]:
        user = self.get(entity_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        db_user = UserMapper.to_db(user)
        self.session.merge(db_user)
        self.session.commit()
        return user

    def delete(self, entity_id: int) -> bool:
        db_user = self.session.get(DBUser, entity_id)
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.session.scalar(select(DBUser).where(DBUser.email == email))
        return UserMapper.to_domain(db_user) if db_user else None


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Movie]:
        db_movie = self.session.get(DBMovie, entity_id)
        return MovieMapper.to_domain(db_movie) if db_movie else None

    def get_all(self) -> List[Movie]:
        db_movies = self.session.scalars(select(DBMovie)).all()
        return [MovieMapper.to_domain(m) for m in db_movies]

    def add(self, entity: Movie) -> Movie:
        db_movie = MovieMapper.to_db(entity)
        self.session.add(db_movie)
        self.session.commit()
        self.session.refresh(db_movie)
        return MovieMapper.to_domain(db_movie)

    def update(self, entity_id: int, **kwargs) -> Optional[Movie]:
        movie = self.get(entity_id)
        if not movie:
            return None
        for key, value in kwargs.items():
            setattr(movie, key, value)
        db_movie = MovieMapper.to_db(movie)
        self.session.merge(db_movie)
        self.session.commit()
        return movie

    def delete(self, entity_id: int) -> bool:
        db_movie = self.session.get(DBMovie, entity_id)
        if db_movie:
            self.session.delete(db_movie)
            self.session.commit()
            return True
        return False

    def get_active_movies(self) -> List[Movie]:
        db_movies = self.session.scalars(
            select(DBMovie).where(DBMovie.is_active == True)
        ).all()
        return [MovieMapper.to_domain(m) for m in db_movies]


class SQLAlchemyHallRepository(HallRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Hall]:
        db_hall = self.session.get(DBHall, entity_id)
        return HallMapper.to_domain(db_hall) if db_hall else None

    def get_all(self) -> List[Hall]:
        db_halls = self.session.scalars(select(DBHall)).all()
        return [HallMapper.to_domain(h) for h in db_halls]

    def add(self, entity: Hall) -> Hall:
        db_hall = HallMapper.to_db(entity)
        self.session.add(db_hall)
        self.session.commit()
        self.session.refresh(db_hall)
        return HallMapper.to_domain(db_hall)

    def update(self, entity_id: int, **kwargs) -> Optional[Hall]:
        hall = self.get(entity_id)
        if not hall:
            return None
        for key, value in kwargs.items():
            setattr(hall, key, value)
        db_hall = HallMapper.to_db(hall)
        self.session.merge(db_hall)
        self.session.commit()
        return hall

    def delete(self, entity_id: int) -> bool:
        db_hall = self.session.get(DBHall, entity_id)
        if db_hall:
            self.session.delete(db_hall)
            self.session.commit()
            return True
        return False


class SQLAlchemyScreeningRepository(ScreeningRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Screening]:
        db_screening = self.session.get(DBScreening, entity_id)
        return ScreeningMapper.to_domain(db_screening) if db_screening else None

    def get_all(self) -> List[Screening]:
        db_screenings = self.session.scalars(select(DBScreening)).all()
        return [ScreeningMapper.to_domain(s) for s in db_screenings]

    def add(self, entity: Screening) -> Screening:
        db_screening = ScreeningMapper.to_db(entity)
        self.session.add(db_screening)
        self.session.commit()
        self.session.refresh(db_screening)
        return ScreeningMapper.to_domain(db_screening)

    def update(self, entity_id: int, **kwargs) -> Optional[Screening]:
        screening = self.get(entity_id)
        if not screening:
            return None
        for key, value in kwargs.items():
            setattr(screening, key, value)
        db_screening = ScreeningMapper.to_db(screening)
        self.session.merge(db_screening)
        self.session.commit()
        return screening

    def delete(self, entity_id: int) -> bool:
        db_screening = self.session.get(DBScreening, entity_id)
        if db_screening:
            self.session.delete(db_screening)
            self.session.commit()
            return True
        return False

    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        db_screenings = self.session.scalars(
            select(DBScreening).where(DBScreening.movie_id == movie_id)
        ).all()
        return [ScreeningMapper.to_domain(s) for s in db_screenings]


class SQLAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entity_id: int) -> Optional[Booking]:
        db_booking = self.session.get(DBBooking, entity_id)
        return BookingMapper.to_domain(db_booking) if db_booking else None

    def get_all(self) -> List[Booking]:
        db_bookings = self.session.scalars(select(DBBooking)).all()
        return [BookingMapper.to_domain(b) for b in db_bookings]

    def add(self, entity: Booking) -> Booking:
        db_booking = BookingMapper.to_db(entity)
        self.session.add(db_booking)
        self.session.commit()
        self.session.refresh(db_booking)
        return BookingMapper.to_domain(db_booking)

    def update(self, entity_id: int, **kwargs) -> Optional[Booking]:
        booking = self.get(entity_id)
        if not booking:
            return None
        for key, value in kwargs.items():
            setattr(booking, key, value)
        db_booking = BookingMapper.to_db(booking)
        self.session.merge(db_booking)
        self.session.commit()
        return booking

    def delete(self, entity_id: int) -> bool:
        db_booking = self.session.get(DBBooking, entity_id)
        if db_booking:
            self.session.delete(db_booking)
            self.session.commit()
            return True
        return False

    def get_by_user(self, user_id: int) -> List[Booking]:
        db_bookings = self.session.scalars(
            select(DBBooking).where(DBBooking.user_id == user_id)
        ).all()
        return [BookingMapper.to_domain(b) for b in db_bookings]