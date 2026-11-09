from pathlib import Path

from database.adapters.sqlite import SqliteConfig
from database.adapters.sqlite import initialize_database as _initialize_database


def initialize_database(database_path: Path | str) -> None:
    _initialize_database(SqliteConfig.from_path(database_path))


__all__ = ["initialize_database"]
