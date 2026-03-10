from __future__ import annotations

import time
import uuid
from contextvars import ContextVar

import structlog
from fastapi import FastAPI, Request, Response

from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestContextMiddleware:
    def __init__(self, app):
        self.app = app
        self.logger = structlog.get_logger("api.request")

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        req_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        token = request_id_ctx_var.set(req_id)
        structlog.contextvars.bind_contextvars(request_id=req_id, path=request.url.path, method=request.method)
        started = time.perf_counter()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                latency = time.perf_counter() - started
                path = request.url.path
                REQUEST_COUNT.labels(method=request.method, path=path, status=str(status_code)).inc()
                REQUEST_LATENCY.labels(method=request.method, path=path).observe(latency)
                headers = message.setdefault("headers", [])
                headers.append((b"x-request-id", req_id.encode("utf-8")))
                self.logger.info(
                    "http.request.completed",
                    status_code=status_code,
                    latency_ms=round(latency * 1000, 2),
                    client=request.client.host if request.client else None,
                )
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            structlog.contextvars.clear_contextvars()
            request_id_ctx_var.reset(token)


def configure_observability(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
