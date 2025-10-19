"""add_model_and_usage_table

Revision ID: 20251019201228662
Revises:
Create Date: 2025-10-20 04:12:39.155718

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "20251019201228662"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
