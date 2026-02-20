from __future__ import annotations

import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.users import router as users_router
from app.api.health import router as health_router
from app.db.session import engine
from app.db.base import Base

configure_logging(settings.log_level)
log = logging.getLogger("app")

API_PREFIX = "/api/v1"

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
        openapi_url=f"{API_PREFIX}/openapi.json",
    )

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        try:
            response = await call_next(request)
        except Exception:
            # Ensure request_id appears in exception logs too
            log.exception("unhandled_exception", extra={"request_id": request_id, "path": str(request.url)})
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
        response.headers["X-Request-Id"] = request_id
        return response

    # Routers
    app.include_router(health_router, prefix=API_PREFIX)
    app.include_router(users_router, prefix=API_PREFIX)

    return app

app = create_app()

# Create tables for local quickstart (migrations recommended for prod).
Base.metadata.create_all(bind=engine)
