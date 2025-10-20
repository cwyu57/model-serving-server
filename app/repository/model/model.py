from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Model, Usage


class ModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute_ocr(self, model_name: str) -> None:
        async with self.session.begin():
            stmt = (
                insert(Model)
                .values(model_name=model_name, usage_count=1)
                .on_conflict_do_update(
                    index_elements=["model_name"],
                    set_={"usage_count": Model.usage_count + 1},
                )
                .returning(Model.id)
            )
            result = await self.session.execute(stmt)
            model_id = result.scalar_one()

            usage = Usage(model_id=model_id)
            self.session.add(usage)

    async def get_all(self) -> list[Model]:
        result = await self.session.execute(select(Model))
        return list(result.scalars().all())

    async def get_all_with_usages(self) -> list[Model]:
        """
        Get all models with their usage records using a single JOIN query.
        Avoids N+1 query problem by eagerly loading the usage relationship.
        """
        stmt = select(Model).options(joinedload(Model.usage))
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())
