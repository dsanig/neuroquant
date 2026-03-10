from fastapi import APIRouter

from app.api.v1 import auth, margin, trades

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
api_router.include_router(margin.router, prefix="/margin", tags=["margin"])
