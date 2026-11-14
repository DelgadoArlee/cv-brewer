from pathlib import Path

from database.adapters.sqlite import (
    SqliteConfig,
    SqliteResumeRepository,
    create_session_factory,
    create_sqlite_engine,
)
from database.adapters.sqlite import initialize_database as _initialize_database
from core.services.resume import ResumeService


def initialize_database(database_path: Path | str) -> None:
    _initialize_database(SqliteConfig.from_path(database_path))


def create_resume_service(
    database_path: Path | str,
    *,
    echo: bool = False,
) -> ResumeService:
    config = SqliteConfig.from_path(database_path, echo=echo)
    engine = create_sqlite_engine(config)
    session_factory = create_session_factory(engine)
    return ResumeService(SqliteResumeRepository(session_factory))


__all__ = ["create_resume_service", "initialize_database"]
