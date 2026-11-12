"""create resume tables

Revision ID: 20261110_0001
Revises:
Create Date: 2026-11-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261110_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "resumes",
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("original_file_path", sa.Text(), nullable=False),
        sa.Column("file_name", sa.Text(), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False),
        sa.Column("upload_timestamp", sa.DateTime(), nullable=False),
        sa.Column("content_fingerprint", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("linkedin_url", sa.Text(), nullable=True),
        sa.Column("github_url", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("file_type_valid", sa.Boolean(), nullable=False),
        sa.Column("metadata_extraction_success", sa.Boolean(), nullable=False),
        sa.Column("deduplication_result", sa.Text(), nullable=False),
        sa.Column("pdf_encryption_check", sa.Boolean(), nullable=False),
        sa.Column("pdf_structure_valid", sa.Boolean(), nullable=False),
        sa.Column("content_extraction_success", sa.Boolean(), nullable=False),
        sa.Column("schema_validation_passed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "file_size_bytes >= 0",
            name="ck_resumes_file_size_bytes_non_negative",
        ),
        sa.PrimaryKeyConstraint("resume_id"),
        sa.UniqueConstraint("content_fingerprint"),
    )
    op.create_index("ix_resumes_created_at", "resumes", ["created_at"])

    op.create_table(
        "resume_experience",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("position_order", sa.Integer(), nullable=False),
        sa.Column("company", sa.Text(), nullable=False),
        sa.Column("position", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.resume_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_experience_resume_position",
        ),
    )
    op.create_index(
        "ix_resume_experience_resume_id",
        "resume_experience",
        ["resume_id"],
    )

    op.create_table(
        "resume_education",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("position_order", sa.Integer(), nullable=False),
        sa.Column("institution", sa.Text(), nullable=False),
        sa.Column("degree", sa.Text(), nullable=False),
        sa.Column("field_of_study", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.resume_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_education_resume_position",
        ),
    )
    op.create_index(
        "ix_resume_education_resume_id",
        "resume_education",
        ["resume_id"],
    )

    op.create_table(
        "resume_certifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("position_order", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("issuer", sa.Text(), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.resume_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_certifications_resume_position",
        ),
    )
    op.create_index(
        "ix_resume_certifications_resume_id",
        "resume_certifications",
        ["resume_id"],
    )

    op.create_table(
        "resume_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resume_id", sa.Text(), nullable=False),
        sa.Column("position_order", sa.Integer(), nullable=False),
        sa.Column("skill", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.resume_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resume_id",
            "position_order",
            name="uq_resume_skills_resume_position",
        ),
    )
    op.create_index("ix_resume_skills_resume_id", "resume_skills", ["resume_id"])

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


def downgrade() -> None:
    op.drop_index(
        "ix_resume_processing_history_resume_id",
        table_name="resume_processing_history",
    )
    op.drop_table("resume_processing_history")
    op.drop_index("ix_resume_skills_resume_id", table_name="resume_skills")
    op.drop_table("resume_skills")
    op.drop_index(
        "ix_resume_certifications_resume_id",
        table_name="resume_certifications",
    )
    op.drop_table("resume_certifications")
    op.drop_index("ix_resume_education_resume_id", table_name="resume_education")
    op.drop_table("resume_education")
    op.drop_index("ix_resume_experience_resume_id", table_name="resume_experience")
    op.drop_table("resume_experience")
    op.drop_index("ix_resumes_created_at", table_name="resumes")
    op.drop_table("resumes")
