# Delete All Resumes Process Document

## 1. Purpose / Summary

This process handles the deletion of all imported resume records from the database. It allows users to clean up stored resume data while keeping original PDF files in the input folder untouched. The operation enforces an all-or-nothing deletion policy where ALL resumes must be deleted together; selective or partial deletion is not supported.

## 2. Process Flow

```` mermaid
flowchart TD
    A([User selects Delete Imported Resumes]) --> B[Explain database-only deletion and permanence]
    B --> C{User confirms deletion?}
    C -->|No| D[Cancel operation]
    C -->|Yes| E[Delete ALL imported resume records]
    E --> F{Deletion completed successfully?}
    F -->|No| G[Report failure with details]
    F -->|Yes| H[Display success message]
    D --> I([End Process])
    G --> I
    H --> I
````

## 3. Rules

- **must** display a clear confirmation prompt before any deletion occurs
- **must** inform the user that deletion clears imported resumes from the database only
- **must** inform the user that files in the input folder are not deleted
- **must** inform the user that deleted resumes cannot be recovered from the database
- **must** delete ALL parsed resume records from storage/database; selective or partial deletion is not supported
- **must** display appropriate success or error feedback messages after completion
- **must** ensure original PDF files in the input folder are never modified, accessed, or deleted
- **must** handle deletion as all-or-nothing; if deletion fails, report the failure and retain the stored records
- **must** not implement soft-delete functionality; only hard delete is supported

## 4. Constraints

- Deletion is limited strictly to parsed resume data stored in the database/storage
- Original PDF files located in the input folder are never touched by this process
- No file system write/edit/delete permissions are granted beyond stored resume storage
- User confirmation is required before any deletion can proceed
- Deletion cannot be undone once completed

## 5. References

- [Uploaded Resume Management Feature](/docs/features/uploaded-resume-management.md)
- [Delete Resumes System Overview](/docs/system/delete-resumes/overview.md)
- [System Rules](/docs/system-rules.md) - File system access constraints
