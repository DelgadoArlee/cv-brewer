# Resume Processing Process

## 1. Purpose / Summary

This process handles the extraction of structured data from uploaded PDF resumes and prepares it for storage and reuse during resume generation. It validates file types, extracts metadata, detects duplicates, verifies PDF integrity, parses content into structured data, always enhances with LLM, validates against schema, and stores results for future use. The process also records a processing run and associated processing step logs, including embedded error data and performance information, so each processing execution can be reviewed independently of stored resume outcomes. The process ensures only valid, readable resumes are processed while preventing duplicate processing and maintaining data quality throughout the workflow.

## 2. Process Flow

````mermaid
flowchart TD
    Start([Resume Uploaded]) --> InitRun[Create Processing Run]
    InitRun --> FileType[file_type_validation]
    FileType --> FileTypeOk{File Type Valid?}
    FileTypeOk -->|No| ValidationFail[Finalize Run: VALIDATION_FAILED]
    FileTypeOk -->|Yes| Metadata[metadata_extraction]
    Metadata --> Dedup[deduplication]
    Dedup --> Duplicate{Duplicate Detected?}
    Duplicate -->|Yes| SkipRest[Mark remaining steps SKIPPED]
    SkipRest --> DuplicateDone[Finalize Run: SUCCESS, result duplicate]
    Duplicate -->|No| PdfValidation[pdf_validation]
    PdfValidation --> PdfOk{PDF Valid?}
    PdfOk -->|No| ValidationFail
    PdfOk -->|Yes| Content[content_extraction]
    Content --> ContentOk{Content Readable?}
    ContentOk -->|No| ValidationFail
    ContentOk -->|Yes| Parsing[parsing with LLM extraction]
    Parsing --> ParsingOk{Parsing Succeeded?}
    ParsingOk -->|No| Failed[Finalize Run: FAILED]
    ParsingOk -->|Yes| Schema[schema_validation]
    Schema --> SchemaOk{Schema Valid?}
    SchemaOk -->|No| ValidationFail
    SchemaOk -->|Yes| Storage[storage]
    Storage --> StorageOk{Storage Succeeded?}
    StorageOk -->|No| Failed
    StorageOk -->|Yes| Stored[Finalize Run: SUCCESS, result stored]
    ValidationFail --> End([End])
    Failed --> End
    DuplicateDone --> End
    Stored --> End
````

Processing step records are recorded for the eight processing steps during the run and linked to the processing run. Steps may include embedded error data, performance data, and input/output summaries. LLM activity logs may reference the step during which a language-model call was made.

## 3. Rules

- A processing run record must be created at the start of processing for each supplied file and finalized with a terminal outcome
- Processing step records must be recorded for executed steps and associated with the owning processing run in a one-to-many relationship
- The recorded steps must be `file_type_validation`, `metadata_extraction`, `deduplication`, `pdf_validation`, `content_extraction`, `parsing`, `schema_validation`, and `storage`
- A duplicate outcome must be recorded with run status `SUCCESS` and a duplicate result, and downstream steps must be recorded as `SKIPPED`
- File signature verification must be performed before any other processing step
- Metadata extraction must occur after successful file type validation
- Deduplication must always be performed after metadata extraction to prevent duplicate processing
- Deterministic extraction methods must be used first for resume data parsing
- LLM extraction must always be invoked after deterministic extraction, not only on failure
- Parsed resume data must not be fabricated or altered beyond what exists in the original document
- PDF validation must verify both encryption status and structural integrity before content extraction
- Content extraction must succeed to produce parseable resume data
- Schema validation must pass before any parsed data is stored for reuse
- Storage operations must go through the Database Service and Database Adapter layers
- Processing run and step log persistence must go through the Database Service and Database Adapter layers
- LLM communication must go through the LLM Service and LLM Adapter layers
- Duplicate resumes must be identified and filtered out during processing without storing a new parsed resume record
- Invalid file types must be rejected with appropriate error messages
- Encrypted or password-protected PDFs must be rejected as unreadable
- Resumes with insufficient readable content must be rejected as unparsable
- Schema validation failures must be reported with specific issues for user notification
- Processing run and step records must include embedded error data when an error is recorded
- A processing run may reference `resume_id` and/or `matched_resume_id` as identifier references without creating database relationships to resume records
- A processing run may be finalized for stored, duplicate, rejected, or failed outcomes, including cases where no stored parsed resume is produced
- Log and processing-log persistence failures must be reported through standard logging and must not stop resume processing

## 4. Constraints

- Only non-encrypted, non-password-protected PDF resumes are accepted for processing
- PDFs must contain sufficient readable content to support reliable parsing
- Parsed resume data must conform to the Resume JSON schema before storage
- The Core Processing Engine remains independent of any specific storage technology or database implementation
- Original PDF files in the input folder are never deleted during parsing
- LLM operations must go through the LLM Service and its configured adapter without direct external calls
- Resume and processing log storage are managed through the Database Service abstraction layer
- Processing run and step records may be finalized for outcomes that do not produce a stored parsed resume
- `resume_id`, `matched_resume_id`, and `input.source_step_id` are identifier references and do not imply database relationships
- An LLM activity log may reference a processing step through a nullable identifier; a step can have many LLM logs, and an LLM log can reference zero or one step
- Callers may receive notifications of the current processing stage while a file is processed
- File type validation uses signature verification rather than file extension checking

## 5. References

- [Resume Processing System Overview](/docs/system/resume-processing/overview.md)
- [File Type Verification Process](/docs/system/resume-processing/processes/1-file-type-verification.md)
- [Metadata Extraction Process](/docs/system/resume-processing/processes/2-metadata-extraction.md)
- [Deduplication Process](/docs/system/resume-processing/processes/3-deduplication.md)
- [PDF Validation Process](/docs/system/resume-processing/processes/4-pdf-validation.md)
- [PDF Extraction Process](/docs/system/resume-processing/processes/5-pdf-extraction.md)
- [Data Parsing Process](/docs/system/resume-processing/processes/6-data-parsing.md)
- [Schema Validation Process](/docs/system/resume-processing/processes/7-schema-validation.md)
- [User Resume Data Model](/docs/data/user-resume.md)
- [Resume Processing Run Data Model](/docs/data/resume-processing-run.md)
- [Resume Processing Step Data Model](/docs/data/resume-processing-step.md)
- [Error Data Model](/docs/data/error.md)
- [Add Resume Processing Run and Step Logging](/docs/adr/Architecture/2026-11-19/resume-processing-run-logging.md)
