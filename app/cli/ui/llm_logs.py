from cli.ui.html_reports import ReportTable
from cli.ui.performance import PERFORMANCE_COLUMNS, performance_values
from core.services.logger import LogStatus
from core.services.llm.log_models import LLMLogRecord

_LABELS = {
    LogStatus.SUCCESS: "Success",
    LogStatus.FAILED: "Failed",
    LogStatus.TIMEOUT: "Timeout",
}


def _token_count(value: int | None) -> str:
    return "-" if value is None else str(value)


def _optional_text(value: str | None) -> str:
    return "-" if value is None else value


def _duration(duration_ms: float | None) -> str:
    return "-" if duration_ms is None else f"{duration_ms / 1000:.3f}"


def _error(record: LLMLogRecord) -> str:
    if record.error.type is None and record.error.message is None:
        return "-"
    error_type = record.error.type or "Error"
    message = record.error.message or ""
    return f"{error_type}: {message}" if message else error_type


def build_llm_logs_report(records: list[LLMLogRecord]) -> ReportTable:
    columns = (
        "ID",
        "Created",
        "Status",
        "Step ID",
        "Provider",
        "Model",
        "Done Reason",
        "Input Tokens",
        "Output Tokens",
        "Total Tokens",
        "Duration (s)",
        *PERFORMANCE_COLUMNS,
        "Error",
    )
    rows = tuple(
        (
            record.id,
            record.created_at.isoformat(sep=" "),
            _LABELS.get(record.status, "Unknown"),
            _optional_text(record.processing_step_id),
            record.provider,
            record.model,
            _optional_text(record.response.finish_reason),
            _token_count(record.usage.input_tokens),
            _token_count(record.usage.output_tokens),
            _token_count(record.usage.total_tokens),
            _duration(record.performance.duration_ms),
            *performance_values(record.performance),
            _error(record),
        )
        for record in records
    )
    return ReportTable("LLM Activity Logs", columns, rows)
