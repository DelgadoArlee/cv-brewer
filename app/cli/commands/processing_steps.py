from rich.console import Console

from cli.modules.logger_context import MAX_LOG_ROWS, LoggerCLIDependencies
from cli.ui.html_reports import generate_html_report
from cli.ui.processing_steps import build_processing_steps_report
from cli.ui.selection import select_option
from core.services.processing_log import ProcessingRunRecord, ProcessingStepRecord


def _run_option(record: ProcessingRunRecord) -> str:
    timestamp = record.started_at.isoformat(sep=" ", timespec="seconds")
    return f"{record.run_id} - {timestamp}"


def _query_runs(dependencies: LoggerCLIDependencies) -> list[ProcessingRunRecord]:
    return dependencies.processing_log_querier.list_recent_runs(MAX_LOG_ROWS)


def _query_steps(
    dependencies: LoggerCLIDependencies,
    run_id: str,
) -> list[ProcessingStepRecord]:
    return dependencies.processing_log_querier.list_steps(run_id, limit=MAX_LOG_ROWS)


def run_processing_steps(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    try:
        runs = _query_runs(dependencies)
        if not runs:
            active_console.print("[yellow]No processing runs found.[/yellow]")
            report = build_processing_steps_report("none", [])
            generate_html_report(
                dependencies,
                report,
                log_type="processing-steps",
                console=active_console,
            )
            return
        selection = select_option(
            active_console,
            [_run_option(run) for run in runs],
            default_index=0,
        )
        selected_run = runs[selection]
        steps = _query_steps(dependencies, selected_run.run_id)
        report = build_processing_steps_report(selected_run.run_id, steps)
        generate_html_report(
            dependencies,
            report,
            log_type=f"processing-steps-{selected_run.run_id}",
            console=active_console,
        )
    except Exception as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
