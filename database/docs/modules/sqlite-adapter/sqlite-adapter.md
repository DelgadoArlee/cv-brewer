# SQLite Adapter Module Technical Specification

## 1. Purpose

Provides the SQLite-specific implementation foundation for the database component. The module owns SQLite configuration, synchronous SQLAlchemy engine and session lifecycle, adapter-level error translation, and Alembic migration infrastructure. Application-level data operations remain outside this module. Resume ORM models and persistence repositories are implemented in dedicated SQLite adapter modules.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `SqliteConfig` | Dataclass | Holds the SQLite connection URL and SQLAlchemy echo setting. | `database_url: str` – SQLite SQLAlchemy URL. `echo: bool = False` – Enables SQL statement logging. | `SqliteConfig` instance. |
| `SqliteConfig.from_path()` | Class method | Builds a SQLite configuration from a file-system path or `:memory:`. | `path: Path \| str` – Database file path or in-memory marker. `echo: bool = False` – Enables SQL statement logging. | `SqliteConfig` instance with a `sqlite+pysqlite` URL. |
| `create_sqlite_engine()` | Function | Creates a synchronous SQLAlchemy engine and enables SQLite foreign-key enforcement on new connections. | `config: SqliteConfig` – SQLite configuration. | `sqlalchemy.Engine`. |
| `create_session_factory()` | Function | Creates a session factory bound to the supplied engine. | `engine: sqlalchemy.Engine` – Configured SQLite engine. | `sessionmaker[Session]`. |
| `session_scope()` | Context manager | Provides a transactional session boundary that commits on success, rolls back on failure, closes the session, and translates SQLAlchemy errors. | `factory: sessionmaker[Session]` – Session factory. | `Iterator[Session]` yielding an active session. |
| `AdapterError` | Exception class | Base class for database adapter failures. | `message: str` – Error description. | `AdapterError` instance. |
| `AdapterIntegrityError` | Exception class | Represents integrity constraint failures. | `message: str` – Error description. | `AdapterIntegrityError` instance. |
| `AdapterOperationalError` | Exception class | Represents operational database failures. | `message: str` – Error description. | `AdapterOperationalError` instance. |
| `AdapterDataError` | Exception class | Represents invalid data failures. | `message: str` – Error description. | `AdapterDataError` instance. |
| `AdapterProgrammingError` | Exception class | Represents programming or statement failures. | `message: str` – Error description. | `AdapterProgrammingError` instance. |
| `AdapterDatabaseError` | Exception class | Represents other DB-API failures. | `message: str` – Error description. | `AdapterDatabaseError` instance. |
| `to_adapter_error()` | Function | Maps SQLAlchemy exceptions to the adapter-local exception hierarchy. | `exc: sqlalchemy.exc.SQLAlchemyError` – SQLAlchemy exception. | `AdapterError` subclass instance. |
| `upgrade_database()` | Function | Runs Alembic migrations for the supplied SQLite configuration. | `config: SqliteConfig` – SQLite configuration. `revision: str = "head"` – Target Alembic revision. | `None`. |
| `initialize_database()` | Function | Prepares an explicit SQLite database path, creates the database file, and runs Alembic migrations. | `config: SqliteConfig` – SQLite configuration. | `None`. |
| Alembic scaffolding | Configuration and templates | Defines `alembic.ini`, the migration environment, and revision template inside the adapter package. | None. | Migration environment and revision template. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `sqlalchemy` | External library | Provides the SQLite engine, connection pooling, sessions, transactions, and exception types. |
| `alembic` | External library | Provides migration configuration, environment, and revision execution. |
| `sqlite3` | Python standard library | Provides the embedded SQLite driver used by the SQLAlchemy SQLite dialect. |

## 4. Architecture Decision Log (ADL)

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/06/2026 | Established the SQLite adapter foundation with synchronous SQLAlchemy, explicit URL configuration, adapter-local errors, and self-contained Alembic scaffolding. | `SqliteConfig`, `create_sqlite_engine()`, `create_session_factory()`, `session_scope()`, `to_adapter_error()`, `upgrade_database()`, Alembic scaffolding | [SQLite adapter foundation](../../adr/11-06-26/sqlite-adapter-foundation.md) |
| 11/07/2026 | Added explicit-path database initialization for application startup while preserving explicit SQLite configuration. | `initialize_database()` | [Development application startup](../../../../cli/docs/adr/11-07-26/development-startup-paths.md) |
| 11/10/2026 | Connected Alembic migration metadata to the resume ORM models and added the initial resume schema migration. | Alembic environment, `migrations/versions/` | [Resume persistence](../../adr/11-10-26/resume-persistence.md) |

## 5. References

- [Database Component Technical Specification](../../technical-specification.md)
- [SQLite Adapter Foundation ADR](../../adr/11-06-26/sqlite-adapter-foundation.md)
- [Resume Persistence ADR](../../adr/11-10-26/resume-persistence.md)
- [Resume Repository Module](resume/repository.md)
- [Resume Models Module](resume/models.md)
- [Database Component ADL](../../adr/ADL.md)
- [Use SQLite through SQLAlchemy and Alembic](../../../../docs/adr/Architecture/2026-11-04/database-persistence.md)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
