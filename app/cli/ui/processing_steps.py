from cli.ui.html_reports import ReportTable
from cli.ui.performance import PERFORMANCE_COLUMNS, performance_values
from core.services.processing_log import ProcessingLogStatus, ProcessingStepRecord

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


def _duration(duration_ms: float | None) -> str:
    return "-" if duration_ms is None else f"{duration_ms / 1000:.3f}"


def _error(record: ProcessingStepRecord) -> str:
    if record.error is None:
        return "-"
    label = record.error.code or record.error.type or "Error"
    message = record.error.message
    return f"{label}: {message}" if message else label


def build_processing_steps_report(
    run_id: str,
    records: list[ProcessingStepRecord],
) -> ReportTable:
    columns = (
        "ID",
        "Step",
        "Order",
        "Attempt",
        "Started",
        "Status",
        "Duration (s)",
        *PERFORMANCE_COLUMNS,
        "Error",
        "Metadata",
    )
    rows = tuple(
        (
            record.step_id,
            record.step_name,
            str(record.step_order),
            str(record.attempt_number),
            record.started_at.isoformat(sep=" "),
            _STATUS_LABELS.get(record.status, "Unknown"),
            _duration(record.duration_ms),
            *performance_values(record.performance),
            _error(record),
            str(record.metadata) if record.metadata else "-",
        )
        for record in records
    )
    return ReportTable(f"Processing Steps - {run_id}", columns, rows)
