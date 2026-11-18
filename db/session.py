from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Фабрика сессий. Используй в сервисах."""
    return SessionLocal()