# Resume Processing Process

## 1. Purpose / Summary

This process handles the extraction of structured data from uploaded PDF resumes and prepares it for storage and reuse during resume generation. It validates file types, extracts metadata, detects duplicates, verifies PDF integrity, parses content into structured data, always enhances with LLM, validates against schema, and stores results for future use. The process ensures only valid, readable resumes are processed while preventing duplicate processing and maintaining data quality throughout the workflow.

## 2. Process Flow

```` mermaid
flowchart TD
    Start([Resume Uploaded]) --> ValidateFileType{File Type Valid?}
    ValidateFileType -->|No| RejectInvalid[Reject: Invalid File Type]
    ValidateFileType -->|Yes| ExtractMetadata[Extract Metadata]
    ExtractMetadata --> CheckDuplicates{Duplicate Detected?}
    CheckDuplicates -->|Yes| SkipProcessing[Skip Processing]
    CheckDuplicates -->|No| ValidatePDF{PDF Valid?}
    ValidatePDF -->|No| RejectEncrypted[Reject: Encrypted/Invalid PDF]
    ValidatePDF -->|Yes| ExtractContent[Extract Content]
    ExtractContent --> ParseData[Parse to Structured Data]
    ParseData --> LLMEnhance[LLM Enhancement]
    LLMEnhance --> ValidateSchema{Schema Valid?}
    ValidateSchema -->|No| RejectSchema[Reject: Schema Validation Failed]
    ValidateSchema -->|Yes| StoreData[Store Parsed Data]
    StoreData --> Success([Success: Resume Stored])
    RejectInvalid --> End([End])
    SkipProcessing --> End
    RejectEncrypted --> End
    RejectSchema --> End
````

## 3. Rules

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
- LLM communication must go through the LLM Service and LLM Adapter layers
- Duplicate resumes must be identified and filtered out during processing without storage
- Invalid file types must be rejected with appropriate error messages
- Encrypted or password-protected PDFs must be rejected as unreadable
- Resumes with insufficient readable content must be rejected as unparsable
- Schema validation failures must be reported with specific issues for user notification

## 4. Constraints

- Only non-encrypted, non-password-protected PDF resumes are accepted for processing
- PDFs must contain sufficient readable content to support reliable parsing
- Parsed resume data must conform to the Resume JSON schema before storage
- The Core Processing Engine remains independent of any specific storage technology or database implementation
- Original PDF files in the input folder are never deleted during parsing
- LLM operations must go through the LLM Service and its configured adapter without direct external calls
- Storage is managed exclusively through the Database Service abstraction layer
- Callers may receive notifications of the current processing stage while a file is processed
- File type validation uses signature verification rather than file extension checking

## 5. References

- [Resume Processing System Overview](../overview.md)
- [File Type Verification Process](1-file-type-verification.md)
- [Metadata Extraction Process](2-metadata-extraction.md)
- [Deduplication Process](3-deduplication.md)
- [PDF Validation Process](4-pdf-validation.md)
- [PDF Extraction Process](5-pdf-extraction.md)
- [Data Parsing Process](6-data-parsing.md)
- [Schema Validation Process](7-schema-validation.md)
- [User Resume Data Model](../../../data/user-resume.md)
