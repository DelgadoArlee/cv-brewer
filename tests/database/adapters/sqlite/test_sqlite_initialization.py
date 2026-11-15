from pathlib import Path

from database import initialize_database as initialize_database_from_path
from database.adapters.sqlite import (
    SqliteConfig,
    initialize_database as initialize_sqlite_database,
)


def test_initialize_database_creates_parent_directory_and_file(tmp_path: Path) -> None:
    database_path = tmp_path / "nested" / "adapter.db"
    config = SqliteConfig.from_path(database_path)

    initialize_sqlite_database(config)

    assert database_path.parent.is_dir()
    assert database_path.is_file()


def test_initialize_database_is_idempotent(tmp_path: Path) -> None:
    database_path = tmp_path / "nested" / "adapter.db"
    config = SqliteConfig.from_path(database_path)

    initialize_sqlite_database(config)
    initialize_sqlite_database(config)

    assert database_path.is_file()


def test_initialize_database_from_path_uses_explicit_path(tmp_path: Path) -> None:
    database_path = tmp_path / "explicit" / "custom.db"

    initialize_database_from_path(database_path)

    assert database_path.is_file()
