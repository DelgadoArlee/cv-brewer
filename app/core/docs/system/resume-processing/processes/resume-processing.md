# Resume Processing Technical Process

## 1. Purpose

Define how the Core Processing Engine coordinates the complete resume-processing workflow for each supplied file.

## 2. Objective

- Process each file independently from supplied bytes.
- Apply file validation, metadata creation, deduplication, PDF validation, extraction, parsing, schema validation, and storage in order.
- Record a processing run and associated processing step logs for each processed file.
- Capture embedded error data and performance information in processing logs.
- Return a final outcome without stopping other files when one file fails.
- Notify callers of stage changes when a stage callback is supplied.

## 3. Scope

### In Scope

- Per-file orchestration under `app/core/pipeline/`.
- Stage sequencing, error translation, and outcome creation.
- Construction and finalization of processing run and step log records.
- Optional stage notifications using processing stage keys.
- Coordination with the Database Service and LLM Service through their interfaces.

### Out of Scope

- File-system discovery, reading, or writing.
- Database-specific connections, queries, and transactions.
- LLM transport and provider-specific communication.
- Resume generation and CLI presentation.

## 4. Rules & Constraints

- Operate only on `ResumeInput` bytes and metadata.
- Create a processing run record at the start of processing and finalize it with the terminal outcome.
- Record processing step records for executed steps and associate them with the processing run in a one-to-many relationship.
- Verify the PDF signature before any other processing stage.
- Build metadata and the content fingerprint before deduplication.
- Skip extraction, parsing, and storage of a new parsed resume record for duplicate fingerprints.
- Validate PDF structure and readable content before parsing.
- Run deterministic extraction before LLM enhancement.
- Validate parsed data against the Resume JSON Schema before storage.
- Do not store partial or invalid resume records.
- Record embedded error data in the affected processing run and/or step records when an error is captured, including `raw` details with traceback text.
- A processing run may reference `resume_id` and/or `matched_resume_id` as identifier references without a database relationship to resume records.
- A processing run may be finalized for stored, duplicate, rejected, or failed outcomes, including outcomes where no stored parsed resume is produced.
- Finalize a duplicate run with status `SUCCESS` and result `duplicate`, and record downstream steps as `SKIPPED`.
- Use `RUNNING`, `SUCCESS`, `FAILED`, `VALIDATION_FAILED`, `PARTIAL_SUCCESS`, `SKIPPED`, `CANCELLED`, or `TIMEOUT` for run and step status values.
- Convert failures into the matching `ResumeProcessingStatus`.
- Continue processing remaining files after a failure.
- Report log and persistence failures through the standard library logger without stopping processing.
- Emit stage notifications only when a callback is provided, using the processing step names `file_type_validation`, `metadata_extraction`, `deduplication`, `pdf_validation`, `content_extraction`, `parsing`, `schema_validation`, and `storage`.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([ResumeInput]) --> InitRun[Create processing run]
    InitRun --> FileType{PDF signature valid?}
    FileType -->|No| InvalidFileType[Record failure and finalize run]
    FileType -->|Yes| Metadata[Build metadata and fingerprint]
    Metadata --> Duplicate{Fingerprint stored?}
    Duplicate -->|Yes| DuplicateOutcome[Record duplicate outcome and finalize run]
    Duplicate -->|No| PdfValid{PDF valid?}
    PdfValid -->|No| InvalidPdf[Record failure and finalize run]
    PdfValid -->|Yes| Extract{Readable text?}
    Extract -->|No| Unreadable[Record failure and finalize run]
    Extract -->|Yes| Parse[Deterministic parse and LLM enhancement]
    Parse --> Schema{Schema valid?}
    Schema -->|No| SchemaInvalid[Record failure and finalize run]
    Schema -->|Yes| Store[Store through Database Service]
    Store -->|Failure| StorageFailure[Record storage failure and finalize run]
    Store -->|Success| Stored[Record stored outcome and finalize run]
````

### Steps

1. Create a processing run record for the supplied file.
2. Record processing step entries for executed stages with order, attempt, timing, input/output summaries, duration, memory and CPU performance measurements, metadata, and embedded error data as applicable.
3. Verify the supplied bytes start with the PDF signature.
4. Build file metadata and the raw-byte content fingerprint.
5. Query the Database Service for a resume with the same fingerprint.
6. Record a duplicate outcome with `matched_resume_id`, mark downstream steps `SKIPPED`, skip parsed resume storage, and finalize the run with status `SUCCESS` and result `duplicate`.
7. Validate PDF encryption, structure, and page count.
8. Extract readable text from the PDF.
9. Parse the text deterministically and enhance it with the LLM Service.
10. Validate the merged payload against the Resume JSON Schema.
11. Store the validated resume through the Database Service when validation succeeds.
12. Finalize the processing run with status, result, timing, summary, performance, `resume_id`/`matched_resume_id` identifier references as applicable, and embedded error data when recorded.

## 6. Modules

- `app/core/pipeline/resume_processing.py` — Coordinates stages, failures, outcomes, and stage callbacks.
- `app/core/models/resume.py` — Defines processing inputs, statuses, outcomes, and the stage callback type.
- `app/core/errors.py` — Defines processing errors translated into outcomes.

## 7. Data

- [User Resume Data Model](/docs/data/user-resume.md) — Defines the resume data contract.
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md) — Defines processing run execution records.
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md) — Defines processing step execution records.
- [Error Data Model](/docs/data/error.md) — Defines embedded error data for run and step records.
- [Resume JSON Schema](/app/core/services/resume/validation/schemas/resume.json) — Defines the parsed resume payload contract.

## 8. Testing

### 8.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-001 | A valid PDF resume and an available LLM model. | The resume is processed. | A stored outcome with a resume ID is returned and a processing run with step records is finalized. |
| RP-002 | File content without a PDF signature. | The file is processed. | An invalid file type outcome is returned and the processing run is finalized with recorded error data. |
| RP-003 | A stored resume with the same fingerprint. | The duplicate is processed. | A duplicate outcome with the matched resume ID is returned; the run is finalized with status `SUCCESS` and result `duplicate`, downstream steps are `SKIPPED`, and no new parsed resume is stored. |
| RP-004 | Multiple files where one fails. | All files are processed. | Remaining files continue and each returns its own outcome with an independently finalized processing run. |
| RP-005 | A stage callback is supplied. | A resume is processed. | Stage keys are emitted in processing order and corresponding step records are associated with the processing run. |
| RP-006 | A log sink or persistence operation fails. | A resume is processed. | The failure is reported through the standard library logger and the outcome is returned. |

## 9. References

- [Resume Processing System Overview](/app/core/docs/system/resume-processing/overview.md)
- [Resume Processing High-Level Process](/docs/system/resume-processing/processes/resume-processing.md)
- [Core Component Technical Specification](/app/core/docs/technical-specification.md)
- [Add Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
- [Record resume processing runs and steps in Core](/app/core/docs/adr/11-19-26/resume-processing-run-logging.md)
- [Establish the resume-processing foundation](/app/core/docs/adr/11-12-26/resume-processing-foundation.md)
