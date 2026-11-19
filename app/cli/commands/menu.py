from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cli.commands.options import run_options_menu
from cli.commands.resume_upload import run_resume_upload
from cli.modules.context import CLIDependencies
from cli.ui.selection import select_option

_OPTIONS = ["Import Resumes", "Options", "Exit"]


def _select_option(active_console: Console) -> int:
    return select_option(active_console, _OPTIONS)


def run_menu(
    dependencies: CLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()

    while True:
        active_console.print(
            Panel(
                Text("CVBrewer", style="bold", justify="center"),
                width=active_console.width,
                padding=(2, 4),
                border_style="#D9A441",
                expand=True,
            )
        )
        selection = _select_option(active_console)

        if selection == len(_OPTIONS) - 1:
            active_console.print("[dim]Exiting CVBrewer.[/dim]")
            return
        if selection == 0:
            try:
                run_resume_upload(
                    dependencies.paths,
                    dependencies.resume_processor,
                    console=active_console,
                )
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        elif selection == 1:
            try:
                run_options_menu(dependencies, console=active_console)
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        else:
            active_console.print("[red]Invalid selection.[/red]")
