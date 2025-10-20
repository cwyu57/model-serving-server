from app.entity.use_case.usage import ModelUsageCountOutput, ModelUsageOutput
from app.repository.model import ModelRepository
from app.repository.usage import UsageRepository


class UsageUseCase:
    def __init__(self, model_repository: ModelRepository, usage_repository: UsageRepository):
        self.model_repository = model_repository
        self.usage_repository = usage_repository

    def get_all_model_usages(self) -> list[ModelUsageOutput]:
        """
        Get detailed usage logs for all models with timestamps
        """
        models = self.model_repository.get_all()

        return [
            ModelUsageOutput(
                model_name=model.model_name,
                usages=[
                    usage.used_at
                    for usage in self.usage_repository.get_usages_by_model_id(model.id)
                ],
            )
            for model in models
        ]

    def get_all_model_usage_counts(self) -> list[ModelUsageCountOutput]:
        """
        Get usage counts for all models
        """
        models = self.model_repository.get_all()
        return [
            ModelUsageCountOutput(
                model_name=model.model_name,
                usage_count=model.usage_count,
            )
            for model in models
        ]
