from typing import Annotated

from fastapi import Depends

from app.repository.model import ModelRepository, get_model_repository
from app.use_case.ocr.ocr import OCRUseCase


def get_ocr_use_case(
    model_repository: Annotated[ModelRepository, Depends(get_model_repository)],
) -> OCRUseCase:
    return OCRUseCase(model_repository)
