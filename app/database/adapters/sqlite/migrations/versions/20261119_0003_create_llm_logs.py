"""create llm logs table

Revision ID: 20261119_0003
Revises: 20261110_0001
Create Date: 2026-11-19
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261119_0003"
down_revision: str | None = "20261110_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "llm_logs",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("operation", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("response_content", sa.Text(), nullable=True),
        sa.Column("finish_reason", sa.Text(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("total_tokens", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column("memory_before_bytes", sa.Integer(), nullable=True),
        sa.Column("memory_after_bytes", sa.Integer(), nullable=True),
        sa.Column("memory_peak_bytes", sa.Integer(), nullable=True),
        sa.Column("memory_delta_bytes", sa.Integer(), nullable=True),
        sa.Column("error_type", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('success', 'failed', 'timeout')",
            name="ck_llm_logs_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_llm_logs_created_at", "llm_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_llm_logs_created_at", table_name="llm_logs")
    op.drop_table("llm_logs")
