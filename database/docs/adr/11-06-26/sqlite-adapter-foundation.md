# Establish SQLite Adapter Foundation

## Date

2026-11-06

## Status

Accepted

## Context

The database component contains an empty adapter package. The adapter must provide database-specific infrastructure without implementing application-level data operations. The Database Service interface and database schema are not yet documented, so resume persistence cannot be implemented yet.

The component technical specification requires the SQLite adapter to own connections, connection lifecycle, ORM configuration, transactions, migrations, and database-specific error translation.

## Decision

- Use synchronous SQLAlchemy 2.0 for the SQLite adapter.
- Require an explicit SQLite SQLAlchemy URL through `SqliteConfig`; do not select an implicit database file location.
- Enable SQLite foreign-key enforcement for every new adapter connection.
- Provide a transactional `session_scope` boundary that commits on success, rolls back on failure, and always closes the session.
- Define an adapter-local exception hierarchy and translate SQLAlchemy exceptions into it.
- Keep Alembic configuration, environment, and revision templates inside the SQLite adapter package.
- Defer resume tables, migration revisions, CRUD operations, and Database Service integration until their documentation and schema are approved.

## Consequences

- The adapter can create engines, sessions, transactions, and migrations independently of the Database Service.
- Database-specific errors remain isolated from application code.
- The adapter has no persistence schema yet, so the migration environment currently contains no revisions.
- Future Database Service operations can build on the adapter foundation without changing its connection or transaction behavior.
