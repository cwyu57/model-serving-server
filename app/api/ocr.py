from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entity.ocr import OCRRequest, OCRResponse
from app.models import Models, Usage
from app.service.ocr import fake_ocr

router = APIRouter()


@router.post(
    "/ocr",
    response_model=OCRResponse,
    summary="Run OCR",
    description="Process an image using the specified OCR model and track usage",
    tags=["OCR"],
)
def run_ocr(request: OCRRequest, db: Annotated[Session, Depends(get_db)]) -> OCRResponse:
    model_name = request.model_name
    image = request.image
    model = db.query(Models).filter(Models.model_name == model_name).first()
    if not model:
        model = Models(model_name=model_name)
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
