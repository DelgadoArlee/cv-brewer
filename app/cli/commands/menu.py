from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

from cli.commands.options import run_options_menu
from cli.commands.resume_upload import run_resume_upload
from cli.modules.context import CLIDependencies

_OPTIONS = ["Import Resumes", "Options", "Exit"]


def _questionary_select() -> int:
    import questionary
    from prompt_toolkit.styles import Style

    answer = questionary.select(
        "",
        choices=_OPTIONS,
        default=_OPTIONS[-1],
        pointer="»",
        use_indicator=False,
        qmark="",
        instruction=" ",
        style=Style([("selected", "noreverse"), ("highlighted", "noreverse"), ("pointer", "fg:#D9A441")]),
    ).ask()
    for index, option in enumerate(_OPTIONS):
        if answer == option:
            return index
    return len(_OPTIONS) - 1


def _text_select(active_console: Console) -> int:
    for index, option in enumerate(_OPTIONS, start=1):
        active_console.print(f"  {index}. {option}")
    choice = Prompt.ask(
        "",
        choices=[str(index) for index in range(1, len(_OPTIONS) + 1)],
        default=str(len(_OPTIONS)),
        console=active_console,
    )
    try:
        return int(choice) - 1
    except (TypeError, ValueError):
        return len(_OPTIONS) - 1


def _select_option(active_console: Console) -> int:
    import sys

    if sys.stdin.isatty() and sys.stdout.isatty():
        try:
            return _questionary_select()
        except Exception:  # noqa: BLE001
            pass
    return _text_select(active_console)


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
