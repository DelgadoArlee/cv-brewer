import hashlib
from datetime import datetime, timezone

from core.models import ResumeInput
from core.modules.metadata import (
    build_resume_metadata,
    calculate_content_fingerprint,
    resolve_upload_timestamp,
)


def test_calculate_content_fingerprint_uses_raw_bytes() -> None:
    assert calculate_content_fingerprint(b"resume") == hashlib.sha256(
        b"resume"
    ).hexdigest()
    assert calculate_content_fingerprint(b"resume") != calculate_content_fingerprint(
        b"Resume"
    )


def test_resolve_upload_timestamp_uses_current_time_when_missing() -> None:
    timestamp = resolve_upload_timestamp(None)

    assert timestamp.tzinfo is None
    assert timestamp.year >= 2026


def test_resolve_upload_timestamp_normalizes_aware_values() -> None:
    timestamp = resolve_upload_timestamp(
        datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc)
    )

    assert timestamp == datetime(2026, 1, 1, 10, 0)
    assert timestamp.tzinfo is None


def test_build_resume_metadata_uses_input_values() -> None:
    resume_input = ResumeInput(
        file_name="resume.pdf",
        original_file_path="/resumes/resume.pdf",
        content=b"%PDF-1.7\ncontent",
        upload_timestamp=datetime(2026, 1, 1, 10, 0),
    )

    metadata = build_resume_metadata(resume_input)

    assert metadata.file_name == "resume.pdf"
    assert metadata.file_size_bytes == len(resume_input.content)
    assert metadata.upload_timestamp == datetime(2026, 1, 1, 10, 0)
    assert metadata.content_fingerprint == calculate_content_fingerprint(
        resume_input.content
    )
