# Resume Processing Technical System Specification

## 1. Purpose

Defines the Core Processing Engine system that turns uploaded PDF resume bytes into validated, structured resume data. The system owns file-type and PDF validation, content extraction, deterministic parsing, LLM-assisted enhancement, schema validation, deduplication, and storage coordination through the Database Service.

## 2. Objective

- Validate that uploaded content is a PDF before further processing.
- Produce file metadata and a raw-byte content fingerprint for deduplication.
- Reject duplicate resumes without storing new records.
- Reject encrypted, structurally invalid, or unreadable PDFs.
- Extract readable text from valid PDF resumes.
- Produce structured resume data using deterministic extraction followed by LLM enhancement.
- Validate structured resume data against the Resume JSON Schema.
- Store valid resume records through the Database Service.
- Return a final outcome for each processed file without allowing one failure to stop other files.
- Optionally notify callers of the current processing stage while a file is processed.

## 3. Scope

### In Scope

- The resume-processing system under `core/src/core/pipeline/`, `core/src/core/modules/`, `core/src/core/validation/`, and `core/src/core/models/`.
- File signature verification on supplied file bytes.
- File metadata and raw-byte fingerprint creation.
- Deduplication against stored resume records.
- PDF encryption, structure, and readable-content validation.
- PDF text extraction.
- Deterministic resume parsing and LLM enhancement.
- Resume JSON Schema validation and conversion to Database Service records.
- Per-file processing outcomes and processing history.

### Out of Scope

- Input folder discovery and file-system access, which belong to the CLI.
- Reading or writing original PDF files.
- Database-specific connections, queries, transactions, migrations, and error translation.
- LLM service communication, configuration, and error translation.
- Resume generation, template mapping, and Markdown rendering.
- CLI user interaction and result presentation.
- High-level schema and validation documentation.

## 4. Rules & Constraints

- The system must operate on file bytes supplied by the caller and must not access the file system.
- File signature verification must run before metadata extraction, deduplication, PDF validation, and content extraction.
- The content fingerprint must be the SHA-256 hash of the raw file bytes.
- Duplicate fingerprints must skip processing and storage.
- Encrypted or password-protected PDFs must be rejected.
- PDFs with invalid structure or no pages must be rejected.
- PDFs with no non-whitespace extracted text must be rejected.
- Deterministic extraction must run before LLM enhancement.
- LLM enhancement must always be invoked after deterministic extraction.
- LLM parsing must use the first model returned by the LLM Service.
- Parsed data must pass Resume JSON Schema validation before storage.
- The system must not store partial or invalid resume records.
- Each file must produce an independent outcome.
- Stage notifications, when requested, must use the processing stage keys recorded in processing history.
- The system must not import SQLAlchemy, SQLite, `httpx`, or Ollama-specific modules.
- The system must not fabricate resume information beyond the supplied document.

## 5. Process

| Process | Description | Specification |
| --- | --- | --- |
| Resume Processing | Coordinates file validation, extraction, parsing, schema validation, deduplication, and storage. | [Resume Processing Process](processes/resume-processing.md) |
| File Type Verification | Verifies the supplied bytes begin with the PDF signature. | [File Type Verification Process](processes/1-file-type-verification.md) |
| Metadata Extraction | Produces file metadata and a raw-byte content fingerprint. | [Metadata Extraction Process](processes/2-metadata-extraction.md) |
| Deduplication | Detects existing resumes with the same content fingerprint. | [Deduplication Process](processes/3-deduplication.md) |
| PDF Validation | Rejects encrypted, password-protected, or structurally invalid PDFs. | [PDF Validation Process](processes/4-pdf-validation.md) |
| PDF Extraction | Extracts readable text from valid PDFs. | [PDF Extraction Process](processes/5-pdf-extraction.md) |
| Data Parsing | Applies deterministic extraction followed by LLM enhancement. | [Data Parsing Process](processes/6-data-parsing.md) |
| Schema Validation | Validates structured resume data against the Resume JSON Schema. | [Schema Validation Process](processes/7-schema-validation.md) |

## 6. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| `ResumeService` | Database Service interface | Finds duplicates and stores validated resume records. |
| `LLMService` | LLM Service interface | Provides model discovery and structured generation for parsing enhancement. |
| `pypdf` | External library | Validates PDF encryption and structure. |
| `pdfplumber` | External library | Extracts text from valid PDFs. |
| `pydantic` | External library | Provides runtime resume data models. |
| `jsonschema` | External library | Validates resume data against the Resume JSON Schema. |

## 7. Test Cases

| Scenario ID | Given | When | Then |
| --- | --- | --- | --- |
| RP-SYS-001 | A valid PDF resume and an available LLM model. | The resume is processed. | A resume record is stored and a stored outcome is returned. |
| RP-SYS-002 | File content without a PDF signature. | The file is processed. | The file is rejected as an invalid file type and is not stored. |
| RP-SYS-003 | A stored resume with the same raw-byte fingerprint. | The duplicate file is processed. | The file is reported as a duplicate and no new record is stored. |
| RP-SYS-004 | An encrypted PDF. | The file is processed. | The file is rejected as invalid and is not stored. |
| RP-SYS-005 | A PDF with no non-whitespace extracted text. | The file is processed. | The file is rejected as unreadable and is not stored. |
| RP-SYS-006 | No LLM model is available. | A resume is processed. | The file fails with an LLM failure outcome and is not stored. |
| RP-SYS-007 | An LLM payload that fails Resume JSON Schema validation. | A resume is processed. | The file fails with a schema-invalid outcome and is not stored. |
| RP-SYS-008 | A valid resume and a failing Database Service. | The resume is processed. | The file fails with a storage failure outcome. |
| RP-SYS-009 | Multiple files where one file fails. | All files are processed. | Remaining files continue processing independently. |

## 8. Diagrams

````mermaid
flowchart TD
    Input[Resume bytes and file metadata] --> FileType{PDF signature valid?}
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
    Store --> Stored[Stored outcome]
````

## 9. Architecture Decision Log

| ADR | Decision Summary |
| --- | --- |
| [Organize Core packages by responsibility](../../adr/11-12-26/core-package-structure.md) | Separate pipeline processes, modules, validation, and models into dedicated packages and keep shared errors at the Core package root. |
| [Establish the resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) | Use raw-byte fingerprints, first-available model selection, always-on LLM enhancement, basic deterministic parsing, and a schema derived from the user resume data model. |

## 10. Data

- [User Resume Data Model](../../../../docs/data/user-resume.md) — Defines the resume data contract.
- [Resume JSON Schema](../../../src/core/validation/schemas/resume.json) — Defines the parsed resume data contract used for validation and structured LLM output.

## 11. References

- [Resume Processing System Overview](../../../../docs/system/resume-processing/overview.md)
- [Resume Processing Process](../../../../docs/system/resume-processing/processes/resume-processing.md)
- [Core Component Technical Specification](../../technical-specification.md)
- [User Resume Data Model](../../../../docs/data/user-resume.md)
- [Resume Persistence ADR](../../../../database/docs/adr/11-10-26/resume-persistence.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md)
- [Use pypdf and pdfplumber for PDF processing](../../../../docs/adr/Architecture/2026-11-04/pdf-processing.md)
- [Use JSON Schema and Pydantic for data validation](../../../../docs/adr/Architecture/2026-11-04/schema-validation.md)
- [Establish the resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md)
