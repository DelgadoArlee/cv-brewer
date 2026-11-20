"""add processing run and step tables

Revision ID: 20261120_0004
Revises: 20261119_0003
Create Date: 2026-11-20
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261120_0004"
down_revision: str | None = "20261119_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_PROCESSING_STATUSES = (
    "RUNNING",
    "SUCCESS",
    "FAILED",
    "VALIDATION_FAILED",
    "PARTIAL_SUCCESS",
    "SKIPPED",
    "CANCELLED",
    "TIMEOUT",
)

_PROCESSING_STATUS_CHECK = "status IN (" + ", ".join(
    "'" + status + "'" for status in _PROCESSING_STATUSES
) + ")"

_LLM_STATUS_CHECK = "status IN ('SUCCESS', 'FAILED', 'TIMEOUT')"
_LEGACY_LLM_STATUS_CHECK = "status IN ('success', 'failed', 'timeout')"


def upgrade() -> None:
    op.create_table(
        "resume_processing_runs",
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("process_name", sa.Text(), nullable=False),
        sa.Column("process_version", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("resume_id", sa.Text(), nullable=True),
        sa.Column("matched_resume_id", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column("summary", sa.JSON(), nullable=False),
        sa.Column("performance", sa.JSON(), nullable=False),
        sa.Column("error", sa.JSON(), nullable=True),
        sa.CheckConstraint(
            _PROCESSING_STATUS_CHECK,
            name="ck_resume_processing_runs_status",
        ),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index(
        "ix_resume_processing_runs_started_at",
        "resume_processing_runs",
        ["started_at"],
    )
    op.create_index(
        "ix_resume_processing_runs_resume_id",
        "resume_processing_runs",
        ["resume_id"],
    )

    op.create_table(
        "resume_processing_steps",
        sa.Column("step_id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("step_name", sa.Text(), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column("input", sa.JSON(), nullable=False),
        sa.Column("output", sa.JSON(), nullable=False),
        sa.Column("performance", sa.JSON(), nullable=False),
        sa.Column("error", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.CheckConstraint(
            _PROCESSING_STATUS_CHECK,
            name="ck_resume_processing_steps_status",
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["resume_processing_runs.run_id"],
            name="fk_resume_processing_steps_run_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("step_id"),
        sa.UniqueConstraint(
            "run_id",
            "step_order",
            "attempt_number",
            name="uq_resume_processing_step_order_attempt",
        ),
    )
    op.create_index(
        "ix_resume_processing_steps_run_id",
        "resume_processing_steps",
        ["run_id"],
    )

    op.drop_index(
        "ix_resume_processing_history_resume_id",
        table_name="resume_processing_history",
    )
    op.drop_table("resume_processing_history")

    with op.batch_alter_table("llm_logs", recreate="always") as batch:
        batch.add_column(sa.Column("processing_step_id", sa.Text(), nullable=True))
        batch.add_column(sa.Column("start_memory_mb", sa.Float(), nullable=True))
        batch.add_column(sa.Column("peak_memory_mb", sa.Float(), nullable=True))
        batch.add_column(sa.Column("end_memory_mb", sa.Float(), nullable=True))
        batch.add_column(sa.Column("memory_delta_mb", sa.Float(), nullable=True))
        batch.add_column(sa.Column("cpu_avg_percent", sa.Float(), nullable=True))
        batch.add_column(sa.Column("cpu_peak_percent", sa.Float(), nullable=True))
        batch.add_column(
            sa.Column("sample_count", sa.Integer(), nullable=False, server_default="0")
        )
        batch.create_foreign_key(
            "fk_llm_logs_processing_step_id",
            "resume_processing_steps",
            ["processing_step_id"],
            ["step_id"],
            ondelete="SET NULL",
        )
        batch.create_index(
            "ix_llm_logs_processing_step_id",
            ["processing_step_id"],
        )
        batch.drop_constraint("ck_llm_logs_status", type_="check")
        batch.create_check_constraint(
            "ck_llm_logs_status",
            _LLM_STATUS_CHECK,
        )

    op.execute("UPDATE llm_logs SET status = UPPER(status)")
    op.execute(
        """
        UPDATE llm_logs
        SET start_memory_mb = memory_before_bytes / 1048576.0,
            end_memory_mb = memory_after_bytes / 1048576.0,
            peak_memory_mb = memory_peak_bytes / 1048576.0,
            memory_delta_mb = memory_delta_bytes / 1048576.0
        """
    )

    with op.batch_alter_table("llm_logs", recreate="always") as batch:
        batch.drop_column("memory_before_bytes")
        batch.drop_column("memory_after_bytes")
        batch.drop_column("memory_peak_bytes")
        batch.drop_column("memory_delta_bytes")
        batch.alter_column("sample_count", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("llm_logs", recreate="always") as batch:
        batch.add_column(sa.Column("memory_before_bytes", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("memory_after_bytes", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("memory_peak_bytes", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("memory_delta_bytes", sa.Integer(), nullable=True))

    op.execute("UPDATE llm_logs SET status = LOWER(status)")
    op.execute(
        """
        UPDATE llm_logs
        SET memory_before_bytes = CAST(start_memory_mb * 1048576 AS INTEGER),
            memory_after_bytes = CAST(end_memory_mb * 1048576 AS INTEGER),
            memory_peak_bytes = CAST(peak_memory_mb * 1048576 AS INTEGER),
            memory_delta_bytes = CAST(memory_delta_mb * 1048576 AS INTEGER)
        """
    )

    with op.batch_alter_table("llm_logs", recreate="always") as batch:
        batch.drop_constraint("ck_llm_logs_status", type_="check")
        batch.create_check_constraint(
            "ck_llm_logs_status",
            _LEGACY_LLM_STATUS_CHECK,
        )
        batch.drop_index("ix_llm_logs_processing_step_id")
        batch.drop_constraint(
            "fk_llm_logs_processing_step_id",
            type_="foreignkey",
        )
        batch.drop_column("sample_count")
        batch.drop_column("cpu_peak_percent")
        batch.drop_column("cpu_avg_percent")
        batch.drop_column("memory_delta_mb")
        batch.drop_column("end_memory_mb")
        batch.drop_column("peak_memory_mb")
        batch.drop_column("start_memory_mb")
        batch.drop_column("processing_step_id")

    op.create_table(
        "resume_processing_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("position_order", sa.Integer(), nullable=False),
        sa.Column("step", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.resume_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_processing_history_resume_position",
        ),
    )
    op.create_index(
        "ix_resume_processing_history_resume_id",
        "resume_processing_history",
        ["resume_id"],
    )
    op.drop_index(
        "ix_resume_processing_steps_run_id",
        table_name="resume_processing_steps",
    )
    op.drop_table("resume_processing_steps")
    op.drop_index(
        "ix_resume_processing_runs_resume_id",
        table_name="resume_processing_runs",
    )
    op.drop_index(
        "ix_resume_processing_runs_started_at",
        table_name="resume_processing_runs",
    )
    op.drop_table("resume_processing_runs")
