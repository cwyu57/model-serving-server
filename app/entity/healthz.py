from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str = "model-serving-server"
    version: str = "0.1.0"
