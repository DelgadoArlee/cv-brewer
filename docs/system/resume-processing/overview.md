# Resume Processing system Overview

## 1. Purpose

This system handles the extraction of structured data from uploaded PDF resumes and prepares it for storage and reuse during resume generation. It ensures that only valid, readable resumes are processed and that extracted data conforms to the required schema before being stored. The system now includes file type validation using signature verification, metadata extraction, and deduplication to prevent processing duplicate resumes.

## 2. Objectives

- Verify file type using file signature validation
- Extract metadata from uploaded resume files
- Detect and remove duplicate resumes based on raw file bytes
- Extract readable content from uploaded PDF resumes
- Parse extracted content into structured resume data
- Validate parsed resume data against the Resume JSON schema
- Store successfully parsed resume data for future reuse
- Record processing run and step execution logs for each processed file
- Capture embedded error data and performance information in processing logs
- Make stored resume data available for resume generation workflows
- Avoid reprocessing resumes when their parsed data is already available

## 3. Scope

### In Scope

- File type validation using file signature verification
- Metadata extraction from uploaded resume files
- Deduplication of resume files based on raw file bytes
- PDF file validation (structural validity, encryption status)
- Text extraction from valid PDF resumes
- Deterministic parsing of resume content into structured data
- LLM-based extraction to supplement deterministic extraction results
- Schema validation of extracted resume data
- Storage of validated parsed resume data
- Recording processing run and step execution logs, including embedded error data
- Retrieval of stored parsed resume data for generation workflows

### Out of Scope

- File upload handling (handled by CLI input folder management)
- Original PDF file storage and management (CLI owns original files)
- Job description processing
- Resume generation logic
- Resume output rendering to output documents
- Database-specific persistence implementation details

## 4. Workflow

The resume processing workflow follows these steps:

1. **Run Initialization**: A processing run record is created for the file being processed
2. **File Type Validation** (`file_type_validation`): The Core verifies the uploaded file is a valid PDF using file signature verification
3. **Metadata Extraction** (`metadata_extraction`): Metadata is extracted from the validated file bytes
4. **Deduplication** (`deduplication`): Duplicate resumes are detected based on the raw-byte content fingerprint
5. **PDF Validation** (`pdf_validation`): Each remaining PDF undergoes validation checks before processing
   - Verify the PDF is not encrypted or password-protected
   - Check structural integrity of the PDF document
6. **Content Extraction** (`content_extraction`): Valid PDFs are processed to extract readable text content from all pages
7. **Data Parsing** (`parsing`): Extracted content is parsed into structured resume data using deterministic methods first, with LLM extraction used to supplement information that cannot be reliably extracted deterministically
8. **Schema Validation** (`schema_validation`): Parsed data is validated against the Resume JSON schema to ensure completeness and correctness
9. **Storage** (`storage`): Validated parsed data is stored for future reuse during generation workflows
10. **Run Finalization**: The processing run record is finalized with status, result, timing, summary, performance, resume identifier references, and embedded error data
11. **Retrieval**: Stored parsed data is made available when needed for resume generation

The eight recorded processing steps are `file_type_validation`, `metadata_extraction`, `deduplication`, `pdf_validation`, `content_extraction`, `parsing`, `schema_validation`, and `storage`. Processing step records are captured for these steps within the run and are associated with the run in a one-to-many relationship. When a duplicate is detected, downstream steps are recorded as skipped.

## 5. Constraints

- Only non-encrypted, non-password-protected PDF resumes are accepted
- PDFs must contain at least one non-whitespace character of extracted text to support parsing
- Parsed resume data must conform to the Resume JSON schema before storage
- The Core remains independent of any specific storage technology or database implementation
- Storage is managed through the Database Service and Database Adapter
- Duplicate resumes are identified and filtered out during processing
- Original PDF files in the input folder are never deleted during parsing
- LLM operations go through the LLM Service and LLM Adapter layers

## 6. Rules

- File signature verification is performed before any other processing
- Metadata extraction occurs after file type validation
- Deduplication is always performed after metadata extraction
- The content fingerprint is the SHA-256 hash of the raw file bytes
- Deterministic extraction methods are used first for resume data extraction
- LLM extraction is always invoked after deterministic extraction, not only on failure
- LLM handles information that cannot be reliably extracted through deterministic methods
- Parsed resume data must not be fabricated or altered beyond what exists in the original document
- All database operations go through the Database Service and Database Adapter
- LLM communication goes through the LLM Service and LLM Adapter
- A processing run record must be created for each processed file and finalized with its terminal outcome
- Processing step records must be associated with their owning processing run in a one-to-many relationship
- Processing run and step records must capture embedded error data when an error is recorded
- A processing run may reference a saved parsed resume identifier (`resume_id`) or matched resume identifier (`matched_resume_id`) without creating a database relationship to resume records
- A processing run may be recorded for outcomes where no stored parsed resume is produced
- A duplicate outcome is recorded with run status `SUCCESS` and a duplicate result, with downstream steps recorded as `SKIPPED`
- Log and processing-log persistence failures must be reported through standard logging and must not stop resume processing

## 7. Validation

The following validation responsibilities apply:

| Validation Step                              | Responsible Component | Reference                                                                     |
| -------------------------------------------- | --------------------- | ----------------------------------------------------------------------------- |
| File type signature verification             | Core                  | [File Type Verification Process](/docs/system/resume-processing/processes/1-file-type-verification.md)       |
| PDF structural validity and encryption check | Core                  | [PDF Validation Process](/docs/system/resume-processing/processes/4-pdf-validation.md)                       |
| Resume JSON schema validation                | Core                  | [Schema Validation Process](/docs/system/resume-processing/processes/7-schema-validation.md)                 |
| Readable content verification                | Core                  | [PDF Extraction Process](/docs/system/resume-processing/processes/5-pdf-extraction.md)                       |
| Processing log record completeness           | Core                  | [Resume Processing Process](/docs/system/resume-processing/processes/resume-processing.md)                  |

## 8. Data Management

The system works with the following data categories:

- **Original resume files**: PDF files in the input folder (managed by CLI)
- **Metadata**: Extracted metadata from validated PDF files
- **Parsed resume data**: Structured data stored through Database Service for reuse
- **Resume JSON schema**: Contract for parsed resume data structure
- **Resume processing execution logs**: Run and step records stored through the Database Service for processing review
- **LLM activity logs**: Records that may reference the processing step during which a language-model call was made

Refer to [User Resume Data Model](/docs/data/user-resume.md), [Resume Processing Run Data Model](/docs/data/resume-processing-run.md), [Resume Processing Step Data Model](/docs/data/resume-processing-step.md), and [Error Data Model](/docs/data/error.md) for data structure definitions.

## 9. Error Handling

The system handles the following error scenarios:

- **Invalid file type**: Reject with appropriate error message if file signature does not match PDF
- **Encrypted or password-protected PDF**: Reject as unreadable
- **No non-whitespace readable content**: Reject as unreadable (determined by text extraction results)
- **Schema validation failure**: Reject parsed data and report specific issues
- **Storage errors**: Report to CLI for user notification through Database Service
- **Duplicate resume detected**: Skip processing and log duplicate detection
- **Processing failures**: Record embedded error data in the affected processing run and/or step records when an error is captured

Processing execution is recorded through run and step records; there is no per-resume processing history record. A processing run may be finalized with a non-stored outcome (such as rejection or duplication) while still referencing related identifiers where applicable.


