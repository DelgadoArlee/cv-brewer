from dataclasses import dataclass
from pathlib import Path

_CLI_ROOT = Path(__file__).resolve().parents[1]
_DEVELOPMENT_DATA_DIR = _CLI_ROOT / "data"


@dataclass(frozen=True, slots=True)
class StartupPaths:
    database: Path
    resumes: Path
    generated: Path


def startup_paths(data_dir: Path) -> StartupPaths:
    return StartupPaths(
        database=data_dir / "cvbrewer.db",
        resumes=data_dir / "local" / "resumes",
        generated=data_dir / "local" / "generated",
    )


def development_startup_paths() -> StartupPaths:
    return startup_paths(_DEVELOPMENT_DATA_DIR)
