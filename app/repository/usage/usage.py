from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Usage


class UsageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_usages_by_model_id(self, model_id: int) -> list[Usage]:
        stmt = select(Usage).where(Usage.model_id == model_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
