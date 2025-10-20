from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Model, Usage


class ModelRepository:
    def __init__(self, session: Session):
        self.session = session

    def execute_ocr(self, model_name: str) -> None:
        with self.session.begin():
            stmt = (
                insert(Model)
                .values(model_name=model_name, usage_count=1)
                .on_conflict_do_update(
                    index_elements=["model_name"],
                    set_={"usage_count": Model.usage_count + 1},
                )
                .returning(Model.id)
            )
            result = self.session.execute(stmt)
            model_id = result.scalar_one()

            usage = Usage(model_id=model_id)
            self.session.add(usage)

    def get_all(self) -> list[Model]:
        return self.session.query(Model).all()
