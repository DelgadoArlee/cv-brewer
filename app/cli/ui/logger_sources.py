from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cli.ui.selection import select_option


def select_log_source(active_console: Console, options: list[str]) -> int:
    active_console.print(
        Panel(
            Text("Log Database", style="bold", justify="center"),
            width=active_console.width,
            padding=(2, 4),
            border_style="#D9A441",
            expand=True,
        )
    )
    return select_option(active_console, options, default_index=0)
