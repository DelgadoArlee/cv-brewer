import ast
from datetime import datetime
from pathlib import Path
from typing import Any

from database import create_resume_service, initialize_database
from llm.llm_service import (
    LLMAdapter,
    LLMService,
    ModelInfo,
    StructuredGenerationRequest,
)

from core.models import ResumeInput, ResumeProcessingStatus
from core.pipeline import ResumeProcessor
from tests.fixtures.resumes.pdf_factory import build_pdf, encrypt_pdf

_FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "sqlite3",
    "httpx",
    "ollama",
    "database.adapters",
    "llm.adapters",
)


def _llm_payload() -> dict[str, Any]:
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
        "education": [],
        "skills": ["Python", "SQL"],
        "certifications": [],
    }


class _FakeAdapter(LLMAdapter):
    def __init__(self) -> None:
        self.available = True
        self.models = [ModelInfo(name="model-a")]
        self.response = _llm_payload()
        self.requests: list[StructuredGenerationRequest] = []

    def check_availability(self) -> bool:
        return self.available

    def list_models(self) -> list[ModelInfo]:
        return self.models

    def generate_structured(
        self,
        request: StructuredGenerationRequest,
    ) -> dict[str, Any]:
        self.requests.append(request)
        return self.response


class _FailingResumeService:
    def find_resume_by_content_fingerprint(self, content_fingerprint: str) -> None:
        return None

    def save_resume(self, record: Any) -> Any:
        raise RuntimeError("storage unavailable")


def _resume_input(
    content: bytes,
    *,
    file_name: str = "resume.pdf",
) -> ResumeInput:
    return ResumeInput(
        file_name=file_name,
        original_file_path=f"/resumes/{file_name}",
        content=content,
        upload_timestamp=datetime(2026, 1, 1, 10, 0),
    )


def _processor(tmp_path: Path, adapter: _FakeAdapter | None = None) -> tuple[
    ResumeProcessor, Any, _FakeAdapter
]:
    database_path = tmp_path / "resumes.db"
    initialize_database(database_path)
    resume_service = create_resume_service(database_path)
    fake_adapter = adapter or _FakeAdapter()
    return ResumeProcessor(resume_service, LLMService(fake_adapter)), resume_service, fake_adapter


def test_process_stores_valid_resume(tmp_path: Path) -> None:
    processor, resume_service, adapter = _processor(tmp_path)
    content = build_pdf("Jane Doe\njane@example.com\nSkills: Python, SQL")

    outcome = processor.process(_resume_input(content))

    assert outcome.status is ResumeProcessingStatus.STORED
    assert outcome.resume_id is not None
    stored_record = resume_service.get_resume(outcome.resume_id)
    assert stored_record is not None
    assert stored_record.metadata.file_name == "resume.pdf"
    assert stored_record.parsed_data.personal_info.name == "Jane Doe"
    assert stored_record.parsed_data.personal_info.email == "jane@example.com"
    assert stored_record.validation_status.schema_validation_passed is True
    assert [entry.step for entry in outcome.processing_history] == [
        "file_type_validation",
        "metadata_extraction",
        "deduplication",
        "pdf_validation",
        "content_extraction",
        "parsing",
        "schema_validation",
        "storage",
    ]
    assert len(adapter.requests) == 1


def test_process_rejects_invalid_file_type(tmp_path: Path) -> None:
    processor, resume_service, _ = _processor(tmp_path)

    outcome = processor.process(_resume_input(b"not a pdf"))

    assert outcome.status is ResumeProcessingStatus.INVALID_FILE_TYPE
    assert resume_service.list_resumes() == []


def test_process_reports_duplicate_without_storing(tmp_path: Path) -> None:
    processor, resume_service, _ = _processor(tmp_path)
    content = build_pdf("Jane Doe\njane@example.com")

    first = processor.process(_resume_input(content, file_name="first.pdf"))
    second = processor.process(_resume_input(content, file_name="second.pdf"))

    assert first.status is ResumeProcessingStatus.STORED
    assert second.status is ResumeProcessingStatus.DUPLICATE
    assert second.duplicate_resume_id == first.resume_id
    assert len(resume_service.list_resumes()) == 1


def test_process_rejects_encrypted_pdf(tmp_path: Path) -> None:
    processor, resume_service, _ = _processor(tmp_path)

    outcome = processor.process(_resume_input(encrypt_pdf(build_pdf("Jane Doe"))))

    assert outcome.status is ResumeProcessingStatus.INVALID_PDF
    assert resume_service.list_resumes() == []


def test_process_rejects_unreadable_pdf(tmp_path: Path) -> None:
    processor, resume_service, _ = _processor(tmp_path)

    outcome = processor.process(_resume_input(build_pdf("")))

    assert outcome.status is ResumeProcessingStatus.UNREADABLE
    assert resume_service.list_resumes() == []


def test_process_reports_llm_failure_when_no_model_is_available(
    tmp_path: Path,
) -> None:
    adapter = _FakeAdapter()
    adapter.models = []
    processor, resume_service, _ = _processor(tmp_path, adapter)

    outcome = processor.process(_resume_input(build_pdf("Jane Doe\njane@example.com")))

    assert outcome.status is ResumeProcessingStatus.LLM_FAILURE
    assert resume_service.list_resumes() == []


def test_process_rejects_schema_invalid_llm_payload(tmp_path: Path) -> None:
    adapter = _FakeAdapter()
    adapter.response = _llm_payload()
    adapter.response["personal_info"]["email"] = ""
    processor, resume_service, _ = _processor(tmp_path, adapter)

    outcome = processor.process(_resume_input(build_pdf("Jane Doe")))

    assert outcome.status is ResumeProcessingStatus.SCHEMA_INVALID
    assert resume_service.list_resumes() == []


def test_process_reports_storage_failure(tmp_path: Path) -> None:
    processor = ResumeProcessor(_FailingResumeService(), LLMService(_FakeAdapter()))

    outcome = processor.process(_resume_input(build_pdf("Jane Doe\njane@example.com")))

    assert outcome.status is ResumeProcessingStatus.STORAGE_FAILURE


def test_process_many_continues_after_a_failure(tmp_path: Path) -> None:
    processor, resume_service, _ = _processor(tmp_path)

    outcomes = processor.process_many(
        [
            _resume_input(b"not a pdf", file_name="invalid.pdf"),
            _resume_input(build_pdf("Jane Doe\njane@example.com"), file_name="valid.pdf"),
        ]
    )

    assert [outcome.status for outcome in outcomes] == [
        ResumeProcessingStatus.INVALID_FILE_TYPE,
        ResumeProcessingStatus.STORED,
    ]
    assert len(resume_service.list_resumes()) == 1


def test_core_does_not_import_adapters_or_concrete_clients() -> None:
    core_source = Path(__file__).resolve().parents[3] / "core" / "src" / "core"

    imported_modules: list[str] = []
    for source_path in core_source.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.append(node.module)

    assert not [
        module
        for module in imported_modules
        if module.startswith(_FORBIDDEN_IMPORT_PREFIXES)
    ]


def test_process_reports_stages_in_order(tmp_path: Path) -> None:
    processor, resume_service, adapter = _processor(tmp_path)
    content = build_pdf("Jane Doe\njane@example.com\nSkills: Python, SQL")

    stages: list[str] = []
    outcome = processor.process(_resume_input(content), on_stage=stages.append)

    assert outcome.status is ResumeProcessingStatus.STORED
    assert stages == [
        "file_type_validation",
        "metadata_extraction",
        "deduplication",
        "pdf_validation",
        "content_extraction",
        "parsing",
        "schema_validation",
        "storage",
    ]
