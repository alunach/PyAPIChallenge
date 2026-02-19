import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.users import router as users_router
from app.db.session import engine
from app.db.base import Base

configure_logging(settings.log_level)
log = logging.getLogger("app")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        root_path="/api",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Simple request-id middleware (helps tracing in logs)
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

    # Centralized error handler for unexpected exceptions
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        log.exception("unhandled_exception", path=str(request.url))
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    @app.get("/healthz", tags=["Health"])
    def healthz():
        return {"status": "ok"}

    app.include_router(users_router)

    return app

app = create_app()

# For local/dev convenience: create tables if not using Alembic yet.
# In production you should run migrations (see README).
Base.metadata.create_all(bind=engine)
