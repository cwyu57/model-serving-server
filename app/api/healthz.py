from fastapi import APIRouter, status

from app.entity.controller.healthz import HealthResponse

router = APIRouter()


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the health status of the service",
    tags=["Health"],
)
async def healthz() -> HealthResponse:
    return HealthResponse(status="healthy")
