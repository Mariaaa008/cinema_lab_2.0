from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    CLIENT = "client"
    ADMIN = "admin"

@dataclass
class User:
    id: int | None
    email: str
    password: str
    role: UserRole = UserRole.CLIENT