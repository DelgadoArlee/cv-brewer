# Move the Database Service into the Core Application Layer

## Date

2026-11-13

## Status

Accepted

## Category

architecture

## Context

The Database Service previously lived in the database component alongside the Database Adapter. The Core depended on the Database Service for application-level resume persistence, while the database component owned both the application-level service and database-specific adapters.

The application-level resume operations, records, and repository contract are Core concerns. Keeping them in the database component blurred the boundary between application logic and database-specific implementation.

## Decision

- Move the Database Service application layer into the Core component.
- Place all resume-specific service code under `app/core/services/resume/`, including resume records, the repository contract, and resume service operations.
- Keep Database Adapters in the database component under `app/database/adapters/`.
- Database Adapters implement Core-owned repository contracts.
- Keep the `initialize_database` and `create_resume_service` composition helpers in `app/database/__init__.py`.
- Do not introduce a reusable database abstraction package until a concrete shared need exists.
- The Core must not import database adapters, SQLAlchemy, or SQLite directly.

## Consequences

- Core owns application-level resume data operations while the database component owns database-specific implementation.
- Database adapters depend on Core-owned service contracts.
- Import paths, tests, and component documentation must be updated.
- The existing SQLite persistence decision remains in effect; this decision changes service ownership and code placement, not the persistence technology or schema.
