import hashlib
from datetime import datetime, timezone

from database.database_service.modules.resume import ResumeMetadata

from core.models import ResumeInput


def calculate_content_fingerprint(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def resolve_upload_timestamp(upload_timestamp: datetime | None) -> datetime:
    if upload_timestamp is None:
        return datetime.now(timezone.utc).replace(tzinfo=None)
    if upload_timestamp.tzinfo is None:
        return upload_timestamp
    return upload_timestamp.astimezone(timezone.utc).replace(tzinfo=None)


def build_resume_metadata(resume_input: ResumeInput) -> ResumeMetadata:
    return ResumeMetadata(
        file_name=resume_input.file_name,
        file_size_bytes=len(resume_input.content),
        upload_timestamp=resolve_upload_timestamp(resume_input.upload_timestamp),
        content_fingerprint=calculate_content_fingerprint(resume_input.content),
    )
