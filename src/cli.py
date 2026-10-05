from typing import Optional
from .models import User, UserRole, SeatStatus
from .services import (
    AuthService, CatalogService, ScheduleService, 
    BookingService, NotificationService
)


class CinemaCLI:
    """Главный класс CLI приложения."""

    def __init__(self) -> None:
        self.catalog = CatalogService()
        self.schedule = ScheduleService(self.catalog)
        
        # Настройки SMTP (замените на свои для реальной отправки)
        self.notifier = NotificationService(
            smtp_host="smtp.gmail.com", smtp_port=587,
            sender_email="your_app@gmail.com", sender_password="app_password"
        )
        
        self.booking = BookingService(
            schedule=self.schedule, catalog=self.catalog,
            notifier=self.notifier
        )
        self.auth = AuthService()
        self.current_user: Optional[User] = None

    def run(self) -> None:
        """Запускает основной цикл программы."""
        print("=" * 40)
        print("  Cinema Booking System (Lab 3)")
        print("=" * 40)
        
        while True:
            if not self.current_user:
                self._auth_menu()
            elif self.current_user.role == UserRole.ADMIN:
                self._admin_menu()
            else:
                self._client_menu()

    def _auth_menu(self) -> None:
        """Меню авторизации."""
        print("\n1. Войти | 2. Регистрация | 0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            email = input("Email: ")
            password = input("Пароль: ")
            user = self.auth.login(email, password)
            if user:
                self.current_user = user
                print(f"Вы вошли как {user.email}")
            else:
                print("Неверный логин или пароль")
        elif choice == "2":
            email = input("Email: ")
            password = input("Пароль: ")
            self.auth.register(email, password)
            print("Регистрация успешна!")
        elif choice == "0":
            exit(0)

    def _client_menu(self) -> None:
        """Меню клиента."""
        print(f"\n--- Клиент ({self.current_user.email}) ---")
        print("1. Афиша и бронь | 2. Мои билеты | 3. Выйти")
        choice = input("Выбор: ").strip()

        if choice == "1":
            self._show_movies_and_book()
        elif choice == "2":
            self._show_my_tickets()
        elif choice == "3":
            self.current_user = None

    def _admin_menu(self) -> None:
        """Меню администратора."""
        print(f"\n--- Администратор ---")
        print("1. Добавить фильм | 2. Добавить зал | 3. Создать сеанс | 4. Выйти")
        choice = input("Выбор: ").strip()

        if choice == "1":
            t = input("Название: "); d = input("Описание: ")
            dur = int(input("Длительность (мин): "))
            age = int(input("Возраст: "))
            self.catalog.add_movie(t, d, dur, age)
            print("Фильм добавлен.")
        elif choice == "2":
            n = input("Название зала: ")
            r = int(input("Рядов: ")); s = int(input("Мест в ряду: "))
            self.catalog.add_hall(n, r, s)
            print("Зал добавлен.")
        elif choice == "3":
            mid = int(input("ID фильма: "))
            hid = int(input("ID зала: "))
            time = input("Время (YYYY-MM-DD HH:MM): ")
            if self.schedule.create_screening(mid, hid, time):
                print("Сеанс создан.")
        elif choice == "4":
            self.current_user = None

    def _show_movies_and_book(self) -> None:
        """Просмотр афиши, схемы зала и бронирование."""
        movies = self.catalog.get_movies()
        if not movies:
            print("Нет активных фильмов."); return

        print("\nАфиша:")
        for m in movies:
            print(f"[{m.id}] {m.title} ({m.duration_min} мин, {m.age_limit}+)")

        mid = int(input("ID фильма: "))
        screenings = [s for s in self.schedule.get_screenings() if s.movie_id == mid]
        if not screenings:
            print("Нет сеансов."); return

        print("\nСеансы:")
        for s in screenings:
            h = self.catalog._halls[s.hall_id]
            print(f"[{s.id}] {s.start_time.strftime('%Y-%m-%d %H:%M')} | Зал: {h.name}")

        sid = int(input("ID сеанса: "))
        screening = self.schedule.get_screening(sid)
        if not screening: return

        hall = self.catalog._halls[screening.hall_id]
        print(f"\nСхема зала '{hall.name}':")
        for r in range(1, hall.rows + 1):
            row_str = f"Ряд {r}: "
            for s_num in range(1, hall.seats_per_row + 1):
                seat_id = hall.get_seat_id(r, s_num)
                status = screening.seat_map.get(seat_id)
                row_str += "[X] " if status == SeatStatus.BOOKED else "[.] "
            print(row_str)

        seats_input = input("Места (через запятую, напр. 1-1,1-2): ")
        seat_list = [s.strip() for s in seats_input.split(",")]
        
        self.booking.book_seats(
            user_id=self.current_user.id, screening_id=sid,
            seat_ids=seat_list, auth_service=self.auth
        )

    def _show_my_tickets(self) -> None:
        """Просмотр истории заказов и отмена."""
        bookings = self.booking.get_user_bookings(self.current_user.id)
        if not bookings:
            print("Нет билетов."); return

        print("\nВаши билеты:")
        for b in bookings:
            scr = self.schedule.get_screening(b.screening_id)
            mov = self.catalog._movies.get(scr.movie_id) if scr else None
            print(f"#{b.id}: {mov.title if mov else '?'} | Места: {', '.join(b.seats)} | QR: {b.qr_code}")
        
        cancel_id = input("ID для отмены (Enter - пропуск): ")
        if cancel_id:
            self.booking.cancel_booking(int(cancel_id), self.current_user.id)