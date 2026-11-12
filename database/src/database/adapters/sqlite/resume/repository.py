from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from database.adapters.sqlite.engine import session_scope
from database.adapters.sqlite.resume.models import (
    Resume,
    ResumeCertification,
    ResumeEducation,
    ResumeExperience,
    ResumeProcessingHistory,
    ResumeSkill,
)
from database.database_service.modules.resume.models import (
    Certification,
    Education,
    Experience,
    ParsedResumeData,
    PersonalInfo,
    ProcessingHistoryEntry,
    ResumeMetadata,
    ResumeRecord,
    ValidationStatus,
)
from database.database_service.modules.resume.repository import ResumeRepository


def _to_experience_model(
    position_order: int,
    experience: Experience,
) -> ResumeExperience:
    return ResumeExperience(
        position_order=position_order,
        company=experience.company,
        position=experience.position,
        start_date=experience.start_date,
        end_date=experience.end_date,
        description=experience.description,
    )


def _to_education_model(
    position_order: int,
    education: Education,
) -> ResumeEducation:
    return ResumeEducation(
        position_order=position_order,
        institution=education.institution,
        degree=education.degree,
        field_of_study=education.field_of_study,
        start_date=education.start_date,
        end_date=education.end_date,
    )


def _to_certification_model(
    position_order: int,
    certification: Certification,
) -> ResumeCertification:
    return ResumeCertification(
        position_order=position_order,
        name=certification.name,
        issuer=certification.issuer,
        issue_date=certification.issue_date,
        expiry_date=certification.expiry_date,
    )


def _to_skill_model(position_order: int, skill: str) -> ResumeSkill:
    return ResumeSkill(position_order=position_order, skill=skill)


def _to_processing_history_model(
    position_order: int,
    entry: ProcessingHistoryEntry,
) -> ResumeProcessingHistory:
    return ResumeProcessingHistory(
        position_order=position_order,
        step=entry.step,
        timestamp=entry.timestamp,
        status=entry.status,
        error_message=entry.error_message,
    )


def _to_resume_model(record: ResumeRecord) -> Resume:
    return Resume(
        resume_id=record.resume_id,
        original_file_path=record.original_file_path,
        file_name=record.metadata.file_name,
        file_size_bytes=record.metadata.file_size_bytes,
        upload_timestamp=record.metadata.upload_timestamp,
        content_fingerprint=record.metadata.content_fingerprint,
        name=record.parsed_data.personal_info.name,
        email=record.parsed_data.personal_info.email,
        phone=record.parsed_data.personal_info.phone,
        address=record.parsed_data.personal_info.address,
        linkedin_url=record.parsed_data.personal_info.linkedin_url,
        github_url=record.parsed_data.personal_info.github_url,
        summary=record.parsed_data.summary,
        file_type_valid=record.validation_status.file_type_valid,
        metadata_extraction_success=(
            record.validation_status.metadata_extraction_success
        ),
        deduplication_result=record.validation_status.deduplication_result,
        pdf_encryption_check=record.validation_status.pdf_encryption_check,
        pdf_structure_valid=record.validation_status.pdf_structure_valid,
        content_extraction_success=(
            record.validation_status.content_extraction_success
        ),
        schema_validation_passed=(
            record.validation_status.schema_validation_passed
        ),
        created_at=record.created_at,
        deleted_at=record.deleted_at,
        experience=[
            _to_experience_model(index, experience)
            for index, experience in enumerate(record.parsed_data.experience)
        ],
        education=[
            _to_education_model(index, education)
            for index, education in enumerate(record.parsed_data.education)
        ],
        certifications=[
            _to_certification_model(index, certification)
            for index, certification in enumerate(record.parsed_data.certifications)
        ],
        skills=[
            _to_skill_model(index, skill)
            for index, skill in enumerate(record.parsed_data.skills)
        ],
        processing_history=[
            _to_processing_history_model(index, entry)
            for index, entry in enumerate(record.processing_history)
        ],
    )


def _to_experience(model: ResumeExperience) -> Experience:
    return Experience(
        company=model.company,
        position=model.position,
        start_date=model.start_date,
        end_date=model.end_date,
        description=model.description,
    )


def _to_education(model: ResumeEducation) -> Education:
    return Education(
        institution=model.institution,
        degree=model.degree,
        field_of_study=model.field_of_study,
        start_date=model.start_date,
        end_date=model.end_date,
    )


def _to_certification(model: ResumeCertification) -> Certification:
    return Certification(
        name=model.name,
        issuer=model.issuer,
        issue_date=model.issue_date,
        expiry_date=model.expiry_date,
    )


def _to_processing_history(
    model: ResumeProcessingHistory,
) -> ProcessingHistoryEntry:
    return ProcessingHistoryEntry(
        step=model.step,
        timestamp=model.timestamp,
        status=model.status,
        error_message=model.error_message,
    )


def _to_record(model: Resume) -> ResumeRecord:
    return ResumeRecord(
        resume_id=model.resume_id,
        original_file_path=model.original_file_path,
        metadata=ResumeMetadata(
            file_name=model.file_name,
            file_size_bytes=model.file_size_bytes,
            upload_timestamp=model.upload_timestamp,
            content_fingerprint=model.content_fingerprint,
        ),
        parsed_data=ParsedResumeData(
            personal_info=PersonalInfo(
                name=model.name,
                email=model.email,
                phone=model.phone,
                address=model.address,
                linkedin_url=model.linkedin_url,
                github_url=model.github_url,
            ),
            summary=model.summary,
            experience=[_to_experience(experience) for experience in model.experience],
            education=[_to_education(education) for education in model.education],
            skills=[skill.skill for skill in model.skills],
            certifications=[
                _to_certification(certification)
                for certification in model.certifications
            ],
        ),
        validation_status=ValidationStatus(
            file_type_valid=model.file_type_valid,
            metadata_extraction_success=model.metadata_extraction_success,
            deduplication_result=model.deduplication_result,
            pdf_encryption_check=model.pdf_encryption_check,
            pdf_structure_valid=model.pdf_structure_valid,
            content_extraction_success=model.content_extraction_success,
            schema_validation_passed=model.schema_validation_passed,
        ),
        processing_history=[
            _to_processing_history(entry) for entry in model.processing_history
        ],
        created_at=model.created_at,
        deleted_at=model.deleted_at,
    )


class SqliteResumeRepository(ResumeRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, record: ResumeRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.add(_to_resume_model(record))

    def get(self, resume_id: str) -> ResumeRecord | None:
        with session_scope(self._session_factory) as session:
            model = session.get(Resume, resume_id)
            return _to_record(model) if model is not None else None

    def find_by_content_fingerprint(
        self,
        content_fingerprint: str,
    ) -> ResumeRecord | None:
        with session_scope(self._session_factory) as session:
            statement = select(Resume).where(
                Resume.content_fingerprint == content_fingerprint
            )
            model = session.execute(statement).scalar_one_or_none()
            return _to_record(model) if model is not None else None

    def list_all(self) -> list[ResumeRecord]:
        with session_scope(self._session_factory) as session:
            statement = select(Resume).order_by(Resume.created_at)
            models = session.scalars(statement).all()
            return [_to_record(model) for model in models]
