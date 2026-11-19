from rich.console import Console

from cli.commands.application_startup import StartupError
from cli.commands.llm_menu import run_llm_menu
from cli.modules.logger_context import LoggerEnvironment, LoggerSources
from cli.ui.logger_sources import select_log_source


def _select_source(active_console: Console, sources: LoggerSources) -> LoggerEnvironment:
    environments = list(sources)
    if len(environments) == 1:
        return environments[0]
    selection = select_log_source(active_console, environments)
    return environments[selection]


def run_logger_menu(
    sources: LoggerSources,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    environment = _select_source(active_console, sources)
    try:
        dependencies = sources[environment]()
    except StartupError as exc:
        active_console.print(f"[red]Error:[/red] {exc}")
        return
    run_llm_menu(dependencies, console=active_console)
