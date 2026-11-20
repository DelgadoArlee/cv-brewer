from rich.console import Console

from cli.commands.all_logs import run_all_logs
from cli.commands.error_logs import run_error_logs
from cli.commands.llm_logs import run_llm_logs
from cli.commands.resume_upload_menu import run_resume_upload_menu
from cli.modules.logger_context import LoggerCLIDependencies
from cli.ui.logger_menus import render_logger_menu
from cli.ui.selection import select_option

_OPTIONS = ["llm", "resume-upload", "error", "all"]


def run_llm_menu(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    render_logger_menu(active_console, "CVBrewer Logs")
    selection = select_option(active_console, _OPTIONS, default_index=0)
    if selection == 0:
        run_llm_logs(dependencies, console=active_console)
    elif selection == 1:
        run_resume_upload_menu(dependencies, console=active_console)
    elif selection == 2:
        run_error_logs(dependencies, console=active_console)
    elif selection == 3:
        run_all_logs(dependencies, console=active_console)
