# Database Service System Overview

## 1. Purpose

The Database Service provides the application-level operations used to manage structured application data. It defines what data operations are available while delegating database-specific access to a Database Adapter. The service is owned by the Core application layer; the Database component supplies adapters.

## 2. Objectives

- Provide stable data operations for the Core Processing Engine.
- Store validated resume data for later retrieval and generation.
- Retrieve stored resume records by identifier or content fingerprint.
- Keep database implementation details outside application-level operations.
- Delegate persistence, queries, transactions, and errors to the selected Database Adapter.

## 3. Scope

### In Scope

- Application-level resume data operations.
- Resume data record definitions used by the service boundary.
- Coordination with a Database Adapter implementation.
- Reporting adapter failures to callers.

### Out of Scope

- SQLite connections, SQLAlchemy models, queries, transactions, and migrations.
- Resume validation, parsing, and generation.
- File-system and upload workflow management.
- Delete-all resume behavior, which belongs to the delete-resumes feature.

## 4. Workflow

The service receives application-level resume operations, prepares the record for persistence, delegates the request to the configured Database Adapter, and returns the resulting record or lookup outcome.

See the [Store Resume Process](processes/store-resume.md) and [Retrieve Resume Process](processes/retrieve-resume.md).

## 5. Constraints

- The service must not depend on SQLAlchemy, SQLite, or a specific database implementation.
- All database access must be performed through a Database Adapter implementation.
- Application-level data must follow the approved user resume data model.
- The service must not perform resume validation or parsing.

## 6. Rules

- A resume must receive a unique identifier before it is persisted.
- A resume must receive a creation timestamp before it is persisted.
- Resume child data must preserve its original order.
- Content fingerprints must be unique across stored resumes.
- Lookups that find no matching record must return no record rather than failing.

## 7. Data Management

The service manages resume records based on the [User Resume Data Model](../../data/user-resume.md). The initial operations store and retrieve metadata, parsed resume data, validation status, and processing history.

## 8. Error Handling

- Database adapter failures must be reported to the caller.
- Duplicate content fingerprints must be reported as persistence failures.
- Missing resume records must not be treated as system errors.

## 9. References

- [Database Component Technical Specification](../../../app/database/docs/technical-specification.md)
- [Database Service Technical Specification](../../../app/core/docs/systems/database-service/overview.md)
- [Move the Database Service into Core](../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [User Resume Data Model](../../data/user-resume.md)
