from rich.console import Console

from cli.modules.logger_context import LoggerCLIDependencies
from cli.ui.llm_logs import render_llm_logs


def run_llm_logs(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    try:
        records = dependencies.llm_log_querier.list_all()
    except Exception as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
        return
    render_llm_logs(active_console, records)
