import typer
from rich.console import Console

from cli.commands.logger_menu import run_logger_menu
from cli.modules.logger_context import LoggerSources


def create_logger_app(sources: LoggerSources) -> typer.Typer:
    app = typer.Typer(add_completion=False, no_args_is_help=False)

    @app.callback(invoke_without_command=True)
    def main(ctx: typer.Context) -> None:
        ctx.obj = sources
        if ctx.invoked_subcommand is None:
            run_logger_menu(sources, console=Console())

    return app
