from fastapi import FastAPI, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.metrics import metrics_response
from app.core.observability import configure_observability
from app.db.session import SessionLocal, wait_for_database

setup_logging()

app = FastAPI(title=settings.app_name)
app.state.ready = False
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"] if settings.environment != "production" else ["localhost", "nginx", "127.0.0.1"])
configure_observability(app)


@app.on_event("startup")
def on_startup() -> None:
    wait_for_database()
    app.state.ready = True


@app.get("/healthz", tags=["health"])
def liveness_probe() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/readyz", tags=["health"])
def readiness_probe() -> dict[str, str]:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        app.state.ready = False
        return {"status": "not_ready"}
    finally:
        db.close()
    app.state.ready = True
    return {"status": "ready" if app.state.ready else "not_ready"}


@app.get("/metrics", tags=["observability"])
def metrics() -> Response:
    payload, content_type = metrics_response()
    return Response(content=payload, media_type=content_type)


app.include_router(api_router, prefix=settings.api_v1_prefix)
