from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class ResumeMetadata:
    file_name: str
    file_size_bytes: int
    upload_timestamp: datetime
    content_fingerprint: str


@dataclass(frozen=True, slots=True)
class PersonalInfo:
    name: str
    email: str
    phone: str | None = None
    address: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None


@dataclass(frozen=True, slots=True)
class Experience:
    company: str
    position: str
    start_date: date
    end_date: date | None
    description: str


@dataclass(frozen=True, slots=True)
class Education:
    institution: str
    degree: str
    field_of_study: str | None
    start_date: date
    end_date: date | None


@dataclass(frozen=True, slots=True)
class Certification:
    name: str
    issuer: str
    issue_date: date
    expiry_date: date | None


@dataclass(frozen=True, slots=True)
class ParsedResumeData:
    personal_info: PersonalInfo
    summary: str | None
    experience: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ValidationStatus:
    file_type_valid: bool
    metadata_extraction_success: bool
    deduplication_result: str
    pdf_encryption_check: bool
    pdf_structure_valid: bool
    content_extraction_success: bool
    schema_validation_passed: bool


@dataclass(frozen=True, slots=True)
class ProcessingHistoryEntry:
    step: str
    timestamp: datetime
    status: str
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class NewResume:
    original_file_path: str
    metadata: ResumeMetadata
    parsed_data: ParsedResumeData
    validation_status: ValidationStatus
    processing_history: list[ProcessingHistoryEntry] = field(default_factory=list)
    resume_id: str | None = None
    created_at: datetime | None = None
    deleted_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ResumeRecord:
    resume_id: str
    original_file_path: str
    metadata: ResumeMetadata
    parsed_data: ParsedResumeData
    validation_status: ValidationStatus
    processing_history: list[ProcessingHistoryEntry]
    created_at: datetime
    deleted_at: datetime | None = None
