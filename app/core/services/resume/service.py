import json
from datetime import datetime, timezone
from functools import lru_cache
from importlib.resources import files
from typing import Any
from uuid import uuid4

import jsonschema
from jsonschema import FormatChecker
from pydantic import ValidationError

from core.errors import ResumeSchemaError
from core.services.resume.models import (
    Certification,
    Education,
    Experience,
    NewResume,
    ParsedResumeData,
    PersonalInfo,
    ResumeRecord,
)
from core.services.resume.repository import ResumeRepository
from core.services.resume.validation.models import (
    CertificationModel,
    EducationModel,
    ExperienceModel,
    ParsedResumePayloadModel,
    PersonalInfoModel,
)


def _to_personal_info(model: PersonalInfoModel) -> PersonalInfo:
    return PersonalInfo(
        name=model.name,
        email=model.email,
        phone=model.phone,
        address=model.address,
        linkedin_url=model.linkedin_url,
        github_url=model.github_url,
    )


def _to_experience(model: ExperienceModel) -> Experience:
    return Experience(
        company=model.company,
        position=model.position,
        start_date=model.start_date,
        end_date=model.end_date,
        description=model.description,
    )


def _to_education(model: EducationModel) -> Education:
    return Education(
        institution=model.institution,
        degree=model.degree,
        field_of_study=model.field_of_study,
        start_date=model.start_date,
        end_date=model.end_date,
    )


def _to_certification(model: CertificationModel) -> Certification:
    return Certification(
        name=model.name,
        issuer=model.issuer,
        issue_date=model.issue_date,
        expiry_date=model.expiry_date,
    )


def _to_parsed_resume_data(model: ParsedResumePayloadModel) -> ParsedResumeData:
    return ParsedResumeData(
        personal_info=_to_personal_info(model.personal_info),
        summary=model.summary,
        experience=[_to_experience(item) for item in model.experience],
        education=[_to_education(item) for item in model.education],
        skills=list(model.skills),
        certifications=[_to_certification(item) for item in model.certifications],
    )


@lru_cache(maxsize=1)
def load_resume_schema() -> dict[str, Any]:
    schema_path = files("core.services.resume.validation").joinpath(
        "schemas/resume.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return schema


def validate_resume_payload(payload: dict[str, Any]) -> ParsedResumeData:
    schema = load_resume_schema()
    try:
        jsonschema.validate(
            instance=payload,
            schema=schema,
            format_checker=FormatChecker(),
        )
    except jsonschema.ValidationError as exc:
        raise ResumeSchemaError(exc.message) from exc
    except jsonschema.SchemaError as exc:
        raise ResumeSchemaError("Resume JSON Schema is invalid.") from exc

    try:
        model = ParsedResumePayloadModel.model_validate(payload)
    except ValidationError as exc:
        raise ResumeSchemaError(str(exc)) from exc

    return _to_parsed_resume_data(model)


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
