from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entity.usage import ModelUsage, ModelUsageCount
from app.models import Models, Usage

router = APIRouter()


@router.get(
    "/usage",
    response_model=list[ModelUsage],
    summary="Get Usage Logs",
    description="Retrieve detailed usage logs for all models with timestamps",
    tags=["Usage"],
)
def get_usage(db: Annotated[Session, Depends(get_db)]) -> list[ModelUsage]:
    models = db.query(Models).all()
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


@router.get(
    "/models_usage",
    response_model=list[ModelUsageCount],
    summary="Get Model Usage Counts",
    description="Retrieve usage counts for all models",
    tags=["Usage"],
)
def get_models_usage(db: Annotated[Session, Depends(get_db)]) -> list[ModelUsageCount]:
    models = db.query(Models).all()
    result = []
    for model in models:
        result.append(ModelUsageCount(model_name=model.model_name, usage_count=model.usage_count))
    return result
