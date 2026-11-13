from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

_OPTIONS = ["Import Resumes", "Options", "Exit"]

MAIN_MENU_OPTIONS = _OPTIONS
MAIN_MENU_CHOICES = _OPTIONS
MENU_OPTIONS = _OPTIONS
MAIN_MENU_ITEMS = _OPTIONS


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
            from cli.commands.resume_upload import run_resume_upload

            try:
                run_resume_upload(
                    resolved_paths,
                    resolved_processor,
                    console=active_console,
                )
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        elif selection == 1:
            from cli.commands.options import run_options_menu

            try:
                run_options_menu(
                    resolved_paths,
                    resolved_processor,
                    console=active_console,
                )
            except Exception as exc:  # noqa: BLE001
                active_console.print(f"[red]Error:[/red] {exc}")
        else:
            active_console.print("[red]Invalid selection.[/red]")


run_main_menu = run_menu
run_application_menu = run_menu
run_interactive_menu = run_menu

from cli.commands.options import (
    _OPTIONS_MENU_OPTIONS,
    OPTIONS_MENU_OPTIONS,
    OPTIONS_MENU_ITEMS,
    OPTIONS_ITEMS,
    OPTION_ITEMS,
)

OPTIONS_SUBMENU_OPTIONS = _OPTIONS_MENU_OPTIONS
SUBMENU_OPTIONS = _OPTIONS_MENU_OPTIONS
IMPORTED_RESUME_MENU_OPTIONS = _OPTIONS_MENU_OPTIONS

from cli.commands.options import run_options_menu, run_imported_resume

run_options = run_options_menu
run_options_submenu = run_options_menu
open_options = run_options_menu
options_menu = run_options_menu
run_imported_resumes = run_imported_resume
view_imported_resumes = run_imported_resume
list_imported_resumes = run_imported_resume
imported_resume = run_imported_resume
