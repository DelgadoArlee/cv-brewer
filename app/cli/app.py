import typer
from rich.console import Console

from cli.modules.context import CLIDependencies


def _run_upload_command(ctx: typer.Context) -> None:
    from cli.commands.resume_upload import ResumeUploadError, run_resume_upload

    dependencies: CLIDependencies = ctx.obj
    console = Console()
    try:
        run_resume_upload(
            dependencies.paths,
            dependencies.resume_processor,
            console=console,
        )
    except ResumeUploadError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def _run_main_menu(ctx: typer.Context) -> None:
    from cli.commands.menu import run_menu

    dependencies: CLIDependencies = ctx.obj
    run_menu(dependencies, console=Console())


def create_app(dependencies: CLIDependencies) -> typer.Typer:
    app = typer.Typer(add_completion=False, no_args_is_help=False)

    @app.callback(invoke_without_command=True)
    def main(ctx: typer.Context) -> None:
        ctx.obj = dependencies
        if ctx.invoked_subcommand is None:
            _run_main_menu(ctx)

    app.command("upload")(_run_upload_command)
    app.command("upload-resumes", hidden=True)(_run_upload_command)
    return app
