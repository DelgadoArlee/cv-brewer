from cli.modules.logger_records import LogOverviewRecord
from cli.ui.html_reports import ReportTable
from cli.ui.performance import PERFORMANCE_COLUMNS, performance_values
from core.services.logger import LogStatus
from core.services.processing_log import ProcessingLogStatus

_STATUS_LABELS = {
    LogStatus.RUNNING: "Running",
    LogStatus.SUCCESS: "Success",
    LogStatus.FAILED: "Failed",
    LogStatus.VALIDATION_FAILED: "Validation Failed",
    LogStatus.PARTIAL_SUCCESS: "Partial Success",
    LogStatus.SKIPPED: "Skipped",
    LogStatus.CANCELLED: "Cancelled",
    LogStatus.TIMEOUT: "Timeout",
    ProcessingLogStatus.RUNNING: "Running",
    ProcessingLogStatus.SUCCESS: "Success",
    ProcessingLogStatus.FAILED: "Failed",
    ProcessingLogStatus.VALIDATION_FAILED: "Validation Failed",
    ProcessingLogStatus.PARTIAL_SUCCESS: "Partial Success",
    ProcessingLogStatus.SKIPPED: "Skipped",
    ProcessingLogStatus.CANCELLED: "Cancelled",
    ProcessingLogStatus.TIMEOUT: "Timeout",
}


def build_log_overview_report(
    records: list[LogOverviewRecord],
    title: str = "Log Records",
) -> ReportTable:
    columns = (
        "Source",
        "ID",
        "Timestamp",
        "Status",
        "Summary",
        "Details",
        *PERFORMANCE_COLUMNS,
        "Error",
    )
    rows = tuple(
        (
            record.source,
            record.record_id,
            record.timestamp.isoformat(sep=" "),
            _STATUS_LABELS.get(record.status, "Unknown"),
            record.summary,
            record.details,
            *performance_values(record.performance),
            record.error,
        )
        for record in records
    )
    return ReportTable(title, columns, rows)
