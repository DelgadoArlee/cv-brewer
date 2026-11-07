from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.engine import make_url


@dataclass(frozen=True, slots=True)
class SqliteConfig:
    database_url: str
    echo: bool = False

    def __post_init__(self) -> None:
        if not self.database_url:
            raise ValueError("database_url must not be empty")

        url = make_url(self.database_url)
        if url.get_backend_name() != "sqlite":
            raise ValueError("database_url must use the sqlite dialect")

    @classmethod
    def from_path(cls, path: Path | str, *, echo: bool = False) -> "SqliteConfig":
        value = str(path)
        if value == ":memory:":
            return cls(database_url="sqlite+pysqlite:///:memory:", echo=echo)

        resolved = Path(path).expanduser().resolve()
        return cls(database_url=f"sqlite+pysqlite:///{resolved.as_posix()}", echo=echo)
