from datetime import datetime
from typing import Any

from sqlalchemy import JSON, CheckConstraint, DateTime, Float, Text
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


class ResumeProcessingRun(Base):
    __tablename__ = "resume_processing_runs"
    __table_args__ = (
        CheckConstraint(_STATUS_CHECK, name="ck_resume_processing_runs_status"),
    )

    run_id: Mapped[str] = mapped_column(Text, primary_key=True)
    process_name: Mapped[str] = mapped_column(Text, nullable=False)
    process_version: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_id: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    matched_resume_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    summary: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    performance: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    error: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
