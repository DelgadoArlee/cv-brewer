# User Resume Data Model

## 1. Description

This document defines the data model for user-uploaded resumes in the CVBrewer system. The model describes the structure and relationships of resume-related data stored in the database, including original file references, extracted metadata, parsed content, validation status, and processing history. This data model supports the resume processing workflow from upload through storage and retrieval for generation workflows.

## 2. JSON Model

```json
{
  "resume_id": "string",
  "original_file_path": "string",
  "metadata": {
    "file_name": "string",
    "file_size_bytes": "number",
    "upload_timestamp": "datetime",
    "content_fingerprint": "string"
  },
  "parsed_data": {
    "personal_info": {
      "name": "string",
      "email": "string",
      "phone": null,
      "address": null,
      "linkedin_url": null,
      "github_url": null
    },
    "summary": null,
    "experience": [
      {
        "company": "string",
        "position": "string",
        "start_date": "date",
        "end_date": null,
        "description": "string"
      }
    ],
    "education": [
      {
        "institution": "string",
        "degree": "string",
        "field_of_study": null,
        "start_date": "date",
        "end_date": null
      }
    ],
    "skills": ["string"],
    "certifications": [
      {
        "name": "string",
        "issuer": "string",
        "issue_date": "date",
        "expiry_date": null
      }
    ]
  },
  "validation_status": {
    "file_type_valid": "boolean",
    "metadata_extraction_success": "boolean",
    "deduplication_result": "string",
    "pdf_encryption_check": "boolean",
    "pdf_structure_valid": "boolean",
    "content_extraction_success": "boolean",
    "schema_validation_passed": "boolean"
  },
  "processing_history": [
    {
      "step": "string",
      "timestamp": "datetime",
      "status": "string",
      "error_message": null
    }
  ],
  "created_at": "datetime",
  "deleted_at": "datetime"
}
```

## 3. Data Fields

### Resume Root Object

| Name               | Type     | Required | Description                                         |
| ------------------ | -------- | -------- | --------------------------------------------------- |
| resume_id          | string   | Yes      | Unique identifier for the resume record             |
| original_file_path | string   | Yes      | Path to the original PDF file in input folder       |
| metadata           | object   | Yes      | Extracted metadata from the PDF file                |
| parsed_data        | object   | Yes      | Structured resume data extracted from PDF           |
| validation_status  | object   | Yes      | Results of all validation checks                    |
| processing_history | array    | Yes      | Log of processing steps and outcomes                |
| created_at         | datetime | Yes      | Timestamp when resume was uploaded                  |
| deleted_at         | datetime | No      | Timestamp when user manually deletes the resume record |

### Metadata Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_name | string | Yes | Original filename of the uploaded PDF |
| file_size_bytes | number | Yes | Size of the file in bytes |
| upload_timestamp | datetime | Yes | When the file was uploaded |
| content_fingerprint | string | Yes | Hash/fingerprint for deduplication |

### Parsed Data Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| personal_info | object | Yes | Personal contact information from resume |
| summary | string | No | Professional summary or objective |
| experience | array | Yes | Work experience entries |
| education | array | No | Educational background entries |
| skills | array | Yes | List of skills mentioned in resume |
| certifications | array | No | Professional certifications |

### Personal Info Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Full name of the candidate |
| email | string | Yes | Email address |
| phone | string | No | Phone number |
| address | string | No | Physical address |
| linkedin_url | string | No | LinkedIn profile URL |
| github_url | string | No | GitHub profile URL |

### Experience Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| company | string | Yes | Company name |
| position | string | Yes | Job title/position held |
| start_date | date | Yes | Start date of employment |
| end_date | date | No | End date of employment (null if current) |
| description | string | Yes | Job responsibilities and achievements |

### Education Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| institution | string | Yes | Educational institution name |
| degree | string | Yes | Degree obtained |
| field_of_study | string | No | Field of study or major |
| start_date | date | Yes | Start date of studies |
| end_date | date | No | End date of studies (null if current) |

### Certifications Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Certification name |
| issuer | string | Yes | Issuing organization |
| issue_date | date | Yes | Date certification was issued |
| expiry_date | date | No | Expiration date if applicable |

### Validation Status Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_type_valid | boolean | Yes | Result of file signature verification |
| metadata_extraction_success | boolean | Yes | Whether metadata extraction succeeded |
| deduplication_result | string | Yes | Duplicate status (unique/duplicate) |
| pdf_encryption_check | boolean | Yes | Whether PDF is not encrypted |
| pdf_structure_valid | boolean | Yes | Whether PDF structure is valid |
| content_extraction_success | boolean | Yes | Whether text extraction succeeded |
| schema_validation_passed | boolean | Yes | Whether parsed data passes schema validation |

### Processing History Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| step | string | Yes | Name of processing step |
| timestamp | datetime | Yes | When the step was executed |
| status | string | Yes | Success/failure/processing status |
| error_message | string | No | Error details if failed |

## 4. Validation

- **resume_id**: Must be a unique UUID or auto-generated identifier
- **original_file_path**: Must reference an existing file in the input folder
- **metadata.file_name**: Must match the actual filename of uploaded file
- **metadata.content_fingerprint**: Must be a consistent hash for deduplication
- **parsed_data.personal_info.name**: Required field, must not be empty
- **parsed_data.email**: Required field, must be valid email format
- **parsed_data.experience**: Array may be empty if no experience exists
- **parsed_data.education**: Optional array, may be empty
- **parsed_data.skills**: Must contain at least one skill if present
- **parsed_data.certifications**: Optional array, may be empty
- **validation_status.file_type_valid**: Must be true to proceed with processing
- **validation_status.schema_validation_passed**: Must be true for storage
- **deleted_at**: Timestamp when user manually deletes the resume record

## 5. References

- [Data Model Format Rules](../../rules/format/data-model-rules.md)
- [Resume Processing Feature Overview](../resume-processing/feature-overview.md)
