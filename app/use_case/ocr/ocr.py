from app.entity.use_case.ocr import OCRInput, OCROutput
from app.repository.model.model import ModelRepository
from app.service.ocr import fake_ocr


class OCRUseCase:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    async def execute(self, request: OCRInput) -> OCROutput:
        """
        Execute OCR use case:
        1. Get or create the model
        2. Record usage
        3. Increment usage count
        4. Perform OCR
        """
        await self.model_repository.execute_ocr(request.model_name)
        ocr_result = fake_ocr(request.image)

        return OCROutput(result=ocr_result)
