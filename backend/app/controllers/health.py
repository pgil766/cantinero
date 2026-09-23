from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter(tags=["salud"])


@router.get("/health", response_model=HealthResponse, summary="Verificación de vida del servicio")
def health() -> HealthResponse:
    """Sin datos ni dependencias: solo indica que el proceso responde (Docker, Caddy)."""
    return HealthResponse(status="ok")
