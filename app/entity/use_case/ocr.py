from pydantic import BaseModel, Field


class OCRInput(BaseModel):
    image: str = Field(
        description="Base64 encoded image or image path",
        examples=["base64_image_data"],
    )
    model_name: str = Field(
        description="Name of the OCR model to use",
        examples=["tesseract-v1"],
    )


class OCROutput(BaseModel):
    result: str = Field(
        description="OCR extracted text result",
        examples=["Extracted text from image"],
    )
