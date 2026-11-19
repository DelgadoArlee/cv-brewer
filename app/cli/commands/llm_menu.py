from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cli.commands.llm_logs import run_llm_logs
from cli.modules.logger_context import LoggerCLIDependencies
from cli.ui.selection import select_option

_OPTIONS = ["llm"]


def run_llm_menu(
    dependencies: LoggerCLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    active_console.print(
        Panel(
            Text("CVBrewer Logs", style="bold", justify="center"),
            width=active_console.width,
            padding=(2, 4),
            border_style="#D9A441",
            expand=True,
        )
    )
    select_option(active_console, _OPTIONS)
    run_llm_logs(dependencies, console=active_console)
