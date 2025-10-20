from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repository.usage.usage import UsageRepository


def get_usage_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UsageRepository:
    return UsageRepository(session)
