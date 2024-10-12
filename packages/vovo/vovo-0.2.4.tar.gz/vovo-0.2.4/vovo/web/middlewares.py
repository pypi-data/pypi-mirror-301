import structlog
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send

from vovo.custom_logger import generate_correlation_id
from vovo.settings import global_settings


def add_cors_middleware(app):
    """cors中间件"""
    origins = [str(origin).strip("/") for origin in global_settings.CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 允许的来源
        allow_credentials=True,  # 允许发送 cookies
        allow_methods=["*"],  # 允许的 HTTP 方法，例如 GET, POST 等
        allow_headers=["*"],  # 允许的 HTTP 头
    )


class LogCorrelationIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        structlog.contextvars.bind_contextvars(
            correlation_id=generate_correlation_id(),
            method=scope["method"],
            path=scope["path"],
        )

        await self.app(scope, receive, send)

        structlog.contextvars.unbind_contextvars("correlation_id", "method", "path")
