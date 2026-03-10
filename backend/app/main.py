from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import wait_for_database

setup_logging()

app = FastAPI(title=settings.app_name)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"] if settings.environment != "production" else ["localhost", "nginx", "127.0.0.1"])


@app.on_event("startup")
def on_startup() -> None:
    wait_for_database()


app.include_router(api_router, prefix=settings.api_v1_prefix)
