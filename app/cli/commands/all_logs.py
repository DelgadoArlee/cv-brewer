from rich.console import Console

from cli.modules.logger_context import MAX_LOG_ROWS, LoggerCLIDependencies
from cli.modules.logger_records import (
    LogOverviewRecord,
    from_llm_log,
    from_processing_run,
)
from cli.ui.html_reports import generate_html_report
from cli.ui.log_overview import build_log_overview_report


def _query_records(dependencies: LoggerCLIDependencies) -> list[LogOverviewRecord]:
    llm_logs = dependencies.llm_log_querier.list_recent(MAX_LOG_ROWS)
    runs = dependencies.processing_log_querier.list_recent_runs(MAX_LOG_ROWS)
    records = [from_llm_log(record) for record in llm_logs]
    records.extend(from_processing_run(record) for record in runs)
    records.sort(key=lambda record: record.timestamp, reverse=True)
    return records[:MAX_LOG_ROWS]


def run_all_logs(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    try:
        records = _query_records(dependencies)
        report = build_log_overview_report(records, "All Logs")
        generate_html_report(
            dependencies,
            report,
            log_type="all",
            console=active_console,
        )
    except Exception as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
