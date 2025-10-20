"""add_model_and_usage_table

Revision ID: 20251019201228662
Revises:
Create Date: 2025-10-20 04:12:39.155718

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20251019201228662"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create models table
    op.create_table(
        "models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_models_id"), "models", ["id"], unique=False)
    op.create_index(op.f("ix_models_model_name"), "models", ["model_name"], unique=True)

    # Create usage table
    op.create_table(
        "usage",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=True),
        sa.Column("used_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usage_id"), "usage", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop usage table first (due to foreign key constraint)
    op.drop_index(op.f("ix_usage_id"), table_name="usage")
    op.drop_table("usage")

    # Drop models table
    op.drop_index(op.f("ix_models_model_name"), table_name="models")
    op.drop_index(op.f("ix_models_id"), table_name="models")
    op.drop_table("models")
