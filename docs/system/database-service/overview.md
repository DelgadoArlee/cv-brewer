# Database Service System Overview

## 1. Purpose

The Database Service provides the application-level operations used to manage structured application data. It defines what data operations are available while delegating database-specific access to a Database Adapter. The service is owned by the Core application layer; the Database component supplies adapters.

## 2. Objectives

- Provide stable data operations for the Core Processing Engine.
- Store validated resume data for later retrieval and generation.
- Retrieve stored resume records by identifier or content fingerprint.
- Store resume processing run and step records for processing execution review.
- Store LLM activity log records for later review.
- Retrieve stored LLM activity logs as all records, newest records, or newest error-indicating records.
- Retrieve stored processing runs as all records, newest records, or newest error-indicating records, and retrieve steps for one run.
- Keep database implementation details outside application-level operations.
- Delegate persistence, queries, transactions, and errors to the selected Database Adapter.

## 3. Scope

### In Scope

- Application-level resume data operations.
- Resume data record definitions used by the service boundary.
- Application-level resume processing run and step persistence operations.
- Resume processing run and step record definitions used by the service boundary.
- Application-level LLM activity log persistence and query operations.
- Application-level processing run and step query operations.
- Coordination with a Database Adapter implementation.
- Reporting adapter failures to callers.

### Out of Scope

- SQLite connections, SQLAlchemy models, queries, transactions, and migrations.
- Resume validation, parsing, and generation.
- Resume processing workflow orchestration and run/step record construction.
- File-system and upload workflow management.
- Delete-all resume behavior, which belongs to the delete-resumes feature.

## 4. Workflow

The service receives application-level operations, prepares records for persistence, delegates requests to the configured Database Adapter, and returns resulting records or outcomes.

Resume operations store and retrieve resume records. Resume processing logging operations store run and step records independently of resume persistence, including runs that do not produce a stored parsed resume. Log query operations return stored LLM activity logs and processing run or step records for review; capped queries return the newest matching records, and step queries remain ordered by execution order unless a limit is supplied.

See the [Store Resume Process](/docs/system/database-service/processes/store-resume.md), [Retrieve Resume Process](/docs/system/database-service/processes/retrieve-resume.md), [Persist Resume Processing Run Process](/docs/system/database-service/processes/persist-resume-processing-run.md), [Persist Resume Processing Step Process](/docs/system/database-service/processes/persist-resume-processing-step.md), [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md), and [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md).

## 5. Constraints

- The service must not depend on SQLAlchemy, SQLite, or a specific database implementation.
- All database access must be performed through a Database Adapter implementation.
- Application-level resume data must follow the approved [User Resume Data Model](/docs/data/user-resume.md).
- Application-level processing log data must follow the approved [Resume Processing Run Data Model](/docs/data/resume-processing-run.md), [Resume Processing Step Data Model](/docs/data/resume-processing-step.md), and [Error Data Model](/docs/data/error.md).
- Application-level LLM activity log data must follow the approved [LLM Activity Log Data Model](/docs/data/llm-activity-log.md).
- The service must not perform resume validation, parsing, or processing workflow orchestration.
- The service must not provide the CLI with direct database access; the CLI must reach stored logs only through the service boundary.
- Log query capabilities must not require schema or migration changes.

## 6. Rules

- A resume must receive a unique identifier before it is persisted.
- A resume must receive a creation timestamp before it is persisted.
- Resume child data must preserve its original order.
- Content fingerprints must be unique across stored resumes.
- Lookups that find no matching record must return no record rather than failing.
- Processing run and step records must be stored without changing their recorded values.
- A processing step record must belong to exactly one processing run.
- `resume_id` and `matched_resume_id` on processing run records must be treated as identifier references only and must not imply database relationships to resume records.
- `source_step_id` on processing step records must be treated as an identifier reference only.
- An LLM activity log may reference a processing step through a nullable `processing_step_id`; a step may have many LLM logs, and an LLM log may reference zero or one step.
- Processing run and step records may include embedded `error` data; records without an error must preserve a null error value.
- Capped LLM log queries must order results by creation time descending, and capped processing run queries must order results by start time descending.
- Error-indicating LLM logs are those with `FAILED` or `TIMEOUT` status or with an error type or error message; error-indicating processing runs are those with `FAILED`, `VALIDATION_FAILED`, or `PARTIAL_SUCCESS` status or with an embedded error object.
- Step queries must remain ordered by step order and attempt number unless a caller supplies a limit; a limited step query must return the newest steps by start time first.

## 7. Data Management

The service manages resume records based on the [User Resume Data Model](/docs/data/user-resume.md), including metadata, parsed resume data, and validation status.

The service also manages resume processing execution records based on the [Resume Processing Run Data Model](/docs/data/resume-processing-run.md), [Resume Processing Step Data Model](/docs/data/resume-processing-step.md), and [Error Data Model](/docs/data/error.md). Processing run and step records are stored as execution logs; there is no per-resume processing history record.

## 8. Error Handling

- Database adapter failures must be reported to the caller.
- Duplicate content fingerprints must be reported as persistence failures.
- Missing resume records must not be treated as system errors.
- Processing-log persistence failures must be reported through standard logging and must not stop resume processing.
- LLM log delivery failures must be reported through standard logging and must not stop the originating workflow.
- Log query failures must be reported to the caller.

## 9. References

- [Database Component Technical Specification](/app/database/docs/technical-specification.md)
- [Database Service Technical Specification](/app/core/docs/system/database-service/overview.md)
- [Move the Database Service into Core](/docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [Add Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
- [User Resume Data Model](/docs/data/user-resume.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [LLM Activity Log Data Model](/docs/data/llm-activity-log.md)
- [Query LLM Logs Process](/docs/system/database-service/processes/query-llm-logs.md)
- [Query Processing Logs Process](/docs/system/database-service/processes/query-processing-logs.md)
