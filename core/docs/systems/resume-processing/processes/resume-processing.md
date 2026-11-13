# Resume Processing Technical Process

## 1. Purpose

Define how the Core Processing Engine coordinates the complete resume-processing workflow for each supplied file.

## 2. Objective

- Process each file independently from supplied bytes.
- Apply file validation, metadata creation, deduplication, PDF validation, extraction, parsing, schema validation, and storage in order.
- Return a final outcome without stopping other files when one file fails.
- Notify callers of stage changes when a stage callback is supplied.

## 3. Scope

### In Scope

- Per-file orchestration under `core/src/core/pipeline/`.
- Stage sequencing, error translation, and outcome creation.
- Optional stage notifications using processing stage keys.
- Coordination with the Database Service and LLM Service through their interfaces.

### Out of Scope

- File-system discovery, reading, or writing.
- Database-specific connections, queries, and transactions.
- LLM transport and provider-specific communication.
- Resume generation and CLI presentation.

## 4. Rules & Constraints

- Operate only on `ResumeInput` bytes and metadata.
- Verify the PDF signature before any other processing stage.
- Build metadata and the content fingerprint before deduplication.
- Skip extraction, parsing, and storage for duplicate fingerprints.
- Validate PDF structure and readable content before parsing.
- Run deterministic extraction before LLM enhancement.
- Validate parsed data against the Resume JSON Schema before storage.
- Do not store partial or invalid records.
- Convert failures into the matching `ResumeProcessingStatus`.
- Continue processing remaining files after a failure.
- Emit stage notifications only when a callback is provided.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([ResumeInput]) --> FileType{PDF signature valid?}
    FileType -->|No| InvalidFileType[Invalid file type outcome]
    FileType -->|Yes| Metadata[Build metadata and fingerprint]
    Metadata --> Duplicate{Fingerprint stored?}
    Duplicate -->|Yes| DuplicateOutcome[Duplicate outcome]
    Duplicate -->|No| PdfValid{PDF valid?}
    PdfValid -->|No| InvalidPdf[Invalid PDF outcome]
    PdfValid -->|Yes| Extract{Readable text?}
    Extract -->|No| Unreadable[Unreadable outcome]
    Extract -->|Yes| Parse[Deterministic parse and LLM enhancement]
    Parse --> Schema{Schema valid?}
    Schema -->|No| SchemaInvalid[Schema invalid outcome]
    Schema -->|Yes| Store[Store through Database Service]
    Store -->|Failure| StorageFailure[Storage failure outcome]
    Store -->|Success| Stored[Stored outcome]
````

### Steps

1. Verify the supplied bytes start with the PDF signature.
2. Build file metadata and the raw-byte content fingerprint.
3. Query the Database Service for a resume with the same fingerprint.
4. Return a duplicate outcome when a matching resume exists.
5. Validate PDF encryption, structure, and page count.
6. Extract readable text from the PDF.
7. Parse the text deterministically and enhance it with the LLM Service.
8. Validate the merged payload against the Resume JSON Schema.
9. Store the validated resume through the Database Service and return the outcome.

## 6. Modules

- `core/src/core/pipeline/resume_processing.py` — Coordinates stages, failures, outcomes, and stage callbacks.
- `core/src/core/models/resume.py` — Defines processing inputs, statuses, outcomes, and the stage callback type.
- `core/src/core/errors.py` — Defines processing errors translated into outcomes.

## 7. Data

- [User Resume Data Model](../../../../../docs/data/user-resume.md) — Defines the resume data contract.
- [Resume JSON Schema](../../../../src/core/validation/schemas/resume.json) — Defines the parsed resume payload contract.

## 8. Testing

### 8.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-001 | A valid PDF resume and an available LLM model. | The resume is processed. | A stored outcome with a resume ID is returned. |
| RP-002 | File content without a PDF signature. | The file is processed. | An invalid file type outcome is returned. |
| RP-003 | A stored resume with the same fingerprint. | The duplicate is processed. | A duplicate outcome with the existing resume ID is returned. |
| RP-004 | Multiple files where one fails. | All files are processed. | Remaining files continue and each returns its own outcome. |
| RP-005 | A stage callback is supplied. | A resume is processed. | Stage keys are emitted in processing order. |

## 9. References

- [Resume Processing System Overview](../overview.md)
- [Resume Processing High-Level Process](../../../../../docs/system/resume-processing/processes/resume-processing.md)
- [Core Component Technical Specification](../../../technical-specification.md)
- [Establish the resume-processing foundation](../../../adr/11-12-26/resume-processing-foundation.md)
