# Database Service Technical System Specification

## 1. Purpose

Defines the application-level data operations exposed by the database component. The Database Service owns resume operation definitions and record structures while delegating persistence to a Database Adapter.

## 2. Objective

- Provide resume persistence and retrieval operations without database-specific coupling.
- Define resume record structures used across the service boundary.
- Generate record identifiers and creation timestamps when omitted.
- Delegate all persistence work to a repository implemented by the Database Adapter.

## 3. Scope

### In Scope

- Resume module under `app/database/database_service/modules/resume/`.
- Application-level resume record definitions.
- Resume repository abstraction.
- Resume service operations for save, get, find by fingerprint, and list.

### Out of Scope

- SQLAlchemy models, SQLite queries, transactions, and migrations.
- Resume parsing, validation, and generation.
- Upload workflow orchestration.
- Delete-all resume behavior.

## 4. Rules & Constraints

- The service must not import SQLAlchemy or SQLite modules.
- All persistence must go through the `ResumeRepository` abstraction.
- A resume identifier must be generated with `uuid4` when absent.
- A creation timestamp must be generated when absent.
- Child resume data order must be preserved by the adapter.
- Duplicate content fingerprints must be surfaced from the adapter as failures.
- Lookups that find no record must return `None`.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Store Resume | Creates a stored resume record from application-level resume data. | [Store Resume](processes/store-resume.md) |
| Retrieve Resume | Retrieves stored resume records by identifier, fingerprint, or listing. | [Retrieve Resume](processes/retrieve-resume.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `ResumeRepository` | Internal interface | Accepts application-level resume records for persistence and retrieval. |
| Database Adapter | Internal system | Provides the concrete repository implementation. |
| Python `uuid` | Standard library | Generates resume identifiers. |
| Python `datetime` | Standard library | Generates creation timestamps. |

## 7. Test Cases

| Test Case ID | Scenario | Expected Result | Related Rule |
| --- | --- | --- | --- |
| DB-SVC-001 | Save a complete resume record. | The record is stored and returned with resume ID and creation timestamp. | Save operation |
| DB-SVC-002 | Save a resume with an existing identifier and timestamp. | Provided values are preserved. | Identifier and timestamp rules |
| DB-SVC-003 | Save a duplicate content fingerprint. | The adapter integrity failure is surfaced and no duplicate is stored. | Unique fingerprint rule |
| DB-SVC-004 | Retrieve a stored resume by ID. | The matching resume record is returned. | Retrieve operation |
| DB-SVC-005 | Retrieve a missing resume by ID. | `None` is returned. | Missing record rule |
| DB-SVC-006 | Find a resume by content fingerprint. | The matching resume record is returned. | Retrieve operation |
| DB-SVC-007 | List stored resumes. | All stored resume records are returned. | List operation |

## 8. Diagrams

````mermaid
flowchart LR
    Caller[Application Caller] --> Service[ResumeService]
    Service --> Port[ResumeRepository]
    Port --> Adapter[SQLite Resume Repository]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Establish resume persistence](../../adr/11-10-26/resume-persistence.md) | Use a hybrid relational schema, unique fingerprints, and service-layer resume operations. |

## 10. Data

The service uses the [User Resume Data Model](../../../../../docs/data/user-resume.md) and defines application-level record structures in `app/database/database_service/modules/resume/models.py`.

## 11. References

- [Database Service System Overview](../../../../../docs/system/database-service/overview.md)
- [Database Component Technical Specification](../../technical-specification.md)
- `app/database/database_service/modules/resume/models.py` — Defines resume records.
- `app/database/database_service/modules/resume/repository.py` — Defines the retrieval and persistence contract.
- `app/database/database_service/modules/resume/service.py` — Defines resume operations.
- [Resume Persistence ADR](../../adr/11-10-26/resume-persistence.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
