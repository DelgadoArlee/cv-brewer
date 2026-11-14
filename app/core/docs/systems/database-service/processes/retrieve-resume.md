# Retrieve Resume Technical Process

## 1. Purpose

Retrieve stored resume records through the resume repository by identifier, content fingerprint, or listing.

## 2. Objective

Return complete application-level resume records for stored resume data while keeping database access behind the repository abstraction.

## 3. Scope

- Retrieve a resume by identifier.
- Find a resume by content fingerprint.
- List stored resumes.
- Return `None` when a single-record lookup finds no match.

The process does not perform database queries directly.

## 4. Rules & Constraints

- All retrieval must be delegated to the resume repository.
- Missing single-record lookups must return `None`.
- Listing must return all stored resume records.
- Database failures must be propagated to the caller.
- The process must not import or call SQLAlchemy or SQLite.

## 5. Workflow

### Diagram

```` mermaid
    flowchart TD
        A([Start]) --> B{Lookup type}
        B -->|By ID| C[Request resume by ID]
        B -->|By fingerprint| D[Request resume by fingerprint]
        B -->|List| E[Request all resumes]
        C --> F{Found?}
        D --> F
        F -->|Yes| G([Return record])
        F -->|No| H([Return none])
        E --> I([Return records])
````

### Steps

1. Determine whether the caller requests a record by ID, by fingerprint, or a list.
2. Delegate the request to the resume repository.
3. Return the matching record, `None` for a missing single record, or the stored record list.

## 6. Modules

- `app/core/services/resume/service.py` — Defines retrieval operations.
- `app/core/services/resume/repository.py` — Defines the retrieval contract.
- `app/core/services/resume/models.py` — Defines resume records.

## 7. Data

- [User Resume Data Model](../../../../../../docs/data/user-resume.md) — Structure of returned resume records.

## 8. Testing

### 8.1 Test Level

Process level.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| RETRIEVE-001 | A stored resume record. | Retrieve by ID. | The matching record is returned. |
| RETRIEVE-002 | No matching resume. | Retrieve by ID. | `None` is returned. |
| RETRIEVE-003 | A stored resume record. | Find by content fingerprint. | The matching record is returned. |
| RETRIEVE-004 | Multiple stored resumes. | List resumes. | All records are returned. |

### 8.3 Test Coverage

Tests must verify observable retrieval behavior, including missing-record outcomes.

## 9. References

- [Database Service Technical System Specification](../overview.md)
- [Database Service System Overview](../../../../../../docs/system/database-service/overview.md)
- [Move the Database Service into Core](../../../../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [Establish the resume service package](../../../adr/11-13-26/resume-service-package.md)
- [Resume Persistence ADR](../../../../../database/docs/adr/11-10-26/resume-persistence.md)
