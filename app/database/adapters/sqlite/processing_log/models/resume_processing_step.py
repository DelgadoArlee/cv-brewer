from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.adapters.sqlite.resume.models.base import Base

_STATUS_VALUES = (
    "RUNNING",
    "SUCCESS",
    "FAILED",
    "VALIDATION_FAILED",
    "PARTIAL_SUCCESS",
    "SKIPPED",
    "CANCELLED",
    "TIMEOUT",
)

_STATUS_CHECK = "status IN (" + ", ".join(
    "'" + status + "'" for status in _STATUS_VALUES
) + ")"


class ResumeProcessingStep(Base):
    __tablename__ = "resume_processing_steps"
    __table_args__ = (
        CheckConstraint(_STATUS_CHECK, name="ck_resume_processing_steps_status"),
        UniqueConstraint(
            "run_id",
            "step_order",
            "attempt_number",
            name="uq_resume_processing_step_order_attempt",
        ),
    )

    step_id: Mapped[str] = mapped_column(Text, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey(
            "resume_processing_runs.run_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    step_name: Mapped[str] = mapped_column(Text, nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    input: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    output: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    performance: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    error: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
    )
