from datetime import date
from typing import Any

import pytest

from database.database_service.modules.resume import ParsedResumeData

from core.errors import ResumeSchemaError
from core.validation.schema_validation import (
    load_resume_schema,
    validate_resume_payload,
)


def _valid_payload() -> dict[str, Any]:
    return {
        "personal_info": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+1-555-0100",
            "address": None,
            "linkedin_url": None,
            "github_url": None,
        },
        "summary": "Software engineer",
        "experience": [
            {
                "company": "Acme",
                "position": "Engineer",
                "start_date": "2020-01-01",
                "end_date": None,
                "description": "Built services",
            }
        ],
        "education": [
            {
                "institution": "University",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2014-09-01",
                "end_date": "2018-05-31",
            }
        ],
        "skills": ["Python", "SQL"],
        "certifications": [
            {
                "name": "Cloud Certification",
                "issuer": "Cloud Provider",
                "issue_date": "2022-06-15",
                "expiry_date": None,
            }
        ],
    }


def test_load_resume_schema_returns_packaged_schema() -> None:
    schema = load_resume_schema()

    assert schema["title"] == "Parsed Resume Data"
    assert schema["required"] == ["personal_info", "experience", "skills"]


def test_validate_resume_payload_converts_to_database_model() -> None:
    parsed_data = validate_resume_payload(_valid_payload())

    assert isinstance(parsed_data, ParsedResumeData)
    assert parsed_data.personal_info.name == "Jane Doe"
    assert parsed_data.experience[0].start_date == date(2020, 1, 1)
    assert parsed_data.education[0].end_date == date(2018, 5, 31)
    assert parsed_data.skills == ["Python", "SQL"]
    assert parsed_data.certifications[0].issue_date == date(2022, 6, 15)


def test_validate_resume_payload_defaults_optional_arrays() -> None:
    payload = _valid_payload()
    del payload["education"]
    del payload["certifications"]

    parsed_data = validate_resume_payload(payload)

    assert parsed_data.education == []
    assert parsed_data.certifications == []


def test_validate_resume_payload_rejects_missing_email() -> None:
    payload = _valid_payload()
    del payload["personal_info"]["email"]

    with pytest.raises(ResumeSchemaError, match="email"):
        validate_resume_payload(payload)


def test_validate_resume_payload_rejects_empty_name() -> None:
    payload = _valid_payload()
    payload["personal_info"]["name"] = ""

    with pytest.raises(ResumeSchemaError):
        validate_resume_payload(payload)


def test_validate_resume_payload_rejects_invalid_email() -> None:
    payload = _valid_payload()
    payload["personal_info"]["email"] = "not-an-email"

    with pytest.raises(ResumeSchemaError, match="email"):
        validate_resume_payload(payload)


def test_validate_resume_payload_rejects_invalid_date() -> None:
    payload = _valid_payload()
    payload["experience"][0]["start_date"] = "not-a-date"

    with pytest.raises(ResumeSchemaError):
        validate_resume_payload(payload)


def test_validate_resume_payload_rejects_unknown_fields() -> None:
    payload = _valid_payload()
    payload["unexpected"] = "value"

    with pytest.raises(ResumeSchemaError):
        validate_resume_payload(payload)
