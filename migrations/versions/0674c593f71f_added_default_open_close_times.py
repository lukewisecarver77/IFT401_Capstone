"""Added default open/close times

Revision ID: 0674c593f71f
Revises: 50718323a45a
Create Date: 2025-11-09 12:00:11.459825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0674c593f71f'
down_revision = '50718323a45a'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch_alter_table for SQLite
    with op.batch_alter_table("market_settings") as batch_op:
        batch_op.alter_column(
            "open_time",
            existing_type=sa.Time(),
            server_default=sa.text("'09:00:00'"),
            existing_nullable=False
        )
        batch_op.alter_column(
            "close_time",
            existing_type=sa.Time(),
            server_default=sa.text("'16:00:00'"),
            existing_nullable=False
        )


def downgrade():
    with op.batch_alter_table("market_settings") as batch_op:
        batch_op.alter_column(
            "open_time",
            existing_type=sa.Time(),
            server_default=None,
            existing_nullable=False
        )
        batch_op.alter_column(
            "close_time",
            existing_type=sa.Time(),
            server_default=None,
            existing_nullable=False
        )
