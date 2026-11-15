# Delete All Resumes Technical Process

## 1. Purpose

Delete every stored resume row from SQLite and rely on database cascades to remove related child records.

## 2. Objective

Remove all resume data in one adapter transaction and return the number of deleted resume records.

## 3. Scope

- Delete all rows from the resume root table.
- Remove related child rows through database cascades.
- Return the deleted resume count.

The process does not define application-level operation behavior.

## 4. Rules & Constraints

- Deletion must use the adapter session boundary.
- All resume rows must be deleted in one transaction.
- Related child rows must be removed by `ON DELETE CASCADE`.
- The deleted root record count must be returned.
- Database failures must be translated into adapter errors.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Open session]
        B --> C[Delete all resume rows]
        C --> D[Child rows removed by cascade]
        D --> E([Return deleted count])
````

### Steps

1. Open an adapter session.
2. Delete every row from the resume root table.
3. Let database cascades remove related child rows.
4. Return the number of deleted resume records.

## 6. Modules

- `app/database/adapters/sqlite/resume/repository.py` — Implements the adapter delete-all operation.
- `app/database/adapters/sqlite/resume/models/` — Defines the SQLite ORM models and cascade relationships.

## 7. Data

- [Resume Table](../../../sqlite/schemas/resumes.md) — Root resume schema.
- [SQLite Database Overview](../../../sqlite/overview.md) — Related child tables.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| DELETE-ADP-001 | Multiple stored resumes with child records. | Delete all resumes. | All root and child rows are removed and the count is returned. |
| DELETE-ADP-002 | No stored resumes. | Delete all resumes. | `0` is returned. |
| DELETE-ADP-003 | A database failure occurs. | Delete all resumes. | An adapter error is raised and no partial deletion remains. |

### 8.3 Test Coverage

Tests must verify cascade deletion, the returned count, the empty-database outcome, and failure translation.

## 9. References

- [Database Adapter Technical System Specification](../overview.md)
- [Database Adapter System Overview](../../../../../../docs/system/database-adapter/overview.md)
- [Delete Resumes System Overview](../../../../../../docs/system/delete-resumes/overview.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
