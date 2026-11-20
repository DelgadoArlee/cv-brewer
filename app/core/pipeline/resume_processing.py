import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass, replace
from typing import Any

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
from core.services.llm import LLMService, LLMTimeoutError
from core.services.logger import RunPerformanceMonitor
from core.services.metadata import build_resume_metadata
from core.services.parsing import parse_resume_text, resolve_parsing_model
from core.services.pdf import extract_pdf_text, validate_pdf, verify_pdf_signature
from core.services.processing_log import (
    ProcessingError,
    ProcessingLogStatus,
    ProcessingPerformance,
    ProcessingLogService,
    ProcessingRunRecord,
    ProcessingStepInput,
    ProcessingStepOutput,
    ProcessingStepRecord,
    ProcessingSummary,
    error_from_exception,
    performance_from_log,
)
from core.services.resume import (
    NewResume,
    ParsedResumeData,
    ResumeMetadata,
    ResumeService,
    ValidationStatus,
    validate_resume_payload,
)

_PROCESS_NAME = "resume_processing"
_PROCESS_VERSION = "1.0"

_STEP_NAMES = (
    "file_type_validation",
    "metadata_extraction",
    "deduplication",
    "pdf_validation",
    "content_extraction",
    "parsing",
    "schema_validation",
    "storage",
)

_RUN_STATUS_BY_OUTCOME = {
    ResumeProcessingStatus.STORED: ProcessingLogStatus.SUCCESS,
    ResumeProcessingStatus.DUPLICATE: ProcessingLogStatus.SUCCESS,
    ResumeProcessingStatus.INVALID_FILE_TYPE: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.INVALID_PDF: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.UNREADABLE: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.SCHEMA_INVALID: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.LLM_FAILURE: ProcessingLogStatus.FAILED,
    ResumeProcessingStatus.STORAGE_FAILURE: ProcessingLogStatus.FAILED,
    ResumeProcessingStatus.PROCESSING_FAILURE: ProcessingLogStatus.FAILED,
}

_STEP_STATUS_BY_OUTCOME = {
    ResumeProcessingStatus.INVALID_FILE_TYPE: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.INVALID_PDF: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.UNREADABLE: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.SCHEMA_INVALID: ProcessingLogStatus.VALIDATION_FAILED,
    ResumeProcessingStatus.LLM_FAILURE: ProcessingLogStatus.FAILED,
    ResumeProcessingStatus.STORAGE_FAILURE: ProcessingLogStatus.FAILED,
    ResumeProcessingStatus.PROCESSING_FAILURE: ProcessingLogStatus.FAILED,
}

_ERROR_CODE_BY_OUTCOME = {
    ResumeProcessingStatus.INVALID_FILE_TYPE: "INVALID_FILE_TYPE",
    ResumeProcessingStatus.INVALID_PDF: "INVALID_PDF",
    ResumeProcessingStatus.UNREADABLE: "UNREADABLE_CONTENT",
    ResumeProcessingStatus.SCHEMA_INVALID: "RESUME_SCHEMA_INVALID",
    ResumeProcessingStatus.LLM_FAILURE: "LLM_PROCESSING_FAILURE",
    ResumeProcessingStatus.STORAGE_FAILURE: "RESUME_STORAGE_FAILURE",
    ResumeProcessingStatus.PROCESSING_FAILURE: "RESUME_PROCESSING_FAILURE",
}

_FAILURE_STATUSES = {
    ProcessingLogStatus.FAILED,
    ProcessingLogStatus.VALIDATION_FAILED,
    ProcessingLogStatus.PARTIAL_SUCCESS,
    ProcessingLogStatus.CANCELLED,
    ProcessingLogStatus.TIMEOUT,
}


@dataclass(slots=True)
class _StepRun:
    record: ProcessingStepRecord
    order: int


def _is_timeout(exc: Exception) -> bool:
    current: BaseException | None = exc
    while current is not None:
        if isinstance(current, (LLMTimeoutError, TimeoutError)):
            return True
        current = current.__cause__ or current.__context__
    return False


def _summarize(records: list[ProcessingStepRecord]) -> ProcessingSummary:
    return ProcessingSummary(
        total_steps=len(records),
        completed_steps=sum(
            record.status == ProcessingLogStatus.SUCCESS for record in records
        ),
        failed_steps=sum(
            record.status in _FAILURE_STATUSES for record in records
        ),
        skipped_steps=sum(
            record.status == ProcessingLogStatus.SKIPPED for record in records
        ),
    )


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _payload_size(value: dict[str, Any]) -> int:
    return len(json.dumps(value, sort_keys=True, default=str).encode("utf-8"))


def _file_input(resume_input: ResumeInput) -> ProcessingStepInput:
    return ProcessingStepInput(
        type="file_content",
        size_bytes=len(resume_input.content),
        hash=_hash_text(resume_input.file_name),
        metadata={
            "file_name": resume_input.file_name,
            "original_file_path": resume_input.original_file_path,
        },
    )


def _validation_output(step_name: str, **metadata: Any) -> ProcessingStepOutput:
    return ProcessingStepOutput(type=step_name, metadata=metadata)


def _metadata_output(metadata: ResumeMetadata) -> ProcessingStepOutput:
    return ProcessingStepOutput(
        type="resume_metadata",
        hash=metadata.content_fingerprint,
        metadata={
            "file_name": metadata.file_name,
            "file_size_bytes": metadata.file_size_bytes,
            "upload_timestamp": metadata.upload_timestamp.isoformat(),
        },
    )


def _text_output(text: str) -> ProcessingStepOutput:
    return ProcessingStepOutput(
        type="extracted_text",
        size_bytes=len(text.encode("utf-8")),
        hash=_hash_text(text),
        metadata={"character_count": len(text)},
    )


def _payload_output(payload: dict[str, Any]) -> ProcessingStepOutput:
    return ProcessingStepOutput(
        type="resume_payload",
        size_bytes=_payload_size(payload),
        metadata={"top_level_fields": sorted(payload)},
    )


def _payload_input(
    payload: dict[str, Any],
    source_step_id: str | None,
) -> ProcessingStepInput:
    return ProcessingStepInput(
        type="resume_payload",
        source_step_id=source_step_id,
        size_bytes=_payload_size(payload),
        metadata={"top_level_fields": sorted(payload)},
    )


def _parsed_data_output(parsed_data: ParsedResumeData) -> ProcessingStepOutput:
    return ProcessingStepOutput(
        type="resume_data",
        metadata={
            "experience_count": len(parsed_data.experience),
            "education_count": len(parsed_data.education),
            "skill_count": len(parsed_data.skills),
            "certification_count": len(parsed_data.certifications),
        },
    )


def _stored_output(resume_id: str) -> ProcessingStepOutput:
    return ProcessingStepOutput(type="stored_resume", metadata={"resume_id": resume_id})


def _outcome(
    run_logger: "_RunLogger",
    resume_input: ResumeInput,
    status: ResumeProcessingStatus,
    message: str,
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
        run_id=run_logger.run_id,
    )


def _step_error(
    exc: Exception,
    status: ResumeProcessingStatus,
    step_name: str,
    resume_input: ResumeInput,
) -> ProcessingError:
    return error_from_exception(
        exc,
        _ERROR_CODE_BY_OUTCOME[status],
        details={
            "step_name": step_name,
            "file_name": resume_input.file_name,
        },
    )


def _step_status(
    exc: Exception,
    status: ResumeProcessingStatus,
) -> str:
    if status is ResumeProcessingStatus.LLM_FAILURE and _is_timeout(exc):
        return ProcessingLogStatus.TIMEOUT
    return _STEP_STATUS_BY_OUTCOME.get(status, ProcessingLogStatus.FAILED)


def _fail_step(
    run_logger: "_RunLogger",
    step: _StepRun,
    resume_input: ResumeInput,
    status: ResumeProcessingStatus,
    message: str,
    exc: Exception,
) -> ResumeProcessingOutcome:
    run_logger.finish_step(
        step,
        _step_status(exc, status),
        ProcessingStepOutput(type=step.record.step_name),
        error=_step_error(exc, status, step.record.step_name, resume_input),
    )
    run_logger.skip_remaining(step.order)
    return _outcome(run_logger, resume_input, status, message)


def _notify(on_stage: StageCallback | None, step_name: str) -> None:
    if on_stage is not None:
        on_stage(step_name)


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
) -> NewResume:
    return NewResume(
        original_file_path=resume_input.original_file_path,
        metadata=metadata,
        parsed_data=parsed_data,
        validation_status=_build_validation_status(),
    )


class _RunLogger:
    def __init__(
        self,
        service: ProcessingLogService,
        resume_input: ResumeInput,
    ) -> None:
        self._service = service
        self._resume_input = resume_input
        self._monitor: RunPerformanceMonitor | None = None
        self._run: ProcessingRunRecord | None = None
        self._records: list[ProcessingStepRecord] = []
        self._recorded_orders: set[int] = set()
        self.active: _StepRun | None = None

    @property
    def run_id(self) -> str:
        if self._run is None:
            raise RuntimeError("Processing run has not been started.")
        return self._run.run_id

    @property
    def _performance_monitor(self) -> RunPerformanceMonitor:
        if self._monitor is None:
            raise RuntimeError("Performance monitor has not been started.")
        return self._monitor

    def start(self) -> None:
        monitor = RunPerformanceMonitor.start()
        self._monitor = monitor
        self._run = self._service.start_run(
            process_name=_PROCESS_NAME,
            process_version=_PROCESS_VERSION,
            started_at=monitor.started_at,
        )

    def start_step(
        self,
        step_name: str,
        order: int,
        input_data: ProcessingStepInput,
    ) -> _StepRun:
        step_id = self._service.new_step_id()
        started_at, _ = self._performance_monitor.begin_step(step_id)
        record = self._service.start_step(
            run_id=self.run_id,
            step_name=step_name,
            step_order=order,
            step_id=step_id,
            input_data=input_data,
            metadata={"file_name": self._resume_input.file_name},
            started_at=started_at,
        )
        step = _StepRun(record=record, order=order)
        self.active = step
        return step

    def finish_step(
        self,
        step: _StepRun,
        status: str,
        output_data: ProcessingStepOutput,
        *,
        error: ProcessingError | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ProcessingStepRecord:
        measurement = self._performance_monitor.end_step(step.record.step_id)
        performance = measurement.performance
        finalized = self._service.finalize_step(
            replace(
                step.record,
                status=status,
                completed_at=performance.completed_at,
                duration_ms=performance.duration_ms,
                output=output_data,
                performance=performance_from_log(performance),
                error=error,
                metadata=(
                    metadata if metadata is not None else step.record.metadata
                ),
            )
        )
        self._records.append(finalized)
        self._recorded_orders.add(step.order)
        if self.active is step:
            self.active = None
        return finalized

    def skip_step(self, step_name: str, order: int, reason: str) -> None:
        if order in self._recorded_orders:
            return
        record = self._service.start_step(
            run_id=self.run_id,
            step_name=step_name,
            step_order=order,
            input_data=ProcessingStepInput(type=step_name),
            metadata={"file_name": self._resume_input.file_name},
            started_at=self._performance_monitor.started_at,
        )
        finalized = self._service.finalize_step(
            replace(
                record,
                status=ProcessingLogStatus.SKIPPED,
                completed_at=self._performance_monitor.started_at,
                duration_ms=0.0,
                output=ProcessingStepOutput(
                    type=step_name,
                    metadata={"reason": reason},
                ),
                performance=ProcessingPerformance(duration_ms=0.0),
                metadata={"reason": reason},
            )
        )
        self._records.append(finalized)
        self._recorded_orders.add(order)

    def skip_remaining(self, after_order: int) -> None:
        for order, step_name in enumerate(_STEP_NAMES, start=1):
            if order <= after_order:
                continue
            self.skip_step(step_name, order, "upstream step did not complete")

    def fail_active(
        self,
        exc: Exception,
        status: str,
        code: str,
    ) -> None:
        if self.active is None:
            self.skip_remaining(0)
            return
        step = self.active
        self.finish_step(
            step,
            status,
            ProcessingStepOutput(type=step.record.step_name),
            error=error_from_exception(
                exc,
                code,
                details={
                    "step_name": step.record.step_name,
                    "file_name": self._resume_input.file_name,
                },
            ),
        )
        self.skip_remaining(step.order)

    def finalize_run(self, outcome: ResumeProcessingOutcome) -> ProcessingRunRecord:
        performance = self._performance_monitor.finish()
        run_error = next(
            (
                record.error
                for record in self._records
                if record.error is not None
            ),
            None,
        )
        finalized = self._service.finalize_run(
            replace(
                self._run,
                status=_RUN_STATUS_BY_OUTCOME[outcome.status],
                result=outcome.status.value,
                resume_id=outcome.resume_id,
                matched_resume_id=outcome.duplicate_resume_id,
                completed_at=performance.completed_at,
                duration_ms=performance.duration_ms,
                summary=_summarize(self._records),
                performance=performance_from_log(performance),
                error=run_error,
            )
        )
        return finalized


class ResumeProcessor:
    def __init__(
        self,
        resume_service: ResumeService,
        llm_service: LLMService,
        processing_log_service: ProcessingLogService,
    ) -> None:
        self._resume_service = resume_service
        self._llm_service = llm_service
        self._processing_logs = processing_log_service

    def process(
        self,
        resume_input: ResumeInput,
        *,
        on_stage: StageCallback | None = None,
    ) -> ResumeProcessingOutcome:
        run_logger = _RunLogger(self._processing_logs, resume_input)
        run_logger.start()
        try:
            outcome = self._process(resume_input, run_logger, on_stage=on_stage)
        except Exception as exc:
            run_logger.fail_active(
                exc,
                ProcessingLogStatus.FAILED,
                "RESUME_PROCESSING_FAILURE",
            )
            outcome = _outcome(
                run_logger,
                resume_input,
                ResumeProcessingStatus.PROCESSING_FAILURE,
                "Resume processing failed.",
            )
        run_logger.finalize_run(outcome)
        return outcome

    def process_many(
        self,
        resume_inputs: Iterable[ResumeInput],
        *,
        on_stage: StageCallback | None = None,
    ) -> list[ResumeProcessingOutcome]:
        return [
            self.process(resume_input, on_stage=on_stage)
            for resume_input in resume_inputs
        ]

    def _process(
        self,
        resume_input: ResumeInput,
        run_logger: _RunLogger,
        *,
        on_stage: StageCallback | None = None,
    ) -> ResumeProcessingOutcome:
        _notify(on_stage, "file_type_validation")
        step = run_logger.start_step(
            "file_type_validation",
            1,
            _file_input(resume_input),
        )
        try:
            verify_pdf_signature(resume_input.content)
        except InvalidFileTypeError as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.INVALID_FILE_TYPE,
                str(exc),
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _validation_output("file_type_validation", valid=True),
        )

        _notify(on_stage, "metadata_extraction")
        step = run_logger.start_step(
            "metadata_extraction",
            2,
            ProcessingStepInput(type="file_content"),
        )
        try:
            metadata = build_resume_metadata(resume_input)
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.PROCESSING_FAILURE,
                "Resume metadata extraction failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _metadata_output(metadata),
        )

        _notify(on_stage, "deduplication")
        step = run_logger.start_step(
            "deduplication",
            3,
            ProcessingStepInput(
                type="resume_metadata",
                hash=metadata.content_fingerprint,
            ),
        )
        try:
            existing_resume = self._resume_service.find_resume_by_content_fingerprint(
                metadata.content_fingerprint
            )
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.STORAGE_FAILURE,
                "Resume duplicate check failed.",
                exc,
            )
        if existing_resume is not None:
            run_logger.finish_step(
                step,
                ProcessingLogStatus.SUCCESS,
                _validation_output(
                    "deduplication",
                    duplicate=True,
                    matched_resume_id=existing_resume.resume_id,
                ),
            )
            run_logger.skip_remaining(step.order)
            return _outcome(
                run_logger,
                resume_input,
                ResumeProcessingStatus.DUPLICATE,
                "Resume content already exists.",
                duplicate_resume_id=existing_resume.resume_id,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _validation_output("deduplication", duplicate=False),
        )

        _notify(on_stage, "pdf_validation")
        step = run_logger.start_step(
            "pdf_validation",
            4,
            ProcessingStepInput(
                type="file_content",
                hash=metadata.content_fingerprint,
            ),
        )
        try:
            validate_pdf(resume_input.content)
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.INVALID_PDF,
                str(exc) if isinstance(exc, InvalidPdfError) else "PDF validation failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _validation_output("pdf_validation", valid=True),
        )

        _notify(on_stage, "content_extraction")
        step = run_logger.start_step(
            "content_extraction",
            5,
            ProcessingStepInput(
                type="file_content",
                hash=metadata.content_fingerprint,
            ),
        )
        try:
            text = extract_pdf_text(resume_input.content)
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.UNREADABLE,
                str(exc)
                if isinstance(exc, UnreadableContentError)
                else "PDF text extraction failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _text_output(text),
        )

        _notify(on_stage, "parsing")
        step = run_logger.start_step(
            "parsing",
            6,
            ProcessingStepInput(
                type="extracted_text",
                size_bytes=len(text.encode("utf-8")),
                hash=_hash_text(text),
                source_step_id=None,
            ),
        )
        try:
            with self._llm_service.processing_step(step.record.step_id):
                model = resolve_parsing_model(self._llm_service)
                payload = parse_resume_text(text, self._llm_service, model)
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.LLM_FAILURE,
                str(exc)
                if isinstance(exc, LlmProcessingError)
                else "Resume parsing failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _payload_output(payload),
        )

        _notify(on_stage, "schema_validation")
        step = run_logger.start_step(
            "schema_validation",
            7,
            _payload_input(payload, step.record.step_id),
        )
        try:
            parsed_data = validate_resume_payload(payload)
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.SCHEMA_INVALID,
                str(exc) if isinstance(exc, ResumeSchemaError) else "Resume schema validation failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _parsed_data_output(parsed_data),
        )

        _notify(on_stage, "storage")
        step = run_logger.start_step(
            "storage",
            8,
            ProcessingStepInput(type="resume_data"),
        )
        try:
            stored_resume = self._resume_service.save_resume(
                _build_new_resume(resume_input, metadata, parsed_data)
            )
        except Exception as exc:
            return _fail_step(
                run_logger,
                step,
                resume_input,
                ResumeProcessingStatus.STORAGE_FAILURE,
                "Resume storage failed.",
                exc,
            )
        run_logger.finish_step(
            step,
            ProcessingLogStatus.SUCCESS,
            _stored_output(stored_resume.resume_id),
        )

        return _outcome(
            run_logger,
            resume_input,
            ResumeProcessingStatus.STORED,
            "Resume stored.",
            resume_id=stored_resume.resume_id,
        )
