from sqlalchemy.orm import Session

from app.models import Model, Usage


class ModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, model_name: str) -> Model | None:
        """Get model by name"""
        return self.db.query(Model).filter(Model.model_name == model_name).first()

    def create(self, model_name: str) -> Model:
        """Create a new model"""
        model = Model(model_name=model_name)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_or_create(self, model_name: str) -> Model:
        """Get existing model or create a new one"""
        model = self.get_by_name(model_name)
        if not model:
            model = self.create(model_name)
        return model

    def increment_usage_count(self, model: Model) -> None:
        """Increment the usage count for a model"""
        model.usage_count += 1
        self.db.commit()

    def record_usage(self, model_id: int) -> Usage:
        """Record a usage entry for a model"""
        usage = Usage(model_id=model_id)
        self.db.add(usage)
        self.db.commit()
        return usage

    def get_all_models(self) -> list[Model]:
        """Get all models"""
        return self.db.query(Model).all()

    def get_usages_by_model_id(self, model_id: int) -> list[Usage]:
        """Get all usage records for a specific model"""
        return self.db.query(Usage).filter(Usage.model_id == model_id).all()
