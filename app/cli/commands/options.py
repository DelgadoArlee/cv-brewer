from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

_OPTIONS_MENU_OPTIONS = ["Imported Resume", "Back"]
OPTIONS_MENU_OPTIONS = _OPTIONS_MENU_OPTIONS
OPTIONS_MENU_CHOICES = _OPTIONS_MENU_OPTIONS
OPTIONS_MENU_ITEMS = _OPTIONS_MENU_OPTIONS
OPTIONS_ITEMS = _OPTIONS_MENU_OPTIONS
OPTION_ITEMS = _OPTIONS_MENU_OPTIONS
OPTIONS_SUBMENU_OPTIONS = _OPTIONS_MENU_OPTIONS
SUBMENU_OPTIONS = _OPTIONS_MENU_OPTIONS
IMPORTED_RESUME_MENU_OPTIONS = _OPTIONS_MENU_OPTIONS


def _resolve_paths_and_processor(
    paths: Any = None,
    resume_processor: Any = None,
    *,
    startup_paths: Any = None,
    input_folder: Any = None,
    processor: Any = None,
    **kwargs: Any,
) -> tuple[Any, Any]:
    if startup_paths is not None:
        paths = startup_paths
    if input_folder is not None:
        paths = input_folder
    if processor is not None:
        resume_processor = processor
    if paths is None and "path" in kwargs:
        paths = kwargs["path"]

    if paths is None or resume_processor is None:
        from cli.app import get_startup_paths, get_resume_processor

        if paths is None:
            paths = get_startup_paths()
        if resume_processor is None:
            resume_processor = get_resume_processor()

    return paths, resume_processor


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
    resume_processor: Any,
    console: Console,
) -> None:
    service = None
    if resume_processor is not None:
        service = getattr(resume_processor, "_resume_service", None)
        if service is None:
            service = getattr(resume_processor, "resume_service", None)
    if service is None:
        try:
            from cli.app import get_resume_processor

            processor = get_resume_processor()
            service = getattr(processor, "_resume_service", None)
            if service is None:
                service = getattr(processor, "resume_service", None)
        except Exception:  # noqa: BLE001
            service = None

    resumes = []
    if service is not None and hasattr(service, "list_resumes"):
        try:
            resumes = list(service.list_resumes())
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
    paths: Any = None,
    resume_processor: Any = None,
    *,
    startup_paths: Any = None,
    input_folder: Any = None,
    processor: Any = None,
    console: Console | None = None,
    **kwargs: Any,
) -> None:
    resolved_paths, resolved_processor = _resolve_paths_and_processor(
        paths,
        resume_processor,
        startup_paths=startup_paths,
        input_folder=input_folder,
        processor=processor,
        **kwargs,
    )
    active_console = console or Console()
    _list_imported_resumes(resolved_processor, active_console)


def run_options_menu(
    paths: Any = None,
    resume_processor: Any = None,
    *,
    startup_paths: Any = None,
    input_folder: Any = None,
    processor: Any = None,
    console: Console | None = None,
    **kwargs: Any,
) -> None:
    resolved_paths, resolved_processor = _resolve_paths_and_processor(
        paths,
        resume_processor,
        startup_paths=startup_paths,
        input_folder=input_folder,
        processor=processor,
        **kwargs,
    )

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
                run_imported_resume(
                    resolved_paths,
                    resolved_processor,
                    console=active_console,
                )
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        else:
            active_console.print("[red]Invalid selection.[/red]")


run_options = run_options_menu
run_options_submenu = run_options_menu
run_submenu = run_options_menu
open_options = run_options_menu
options_menu = run_options_menu

run_imported_resumes = run_imported_resume
view_imported_resumes = run_imported_resume
list_imported_resumes = run_imported_resume
imported_resume = run_imported_resume
imported_resumes = run_imported_resume
run_view_imported_resumes = run_imported_resume
run_list_imported_resumes = run_imported_resume
run_imported_resume_menu = run_imported_resume
