# Delete Resumes System Overview

## 1. Purpose

This feature allows users to delete all saved resume records from the system's storage. It provides a way for users to clean up their stored resume data when no longer needed, while maintaining security boundaries that prevent access to the input folder and file system beyond parsed resume data deletion. This operation deletes ALL resumes - selective or partial deletion is not supported.

## 2. Objectives

- Delete all parsed resume records from the database/storage
- Display a confirmation prompt before deletion occurs
- Provide clear feedback on deletion success or failure
- Prevent accidental deletion of original PDF files in the input folder
- Ensure no write/edit/delete access is granted to the file system beyond stored resume data
- Enforce all-or-nothing deletion (no selective or partial deletion allowed)

## 3. Scope

### In Scope

- Deleting ALL parsed resume data from storage/database
- Displaying confirmation dialog before deletion
- Informing the user that deletion affects only the database and not input folder files
- Providing success/error feedback messages
- Enforcing all-or-nothing deletion policy

### Out of Scope

- Deleting original PDF files from the input folder
- Modifying or accessing any file system beyond stored resume data
- Deleting job description data or generated resumes
- Accessing LLM services or external dependencies for deletion
- Implementing soft-delete functionality (only hard delete)
- Selective deletion of individual resumes
- Partial deletion of resume records

## 4. Workflow

The feature follows this workflow:

1. User initiates the Delete Imported Resumes action
2. System displays a confirmation prompt explaining that all imported resumes will be deleted from the database, input folder files are not deleted, and deleted resumes cannot be recovered
3. User confirms or cancels deletion
4. If confirmed, system deletes ALL parsed resume records (no selective deletion)
5. System validates deletion completion
6. System displays appropriate success or error message

See the [Uploaded Resume Management Feature](../../features/uploaded-resume-management.md) for the user journey.

## 5. Constraints

- Deletion is limited to parsed resume data only
- Original PDF files in the input folder are never modified or deleted
- No file system write/edit/delete permissions beyond stored resume storage
- Deletion requires explicit user confirmation
- **All resumes must be deleted together - selective or partial deletion is not supported**

## 6. Error Handling

The feature handles these error scenarios:

- **Deletion fails**: Display error message with appropriate details
- **No resumes to delete**: Inform user that no imported resumes were deleted
- **Permission denied**: Report if storage access is unavailable

## 7. Data Management

This feature operates on:

- **Parsed resume data**: Structured resume data stored in the database/storage for reuse
- **Original PDF files**: Located in input folder (never touched by this feature)
- **Generated resumes**: Not affected by this deletion operation
- **Job descriptions**: Not affected by this deletion operation

## 8. References

- [Requirements Document](../../requirements.md) - Section 4.1 Data Categories
- [Uploaded Resume Management Feature](../../features/uploaded-resume-management.md)
- [Delete All Resumes Process](processes/delete-all-resumes.md)
- [System Rules](../../system-rules.md) - File system access constraints
