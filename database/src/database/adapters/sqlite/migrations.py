from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url

from database.adapters.sqlite.config import SqliteConfig
from database.adapters.sqlite.engine import create_sqlite_engine

_ADAPTER_DIR = Path(__file__).resolve().parent
_ALEMBIC_INI = _ADAPTER_DIR / "alembic.ini"
_MIGRATIONS_DIR = _ADAPTER_DIR / "migrations"


def initialize_database(config: SqliteConfig) -> None:
    database_path = make_url(config.database_url).database
    if database_path and database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    engine = create_sqlite_engine(config)
    try:
        with engine.connect():
            pass
    finally:
        engine.dispose()

    upgrade_database(config)


def upgrade_database(config: SqliteConfig, revision: str = "head") -> None:
    alembic_config = Config(str(_ALEMBIC_INI))
    alembic_config.set_main_option("script_location", str(_MIGRATIONS_DIR))
    alembic_config.set_main_option(
        "sqlalchemy.url",
        config.database_url.replace("%", "%%"),
    )
    command.upgrade(alembic_config, revision)
