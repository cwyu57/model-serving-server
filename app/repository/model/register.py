from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session_generator
from app.repository.model.model import ModelRepository


def get_model_repository(
    session: Annotated[Session, Depends(get_session_generator)],
) -> ModelRepository:
    return ModelRepository(session)
