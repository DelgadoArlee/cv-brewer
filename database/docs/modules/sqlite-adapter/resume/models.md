# Resume Models Module Technical Specification

## 1. Purpose

Defines the SQLAlchemy ORM models used by the SQLite adapter to persist resume records and their ordered child data.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `Base` | Class | Declarative base for SQLite ORM models. | None. | Base metadata and mapper registry. |
| `Resume` | ORM model | Maps the `resumes` table and owns resume child relationships. | Model field values. | `Resume` instance. |
| `ResumeExperience` | ORM model | Maps the `resume_experience` table. | Model field values. | `ResumeExperience` instance. |
| `ResumeEducation` | ORM model | Maps the `resume_education` table. | Model field values. | `ResumeEducation` instance. |
| `ResumeCertification` | ORM model | Maps the `resume_certifications` table. | Model field values. | `ResumeCertification` instance. |
| `ResumeSkill` | ORM model | Maps the `resume_skills` table. | Model field values. | `ResumeSkill` instance. |
| `ResumeProcessingHistory` | ORM model | Maps the `resume_processing_history` table. | Model field values. | `ResumeProcessingHistory` instance. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| SQLAlchemy | External library | Declarative mappings, column types, relationships, and constraints. |
| Alembic | External library | Reads ORM metadata for migrations. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/10/2026 | Added SQLite resume ORM models under `resume/models/` with ordered child relationships and cascade deletion. | `Resume`, `ResumeExperience`, `ResumeEducation`, `ResumeCertification`, `ResumeSkill`, `ResumeProcessingHistory` | [Resume persistence ADR](../../../adr/11-10-26/resume-persistence.md) |

## 5. References

- [Database Adapter Technical System Specification](../../../systems/database-adapter/overview.md)
- [SQLite Adapter Module](../sqlite-adapter.md)
- [SQLite Database Overview](../../../sqlite/overview.md)
- [Resume Table Schema](../../../sqlite/schemas/resumes.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
- [Database Component Coding Guidelines](../../../guidelines.md)
