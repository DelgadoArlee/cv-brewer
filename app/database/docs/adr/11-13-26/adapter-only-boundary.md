# Retain Database Adapters as the Database Component Boundary

## Date

2026-11-13

## Status

Accepted

## Context

The Database Service application layer moved into the Core under `app/core/services/resume/` as part of the [Move the Database Service into the Core application layer](../../../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md) decision. The database component must now define its boundary around database-specific adapters rather than application-level data operations. Resume persistence still requires a hybrid relational schema, ordered child data, unique content fingerprints, and SQLite repository implementations.

## Decision

- Keep Database Adapters under `app/database/adapters/`.
- Implement the Core-owned `ResumeRepository` contract in `adapters/sqlite/resume/repository.py`.
- Keep SQLAlchemy models under `adapters/sqlite/resume/models/`.
- Preserve the hybrid relational resume schema, ordered child tables, unique `content_fingerprint`, and nullable `deleted_at` column.
- Keep database connections, ORM configuration, queries, transactions, migrations, and error translation inside the adapter.
- Do not define application-level operations or application-level record structures in the database component.
- Keep the `initialize_database` and `create_resume_service` composition helpers in `app/database/__init__.py`.

## Consequences

- The database component depends on Core-owned resume service contracts.
- Adapter persistence code remains grouped by class, with the repository at the class directory root and models under `models/`.
- Application-level resume behavior changes belong in Core, not in the database component.
- This decision supersedes the service-placement portions of [Establish resume persistence](../11-10-26/resume-persistence.md).
- Future database adapters must provide compatible implementations of the Core-owned resume repository contract.
