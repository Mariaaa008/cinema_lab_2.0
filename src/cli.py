import os
from enum import IntEnum

from src.models import User, UserRole, SeatStatus
from src.services import (
    AuthService, CatalogService, ScheduleService,
    BookingService, NotificationService
)


class AuthMenuChoice(IntEnum):
    """Варианты выбора в меню авторизации."""
    LOGIN = 1
    REGISTER = 2
    EXIT = 0


class ClientMenuChoice(IntEnum):
    """Варианты выбора в клиентском меню."""
    SHOW_MOVIES_AND_BOOK = 1
    SHOW_TICKETS = 2
    LOGOUT = 3


class AdminMenuChoice(IntEnum):
    """Варианты выбора в меню администратора."""
    ADD_MOVIE = 1
    ADD_HALL = 2
    CREATE_SCREENING = 3
    LOGOUT = 4


class CinemaCLI:
    """Главный класс CLI приложения."""

    def __init__(self) -> None:
        self.catalog = CatalogService()
        self.schedule = ScheduleService(self.catalog)
        
        self.notifier = NotificationService(
            smtp_host=os.getenv("SMTP_HOST"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            sender_email=os.getenv("SENDER_EMAIL"),
            sender_password=os.getenv("SENDER_PASSWORD")
        )
        
        self.auth = AuthService()
        self.booking = BookingService(
            schedule=self.schedule,
            catalog=self.catalog,
            auth=self.auth
        )
        
        self.current_user: User | None = None

    def run(self) -> None:
        print("  Cinema Booking System (Lab 3)")
        
        while True:
            if not self.current_user:
                self._handle_authentication()
            elif self.current_user.role == UserRole.ADMIN:
                self._handle_admin()
            else:
                self._handle_client()

    def _handle_authentication(self) -> None:
        print("\n1. Войти | 2. Регистрация | 0. Выход")
        choice_str = input("Выбор: ").strip()

        try:
            choice = AuthMenuChoice(int(choice_str))
        except ValueError:
            print("Неизвестная команда")
            return

        if choice == AuthMenuChoice.LOGIN:
            email = input("Email: ")
            password = input("Пароль: ")
            user = self.auth.login(email, password)
            if user:
                self.current_user = user
                print(f"Вы вошли как {user.email}")
            else:
                print("Неверный логин или пароль")
        elif choice == AuthMenuChoice.REGISTER:
            email = input("Email: ")
            password = input("Пароль: ")
            self.auth.register(email, password)
            print("Регистрация успешна!")
        elif choice == AuthMenuChoice.EXIT:
            exit(0)

    def _handle_client(self) -> None:
        print(f"\n--- Клиент ({self.current_user.email}) ---")
        print("1. Афиша и бронь | 2. Мои билеты | 3. Выйти")
        choice_str = input("Выбор: ").strip()

        try:
            choice = ClientMenuChoice(int(choice_str))
        except ValueError:
            print("Неизвестная команда")
            return

        if choice == ClientMenuChoice.SHOW_MOVIES_AND_BOOK:
            self._display_movies_and_book()
        elif choice == ClientMenuChoice.SHOW_TICKETS:
            self._display_and_cancel_tickets()
        elif choice == ClientMenuChoice.LOGOUT:
            self.current_user = None

    def _handle_admin(self) -> None:
        print("\n--- Администратор ---")
        print("1. Добавить фильм | 2. Добавить зал | 3. Создать сеанс | 4. Выйти")
        choice_str = input("Выбор: ").strip()

        try:
            choice = AdminMenuChoice(int(choice_str))
        except ValueError:
            print("Неизвестная команда")
            return

        if choice == AdminMenuChoice.ADD_MOVIE:
            title = input("Название: ")
            description = input("Описание: ")
            duration_minutes = int(input("Длительность (мин): "))
            age_limit = int(input("Возраст: "))
            self.catalog.add_movie(title, description, duration_minutes, age_limit)
            print("Фильм добавлен.")
        elif choice == AdminMenuChoice.ADD_HALL:
            name = input("Название зала: ")
            rows = int(input("Рядов: "))
            seats_per_row = int(input("Мест в ряду: "))
            self.catalog.add_hall(name, rows, seats_per_row)
            print("Зал добавлен.")
        elif choice == AdminMenuChoice.CREATE_SCREENING:
            movie_id = int(input("ID фильма: "))
            hall_id = int(input("ID зала: "))
            start_time = input("Время (YYYY-MM-DD HH:MM): ")
            if self.schedule.create_screening(movie_id, hall_id, start_time):
                print("Сеанс создан.")
        elif choice == AdminMenuChoice.LOGOUT:
            self.current_user = None

    def _display_movies_and_book(self) -> None:
        movies = self.catalog.get_movies()
        if not movies:
            print("Нет активных фильмов.")
            return

        print("\nАфиша:")
        
        for movie in movies:
            print(f"[{movie.id}] {movie.title} ({movie.duration_min} мин, {movie.age_limit}+)")

        movie_id = int(input("ID фильма: "))
        screenings = self.schedule.get_screenings_by_movie(movie_id)
        if not screenings:
            print("Нет сеансов.")
            return

        print("\nСеансы:")
        for screening in screenings:
            hall = self.catalog.get_hall(screening.hall_id)
            if hall:
                print(f"[{screening.id}] {screening.start_time.strftime('%Y-%m-%d %H:%M')} | Зал: {hall.name}")

        screening_id = int(input("ID сеанса: "))
        current_screening = self.schedule.get_screening(screening_id)
        if not current_screening:
            return

        hall = self.catalog.get_hall(current_screening.hall_id)
        if not hall:
            return
        
        print(f"\nСхема зала '{hall.name}':")
        for row_number in range(1, hall.rows + 1):
            row_string = f"Ряд {row_number}: "
            for seat_number in range(1, hall.seats_per_row + 1):
                seat_id = hall.get_seat_id(row_number, seat_number)
                status = current_screening.seat_map.get(seat_id)
                row_string += "[X] " if status == SeatStatus.BOOKED else "[.] "
            print(row_string)

        seats_input = input("Места (через запятую, напр. 1-1,1-2): ")
        seat_list = [seat.strip() for seat in seats_input.split(",")]
        
        self.booking.book_seats(
            user_id=self.current_user.id,
            screening_id=screening_id,
            seat_ids=seat_list,
            auth_service=self.auth
        )
        print("Бронирование успешно!")

    def _display_and_cancel_tickets(self) -> None:
        bookings = self.booking.get_user_bookings(self.current_user.id)
        if not bookings:
            print("Нет билетов.")
            return

        print("\nВаши билеты:")
        for booking in bookings:
            screening = self.schedule.get_screening(booking.screening_id)
            if screening:
                movie = self.catalog.get_movie(screening.movie_id)
                print(f"#{booking.id}: {movie.title if movie else '?'} | Места: {', '.join(booking.seats)} | QR: {booking.qr_code}")
        
        cancel_id = input("ID для отмены (Enter - пропуск): ")
        if cancel_id:
            self.booking.cancel_booking(int(cancel_id), self.current_user.id)
            print("Бронирование отменено.")
