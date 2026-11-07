from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database.adapters.sqlite import (
    AdapterIntegrityError,
    SqliteConfig,
    create_session_factory,
    create_sqlite_engine,
    session_scope,
    upgrade_database,
)


def _create_items_table(database_url: str) -> None:
    engine = create_sqlite_engine(SqliteConfig(database_url))
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "CREATE TABLE items ("
                    "id INTEGER PRIMARY KEY, "
                    "name TEXT NOT NULL UNIQUE"
                    ")"
                )
            )
    finally:
        engine.dispose()


def test_engine_connects_to_temporary_database(tmp_path: Path) -> None:
    config = SqliteConfig.from_path(tmp_path / "adapter.db")
    engine = create_sqlite_engine(config)

    try:
        with engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
            assert connection.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
    finally:
        engine.dispose()

    assert (tmp_path / "adapter.db").exists()


def test_session_scope_commits_successful_work(tmp_path: Path) -> None:
    config = SqliteConfig.from_path(tmp_path / "session.db")
    _create_items_table(config.database_url)
    engine = create_sqlite_engine(config)
    factory = create_session_factory(engine)

    try:
        with session_scope(factory) as session:
            session.execute(text("INSERT INTO items (name) VALUES (:name)"), {"name": "alpha"})

        with engine.connect() as connection:
            count = connection.execute(text("SELECT COUNT(*) FROM items")).scalar_one()

        assert count == 1
    finally:
        engine.dispose()


def test_session_scope_rolls_back_on_failure(tmp_path: Path) -> None:
    config = SqliteConfig.from_path(tmp_path / "rollback.db")
    _create_items_table(config.database_url)
    engine = create_sqlite_engine(config)
    factory = create_session_factory(engine)

    try:
        with pytest.raises(RuntimeError):
            with session_scope(factory) as session:
                session.execute(
                    text("INSERT INTO items (name) VALUES (:name)"),
                    {"name": "alpha"},
                )
                raise RuntimeError("failure")

        with engine.connect() as connection:
            count = connection.execute(text("SELECT COUNT(*) FROM items")).scalar_one()

        assert count == 0
    finally:
        engine.dispose()


def test_session_scope_translates_integrity_errors(tmp_path: Path) -> None:
    config = SqliteConfig.from_path(tmp_path / "integrity.db")
    _create_items_table(config.database_url)
    engine = create_sqlite_engine(config)
    factory = create_session_factory(engine)

    try:
        with pytest.raises(AdapterIntegrityError) as error:
            with session_scope(factory) as session:
                session.execute(
                    text("INSERT INTO items (name) VALUES (:name)"),
                    {"name": "alpha"},
                )
                session.execute(
                    text("INSERT INTO items (name) VALUES (:name)"),
                    {"name": "alpha"},
                )

        assert isinstance(error.value.__cause__, IntegrityError)
    finally:
        engine.dispose()


def test_config_rejects_non_sqlite_urls() -> None:
    with pytest.raises(ValueError, match="sqlite"):
        SqliteConfig(database_url="postgresql://localhost/cvbrewer")


def test_upgrade_database_is_callable_without_revisions(tmp_path: Path) -> None:
    upgrade_database(SqliteConfig.from_path(tmp_path / "migrated.db"))
