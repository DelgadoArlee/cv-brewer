import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.services.logger.models import LogPerformance, utc_now


class ProcessingLogStatus:
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    SKIPPED = "SKIPPED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True, slots=True)
class ProcessingSummary:
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    skipped_steps: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "failed_steps": self.failed_steps,
            "skipped_steps": self.skipped_steps,
        }


@dataclass(frozen=True, slots=True)
class ProcessingPerformance:
    duration_ms: float | None = None
    start_memory_mb: float | None = None
    peak_memory_mb: float | None = None
    end_memory_mb: float | None = None
    memory_delta_mb: float | None = None
    cpu_avg_percent: float | None = None
    cpu_peak_percent: float | None = None
    sample_count: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "duration_ms": self.duration_ms,
            "start_memory_mb": self.start_memory_mb,
            "peak_memory_mb": self.peak_memory_mb,
            "end_memory_mb": self.end_memory_mb,
            "memory_delta_mb": self.memory_delta_mb,
            "cpu_avg_percent": self.cpu_avg_percent,
            "cpu_peak_percent": self.cpu_peak_percent,
            "sample_count": self.sample_count,
        }


def performance_from_log(performance: LogPerformance | None) -> ProcessingPerformance:
    if performance is None:
        return ProcessingPerformance()
    return ProcessingPerformance(
        duration_ms=performance.duration_ms,
        start_memory_mb=performance.start_memory_mb,
        peak_memory_mb=performance.peak_memory_mb,
        end_memory_mb=performance.end_memory_mb,
        memory_delta_mb=performance.memory_delta_mb,
        cpu_avg_percent=performance.cpu_avg_percent,
        cpu_peak_percent=performance.cpu_peak_percent,
        sample_count=performance.sample_count,
    )


@dataclass(frozen=True, slots=True)
class ProcessingError:
    code: str
    type: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "type": self.type,
            "message": self.message,
            "details": self.details,
            "raw": self.raw,
            "occurred_at": self.occurred_at.isoformat(),
        }


def error_from_exception(
    exc: Exception,
    code: str,
    *,
    error_type: str | None = None,
    details: dict[str, Any] | None = None,
    occurred_at: datetime | None = None,
) -> ProcessingError:
    raw: dict[str, Any] = {
        "exception_class": exc.__class__.__name__,
        "exception_message": str(exc),
        "exception_args": [repr(arg) for arg in exc.args],
        "traceback": "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        ),
        "cause": (
            {
                "exception_class": exc.__cause__.__class__.__name__,
                "exception_message": str(exc.__cause__),
            }
            if exc.__cause__ is not None
            else None
        ),
        "context": (
            {
                "exception_class": exc.__context__.__class__.__name__,
                "exception_message": str(exc.__context__),
            }
            if exc.__context__ is not None and not exc.__suppress_context__
            else None
        ),
    }
    return ProcessingError(
        code=code,
        type=error_type or exc.__class__.__name__,
        message=str(exc) or exc.__class__.__name__,
        details=details or {},
        raw=raw,
        occurred_at=occurred_at or utc_now(),
    )


@dataclass(frozen=True, slots=True)
class ProcessingStepInput:
    type: str
    source_step_id: str | None = None
    size_bytes: int | None = None
    hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    snapshot: Any = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "source_step_id": self.source_step_id,
            "size_bytes": self.size_bytes,
            "hash": self.hash,
            "metadata": self.metadata,
            "snapshot": self.snapshot,
        }


@dataclass(frozen=True, slots=True)
class ProcessingStepOutput:
    type: str
    size_bytes: int | None = None
    hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    snapshot: Any = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "size_bytes": self.size_bytes,
            "hash": self.hash,
            "metadata": self.metadata,
            "snapshot": self.snapshot,
        }


@dataclass(frozen=True, slots=True)
class ProcessingRunRecord:
    run_id: str
    process_name: str
    process_version: str
    status: str
    result: str | None
    resume_id: str | None
    matched_resume_id: str | None
    started_at: datetime
    completed_at: datetime | None
    duration_ms: float | None
    summary: ProcessingSummary
    performance: ProcessingPerformance
    error: ProcessingError | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "process_name": self.process_name,
            "process_version": self.process_version,
            "status": self.status,
            "result": self.result,
            "resume_id": self.resume_id,
            "matched_resume_id": self.matched_resume_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at is not None else None
            ),
            "duration_ms": self.duration_ms,
            "summary": self.summary.as_dict(),
            "performance": self.performance.as_dict(),
            "error": self.error.as_dict() if self.error is not None else None,
        }


@dataclass(frozen=True, slots=True)
class ProcessingStepRecord:
    step_id: str
    run_id: str
    step_name: str
    step_order: int
    attempt_number: int
    status: str
    started_at: datetime
    completed_at: datetime | None
    duration_ms: float | None
    input: ProcessingStepInput
    output: ProcessingStepOutput
    performance: ProcessingPerformance
    error: ProcessingError | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "run_id": self.run_id,
            "step_name": self.step_name,
            "step_order": self.step_order,
            "attempt_number": self.attempt_number,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at is not None else None
            ),
            "duration_ms": self.duration_ms,
            "input": self.input.as_dict(),
            "output": self.output.as_dict(),
            "performance": self.performance.as_dict(),
            "error": self.error.as_dict() if self.error is not None else None,
            "metadata": self.metadata,
        }
