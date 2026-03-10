from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import wait_for_database

setup_logging()

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    wait_for_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.api_v1_prefix)
