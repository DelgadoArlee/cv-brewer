from rich.console import Console

from cli.modules.logger_context import MAX_LOG_ROWS, LoggerCLIDependencies
from cli.ui.html_reports import generate_html_report
from cli.ui.processing_runs import build_processing_runs_report
from core.services.processing_log import ProcessingRunRecord


def _query_runs(dependencies: LoggerCLIDependencies) -> list[ProcessingRunRecord]:
    return dependencies.processing_log_querier.list_recent_runs(MAX_LOG_ROWS)


def run_processing_runs(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    try:
        records = _query_runs(dependencies)
        report = build_processing_runs_report(records)
        generate_html_report(
            dependencies,
            report,
            log_type="processing-runs",
            console=active_console,
        )
    except Exception as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
