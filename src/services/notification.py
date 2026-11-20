import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List


class NotificationService:
    """Сервис отправки уведомлений (Email) через smtplib."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None
    ) -> None:
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