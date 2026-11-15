from rich.console import Console

from cli.modules.context import CLIDependencies
from cli.ui.delete_resumes import (
    confirm_delete_imported_resumes,
    render_delete_cancelled,
    render_delete_result,
)
from cli.ui.progress import create_progress


def run_delete_imported_resumes(
    dependencies: CLIDependencies,
    *,
    console: Console | None = None,
) -> int:
    active_console = console or Console()

    if not confirm_delete_imported_resumes(active_console):
        render_delete_cancelled(active_console)
        return 0

    with create_progress(active_console) as progress:
        task = progress.add_task("Deleting imported resumes", total=1)
        deleted_count = dependencies.resume_deleter.delete_all_resumes()
        progress.advance(task)

    render_delete_result(active_console, deleted_count)
    return deleted_count
