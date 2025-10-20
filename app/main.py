import os

from fastapi import FastAPI

from app.api import api_router

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
    docs_url="/docs" if is_development else None,
)

app.include_router(api_router)
