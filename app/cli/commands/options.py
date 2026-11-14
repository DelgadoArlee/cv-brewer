from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from cli.modules.context import CLIDependencies, ResumeLister

_OPTIONS_MENU_OPTIONS = ["Imported Resume", "Back"]


def _questionary_select(options: list[str]) -> int:
    import questionary
    from prompt_toolkit.styles import Style

    answer = questionary.select(
        "",
        choices=options,
        default=options[-1] if options else None,
        pointer="»",
        use_indicator=False,
        qmark="",
        instruction=" ",
        style=Style([("selected", "noreverse"), ("highlighted", "noreverse"), ("pointer", "fg:#D9A441")]),
    ).ask()
    for index, option in enumerate(options):
        if answer == option:
            return index
    return len(options) - 1


def _text_select(active_console: Console, options: list[str]) -> int:
    for index, option in enumerate(options, start=1):
        active_console.print(f"  {index}. {option}")
    choice = Prompt.ask(
        "",
        choices=[str(index) for index in range(1, len(options) + 1)],
        default=str(len(options)),
        console=active_console,
    )
    try:
        return int(choice) - 1
    except (TypeError, ValueError):
        return len(options) - 1


def _select_option(active_console: Console, options: list[str]) -> int:
    import sys

    if sys.stdin.isatty() and sys.stdout.isatty():
        try:
            return _questionary_select(options)
        except Exception:  # noqa: BLE001
            pass
    return _text_select(active_console, options)


def _list_imported_resumes(
    resume_lister: ResumeLister,
    console: Console,
) -> None:
    try:
        resumes = list(resume_lister.list_resumes())
    except Exception:  # noqa: BLE001
        resumes = []

    if not resumes:
        console.print("[yellow]No imported resumes found.[/yellow]")
        return

    table = Table(title="Imported Resumes", min_width=20)
    table.add_column("File", style="bold")

    for resume in resumes:
        file_name = getattr(getattr(resume, "metadata", None), "file_name", "")
        if not file_name:
            file_name = getattr(resume, "original_file_path", "")
        table.add_row(str(file_name))

    console.print(table)


def run_imported_resume(
    dependencies: CLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()
    _list_imported_resumes(dependencies.resume_lister, active_console)


def run_options_menu(
    dependencies: CLIDependencies,
    *,
    console: Console | None = None,
) -> None:
    active_console = console or Console()

    while True:
        active_console.print(
            Panel(
                Text("Options", style="bold", justify="center"),
                width=active_console.width,
                padding=(2, 4),
                border_style="#D9A441",
                expand=True,
            )
        )
        selection = _select_option(active_console, _OPTIONS_MENU_OPTIONS)

        if selection == 1:
            return
        if selection == 0:
            try:
                run_imported_resume(dependencies, console=active_console)
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        else:
            active_console.print("[red]Invalid selection.[/red]")
