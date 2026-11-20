from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Booking:
    id: int | None
    user_id: int
    screening_id: int
    seats: list[str]
    qr_code: str
    created_at: datetime = field(default_factory=datetime.now)