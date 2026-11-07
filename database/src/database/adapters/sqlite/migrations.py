from pathlib import Path

from alembic import command
from alembic.config import Config

from .config import SqliteConfig

_ADAPTER_DIR = Path(__file__).resolve().parent
_ALEMBIC_INI = _ADAPTER_DIR / "alembic.ini"
_MIGRATIONS_DIR = _ADAPTER_DIR / "migrations"


def upgrade_database(config: SqliteConfig, revision: str = "head") -> None:
    alembic_config = Config(str(_ALEMBIC_INI))
    alembic_config.set_main_option("script_location", str(_MIGRATIONS_DIR))
    alembic_config.set_main_option(
        "sqlalchemy.url",
        config.database_url.replace("%", "%%"),
    )
    command.upgrade(alembic_config, revision)
