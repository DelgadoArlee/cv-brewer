# Database Adapter System Overview

## 1. Purpose

The Database Adapter implements database-specific operations for the Database Service. It owns connections, ORM use, queries, transactions, migrations, and database-specific error translation so that application-level operations remain independent of a database implementation.

## 2. Objectives

- Persist application-level data in the selected database implementation.
- Retrieve stored data for application-level operations.
- Preserve database constraints, relationships, and ordering.
- Translate database failures into adapter-level errors.
- Manage schema creation and migration for persisted data.

## 3. Scope

### In Scope

- SQLite connections, SQLAlchemy engine and session lifecycle, and migrations.
- SQLAlchemy models for resume persistence.
- Repository implementations for resume operations.
- Transaction handling and error translation for persistence operations.

### Out of Scope

- Application-level data operation definitions.
- Resume validation, parsing, or generation.
- CLI workflows and file-system management.
- Business-rule decisions about when resume data may be stored.

## 4. Workflow

The adapter receives repository requests from the Database Service, maps application records to database models, performs the requested operation inside a transaction, and returns mapped application records.

See the [Persist Resume Process](processes/persist-resume.md) and [Load Resume Process](processes/load-resume.md).

## 5. Constraints

- All database-specific implementation details must remain inside the adapter.
- Application-level data management rules must remain in the Database Service.
- Models must not be exposed to other components.
- Transactions must commit successful work and roll back failed work.

## 6. Rules

- Adapter repositories must use the existing transactional session boundary.
- Resume child data must be stored with its ordering preserved.
- Foreign keys must enforce resume child relationships.
- Content fingerprints must be enforced as unique.
- Database exceptions must be translated to adapter-level errors.

## 7. Data Management

The adapter stores resume records using the SQLite schema documented in [SQLite Database Overview](../../../database/docs/sqlite/overview.md).

## 8. Error Handling

- Integrity failures must be translated and reported.
- Operational, data, programming, and other database failures must be translated and reported.
- Failed operations must not leave partial resume records committed.

## 9. References

- [Database Component Technical Specification](../../../database/docs/technical-specification.md)
- [Database Adapter Technical Specification](../../../database/docs/systems/database-adapter/overview.md)
- [User Resume Data Model](../../data/user-resume.md)
