from typing import Optional, List
from src.models import Booking, SeatStatus
from src.repositories import BookingRepository, InMemoryBookingRepository


class BookingService:
    """Сервис бронирования билетов."""

    def __init__(
        self,
        schedule,  # ScheduleService
        catalog,   # CatalogService
        auth,      # AuthService
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
        auth_service
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

        # Сохраняем обновлённую карту мест в БД
        self.schedule.screening_repository.update(screening_id, seat_map=screening.seat_map)

        # Генерируем QR-код
        qr_code = self._generate_qr_code(user_id, screening_id, seat_ids)

        # Создаем бронирование
        booking = Booking(
            id=None,  # ← было id=0
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
            # Сохраняем изменения в БД
            self.schedule.screening_repository.update(booking.screening_id, seat_map=screening.seat_map)

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