from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.adapters.sqlite.resume.models.base import Base

if TYPE_CHECKING:
    from database.adapters.sqlite.resume.models.resume import Resume


class ResumeProcessingHistory(Base):
    __tablename__ = "resume_processing_history"
    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_processing_history_resume_position",
        ),
        Index("ix_resume_processing_history_resume_id", "resume_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resume_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("resumes.resume_id", ondelete="CASCADE"),
        nullable=False,
    )
    position_order: Mapped[int] = mapped_column(Integer, nullable=False)
    step: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    resume: Mapped[Resume] = relationship(back_populates="processing_history")
