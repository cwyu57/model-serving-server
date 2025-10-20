import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Models(Base):
    __tablename__ = "models"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="models_pkey"),
        Index("ix_models_id", "id"),
        Index("ix_models_model_name", "model_name", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String)
    usage_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text("now()"))

    usage: Mapped[list["Usage"]] = relationship("Usage", back_populates="model")


class Usage(Base):
    __tablename__ = "usage"
    __table_args__ = (
        ForeignKeyConstraint(["model_id"], ["models.id"], name="usage_model_id_fkey"),
        PrimaryKeyConstraint("id", name="usage_pkey"),
        Index("ix_usage_id", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    used_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text("now()"))
    model_id: Mapped[int | None] = mapped_column(Integer)

    model: Mapped[Optional["Models"]] = relationship("Models", back_populates="usage")
