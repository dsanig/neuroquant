from fastapi import APIRouter

from app.api.v1 import audit_log, auth, dashboard, health, imports, income, margin, performance, positions, risk, strategies, trades

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(margin.router, prefix="/margin", tags=["margin"])
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])
api_router.include_router(income.router, prefix="/income", tags=["income"])
api_router.include_router(imports.router, prefix="/imports", tags=["imports"])
api_router.include_router(audit_log.router, prefix="/audit-log", tags=["audit-log"])
