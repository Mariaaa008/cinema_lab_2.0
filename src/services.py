import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List

from src.models import User, Movie, Hall, Screening, Booking, UserRole, SeatStatus
from src.repositories import (
    MovieRepository, HallRepository, ScreeningRepository,
    UserRepository, BookingRepository,
    InMemoryMovieRepository, InMemoryHallRepository,
    InMemoryScreeningRepository, InMemoryUserRepository,
    InMemoryBookingRepository
)


class AuthService:
    """Сервис аутентификации и управления пользователями."""

    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        self.user_repository = user_repository or InMemoryUserRepository()
        # Создаем администратора по умолчанию
        try:
            self.register("admin@cinema.ru", "admin", UserRole.ADMIN)
        except ValueError:
            pass  # Админ уже существует

    def register(self, email: str, password: str, role: UserRole = UserRole.CLIENT) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")
        
        user = User(
            id=0,
            email=email,
            password=password,
            role=role
        )
        return self.user_repository.add(user)

    def login(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email)
        if user and user.password == password:
            return user
        return None
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get(user_id)


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
        movie = Movie(
            id=0,
            title=title,
            description=description,
            duration_min=duration_min,
            age_limit=age_limit
        )
        return self.movie_repository.add(movie)
    
    def get_movies(self) -> List[Movie]:
        return self.movie_repository.get_active_movies()
    
    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.movie_repository.get(movie_id)

    def add_hall(self, name: str, rows: int, seats_per_row: int) -> Hall:
        hall = Hall(
            id=0,
            name=name,
            rows=rows,
            seats_per_row=seats_per_row
        )
        return self.hall_repository.add(hall)
    
    def get_halls(self) -> List[Hall]:
        return self.hall_repository.get_all()
    
    def get_hall(self, hall_id: int) -> Optional[Hall]:
        return self.hall_repository.get(hall_id)


class ScheduleService:
    """Сервис управления расписанием сеансов."""

    def __init__(
        self,
        catalog: CatalogService,
        screening_repository: Optional[ScreeningRepository] = None
    ) -> None:
        self.catalog = catalog
        self.screening_repository = screening_repository or InMemoryScreeningRepository()

    def create_screening(self, movie_id: int, hall_id: int, start_time_str: str) -> Optional[Screening]:
        from datetime import datetime
        
        movie = self.catalog.get_movie(movie_id)
        hall = self.catalog.get_hall(hall_id)
        
        if not movie or not hall:
            return None
        
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        
        screening = Screening(
            id=0,
            movie_id=movie_id,
            hall_id=hall_id,
            start_time=start_time,
            seat_map={}
        )
        
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


class NotificationService:
    """Сервис отправки уведомлений (Email) через smtplib."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None
    ) -> None:
        # Исправление: Используем переменные окружения вместо хардкода
        self._smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self._smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self._sender_email = sender_email or os.getenv("SENDER_EMAIL", "your_app@gmail.com")
        self._sender_password = sender_password or os.getenv("SENDER_PASSWORD", "app_password")

    def send_booking_confirmation(
        self,
        recipient_email: str,
        screening_info: str,
        seats: List[str],
        qr_code: str
    ) -> bool:
        subject = "Подтверждение бронирования"
        body = f"""
        Ваше бронирование подтверждено!
        
        Сеанс: {screening_info}
        Места: {', '.join(seats)}
        
        QR-код: {qr_code[:50]}...
        
        Спасибо за бронирование!
        """
        
        return self._send_email(recipient_email, subject, body)
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self._sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
                server.starttls()
                server.login(self._sender_email, self._sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Ошибка при отправке email: {e}")
            return False


class BookingService:
    """Сервис бронирования билетов."""

    def __init__(
        self,
        schedule: ScheduleService,
        catalog: CatalogService,
        auth: 'AuthService',
        booking_repository: Optional[BookingRepository] = None
    ) -> None:
        self.schedule = schedule
        self.catalog = catalog
        self.auth = auth
        self.booking_repository = booking_repository or InMemoryBookingRepository()

    def book_seats(
        self,
        user_id: int,
        screening_id: int,
        seat_ids: List[str],
        auth_service: 'AuthService'
    ) -> Booking:
        screening = self.schedule.get_screening(screening_id)
        if not screening:
            raise ValueError("Сеанс не найден")
        
        user = auth_service.get_user(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        # Проверяем доступность мест
        for seat_id in seat_ids:
            if seat_id not in screening.seat_map:
                raise ValueError(f"Место {seat_id} не существует")
            
            if screening.seat_map[seat_id] != SeatStatus.FREE:
                raise ValueError(f"Место {seat_id} уже забронировано")
        
        # Бронируем места
        for seat_id in seat_ids:
            screening.seat_map[seat_id] = SeatStatus.BOOKED
        
        # Генерируем QR-код
        qr_code = self._generate_qr_code(user_id, screening_id, seat_ids)
        
        # Создаем бронирование
        booking = Booking(
            id=0,
            user_id=user_id,
            screening_id=screening_id,
            seats=seat_ids,
            qr_code=qr_code
        )
        
        return self.booking_repository.add(booking)
    
    def get_user_bookings(self, user_id: int) -> List[Booking]:
        return self.booking_repository.get_by_user(user_id)
    
    def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        booking = self.booking_repository.get(booking_id)
        
        if not booking:
            raise ValueError("Бронирование не найдено")
        
        if booking.user_id != user_id:
            raise ValueError("Только владелец может отменить бронирование")
        
        # Освобождаем места
        screening = self.schedule.get_screening(booking.screening_id)
        if screening:
            for seat_id in booking.seats:
                screening.seat_map[seat_id] = SeatStatus.FREE
        
        return self.booking_repository.delete(booking_id)
    
    def _generate_qr_code(self, user_id: int, screening_id: int, seats: List[str]) -> str:
        import qrcode
        import io
        import base64
        
        data = f"USER:{user_id}|SCREENING:{screening_id}|SEATS:{','.join(seats)}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        
        return base64.b64encode(buffered.getvalue()).decode()[:50]
