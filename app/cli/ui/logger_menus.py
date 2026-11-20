from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def render_logger_menu(console: Console, title: str) -> None:
    console.print(
        Panel(
            Text(title, style="bold", justify="center"),
            width=console.width,
            padding=(2, 4),
            border_style="#D9A441",
            expand=True,
        )
    )
