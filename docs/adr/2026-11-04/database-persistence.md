# Use SQLite through SQLAlchemy and Alembic

## Date

2026-11-04

## Status

Accepted

## Context

The Database Service must manage structured application data without depending on a specific database implementation. SQLite is suitable as an embedded default. The architecture requires a Database Adapter boundary and allows external databases later.

## Decision

Use SQLite as the default database implementation. Access it through SQLAlchemy 2.0 and manage schema changes with Alembic.

Keep database-specific code inside the Database Adapter. The Database Service defines application-level operations, and the Core depends only on the Database Service interface. No Core code imports SQLAlchemy or SQLite directly.

## Consequences

- SQLite keeps installation simple and requires no separate database server.
- Alembic provides a migration path as the data model evolves.
- SQLAlchemy adds dependency and build complexity but supports future database adapters.
- Adapter behavior, migrations, and error translation require dedicated tests.
