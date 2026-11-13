# Persist Resume Technical Process

## 1. Purpose

Map an application-level resume record to SQLAlchemy models and persist it in SQLite within a transaction.

## 2. Objective

Store the complete resume aggregate, including ordered child records, while enforcing database constraints.

## 3. Scope

- Map resume records to ORM models.
- Assign child ordering values from record order.
- Persist root and child records in one transaction.
- Translate database failures into adapter errors.

The process does not define when resume data is valid for storage.

## 4. Rules & Constraints

- The operation must use `session_scope`.
- Root and child records must be committed together.
- Failed operations must roll back completely.
- Child `position_order` must match the source record order.
- Duplicate content fingerprints must raise an adapter integrity failure.
- ORM models must not leave the adapter boundary.

## 5. Workflow

### Diagram

```` mermaid
flowchart TD
    A([Start]) --> B[Receive resume record]
    B --> C[Map root and child models]
    C --> D[Open transactional session]
    D --> E[Add resume aggregate]
    E --> F{Commit succeeds?}
    F -->|Yes| G([Persisted])
    F -->|No| H[Roll back and translate error]
    H --> I([Raise adapter error])
````

### Steps

1. Receive the application-level resume record.
2. Map the root record and ordered child records to ORM models.
3. Open a transactional session.
4. Add the resume aggregate to the session.
5. Commit, or roll back and translate any database failure.

## 6. Modules

- `app/database/adapters/sqlite/resume/repository.py` — Implements the adapter persistence operation.
- `app/database/adapters/sqlite/resume/models/` — Defines the SQLite ORM models.

## 7. Data

- [Resume Table](../../../sqlite/schemas/resumes.md) — Root resume schema.
- [SQLite Database Overview](../../../sqlite/overview.md) — Related child tables.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| PERSIST-001 | A valid resume record. | Persist is called. | Root and child rows are stored. |
| PERSIST-002 | A duplicate content fingerprint. | Persist is called. | An adapter integrity failure is raised and no duplicate is stored. |
| PERSIST-003 | A database failure during save. | Persist is called. | The transaction rolls back and an adapter error is raised. |

### 8.3 Test Coverage

Tests must verify persistence outcomes and rollback behavior.

## 9. References

- [Database Adapter Technical System Specification](../overview.md)
- [Database Adapter System Overview](../../../../../../docs/system/database-adapter/overview.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
