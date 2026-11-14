from typing import Any

import pytest

from llm.llm_service import (
    LLMAdapter,
    LLMService,
    ModelInfo,
    StructuredGenerationRequest,
)

from core.errors import LlmProcessingError
from core.services.parsing import (
    extract_deterministic_data,
    merge_resume_payloads,
    parse_resume_text,
    resolve_parsing_model,
)

_RESUME_TEXT = """Jane Doe
jane@example.com
+1 (555) 010-0100
https://linkedin.com/in/janedoe
https://github.com/janedoe

Summary:
Software engineer with platform experience.

Skills:
Python
SQL
Docker
"""


def _llm_payload() -> dict[str, Any]:
    return {
        "personal_info": {
            "name": "Janet Doe",
            "email": "janet@example.com",
            "phone": None,
            "address": None,
            "linkedin_url": None,
            "github_url": None,
        },
        "summary": "LLM summary",
        "experience": [
            {
                "company": "Acme",
                "position": "Engineer",
                "start_date": "2020-01-01",
                "end_date": None,
                "description": "Built services",
            }
        ],
        "education": [],
        "skills": ["Python", "Kubernetes"],
        "certifications": [],
    }


class _FakeAdapter(LLMAdapter):
    def __init__(self) -> None:
        self.available = True
        self.models = [ModelInfo(name="model-a"), ModelInfo(name="model-b")]
        self.response = _llm_payload()
        self.requests: list[StructuredGenerationRequest] = []
        self.failure: Exception | None = None

    def check_availability(self) -> bool:
        return self.available

    def list_models(self) -> list[ModelInfo]:
        return self.models

    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> dict[str, Any]:
        if self.failure is not None:
            raise self.failure
        self.requests.append(request)
        return self.response


def test_extract_deterministic_data_extracts_contact_and_sections() -> None:
    payload = extract_deterministic_data(_RESUME_TEXT)

    assert payload["personal_info"]["name"] == "Jane Doe"
    assert payload["personal_info"]["email"] == "jane@example.com"
    assert payload["personal_info"]["phone"] == "+1 (555) 010-0100"
    assert payload["personal_info"]["linkedin_url"] == "https://linkedin.com/in/janedoe"
    assert payload["personal_info"]["github_url"] == "https://github.com/janedoe"
    assert payload["summary"] == "Software engineer with platform experience."
    assert payload["skills"] == ["Python", "SQL", "Docker"]


def test_merge_resume_payloads_preserves_deterministic_values() -> None:
    deterministic = extract_deterministic_data(_RESUME_TEXT)

    merged = merge_resume_payloads(deterministic, _llm_payload())

    assert merged["personal_info"]["name"] == "Jane Doe"
    assert merged["personal_info"]["email"] == "jane@example.com"
    assert merged["summary"] == "Software engineer with platform experience."
    assert merged["skills"] == ["Python", "SQL", "Docker", "Kubernetes"]
    assert merged["experience"] == _llm_payload()["experience"]


def test_resolve_parsing_model_returns_first_available_model() -> None:
    service = LLMService(_FakeAdapter())

    assert resolve_parsing_model(service) == "model-a"


def test_resolve_parsing_model_rejects_unavailable_service() -> None:
    adapter = _FakeAdapter()
    adapter.available = False

    with pytest.raises(LlmProcessingError, match="unavailable"):
        resolve_parsing_model(LLMService(adapter))


def test_resolve_parsing_model_rejects_empty_model_list() -> None:
    adapter = _FakeAdapter()
    adapter.models = []

    with pytest.raises(LlmProcessingError, match="No LLM models"):
        resolve_parsing_model(LLMService(adapter))


def test_parse_resume_text_always_invokes_llm_enhancement() -> None:
    adapter = _FakeAdapter()

    payload = parse_resume_text(_RESUME_TEXT, LLMService(adapter), "model-a")

    assert len(adapter.requests) == 1
    request = adapter.requests[0]
    assert request.model == "model-a"
    assert request.json_schema["title"] == "Parsed Resume Data"
    assert payload["personal_info"]["name"] == "Jane Doe"
    assert payload["summary"] == "Software engineer with platform experience."
    assert payload["experience"] == _llm_payload()["experience"]


def test_parse_resume_text_reports_llm_failures() -> None:
    adapter = _FakeAdapter()
    adapter.failure = RuntimeError("generation failed")

    with pytest.raises(LlmProcessingError, match="enhancement failed"):
        parse_resume_text(_RESUME_TEXT, LLMService(adapter), "model-a")
