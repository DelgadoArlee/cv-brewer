from cli.ui.html_reports import ReportTable
from cli.ui.performance import PERFORMANCE_COLUMNS, performance_values
from core.services.processing_log import ProcessingLogStatus, ProcessingRunRecord

_STATUS_LABELS = {
    ProcessingLogStatus.RUNNING: "Running",
    ProcessingLogStatus.SUCCESS: "Success",
    ProcessingLogStatus.FAILED: "Failed",
    ProcessingLogStatus.VALIDATION_FAILED: "Validation Failed",
    ProcessingLogStatus.PARTIAL_SUCCESS: "Partial Success",
    ProcessingLogStatus.SKIPPED: "Skipped",
    ProcessingLogStatus.CANCELLED: "Cancelled",
    ProcessingLogStatus.TIMEOUT: "Timeout",
}


def _optional_text(value: str | None) -> str:
    return "-" if value is None else value


def _duration(duration_ms: float | None) -> str:
    return "-" if duration_ms is None else f"{duration_ms / 1000:.3f}"


def _error(record: ProcessingRunRecord) -> str:
    if record.error is None:
        return "-"
    label = record.error.code or record.error.type or "Error"
    message = record.error.message
    return f"{label}: {message}" if message else label


def _steps(record: ProcessingRunRecord) -> str:
    summary = record.summary
    return (
        f"{summary.completed_steps}/{summary.total_steps} "
        f"({summary.failed_steps} failed, {summary.skipped_steps} skipped)"
    )


def build_processing_runs_report(records: list[ProcessingRunRecord]) -> ReportTable:
    columns = (
        "ID",
        "Started",
        "Status",
        "Result",
        "Resume ID",
        "Matched Resume ID",
        "Steps",
        "Duration (s)",
        *PERFORMANCE_COLUMNS,
        "Error",
    )
    rows = tuple(
        (
            record.run_id,
            record.started_at.isoformat(sep=" "),
            _STATUS_LABELS.get(record.status, "Unknown"),
            _optional_text(record.result),
            _optional_text(record.resume_id),
            _optional_text(record.matched_resume_id),
            _steps(record),
            _duration(record.duration_ms),
            *performance_values(record.performance),
            _error(record),
        )
        for record in records
    )
    return ReportTable("Processing Runs", columns, rows)
