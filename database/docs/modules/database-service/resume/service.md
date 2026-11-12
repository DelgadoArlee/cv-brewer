# Resume Service Module Technical Specification

## 1. Purpose

Coordinates resume operations exposed by the Database Service and generates missing identifiers and creation timestamps before persistence.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `ResumeService` | Class | Coordinates resume operations through a repository implementation. | A `ResumeRepository` implementation. | `ResumeService` instance. |
| `ResumeService.save_resume()` | Method | Stores a resume record. | `record: NewResume`. | `ResumeRecord`. |
| `ResumeService.get_resume()` | Method | Retrieves a resume by ID. | `resume_id: str`. | `ResumeRecord \| None`. |
| `ResumeService.find_resume_by_content_fingerprint()` | Method | Retrieves a resume by fingerprint. | `content_fingerprint: str`. | `ResumeRecord \| None`. |
| `ResumeService.list_resumes()` | Method | Lists stored resumes. | None. | `list[ResumeRecord]`. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Python `uuid` | Standard library | Generates resume identifiers. |
| Python `datetime` | Standard library | Generates creation timestamps. |
| Resume repository | Internal module | Performs persistence and retrieval. |
| Resume models | Internal module | Provides resume record data structures. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/10/2026 | Added resume service operations that generate missing identifiers and timestamps before delegating persistence. | `ResumeService` | [Resume persistence ADR](../../../adr/11-10-26/resume-persistence.md) |

## 5. References

- [Database Service Technical System Specification](../../../systems/database-service/overview.md)
- [Resume Models Module](models.md)
- [Resume Repository Module](repository.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
- [Database Component Coding Guidelines](../../../guidelines.md)
