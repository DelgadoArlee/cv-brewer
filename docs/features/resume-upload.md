# Resume Upload Feature Overview

## 1. Purpose / Summary

The Resume Upload feature manages the discovery and initial handling of resume files in CVBrewery's designated input folder. It checks folder accessibility, discovers files, and coordinates with the Core Processing Engine to process discovered files and stores successfully parsed resume data when the required storage conditions are satisfied.

This feature handles file discovery, folder management, and processing coordination without performing validation, parsing, or storage operations directly.

## 2. Objective

- Check whether the input folder exists and is accessible.
- Create the input folder if it does not exist according to application rules.
- Determine whether the input folder contains files to process.
- Discover files in the input folder.
- Coordinate eligible files with the Core Processing Engine for resume extraction and parsing.
- Receive processing confirmation and outcomes from the Core Processing Engine.
- Handle individual file processing failures without interrupting other files.
- Complete the upload operation after all discovered files have reached a final outcome.

## 3. User Journey

```mermaid
flowchart TD
    A([Select upload resumes]) --> B{Resume folder available?}
    B -->|No| C[Create resume folder]
    B -->|Yes| D{Resumes available?}
    C --> D
    D -->|No| E[Ask user to add resume PDFs]
    E --> F[User adds resumes]
    F --> G[User confirms]
    G --> H{Resumes available?}
    H -->|Yes| I([Available resumes are saved for use])
    D -->|Yes| I
```

## 4. Systems

| System | Description |
|--------|-------------|
| [Resume Upload](../system/resume-upload/overview.md) | Manages input folder discovery, file coordination with Core Processing Engine, and handles individual file processing outcomes. |
| [Core Processing Engine](../system/resume-processing/overview.md) | Handles PDF validation, text extraction, resume parsing, schema validation, and data storage through the Database Service. |

## 5. References

- [Feature Overview Format Rules](../rules/feature.md)
- [Resume Upload System Overview](../system/resume-upload/overview.md)
- [Resume Processing System Overview](../system/resume-processing/overview.md)
- [File Type Verification Process](../system/resume-processing/processes/1-file-type-verification.md)
- [PDF Validation Process](../system/resume-processing/processes/4-pdf-validation.md)
- [PDF Extraction Process](../system/resume-processing/processes/5-pdf-extraction.md)
- [Schema Validation Process](../system/resume-processing/processes/7-schema-validation.md)

## 6. Acceptance Criteria

### Success Scenarios

**Given:** The input folder does not exist  
**When:** User initiates resume upload  
**Then:** System creates the input folder according to application rules  
**And:** User is prompted to add resume files  

**Given:** The input folder exists and contains PDF files  
**When:** User initiates resume upload  
**Then:** System discovers all eligible PDF files in the input folder  
**And:** System coordinates with Core Processing Engine for processing  
**And:** Successfully parsed resumes are stored in the database  

**Given:** Some files fail to process during upload  
**When:** Upload operation completes  
**Then:** Successfully processed files are stored  
**And:** Failed files do not interrupt other file processing  
**And:** User receives feedback on which files succeeded and which failed  

### Failure Scenarios

**Given:** The input folder is inaccessible or cannot be created  
**When:** User initiates resume upload  
**Then:** System displays an error message about folder access  
**And:** Upload operation does not proceed  

**Given:** No PDF files are found in the input folder  
**When:** User initiates resume upload  
**Then:** System prompts user to add resume files  
**And:** No processing occurs until files are added  

**Given:** All files fail validation or parsing  
**When:** Upload operation completes  
**Then:** System displays error messages for each failed file  
**And:** No resume data is stored in the database
