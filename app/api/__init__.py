from fastapi import APIRouter

from .healthz import router as healthz_router
from .ocr import router as ocr_router
from .usage import router as usage_router

api_router = APIRouter()
api_router.include_router(healthz_router)
api_router.include_router(ocr_router)
api_router.include_router(usage_router)
