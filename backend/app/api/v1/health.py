from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.db.session import SessionLocal

try:
    from redis import Redis
except Exception:  # noqa: BLE001
    Redis = None

router = APIRouter()


@router.get("", tags=["health"])
def health() -> dict:
    db_ok = False
    redis_ok = False

    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:  # noqa: BLE001
        db_ok = False
    finally:
        db.close()

    if Redis is not None:
        try:
            client = Redis.from_url(settings.redis_url)
            redis_ok = bool(client.ping())
        except Exception:  # noqa: BLE001
            redis_ok = False

    status = "ok" if db_ok and redis_ok else "degraded"
    return {"status": status, "dependencies": {"postgres": db_ok, "redis": redis_ok}}
