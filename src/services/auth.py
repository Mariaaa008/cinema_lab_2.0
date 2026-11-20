from typing import Optional
from src.models import User, UserRole
from src.repositories import UserRepository, InMemoryUserRepository


class AuthService:
    """Сервис аутентификации и управления пользователями."""

    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        self.user_repository = user_repository or InMemoryUserRepository()
        # Создаем администратора по умолчанию
        try:
            self.register("masya2016dm@gmail.com", "admin", UserRole.ADMIN)
        except ValueError:
            pass  # Админ уже существует

    def register(self, email: str, password: str, role: UserRole = UserRole.CLIENT) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")
        user = User(id=None, email=email, password=password, role=role)
        return self.user_repository.add(user)

    def login(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email)
        if user and user.password == password:
            return user
        return None

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get(user_id)