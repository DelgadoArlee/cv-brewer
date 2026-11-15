# Delete All Resumes Technical Process

## 1. Purpose

Delete all stored resume records through the Core-owned resume repository abstraction.

## 2. Objective

Remove every stored resume record as a single all-or-nothing operation while keeping database access behind the repository contract.

## 3. Scope

- Delete all resume records for the application.
- Return the number of deleted resume records.
- Propagate database failures to the caller.

The process does not perform database queries directly.

## 4. Rules & Constraints

- Deletion must be delegated to the resume repository.
- All resume records must be deleted together; selective deletion is not supported.
- The deleted record count must be returned to the caller.
- Database failures must be propagated to the caller.
- The process must not import or call SQLAlchemy or SQLite.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B[Delegate delete-all request to repository]
        B --> C{Deletion successful?}
        C -->|No| D([Propagate failure])
        C -->|Yes| E([Return deleted count])
````

### Steps

1. Receive the delete-all request.
2. Delegate the request to the resume repository.
3. Return the number of deleted records, or propagate a repository failure.

## 6. Modules

- `app/core/services/resume/service.py` — Defines the delete-all operation.
- `app/core/services/resume/repository.py` — Defines the delete-all contract.

## 7. Data

- [User Resume Data Model](../../../../../../docs/data/user-resume.md) — Structure of stored resume records.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| DELETE-001 | Multiple stored resume records. | Delete all resumes. | All records are deleted and the count is returned. |
| DELETE-002 | No stored resume records. | Delete all resumes. | `0` is returned. |
| DELETE-003 | The repository raises a failure. | Delete all resumes. | The failure is propagated to the caller. |

### 8.3 Test Coverage

Tests must verify the returned count, the empty-database outcome, and failure propagation.

## 9. References

- [Database Service Technical System Specification](../overview.md)
- [Database Service System Overview](../../../../../../docs/system/database-service/overview.md)
- [Delete Resumes System Overview](../../../../../../docs/system/delete-resumes/overview.md)
- [Move the Database Service into Core](../../../../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [Establish the resume service package](../../../adr/11-13-26/resume-service-package.md)
