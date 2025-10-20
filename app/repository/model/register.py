from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repository.model.model import ModelRepository


def get_model_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ModelRepository:
    return ModelRepository(session)
