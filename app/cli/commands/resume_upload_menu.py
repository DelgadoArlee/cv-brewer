from rich.console import Console

from cli.commands.processing_runs import run_processing_runs
from cli.commands.processing_steps import run_processing_steps
from cli.modules.logger_context import LoggerCLIDependencies
from cli.ui.logger_menus import render_logger_menu
from cli.ui.selection import select_option

_OPTIONS = ["view runs", "view steps"]


def run_resume_upload_menu(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    render_logger_menu(active_console, "Resume Upload Logs")
    selection = select_option(active_console, _OPTIONS, default_index=0)
    if selection == 0:
        run_processing_runs(dependencies, console=active_console)
        return
    run_processing_steps(dependencies, console=active_console)
