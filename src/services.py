import random
import string
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional

from .models import User, Movie, Hall, Screening, Booking, UserRole, SeatStatus


class AuthService:
    """Сервис аутентификации и управления пользователями."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id: int = 1
        # Создаем администратора по умолчанию
        self.register("admin@cinema.ru", "admin", UserRole.ADMIN)

    def register(self, email: str, password: str, role: UserRole = UserRole.CLIENT) -> User:
        """Регистрирует нового пользователя."""
        user = User(id=self._next_id, email=email, password=password, role=role)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def login(self, email: str, password: str) -> Optional[User]:
        """Проверяет учетные данные. Возвращает User или None."""
        for user in self._users.values():
            if user.email == email and user.password == password:
                return user
        return None

    def get_user(self, user_id: int) -> Optional[User]:
        """Получает пользователя по ID."""
        return self._users.get(user_id)

    def check_admin(self, user: Optional[User]) -> bool:
        """Проверяет права администратора."""
        return user is not None and user.role == UserRole.ADMIN


class CatalogService:
    """Сервис управления фильмами и залами."""

    def __init__(self) -> None:
        self._movies: dict[int, Movie] = {}
        self._halls: dict[int, Hall] = {}
        self._movie_next_id: int = 1
        self._hall_next_id: int = 1

    def add_movie(self, title: str, desc: str, duration: int, age: int) -> Movie:
        """Добавляет фильм в каталог."""
        movie = Movie(
            id=self._movie_next_id, title=title, description=desc,
            duration_min=duration, age_limit=age
        )
        self._movies[self._movie_next_id] = movie
        self._movie_next_id += 1
        return movie

    def get_movies(self, active_only: bool = True) -> list[Movie]:
        """Возвращает список фильмов."""
        if active_only:
            return [m for m in self._movies.values() if m.is_active]
        return list(self._movies.values())

    def add_hall(self, name: str, rows: int, seats: int) -> Hall:
        """Добавляет зал."""
        hall = Hall(id=self._hall_next_id, name=name, rows=rows, seats_per_row=seats)
        self._halls[self._hall_next_id] = hall
        self._hall_next_id += 1
        return hall

    def get_halls(self) -> list[Hall]:
        """Возвращает список залов."""
        return list(self._halls.values())


class ScheduleService:
    """Сервис управления расписанием сеансов."""

    def __init__(self, catalog: CatalogService) -> None:
        self._catalog = catalog
        self._screenings: dict[int, Screening] = {}
        self._next_id: int = 1

    def create_screening(self, movie_id: int, hall_id: int, time_str: str) -> Optional[Screening]:
        """Создает новый сеанс."""
        try:
            start_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("[Ошибка] Неверный формат времени. Используйте YYYY-MM-DD HH:MM")
            return None

        if movie_id not in self._catalog._movies or hall_id not in self._catalog._halls:
            print("[Ошибка] Фильм или зал не найдены.")
            return None

        screening = Screening(
            id=self._next_id, movie_id=movie_id, 
            hall_id=hall_id, start_time=start_time
        )
        
        # Инициализация карты мест для этого конкретного сеанса
        hall = self._catalog._halls[hall_id]
        for r in range(1, hall.rows + 1):
            for s in range(1, hall.seats_per_row + 1):
                screening.seat_map[hall.get_seat_id(r, s)] = SeatStatus.FREE

        self._screenings[self._next_id] = screening
        self._next_id += 1
        return screening

    def get_screenings(self) -> list[Screening]:
        """Возвращает все сеансы."""
        return list(self._screenings.values())

    def get_screening(self, screening_id: int) -> Optional[Screening]:
        """Получает конкретный сеанс."""
        return self._screenings.get(screening_id)


class NotificationService:
    """Сервис отправки уведомлений (Email) через smtplib."""

    def __init__(
        self, smtp_host: str, smtp_port: int, 
        sender_email: str, sender_password: str
    ) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._sender_email = sender_email
        self._sender_password = sender_password

    def send_ticket_email(
        self, recipient_email: str, movie_title: str,
        screening_time: str, hall_name: str, seats: list[str], qr_code: str
    ) -> bool:
        """Отправляет электронный билет на почту."""
        subject = f"Ваш билет на '{movie_title}'"
        body = (
            f"Здравствуйте!\n\n"
            f"Фильм: {movie_title}\n"
            f"Сеанс: {screening_time}\n"
            f"Зал: {hall_name}\n"
            f"Места: {', '.join(seats)}\n\n"
            f"QR-код: {qr_code}\n"
            f"Покажите этот код на входе."
        )

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self._sender_email
        msg["To"] = recipient_email

        try:
            with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
                server.starttls()
                server.login(self._sender_email, self._sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"[Ошибка Email] {e}")
            return False


class BookingService:
    """Сервис бронирования билетов."""

    def __init__(
        self, schedule: ScheduleService, catalog: CatalogService,
        notifier: Optional[NotificationService] = None
    ) -> None:
        self._schedule = schedule
        self._catalog = catalog
        self._notifier = notifier
        self._bookings: dict[int, Booking] = {}
        self._next_id: int = 1

    def book_seats(
        self, user_id: int, screening_id: int, 
        seat_ids: list[str], auth_service: AuthService
    ) -> Optional[Booking]:
        """Бронирует места и отправляет уведомление."""
        screening = self._schedule.get_screening(screening_id)
        if not screening:
            print("[Ошибка] Сеанс не найден.")
            return None

        # Проверка доступности мест
        for seat_id in seat_ids:
            if seat_id not in screening.seat_map:
                print(f"[Ошибка] Место {seat_id} не существует.")
                return None
            if screening.seat_map[seat_id] != SeatStatus.FREE:
                print(f"[Ошибка] Место {seat_id} уже занято.")
                return None

        # Фиксация брони
        for seat_id in seat_ids:
            screening.seat_map[seat_id] = SeatStatus.BOOKED

        qr = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        booking = Booking(
            id=self._next_id, user_id=user_id,
            screening_id=screening_id, seats=seat_ids, qr_code=qr
        )
        self._bookings[self._next_id] = booking
        self._next_id += 1
        
        print(f"\n[Успех] Билет забронирован! QR-код: {qr}")

        # Отправка уведомления
        if self._notifier:
            user = auth_service.get_user(user_id)
            if user:
                movie = self._catalog._movies.get(screening.movie_id)
                hall = self._catalog._halls.get(screening.hall_id)
                
                success = self._notifier.send_ticket_email(
                    recipient_email=user.email,
                    movie_title=movie.title if movie else "Unknown",
                    screening_time=screening.start_time.strftime("%Y-%m-%d %H:%M"),
                    hall_name=hall.name if hall else "Unknown",
                    seats=seat_ids,
                    qr_code=qr,
                )
                if success:
                    print(f"[Email] Билет отправлен на {user.email}")
                else:
                    print("[Email] Ошибка отправки, но бронь сохранена.")

        return booking

    def get_user_bookings(self, user_id: int) -> list[Booking]:
        """Возвращает историю бронирований пользователя."""
        return [b for b in self._bookings.values() if b.user_id == user_id]

    def cancel_booking(self, booking_id: int, user_id: int) -> bool:
        """Отменяет бронь и освобождает места."""
        booking = self._bookings.get(booking_id)
        if not booking or booking.user_id != user_id:
            print("[Ошибка] Бронь не найдена или нет прав.")
            return False

        screening = self._schedule.get_screening(booking.screening_id)
        if screening:
            for seat_id in booking.seats:
                screening.seat_map[seat_id] = SeatStatus.FREE
        
        del self._bookings[booking_id]
        print("[Успех] Бронь отменена, места освобождены.")
        return True