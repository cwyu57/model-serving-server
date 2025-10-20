from sqlalchemy.orm import Session

from app.models import Usage


class UsageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_usages_by_model_id(self, model_id: int) -> list[Usage]:
        return self.session.query(Usage).filter(Usage.model_id == model_id).all()
