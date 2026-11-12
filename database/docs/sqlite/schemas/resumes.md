# Resumes Table Schema

## 1. Database Object Identification

- **Name:** `resumes`
- **Type:** Table

## 2. Purpose

Stores the root record for each uploaded and processed resume, including its original file reference, extracted metadata, personal information, validation status, and lifecycle timestamps.

## 3. Data Definition

| Name | Type | Constraints | Description |
| --- | --- | --- | --- |
| `resume_id` | TEXT | Primary Key, Not Null | Unique UUID for the resume record. |
| `original_file_path` | TEXT | Not Null | Path to the original PDF in the input folder. |
| `file_name` | TEXT | Not Null | Original filename of the uploaded PDF. |
| `file_size_bytes` | INTEGER | Not Null, Check `>= 0` | Size of the file in bytes. |
| `upload_timestamp` | DATETIME | Not Null | When the file was uploaded. |
| `content_fingerprint` | TEXT | Not Null, Unique | Hash used for deduplication. |
| `name` | TEXT | Not Null | Candidate full name. |
| `email` | TEXT | Not Null | Candidate email address. |
| `phone` | TEXT | Nullable | Candidate phone number. |
| `address` | TEXT | Nullable | Candidate physical address. |
| `linkedin_url` | TEXT | Nullable | LinkedIn profile URL. |
| `github_url` | TEXT | Nullable | GitHub profile URL. |
| `summary` | TEXT | Nullable | Professional summary or objective. |
| `file_type_valid` | BOOLEAN | Not Null | Result of file signature verification. |
| `metadata_extraction_success` | BOOLEAN | Not Null | Whether metadata extraction succeeded. |
| `deduplication_result` | TEXT | Not Null | Duplicate status recorded during processing. |
| `pdf_encryption_check` | BOOLEAN | Not Null | Whether the PDF is not encrypted. |
| `pdf_structure_valid` | BOOLEAN | Not Null | Whether the PDF structure is valid. |
| `content_extraction_success` | BOOLEAN | Not Null | Whether text extraction succeeded. |
| `schema_validation_passed` | BOOLEAN | Not Null | Whether parsed data passed schema validation. |
| `created_at` | DATETIME | Not Null | Timestamp when the resume record was created. |
| `deleted_at` | DATETIME | Nullable | Timestamp when the record was soft-deleted. |

Indexes:
- Unique index on `content_fingerprint`.
- Index on `created_at`.

## 4. Relationships

- One `resumes` record has zero or more records in `resume_experience`.
- One `resumes` record has zero or more records in `resume_education`.
- One `resumes` record has zero or more records in `resume_certifications`.
- One `resumes` record has zero or more records in `resume_skills`.
- One `resumes` record has zero or more records in `resume_processing_history`.

## 5. Validation

- `content_fingerprint` must be unique across all resume records.
- Required columns must not be null.
- `file_size_bytes` must not be negative.
- Child records must reference an existing `resume_id`.

## 6. References

- [SQLite Database Overview](../overview.md)
- [User Resume Data Model](../../../../docs/data/user-resume.md)
- [Database Component Technical Specification](../../technical-specification.md)
