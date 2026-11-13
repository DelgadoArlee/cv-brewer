from collections.abc import Callable
from pathlib import Path

from cli.modules.paths import StartupPaths

DatabaseInitializer = Callable[[Path], None]


class StartupError(Exception):
    pass



def _ensure_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise StartupError(f"Failed to create the directory at {path}") from exc

    if not path.is_dir():
        raise StartupError(f"Expected a directory at {path}")


def initialize_application(
    paths: StartupPaths,
    database_initializer: DatabaseInitializer,
) -> StartupPaths:
    try:
        database_initializer(paths.database)
    except Exception as exc:
        raise StartupError(
            f"Failed to initialize the database at {paths.database}"
        ) from exc

    _ensure_directory(paths.resumes)
    _ensure_directory(paths.generated)

    return paths



