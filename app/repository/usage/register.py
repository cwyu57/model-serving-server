from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session_generator
from app.repository.usage.usage import UsageRepository


def get_usage_repository(
    session: Annotated[Session, Depends(get_session_generator)],
) -> UsageRepository:
    return UsageRepository(session)
