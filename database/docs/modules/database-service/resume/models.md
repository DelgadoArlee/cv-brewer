# Resume Models Module Technical Specification

## 1. Purpose

Defines the application-level resume data records exposed by the Database Service for storage and retrieval.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `ResumeMetadata` | Dataclass | Holds uploaded file metadata. | `file_name`, `file_size_bytes`, `upload_timestamp`, `content_fingerprint`. | `ResumeMetadata` instance. |
| `PersonalInfo` | Dataclass | Holds candidate contact information. | `name`, `email`, optional `phone`, `address`, `linkedin_url`, `github_url`. | `PersonalInfo` instance. |
| `Experience` | Dataclass | Holds one work-experience entry. | `company`, `position`, `start_date`, optional `end_date`, `description`. | `Experience` instance. |
| `Education` | Dataclass | Holds one education entry. | `institution`, `degree`, optional `field_of_study`, `start_date`, optional `end_date`. | `Education` instance. |
| `Certification` | Dataclass | Holds one certification entry. | `name`, `issuer`, `issue_date`, optional `expiry_date`. | `Certification` instance. |
| `ParsedResumeData` | Dataclass | Holds parsed resume content. | `personal_info`, optional `summary`, `experience`, `education`, `skills`, `certifications`. | `ParsedResumeData` instance. |
| `ValidationStatus` | Dataclass | Holds processing validation outcomes. | Validation booleans and `deduplication_result`. | `ValidationStatus` instance. |
| `ProcessingHistoryEntry` | Dataclass | Holds one processing-history entry. | `step`, `timestamp`, `status`, optional `error_message`. | `ProcessingHistoryEntry` instance. |
| `NewResume` | Dataclass | Holds resume data supplied for storage. | Resume fields plus optional `resume_id`, `created_at`, `deleted_at`. | `NewResume` instance. |
| `ResumeRecord` | Dataclass | Holds a stored resume record. | Required `resume_id`, `created_at`, and resume data fields. | `ResumeRecord` instance. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Python `dataclasses` | Standard library | Defines immutable resume data records. |
| Python `datetime` | Standard library | Defines date and timestamp fields. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/10/2026 | Added application-level resume records under the Database Service resume module. | `NewResume`, `ResumeRecord`, resume value objects | [Resume persistence ADR](../../../adr/11-10-26/resume-persistence.md) |

## 5. References

- [Database Service Technical System Specification](../../../systems/database-service/overview.md)
- [Resume Repository Module](repository.md)
- [Resume Service Module](service.md)
- [User Resume Data Model](../../../../../docs/data/user-resume.md)
- [Resume Persistence ADR](../../../adr/11-10-26/resume-persistence.md)
- [Database Component Coding Guidelines](../../../guidelines.md)
