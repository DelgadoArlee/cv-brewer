from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.adapters.sqlite.resume.models.base import Base

if TYPE_CHECKING:
    from database.adapters.sqlite.resume.models.resume import Resume


class ResumeEducation(Base):
    __tablename__ = "resume_education"
    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_education_resume_position",
        ),
        Index("ix_resume_education_resume_id", "resume_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resume_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("resumes.resume_id", ondelete="CASCADE"),
        nullable=False,
    )
    position_order: Mapped[int] = mapped_column(Integer, nullable=False)
    institution: Mapped[str] = mapped_column(Text, nullable=False)
    degree: Mapped[str] = mapped_column(Text, nullable=False)
    field_of_study: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    resume: Mapped[Resume] = relationship(back_populates="education")
