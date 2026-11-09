import typer

from cli.processes.entry_page import run_entry_page

app = typer.Typer(add_completion=False, no_args_is_help=False)


@app.callback(invoke_without_command=True)
def main() -> None:
    run_entry_page()
