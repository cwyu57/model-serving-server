import os
from collections.abc import Generator
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Models as Model
from app.models import Usage

# Enable docs only in development environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
is_development = ENVIRONMENT.lower() == "development"

app = FastAPI(
    title="Model Serving Server",
    description="API for serving ML models with OCR capabilities and usage tracking",
    version="0.1.0",
    contact={
        "name": "API Support",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs" if is_development else None,
    redoc_url="/redoc" if is_development else None,
    openapi_url="/openapi.json" if is_development else None,
)


class HealthResponse(BaseModel):
    status: str
    service: str = "model-serving-server"
    version: str = "0.1.0"


@app.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the health status of the service",
    tags=["Health"],
)
async def healthz() -> HealthResponse:
    return HealthResponse(status="healthy")


# Pydantic Model for API Input
class OCRRequest(BaseModel):
    image: str = Field(
        description="Base64 encoded image or image path",
        examples=["base64_image_data"],
    )
    model_name: str = Field(
        description="Name of the OCR model to use",
        examples=["tesseract-v1"],
    )


class ModelUsage(BaseModel):
    model_name: str = Field(
        description="Name of the model",
        examples=["tesseract-v1"],
    )
    usages: list[datetime] = Field(description="List of timestamps when the model was used")


class ModelUsageCount(BaseModel):
    model_name: str = Field(
        description="Name of the model",
        examples=["tesseract-v1"],
    )
    usage_count: int = Field(
        description="Total number of times the model was used",
        examples=[42],
    )


class OCRResponse(BaseModel):
    result: str = Field(
        description="OCR extracted text result",
        examples=["Extracted text from image"],
    )


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
@app.post(
    "/ocr",
    response_model=OCRResponse,
    summary="Run OCR",
    description="Process an image using the specified OCR model and track usage",
    tags=["OCR"],
)
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
@app.get(
    "/usage",
    response_model=list[ModelUsage],
    summary="Get Usage Logs",
    description="Retrieve detailed usage logs for all models with timestamps",
    tags=["Usage"],
)
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
@app.get(
    "/models_usage",
    response_model=list[ModelUsageCount],
    summary="Get Model Usage Counts",
    description="Retrieve usage counts for all models",
    tags=["Usage"],
)
def get_models_usage(db: Annotated[Session, Depends(get_db)]) -> list[ModelUsageCount]:
    models = db.query(Model).all()
    result = []
    for model in models:
        result.append(ModelUsageCount(model_name=model.model_name, usage_count=model.usage_count))
    return result
