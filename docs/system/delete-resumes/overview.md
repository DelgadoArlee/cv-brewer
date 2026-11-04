# Delete Resumes Feature Overview

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
- Validating user authorization for deletion operation
- Providing success/error feedback messages
- Maintaining audit trail of deletion operations
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

1. User initiates delete all saved resumes action
2. System displays confirmation prompt with clear indication that ALL resumes will be deleted
3. User confirms or cancels deletion
4. If confirmed, system deletes ALL parsed resume records (no selective deletion)
5. System validates deletion completion
6. System displays appropriate success or error message

See [User Journey Diagram](../../user-journey/delete-saved-resumes.md) for visual representation.

## 5. Constraints

- Deletion is limited to parsed resume data only
- Original PDF files in the input folder are never modified or deleted
- No file system write/edit/delete permissions beyond stored resume storage
- Deletion requires explicit user confirmation
- Only one deletion operation per session (no batch partial deletions)
- **All resumes must be deleted together - selective or partial deletion is not supported**

## 6. Error Handling

The feature handles these error scenarios:

- **Deletion fails**: Display error message with appropriate details
- **No resumes to delete**: Inform user that no saved resumes exist
- **Permission denied**: Report if storage access is unavailable
- **Partial deletion failure**: Report which records failed and why (if any)

## 7. Data Management

This feature operates on:

- **Parsed resume data**: Structured resume data stored in the database/storage for reuse
- **Original PDF files**: Located in input folder (never touched by this feature)
- **Generated resumes**: Not affected by this deletion operation
- **Job descriptions**: Not affected by this deletion operation

## 8 References

- [Requirements Document](../../requirements.md) - Section 4.1 Data Categories
- [User Journey Diagram](../../user-journey/delete-saved-resumes.md)
- [System Rules](../../rules/system-rules.md) - File system access constraints
