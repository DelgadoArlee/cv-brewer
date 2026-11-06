# Resume Generation Feature Overview

## 1. Purpose / Summary

The resume generation feature creates tailored resume documents by combining a user's stored parsed resume data with a provided job description, using an external LLM to generate relevant content that matches the target role. This feature enables users to quickly produce customized resumes for specific job applications without manually rewriting their entire resume history.

## 2. Objective

- Generate a tailored resume document based on stored user resume data and a valid job description
- Use the configured LLM to perform intelligent resume customization and content generation
- Validate generated resume data against the Generated Resume JSON schema before output
- Render the final resume as a Markdown document in the configured output folder
- Ensure generated content respects user's original resume information without fabrication

## 3. User Journey

```mermaid
flowchart TD
    A[User selects Generate Resume] --> B[Check output folder availability]
    B --> C{Output folder exists?}
    C -->|No| D[Create output folder]
    C -->|Yes| E[Enter job description]
    D --> E
    E --> F[Verify job description validity]
    F --> G{Job description valid?}
    G -->|No| H[Inform user of error]
    G -->|Yes| I[Check for available reference resumes]
    H --> J[Ask user to re-enter job description]
    J --> F
    I --> K{Reference resumes available?}
    K -->|No| L[Inform user no resumes available]
    K -->|Yes| M[Select reference resume]
    L --> N([Stop])
    M --> O[Generate resume using LLM]
    O --> P{Generation successful?}
    P -->|No| Q[Inform user of error]
    P -->|Yes| R[Save generated resume to output folder]
    Q --> S([Stop])
    R --> T([Complete])
```

## 4. Systems

| System                                                              | Description                                                                                                       |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [Resume Generation System](../system/resume-generation/overview.md) | Handles the complete resume generation workflow including input validation, LLM integration, and output rendering |

## 5. References

- [System Architecture](../../../architecture.md)
- [Functional Requirements](../../../requirements.md)
- [General System Rules](docs/system-rules.md)
- [Feature Overview Format Rules](docs/rules/format/feature-rules.md)
- [Resume Generation Process](processes/resume-generation-process.md)
- [Job Description Schema](../schema/job-description-schema.md)
- [Generated Resume Schema](../schema/generated-resume-schema.md)
- [Resume Data Model](user-resume.md)

## 6. Acceptance Criteria

### Success Scenarios

**Given:** User has stored parsed resume data in the database  
**When:** User provides a valid job description and selects generate resume  
**Then:** System generates a tailored resume using LLM  
**And:** Generated resume is validated against the Generated Resume JSON schema  
**And:** Final resume is rendered as Markdown in the output folder  
**And:** User receives confirmation of successful generation  

**Given:** Output folder does not exist  
**When:** User initiates resume generation  
**Then:** System creates the output folder according to application rules  
**And:** Generation process proceeds normally  

### Failure Scenarios

**Given:** Job description is invalid or missing required fields  
**When:** User attempts to generate a resume  
**Then:** System displays an error message about invalid job description  
**And:** Resume generation does not proceed  

**Given:** No reference resumes are available for selection  
**When:** User attempts to generate a resume  
**Then:** System informs user that no resumes are available  
**And:** Generation process stops until resumes are uploaded  

**Given:** LLM integration fails during content generation  
**When:** Resume generation is initiated  
**Then:** System displays an error message about generation failure  
**And:** No resume data is saved to the output folder  
**And:** User can retry the operation later  

**Given:** Generated resume fails schema validation  
**When:** Resume generation completes  
**Then:** System displays validation error with details  
**And:** Resume is not saved to the output folder  
**And:** User can review and correct the job description
