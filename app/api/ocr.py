from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.controller.ocr import OCRRequest, OCRResponse
from app.entity.use_case.ocr import OCRInput
from app.use_case.ocr import OCRUseCase, get_ocr_use_case

router = APIRouter()


@router.post(
    "/ocr",
    response_model=OCRResponse,
    summary="Run OCR",
    description="Process an image using the specified OCR model and track usage",
    tags=["OCR"],
)
def run_ocr(
    request: OCRRequest,
    ocr_use_case: Annotated[OCRUseCase, Depends(get_ocr_use_case)],
) -> OCRResponse:
    output = ocr_use_case.execute(OCRInput(image=request.image, model_name=request.model_name))
    return OCRResponse(result=output.result)
