from rich.console import Console
from rich.prompt import Confirm


def confirm_delete_imported_resumes(console: Console) -> bool:
    console.print(
        "[yellow]This clears all imported resumes from the database only.[/yellow]\n"
        "[yellow]Files in the input folder are not deleted.[/yellow]\n"
        "[yellow]Deleted resumes cannot be recovered from the database.[/yellow]"
    )
    return Confirm.ask(
        "Delete all imported resumes?",
        default=False,
        console=console,
    )


def render_delete_cancelled(console: Console) -> None:
    console.print("[yellow]Deletion cancelled.[/yellow]")


def render_delete_result(console: Console, deleted_count: int) -> None:
    if deleted_count == 0:
        console.print("[yellow]No imported resumes were deleted.[/yellow]")
        return
    console.print(
        f"[green]Deleted {deleted_count} imported resume(s) from the database.[/green]"
    )
