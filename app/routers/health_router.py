from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.repositories.health_repository import HealthRepository
from app.services.health_service import HealthService

router = APIRouter(prefix="/api/v1/health",tags=["Health"])

@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    repository = HealthRepository(db)
    service = HealthService(repository)

    result = {
        "application": "running",
        "postgresql": "unknown",
        "qdrant": "unknown",
        "gemini_configuration": "unknown"
    }

    try:
        await service.check_database()
        result["postgresql"] = "connected"
    except Exception:
        result["postgresql"] = "disconnected"

    try:
        service.check_qdrant()
        result["qdrant"] = "connected"
    except Exception:
        result["qdrant"] = "disconnected"

    result["gemini_configuration"] = (
        "configured"
        if service.check_gemini_config()
        else "missing_api_key"
    )

    if (
        result["postgresql"] != "connected"
        or result["qdrant"] != "connected"
    ):
        raise HTTPException(
            status_code=503,
            detail=result
        )

    return result