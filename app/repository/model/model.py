from sqlalchemy.orm import Session

from app.models import Model, Usage


class ModelRepository:
    def __init__(self, session: Session):
        self.session = session

    def execute_ocr(self, model_name: str) -> None:
        model = self.session.query(Model).filter(Model.model_name == model_name).first()
        if not model:
            model = Model(model_name=model_name)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

        usage = Usage(model_id=model.id)
        self.session.add(usage)
        self.session.commit()

        model.usage_count += 1
        self.session.commit()

    def get_all(self) -> list[Model]:
        return self.session.query(Model).all()
