# SQLite Database Overview

## 1. Purpose

Describes how the user resume data model is mapped to the SQLite database implementation.

## 2. Database

SQLite is the default embedded database implementation. It is accessed by the Database Adapter through SQLAlchemy, and schema changes are managed with Alembic.

## 3. Entities and Tables

| Entity | Table | Description |
| --- | --- | --- |
| Resume | `resumes` | Stores resume identity, original file reference, metadata, personal information, validation status, and timestamps. |
| Resume Experience | `resume_experience` | Stores ordered work-experience entries for a resume. |
| Resume Education | `resume_education` | Stores ordered education entries for a resume. |
| Resume Certification | `resume_certifications` | Stores ordered certification entries for a resume. |
| Resume Skill | `resume_skills` | Stores ordered skills for a resume. |
| Resume Processing History | `resume_processing_history` | Stores ordered processing-history entries for a resume. |

## 4. Relationships

- One `resumes` record has zero or more `resume_experience` records.
- One `resumes` record has zero or more `resume_education` records.
- One `resumes` record has zero or more `resume_certifications` records.
- One `resumes` record has zero or more `resume_skills` records.
- One `resumes` record has zero or more `resume_processing_history` records.
- All child records reference `resumes.resume_id` with `ON DELETE CASCADE`.

## 5. Database Diagram

````mermaid
erDiagram
    resumes ||--o{ resume_experience : has
    resumes ||--o{ resume_education : has
    resumes ||--o{ resume_certifications : has
    resumes ||--o{ resume_skills : has
    resumes ||--o{ resume_processing_history : has

    resumes {
        TEXT resume_id PK
        TEXT original_file_path
        TEXT file_name
        INTEGER file_size_bytes
        DATETIME upload_timestamp
        TEXT content_fingerprint UK
        TEXT name
        TEXT email
        TEXT phone
        TEXT address
        TEXT linkedin_url
        TEXT github_url
        TEXT summary
        BOOLEAN file_type_valid
        BOOLEAN metadata_extraction_success
        TEXT deduplication_result
        BOOLEAN pdf_encryption_check
        BOOLEAN pdf_structure_valid
        BOOLEAN content_extraction_success
        BOOLEAN schema_validation_passed
        DATETIME created_at
        DATETIME deleted_at
    }

    resume_experience {
        INTEGER id PK
        TEXT resume_id FK
        INTEGER position_order
        TEXT company
        TEXT position
        DATE start_date
        DATE end_date
        TEXT description
    }

    resume_education {
        INTEGER id PK
        TEXT resume_id FK
        INTEGER position_order
        TEXT institution
        TEXT degree
        TEXT field_of_study
        DATE start_date
        DATE end_date
    }
````

## 6. Mapping Rules

- `resume_id` maps to a TEXT primary key containing a UUID.
- `metadata.content_fingerprint` maps to a unique `resumes.content_fingerprint` column.
- `parsed_data.personal_info` and `parsed_data.summary` map to columns on `resumes`.
- `validation_status` maps to boolean and text columns on `resumes`.
- Experience, education, certifications, skills, and processing history map to child tables.
- Child array indexes map to `position_order`.
- Nullable data-model fields map to nullable columns.
- `created_at` and `deleted_at` map to DATETIME columns.

## 7. References

- [Database Component Technical Specification](../technical-specification.md)
- [User Resume Data Model](../../../docs/data/user-resume.md)
- [Resume Table](schemas/resumes.md)
- [Resume Experience Table](schemas/resume-experience.md)
- [Resume Education Table](schemas/resume-education.md)
- [Resume Certification Table](schemas/resume-certifications.md)
- [Resume Skill Table](schemas/resume-skills.md)
- [Resume Processing History Table](schemas/resume-processing-history.md)
