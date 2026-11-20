from dataclasses import dataclass
from datetime import datetime

from core.services.logger import LogPerformance
from core.services.llm.log_models import LLMLogRecord
from core.services.processing_log import ProcessingPerformance, ProcessingRunRecord


@dataclass(frozen=True, slots=True)
class LogOverviewRecord:
    source: str
    record_id: str
    timestamp: datetime
    status: str
    summary: str
    details: str
    performance: LogPerformance | ProcessingPerformance
    error: str


def _optional_text(value: str | None) -> str:
    return "-" if value is None else value


def _llm_error(record: LLMLogRecord) -> str:
    error_type = record.error.type
    message = record.error.message
    if error_type is None and message is None:
        return "-"
    label = error_type or "Error"
    return f"{label}: {message}" if message else label


def _run_error(record: ProcessingRunRecord) -> str:
    if record.error is None:
        return "-"
    label = record.error.code or record.error.type or "Error"
    message = record.error.message
    return f"{label}: {message}" if message else label


def from_llm_log(record: LLMLogRecord) -> LogOverviewRecord:
    details = (
        f"{record.provider}/{record.model}; "
        f"step={_optional_text(record.processing_step_id)}"
    )
    return LogOverviewRecord(
        source="LLM",
        record_id=record.id,
        timestamp=record.created_at,
        status=record.status,
        summary=record.operation,
        details=details,
        performance=record.performance,
        error=_llm_error(record),
    )


def from_processing_run(record: ProcessingRunRecord) -> LogOverviewRecord:
    summary = record.summary
    details = (
        f"result={_optional_text(record.result)}; "
        f"resume={_optional_text(record.resume_id or record.matched_resume_id)}; "
        f"steps={summary.completed_steps}/{summary.total_steps}"
    )
    return LogOverviewRecord(
        source="Run",
        record_id=record.run_id,
        timestamp=record.started_at,
        status=record.status,
        summary=f"{record.process_name} v{record.process_version}",
        details=details,
        performance=record.performance,
        error=_run_error(record),
    )
