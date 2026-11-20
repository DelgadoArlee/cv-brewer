from rich.console import Console

from cli.modules.logger_context import MAX_LOG_ROWS, LoggerCLIDependencies
from cli.ui.html_reports import generate_html_report
from cli.ui.llm_logs import build_llm_logs_report


def run_llm_logs(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    try:
        records = dependencies.llm_log_querier.list_recent(MAX_LOG_ROWS)
        report = build_llm_logs_report(records)
        generate_html_report(
            dependencies,
            report,
            log_type="llm",
            console=active_console,
        )
    except Exception as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
