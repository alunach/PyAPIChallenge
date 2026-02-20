from __future__ import annotations
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/live")
def live():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    # If you want, you could add a DB ping here.
    return {"status": "ok"}
