from rich.console import Console

from cli.ui.entry_page import render_entry_page, wait_for_enter


def run_entry_page(console: Console | None = None) -> None:
    active_console = console or Console()
    render_entry_page(active_console)
    wait_for_enter(active_console)
