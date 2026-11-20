# SQLite Database Overview

## 1. Purpose

Describes how the application data models for resume persistence, LLM activity logging, and resume processing execution logging are mapped to the SQLite database implementation.

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
| Resume Processing Run | `resume_processing_runs` | Stores resume processing run records, including outcome, timing, summary, performance, embedded error data, and resume identifier references. |
| Resume Processing Step | `resume_processing_steps` | Stores processing step records for a run, including ordering, timing, input/output summaries, performance, embedded error data, and metadata. |
| LLM Activity Log | `llm_logs` | Stores LLM generation requests, an optional processing step reference, responses, usage, performance, and errors. |

## 4. Relationships

- One `resumes` record has zero or more `resume_experience` records.
- One `resumes` record has zero or more `resume_education` records.
- One `resumes` record has zero or more `resume_certifications` records.
- One `resumes` record has zero or more `resume_skills` records.
- Resume child records reference `resumes.resume_id` with `ON DELETE CASCADE`.
- One `resume_processing_runs` record has zero or more `resume_processing_steps` records.
- `resume_processing_steps.run_id` references `resume_processing_runs.run_id` with `ON DELETE CASCADE`.
- `resume_processing_runs.resume_id` and `resume_processing_runs.matched_resume_id` are identifier references only and do not define foreign-key relationships to `resumes`.
- `resume_processing_steps.input.source_step_id` is an identifier reference only and does not define a foreign-key relationship.
- Each `llm_logs` record references zero or one `resume_processing_steps` record through indexed nullable `processing_step_id` with `ON DELETE SET NULL`.
- One `resume_processing_steps` record has zero or more `llm_logs` records.

## 5. Database Diagram

````mermaid
erDiagram
    resumes ||--o{ resume_experience : has
    resumes ||--o{ resume_education : has
    resumes ||--o{ resume_certifications : has
    resumes ||--o{ resume_skills : has
    resume_processing_runs ||--o{ resume_processing_steps : has
    resume_processing_steps o|--o{ llm_logs : references

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

    resume_processing_runs {
        TEXT run_id PK
        TEXT process_name
        TEXT process_version
        TEXT status
        TEXT result
        TEXT resume_id
        TEXT matched_resume_id
        DATETIME started_at
        DATETIME completed_at
        FLOAT duration_ms
        JSON summary
        JSON performance
        JSON error
    }

    resume_processing_steps {
        TEXT step_id PK
        TEXT run_id FK
        TEXT step_name
        INTEGER step_order
        INTEGER attempt_number
        TEXT status
        DATETIME started_at
        DATETIME completed_at
        FLOAT duration_ms
        JSON input
        JSON output
        JSON performance
        JSON error
        JSON metadata
    }

    llm_logs {
        TEXT id PK
        TEXT provider
        TEXT model
        TEXT operation
        TEXT processing_step_id FK
        TEXT status
        TEXT system_prompt
        TEXT prompt
        JSON parameters
        TEXT response_content
        TEXT finish_reason
        INTEGER input_tokens
        INTEGER output_tokens
        INTEGER total_tokens
        DATETIME started_at
        DATETIME completed_at
        FLOAT duration_ms
        FLOAT start_memory_mb
        FLOAT peak_memory_mb
        FLOAT end_memory_mb
        FLOAT memory_delta_mb
        FLOAT cpu_avg_percent
        FLOAT cpu_peak_percent
        INTEGER sample_count
        TEXT error_type
        TEXT error_message
        DATETIME created_at
    }
````

## 6. Mapping Rules

- `resume_id` in `resumes` maps to a TEXT primary key containing a UUID.
- `metadata.content_fingerprint` maps to a unique `resumes.content_fingerprint` column.
- `parsed_data.personal_info` and `parsed_data.summary` map to columns on `resumes`.
- `validation_status` maps to boolean and text columns on `resumes`.
- Experience, education, certifications, and skills map to child tables.
- Child array indexes map to `position_order`.
- Nullable data-model fields map to nullable columns.
- `created_at` and `deleted_at` map to DATETIME columns.
- Resume processing run `run_id` and processing step `step_id` map to TEXT primary keys containing UUIDs.
- Resume processing run and step identifiers, timestamps, and durations map to TEXT, DATETIME, and FLOAT columns as defined in their schema documents.
- Resume processing run and step `status` maps to a checked TEXT column with values `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, and `TIMEOUT`.
- Resume processing run `resume_id` and `matched_resume_id` map to nullable TEXT identifier columns without foreign-key constraints.
- Resume processing run nested objects `summary`, `performance`, and `error` map to JSON columns.
- Resume processing step nested objects `input`, `output`, `performance`, `error`, and `metadata` map to JSON columns.
- Resume processing step `run_id` maps to a foreign key referencing `resume_processing_runs.run_id` with `ON DELETE CASCADE`.
- Resume processing step ORM attribute `metadata_json` maps to the `metadata` column.
- LLM activity log `processing_step_id` maps to an indexed nullable foreign key referencing `resume_processing_steps.step_id` with `ON DELETE SET NULL`.
- LLM activity log nested objects map to flat columns on `llm_logs`, except `parameters`, which maps to a JSON column.
- LLM activity log memory and CPU measurements map to `start_memory_mb`, `peak_memory_mb`, `end_memory_mb`, `memory_delta_mb`, `cpu_avg_percent`, `cpu_peak_percent`, and `sample_count` columns; short-running operations may record `sample_count` of 0 with null CPU values.
- LLM activity log `status` maps to a checked TEXT column with values `SUCCESS`, `FAILED`, and `TIMEOUT`.

## 7. References

- [Database Component Technical Specification](/app/database/docs/technical-specification.md)
- [User Resume Data Model](/docs/data/user-resume.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [Resume Table](/app/database/docs/sqlite/schemas/resumes.md)
- [Resume Experience Table](/app/database/docs/sqlite/schemas/resume-experience.md)
- [Resume Education Table](/app/database/docs/sqlite/schemas/resume-education.md)
- [Resume Certification Table](/app/database/docs/sqlite/schemas/resume-certifications.md)
- [Resume Skill Table](/app/database/docs/sqlite/schemas/resume-skills.md)
- [Resume Processing Runs Table](/app/database/docs/sqlite/schemas/resume-processing-runs.md)
- [Resume Processing Steps Table](/app/database/docs/sqlite/schemas/resume-processing-steps.md)
- [LLM Logs Table](/app/database/docs/sqlite/schemas/llm-logs.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
