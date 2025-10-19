from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class HealthResponse(BaseModel):
    status: str
    service: str = "model-serving-server"
    version: str = "0.1.0"


@app.get("/healthz", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def healthz() -> HealthResponse:
    return HealthResponse(status="healthy")
