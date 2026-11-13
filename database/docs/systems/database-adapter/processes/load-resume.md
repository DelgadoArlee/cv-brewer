# Load Resume Technical Process

## 1. Purpose

Load stored SQLite resume models and map them into application-level resume records.

## 2. Objective

Return complete resume records with ordered child data without exposing ORM models outside the adapter.

## 3. Scope

- Retrieve resume models by identifier or content fingerprint.
- List stored resume models.
- Map root and child models into application-level records.
- Return `None` for missing single-record lookups.

The process does not define application-level operation behavior.

## 4. Rules & Constraints

- Retrieval must use the adapter session boundary.
- Mapping must preserve child ordering.
- Missing single records must return `None`.
- ORM models must not be returned to callers.
- Database failures must be translated into adapter errors.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Receive lookup request]
        B --> C[Open session]
        C --> D[Query resume models]
        D --> E{Match found?}
        E -->|No| F([Return none])
        E -->|Yes| G[Map root and ordered children]
        G --> H([Return resume record])
````

### Steps

1. Receive a lookup request.
2. Open a session and query the requested resume model or models.
3. Return `None` when a single-record lookup has no match.
4. Map matching models into application-level records with ordered children.
5. Return the mapped record or records.

## 6. Modules

- `database/src/database/adapters/sqlite/resume/repository.py` — Implements the adapter loading operations.
- `database/src/database/adapters/sqlite/resume/models/` — Defines the SQLite ORM models.

## 7. Data

- [Resume Table](../../../sqlite/schemas/resumes.md) — Root resume schema.
- [SQLite Database Overview](../../../sqlite/overview.md) — Related child tables.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| LOAD-001 | A stored resume record. | Load by ID. | The mapped resume record is returned. |
| LOAD-002 | No matching resume. | Load by ID. | `None` is returned. |
| LOAD-003 | Multiple stored resumes. | List resumes. | All mapped records are returned. |
| LOAD-004 | Stored child records. | Load a resume. | Child order is preserved. |

### 8.3 Test Coverage

Tests must verify mapping outcomes, missing records, and ordering.

## 9. References

- [Database Adapter Technical System Specification](../overview.md)
- [Database Adapter System Overview](../../../../../docs/system/database-adapter/overview.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
