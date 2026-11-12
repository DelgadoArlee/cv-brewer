from datetime import datetime, timezone
from uuid import uuid4

from database.database_service.modules.resume.models import NewResume, ResumeRecord
from database.database_service.modules.resume.repository import ResumeRepository


def _build_resume_record(record: NewResume) -> ResumeRecord:
    return ResumeRecord(
        resume_id=record.resume_id or str(uuid4()),
        original_file_path=record.original_file_path,
        metadata=record.metadata,
        parsed_data=record.parsed_data,
        validation_status=record.validation_status,
        processing_history=record.processing_history,
        created_at=record.created_at
        or datetime.now(timezone.utc).replace(tzinfo=None),
        deleted_at=record.deleted_at,
    )


class ResumeService:
    def __init__(self, repository: ResumeRepository) -> None:
        self._repository = repository

    def save_resume(self, record: NewResume) -> ResumeRecord:
        stored_record = _build_resume_record(record)
        self._repository.save(stored_record)
        return stored_record

    def get_resume(self, resume_id: str) -> ResumeRecord | None:
        return self._repository.get(resume_id)

    def find_resume_by_content_fingerprint(
        self,
        content_fingerprint: str,
    ) -> ResumeRecord | None:
        return self._repository.find_by_content_fingerprint(content_fingerprint)

    def list_resumes(self) -> list[ResumeRecord]:
        return self._repository.list_all()
