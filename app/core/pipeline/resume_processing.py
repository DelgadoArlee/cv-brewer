from datetime import datetime, timezone
from typing import Iterable

from core.services.resume import (
    NewResume,
    ParsedResumeData,
    ProcessingHistoryEntry,
    ResumeMetadata,
    ResumeService,
    ValidationStatus,
    validate_resume_payload,
)
from llm.llm_service import LLMService

from core.errors import (
    InvalidFileTypeError,
    InvalidPdfError,
    LlmProcessingError,
    ResumeSchemaError,
    UnreadableContentError,
)
from core.models import (
    ResumeInput,
    ResumeProcessingOutcome,
    ResumeProcessingStatus,
    StageCallback,
)
from core.services.metadata import build_resume_metadata
from core.services.parsing import parse_resume_text, resolve_parsing_model
from core.services.pdf import extract_pdf_text, validate_pdf, verify_pdf_signature


def _timestamp() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _record(
    history: list[ProcessingHistoryEntry],
    step: str,
    status: str,
    error_message: str | None = None,
) -> None:
    history.append(
        ProcessingHistoryEntry(
            step=step,
            timestamp=_timestamp(),
            status=status,
            error_message=error_message,
        )
    )


def _outcome(
    resume_input: ResumeInput,
    status: ResumeProcessingStatus,
    message: str,
    history: list[ProcessingHistoryEntry],
    *,
    resume_id: str | None = None,
    duplicate_resume_id: str | None = None,
) -> ResumeProcessingOutcome:
    return ResumeProcessingOutcome(
        file_name=resume_input.file_name,
        status=status,
        message=message,
        resume_id=resume_id,
        duplicate_resume_id=duplicate_resume_id,
        processing_history=tuple(history),
    )


def _build_validation_status() -> ValidationStatus:
    return ValidationStatus(
        file_type_valid=True,
        metadata_extraction_success=True,
        deduplication_result="unique",
        pdf_encryption_check=True,
        pdf_structure_valid=True,
        content_extraction_success=True,
        schema_validation_passed=True,
    )


def _build_new_resume(
    resume_input: ResumeInput,
    metadata: ResumeMetadata,
    parsed_data: ParsedResumeData,
    processing_history: list[ProcessingHistoryEntry],
) -> NewResume:
    return NewResume(
        original_file_path=resume_input.original_file_path,
        metadata=metadata,
        parsed_data=parsed_data,
        validation_status=_build_validation_status(),
        processing_history=processing_history,
    )


class ResumeProcessor:
    def __init__(
        self,
        resume_service: ResumeService,
        llm_service: LLMService,
    ) -> None:
        self._resume_service = resume_service
        self._llm_service = llm_service

    def process(
        self,
        resume_input: ResumeInput,
        *,
        on_stage: StageCallback | None = None,
    ) -> ResumeProcessingOutcome:
        history: list[ProcessingHistoryEntry] = []

        try:
            return self._process(resume_input, history, on_stage=on_stage)
        except Exception as exc:
            _record(history, "processing", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.PROCESSING_FAILURE,
                "Resume processing failed.",
                history,
            )

    def process_many(
        self,
        resume_inputs: Iterable[ResumeInput],
        *,
        on_stage: StageCallback | None = None,
    ) -> list[ResumeProcessingOutcome]:
        return [self.process(resume_input, on_stage=on_stage) for resume_input in resume_inputs]

    def _process(
        self,
        resume_input: ResumeInput,
        history: list[ProcessingHistoryEntry],
        *,
        on_stage: StageCallback | None = None,
    ) -> ResumeProcessingOutcome:
        if on_stage is not None:
            on_stage("file_type_validation")
        try:
            verify_pdf_signature(resume_input.content)
        except InvalidFileTypeError as exc:
            _record(history, "file_type_validation", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.INVALID_FILE_TYPE,
                str(exc),
                history,
            )
        _record(history, "file_type_validation", "success")

        if on_stage is not None:
            on_stage("metadata_extraction")
        try:
            metadata = build_resume_metadata(resume_input)
        except Exception as exc:
            _record(history, "metadata_extraction", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.PROCESSING_FAILURE,
                "Resume metadata extraction failed.",
                history,
            )
        _record(history, "metadata_extraction", "success")

        if on_stage is not None:
            on_stage("deduplication")
        try:
            existing_resume = self._resume_service.find_resume_by_content_fingerprint(
                metadata.content_fingerprint
            )
        except Exception as exc:
            _record(history, "deduplication", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.STORAGE_FAILURE,
                "Resume duplicate check failed.",
                history,
            )

        if existing_resume is not None:
            _record(history, "deduplication", "duplicate")
            return _outcome(
                resume_input,
                ResumeProcessingStatus.DUPLICATE,
                "Resume content already exists.",
                history,
                duplicate_resume_id=existing_resume.resume_id,
            )
        _record(history, "deduplication", "success")

        if on_stage is not None:
            on_stage("pdf_validation")
        try:
            validate_pdf(resume_input.content)
        except InvalidPdfError as exc:
            _record(history, "pdf_validation", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.INVALID_PDF,
                str(exc),
                history,
            )
        except Exception as exc:
            _record(history, "pdf_validation", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.INVALID_PDF,
                "PDF validation failed.",
                history,
            )
        _record(history, "pdf_validation", "success")

        if on_stage is not None:
            on_stage("content_extraction")
        try:
            text = extract_pdf_text(resume_input.content)
        except UnreadableContentError as exc:
            _record(history, "content_extraction", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.UNREADABLE,
                str(exc),
                history,
            )
        except Exception as exc:
            _record(history, "content_extraction", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.UNREADABLE,
                "PDF text extraction failed.",
                history,
            )
        _record(history, "content_extraction", "success")

        if on_stage is not None:
            on_stage("parsing")
        try:
            model = resolve_parsing_model(self._llm_service)
            payload = parse_resume_text(text, self._llm_service, model)
        except LlmProcessingError as exc:
            _record(history, "parsing", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.LLM_FAILURE,
                str(exc),
                history,
            )
        except Exception as exc:
            _record(history, "parsing", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.LLM_FAILURE,
                "Resume parsing failed.",
                history,
            )
        _record(history, "parsing", "success")

        if on_stage is not None:
            on_stage("schema_validation")
        try:
            parsed_data = validate_resume_payload(payload)
        except ResumeSchemaError as exc:
            _record(history, "schema_validation", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.SCHEMA_INVALID,
                str(exc),
                history,
            )
        except Exception as exc:
            _record(history, "schema_validation", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.SCHEMA_INVALID,
                "Resume schema validation failed.",
                history,
            )
        _record(history, "schema_validation", "success")

        if on_stage is not None:
            on_stage("storage")
        record_history = [
            *history,
            ProcessingHistoryEntry(
                step="storage",
                timestamp=_timestamp(),
                status="success",
            ),
        ]

        try:
            stored_resume = self._resume_service.save_resume(
                _build_new_resume(
                    resume_input,
                    metadata,
                    parsed_data,
                    record_history,
                )
            )
        except Exception as exc:
            _record(history, "storage", "failed", str(exc))
            return _outcome(
                resume_input,
                ResumeProcessingStatus.STORAGE_FAILURE,
                "Resume storage failed.",
                history,
            )

        return _outcome(
            resume_input,
            ResumeProcessingStatus.STORED,
            "Resume stored.",
            record_history,
            resume_id=stored_resume.resume_id,
        )
