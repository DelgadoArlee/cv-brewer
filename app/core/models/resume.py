from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias


class ResumeProcessingStatus(Enum):
    STORED = "stored"
    DUPLICATE = "duplicate"
    INVALID_FILE_TYPE = "invalid_file_type"
    INVALID_PDF = "invalid_pdf"
    UNREADABLE = "unreadable"
    SCHEMA_INVALID = "schema_invalid"
    LLM_FAILURE = "llm_failure"
    STORAGE_FAILURE = "storage_failure"
    PROCESSING_FAILURE = "processing_failure"


@dataclass(frozen=True, slots=True)
class ResumeInput:
    file_name: str
    original_file_path: str
    content: bytes
    upload_timestamp: datetime | None = None


@dataclass(frozen=True, slots=True)
class ResumeProcessingOutcome:
    file_name: str
    status: ResumeProcessingStatus
    message: str
    resume_id: str | None = None
    duplicate_resume_id: str | None = None
    run_id: str | None = None


StageCallback: TypeAlias = Callable[[str], None]
