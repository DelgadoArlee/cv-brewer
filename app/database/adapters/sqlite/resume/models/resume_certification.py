from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.adapters.sqlite.resume.models.base import Base

if TYPE_CHECKING:
    from database.adapters.sqlite.resume.models.resume import Resume


class ResumeCertification(Base):
    __tablename__ = "resume_certifications"
    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_certifications_resume_position",
        ),
        Index("ix_resume_certifications_resume_id", "resume_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resume_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("resumes.resume_id", ondelete="CASCADE"),
        nullable=False,
    )
    position_order: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    issuer: Mapped[str] = mapped_column(Text, nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    resume: Mapped[Resume] = relationship(back_populates="certifications")
