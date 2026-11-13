import json
from functools import lru_cache
from importlib.resources import files
from typing import Any

import jsonschema
from jsonschema import FormatChecker
from pydantic import ValidationError

from database.database_service.modules.resume import (
    Certification,
    Education,
    Experience,
    ParsedResumeData,
    PersonalInfo,
)

from core.errors import ResumeSchemaError
from core.validation.models import (
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
    schema_path = files("core.validation").joinpath("schemas/resume.json")
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
