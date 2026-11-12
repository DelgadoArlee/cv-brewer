from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.adapters.sqlite.resume.models.base import Base

if TYPE_CHECKING:
    from database.adapters.sqlite.resume.models.resume_certification import (
        ResumeCertification,
    )
    from database.adapters.sqlite.resume.models.resume_education import ResumeEducation
    from database.adapters.sqlite.resume.models.resume_experience import ResumeExperience
    from database.adapters.sqlite.resume.models.resume_processing_history import (
        ResumeProcessingHistory,
    )
    from database.adapters.sqlite.resume.models.resume_skill import ResumeSkill


class Resume(Base):
    __tablename__ = "resumes"
    __table_args__ = (
        CheckConstraint(
            "file_size_bytes >= 0",
            name="ck_resumes_file_size_bytes_non_negative",
        ),
    )

    resume_id: Mapped[str] = mapped_column(Text, primary_key=True)
    original_file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    content_fingerprint: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_type_valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    metadata_extraction_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    deduplication_result: Mapped[str] = mapped_column(Text, nullable=False)
    pdf_encryption_check: Mapped[bool] = mapped_column(Boolean, nullable=False)
    pdf_structure_valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    content_extraction_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    schema_validation_passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    experience: Mapped[list[ResumeExperience]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeExperience.position_order",
    )
    education: Mapped[list[ResumeEducation]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeEducation.position_order",
    )
    certifications: Mapped[list[ResumeCertification]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeCertification.position_order",
    )
    skills: Mapped[list[ResumeSkill]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeSkill.position_order",
    )
    processing_history: Mapped[list[ResumeProcessingHistory]] = relationship(
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeProcessingHistory.position_order",
    )
