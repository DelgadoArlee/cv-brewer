import sys

from rich.console import Console
from rich.prompt import Prompt


def _questionary_select(options: list[str], default_index: int) -> int:
    import questionary
    from prompt_toolkit.styles import Style

    answer = questionary.select(
        "",
        choices=options,
        default=options[default_index] if options else None,
        pointer="»",
        use_indicator=False,
        qmark="",
        instruction=" ",
        style=Style(
            [
                ("selected", "noreverse"),
                ("highlighted", "noreverse"),
                ("pointer", "fg:#D9A441"),
            ]
        ),
    ).ask()
    for index, option in enumerate(options):
        if answer == option:
            return index
    return default_index


def _text_select(active_console: Console, options: list[str], default_index: int) -> int:
    for index, option in enumerate(options, start=1):
        active_console.print(f"  {index}. {option}")
    choice = Prompt.ask(
        "",
        choices=[str(index) for index in range(1, len(options) + 1)],
        default=str(default_index + 1),
        console=active_console,
    )
    try:
        return int(choice) - 1
    except (TypeError, ValueError):
        return default_index


def select_option(
    active_console: Console,
    options: list[str],
    *,
    default_index: int | None = None,
) -> int:
    fallback = len(options) - 1 if default_index is None else default_index
    if sys.stdin.isatty() and sys.stdout.isatty():
        try:
            return _questionary_select(options, fallback)
        except Exception:
            pass
    return _text_select(active_console, options, fallback)
