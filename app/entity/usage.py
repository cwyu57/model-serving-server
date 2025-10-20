from datetime import datetime

from pydantic import BaseModel, Field


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
