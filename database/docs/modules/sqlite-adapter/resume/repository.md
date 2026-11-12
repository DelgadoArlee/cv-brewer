# Resume Repository Module Technical Specification

## 1. Purpose

Implements the Database Service `ResumeRepository` abstraction using SQLite, SQLAlchemy models, and the adapter transactional session boundary.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `SqliteResumeRepository` | Class | SQLite implementation of resume persistence and retrieval. | `session_factory: sessionmaker[Session]`. | `SqliteResumeRepository` instance. |
| `SqliteResumeRepository.save()` | Method | Stores a complete resume record and ordered child records. | `record: ResumeRecord`. | `None`. |
| `SqliteResumeRepository.get()` | Method | Retrieves a resume record by ID. | `resume_id: str`. | `ResumeRecord \| None`. |
| `SqliteResumeRepository.find_by_content_fingerprint()` | Method | Retrieves a resume record by content fingerprint. | `content_fingerprint: str`. | `ResumeRecord \| None`. |
| `SqliteResumeRepository.list_all()` | Method | Lists all stored resume records. | None. | `list[ResumeRecord]`. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `ResumeRepository` | Internal interface | Defines the repository contract. |
| SQLAlchemy | External library | Sessions, queries, and ORM models. |
| SQLite adapter models | Internal module | Defines persisted resume tables. |
| `session_scope` | Internal module | Provides transactional session boundaries and error translation. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/10/2026 | Added the SQLite resume repository under `resume/` and mapped application records to SQLAlchemy models. | `SqliteResumeRepository` | [Resume persistence ADR](../../../adr/11-10-26/resume-persistence.md) |

## 5. References

- [Database Adapter Technical System Specification](../../../systems/database-adapter/overview.md)
- [SQLite Adapter Module](../sqlite-adapter.md)
- [Resume Repository Module](../../database-service/resume/repository.md)
- [Resume Models Module](models.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
- [Database Component Coding Guidelines](../../../guidelines.md)
