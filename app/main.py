from collections.abc import Generator
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Models as Model
from app.models import Usage

app = FastAPI()


class HealthResponse(BaseModel):
    status: str
    service: str = "model-serving-server"
    version: str = "0.1.0"


@app.get("/healthz", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def healthz() -> HealthResponse:
    return HealthResponse(status="healthy")


# Pydantic Model for API Input
class OCRRequest(BaseModel):
    image: str
    model_name: str


class ModelUsage(BaseModel):
    model_name: str
    usages: list[datetime]


class ModelUsageCount(BaseModel):
    model_name: str
    usage_count: int


class OCRResponse(BaseModel):
    result: str


# Fake OCR function
def fake_ocr(image: str) -> str:
    return "0"


# Dependency to get DB session
def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API to run OCR
@app.post("/ocr", response_model=OCRResponse)
def run_ocr(request: OCRRequest, db: Annotated[Session, Depends(get_db)]) -> OCRResponse:
    model_name = request.model_name
    image = request.image
    model = db.query(Model).filter(Model.model_name == model_name).first()
    if not model:
        model = Model(model_name=model_name)
        db.add(model)
        db.commit()
        db.refresh(model)
    usage = Usage(model_id=model.id)
    db.add(usage)
    db.commit()
    model.usage_count += 1
    db.commit()
    ocr_result = fake_ocr(image)
    return OCRResponse(result=ocr_result)


# API to show all individual model usage logs
@app.post("/usage", response_model=list[ModelUsage])
def get_usage(db: Annotated[Session, Depends(get_db)]) -> list[ModelUsage]:
    models = db.query(Model).all()
    result = []
    for model in models:
        usages = db.query(Usage).filter(Usage.model_id == model.id).all()
        result.append(
            {"model_name": model.model_name, "usages": [usage.used_at for usage in usages]}
        )
    return [
        ModelUsage(model_name=model.model_name, usages=[usage.used_at for usage in usages])
        for model in models
    ]


# API to show models and their corresponding usage count
@app.post("/models_usage", response_model=list[ModelUsageCount])
def get_models_usage(db: Annotated[Session, Depends(get_db)]) -> list[ModelUsageCount]:
    models = db.query(Model).all()
    result = []
    for model in models:
        result.append(ModelUsageCount(model_name=model.model_name, usage_count=model.usage_count))
    return result
