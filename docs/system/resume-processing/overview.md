# Resume Processing system Overview

## 1. Purpose

This system handles the extraction of structured data from uploaded PDF resumes and prepares it for storage and reuse during resume generation. It ensures that only valid, readable resumes are processed and that extracted data conforms to the required schema before being stored. The system now includes file type validation using signature verification, metadata extraction, and deduplication to prevent processing duplicate resumes.

## 2. Objectives

- Verify file type using file signature validation
- Extract metadata from uploaded resume files
- Detect and remove duplicate resumes based on extracted content
- Extract readable content from uploaded PDF resumes
- Parse extracted content into structured resume data
- Validate parsed resume data against the Resume JSON schema
- Store successfully parsed resume data for future reuse
- Make stored resume data available for resume generation workflows
- Avoid reprocessing resumes when their parsed data is already available

## 3. Scope

### In Scope

- File type validation using file signature verification
- Metadata extraction from uploaded resume files
- Deduplication of resume files based on extracted content
- PDF file validation (structural validity, encryption status)
- Text extraction from valid PDF resumes
- Deterministic parsing of resume content into structured data
- LLM-based extraction to supplement deterministic extraction results
- Schema validation of extracted resume data
- Storage of validated parsed resume data
- Retrieval of stored parsed resume data for generation workflows

### Out of Scope

- File upload handling (handled by CLI input folder management)
- Original PDF file storage and management (CLI owns original files)
- Job description processing
- Resume generation logic
- Resume output rendering to output documents

## 4. Workflow

The resume processing workflow follows these steps:

1. **File Type Validation**: The Core verifies the uploaded file is a valid PDF using file signature verification
2. **Metadata Extraction**: Metadata is extracted from the validated PDF file
3. **Deduplication**: Duplicate resumes are detected and filtered out based on extracted content
4. **PDF Validation**: Each remaining PDF undergoes validation checks before processing
   - Verify the PDF is not encrypted or password-protected
   - Check structural integrity of the PDF document
5. **Content Extraction**: Valid PDFs are processed to extract readable text content from all pages
6. **Data Parsing**: Extracted content is parsed into structured resume data using deterministic methods first
7. **LLM Enhancement**: LLM extraction is always invoked after deterministic extraction to handle information that cannot be reliably extracted deterministically
8. **Schema Validation**: Parsed data is validated against the Resume JSON schema to ensure completeness and correctness
9. **Storage**: Validated parsed data is stored for future reuse during generation workflows
10. **Retrieval**: Stored parsed data is made available when needed for resume generation

## 5. Constraints

- Only non-encrypted, non-password-protected PDF resumes are accepted
- PDFs must contain sufficient readable content to support parsing (determined by text extraction results)
- Parsed resume data must conform to the Resume JSON schema before storage
- The Core remains independent of any specific storage technology or database implementation
- Storage is managed through the Database Service and Database Adapter
- Duplicate resumes are identified and filtered out during processing
- Original PDF files in the input folder are never deleted during parsing
- LLM operations go through the LLM Provider and LLM Adapter layers

## 6. Rules

- File signature verification is performed before any other processing
- Metadata extraction occurs after file type validation
- Deduplication is always performed after metadata extraction
- Deterministic extraction methods are used first for resume data extraction
- LLM extraction is always invoked after deterministic extraction, not only on failure
- LLM handles information that cannot be reliably extracted through deterministic methods
- Parsed resume data must not be fabricated or altered beyond what exists in the original document
- All database operations go through the Database Service and Database Adapter
- LLM communication goes through the LLM Provider and LLM Adapter

## 7. Validation

The following validation responsibilities apply:

| Validation Step                              | Responsible Component | Reference                                                                     |
| -------------------------------------------- | --------------------- | ----------------------------------------------------------------------------- |
| File type signature verification             | Core                  | [File Type Validation Rules](../file-type-validation/file-type-validation.md) |
| PDF structural validity and encryption check | Core                  | [PDF Validation Rules](../pdf-validation/pdf-validation.md)                   |
| Resume JSON schema validation                | Core                  | [Resume JSON Schema](../../schema/resume-schema.md)                           |
| Readable content verification                | Core                  | [Content Extraction Rules](../content-extraction/content-extraction-rules.md) |

## 8. Data Management

The system works with the following data categories:

- **Original resume files**: PDF files in the input folder (managed by CLI)
- **Metadata**: Extracted metadata from validated PDF files
- **Parsed resume data**: Structured data stored through Database Service for reuse
- **Resume JSON schema**: Contract for parsed resume data structure

Refer to [Data Model Documentation](../data-models/resume-data-model.md) for detailed data structure definitions.

## 9. Error Handling

The system handles the following error scenarios:

- **Invalid file type**: Reject with appropriate error message if file signature does not match PDF
- **Encrypted or password-protected PDF**: Reject as unreadable
- **Insufficient readable content**: Reject as unparsable (determined by text extraction results)
- **Schema validation failure**: Reject parsed data and report specific issues
- **Storage errors**: Report to CLI for user notification through Database Service
- **Duplicate resume detected**: Skip processing and log duplicate detection


