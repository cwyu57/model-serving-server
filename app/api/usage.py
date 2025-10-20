from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.controller.usage import ModelUsageCountResponse, ModelUsageResponse
from app.use_case.usage import UsageUseCase, get_usage_use_case

router = APIRouter()


@router.get(
    "/usage",
    response_model=list[ModelUsageResponse],
    summary="Get Usage Logs",
    description="Retrieve detailed usage logs for all models with timestamps",
    tags=["Usage"],
)
def get_usage(
    usage_use_case: Annotated[UsageUseCase, Depends(get_usage_use_case)],
) -> list[ModelUsageResponse]:
    outputs = usage_use_case.get_all_model_usages()
    return [
        ModelUsageResponse(model_name=output.model_name, usages=output.usages) for output in outputs
    ]


@router.get(
    "/models_usage",
    response_model=list[ModelUsageCountResponse],
    summary="Get Model Usage Counts",
    description="Retrieve usage counts for all models",
    tags=["Usage"],
)
def get_models_usage(
    usage_use_case: Annotated[UsageUseCase, Depends(get_usage_use_case)],
) -> list[ModelUsageCountResponse]:
    outputs = usage_use_case.get_all_model_usage_counts()
    return [
        ModelUsageCountResponse(model_name=output.model_name, usage_count=output.usage_count)
        for output in outputs
    ]
