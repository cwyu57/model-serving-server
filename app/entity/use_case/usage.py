from datetime import datetime

from pydantic import BaseModel, Field


class ModelUsageOutput(BaseModel):
    """Output model for a single model's usage information"""

    model_name: str = Field(description="Name of the model")
    usages: list[datetime] = Field(description="List of timestamps when the model was used")


class ModelUsageCountOutput(BaseModel):
    """Output model for a single model's usage count"""

    model_name: str = Field(description="Name of the model")
    usage_count: int = Field(description="Total number of times the model was used")
