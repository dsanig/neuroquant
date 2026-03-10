from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@retry(stop=stop_after_attempt(10), wait=wait_exponential(min=1, max=10))
def wait_for_database() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
