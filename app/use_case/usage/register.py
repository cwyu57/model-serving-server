from typing import Annotated

from fastapi import Depends

from app.repository.model import ModelRepository, get_model_repository
from app.repository.usage import UsageRepository, get_usage_repository
from app.use_case.usage.usage import UsageUseCase


def get_usage_use_case(
    model_repository: Annotated[ModelRepository, Depends(get_model_repository)],
    usage_repository: Annotated[UsageRepository, Depends(get_usage_repository)],
) -> UsageUseCase:
    return UsageUseCase(model_repository, usage_repository)
