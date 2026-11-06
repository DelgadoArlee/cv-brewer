# Resume Generation Feature Overview

## 1. Purpose

The resume generation feature creates tailored resume documents by combining a user's stored parsed resume data with a provided job description, using an external LLM to generate relevant content that matches the target role. This feature enables users to quickly produce customized resumes for specific job applications without manually rewriting their entire resume history.

## 2. Objectives

- Generate a tailored resume document based on stored user resume data and a valid job description
- Use the configured LLM to perform intelligent resume customization and content generation
- Validate generated resume data against the Generated Resume JSON schema before output
- Render the final resume as a Markdown document in the configured output folder
- Ensure generated content respects user's original resume information without fabrication

## 3. Scope

### In Scope

- Output folder initialization (check existence, create if missing)
- Job description validation and parsing using AI to extract structured job requirements
- Job description parsed data validation against Job Description JSON schema
- Retrieval of stored parsed resume data from database
- LLM-based resume generation using configured model/provider
- Generated resume schema validation
- Resume templating and Markdown rendering
- Output file storage in the designated output folder
- Error handling for invalid inputs, LLM failures, and generation errors

### Out of Scope

- Modifying or fabricating user's original resume information
- Storing generated resumes in the database (output files only)
- Direct access to external LLM services without using adapter layers
- Independent deployment of CLI or Core components
- Cloud-based LLM service bundling (users must provide their own LLM)

## 4. Workflow

The resume generation workflow follows these major steps:

1. **Output Folder Initialization**: System checks if output folder exists; creates it if missing without bypassing OS security; informs user of any creation failure
2. **Job Description Input**: User provides a job description for processing
3. **Job Description Parsing**: AI parses the job description to extract structured requirements, responsibilities, and qualifications using the LLM
4. **Job Description Parsing Validation**: Parsed job description data is validated against the Job Description JSON schema before proceeding
5. **Resume Data Retrieval**: System retrieves stored parsed resume data from database
6. **Generation Request**: Core sends generation request through LLM Provider and Adapter with both parsed user resume and parsed job description as reference inputs
7. **Content Generation**: LLM generates tailored resume content based on job requirements and user's original resume information
8. **Schema Validation**: Generated data is validated against the Generated Resume JSON schema
9. **Template Mapping**: Generated data is mapped to selected resume template
10. **Markdown Rendering**: Template is rendered as Markdown
11. **Output Storage**: Final Markdown file is saved to the output folder

Reference: [Resume Generation Process](processes/resume-generation-process.md)

## 5. Constraints

- Generated resume content must be based exclusively on the user's stored resume data
- The job description may guide selection, prioritization, and presentation but cannot introduce new facts about the user
- LLM operations must go through the configured Provider and Adapter layers
- Normal operation shall not depend on external cloud-based LLM services (though users may choose to use them)
- Generated outputs must conform to the Generated Resume JSON schema before rendering
- Output files must be saved in the designated output folder managed by CLI
- Output folder creation must respect OS security permissions and not bypass system restrictions

## 6. Rules

- Job description must be validated and parsed before generation can proceed
- Parsed job description data must conform to the Job Description JSON schema
- Stored resume data must exist and pass validation before being used for generation
- Generated content must not fabricate or alter user's original information
- Schema validation must pass before Markdown rendering is attempted
- Output files must follow the system's defined output storage rules
- Output folder creation must fail gracefully if permissions are insufficient

## 7. Validation

- Job description must conform to the Job Description JSON schema
- Parsed job description data must conform to the Job Description JSON schema after AI parsing
- Stored resume data must conform to the Resume JSON schema
- Generated resume data must conform to the Generated Resume JSON schema
- LLM adapter must handle connection and response validation
- Markdown rendering must complete successfully before file output

## 8. Data Management

This feature uses the following data models:

| Data Model | Purpose | Documentation Link |
|------------|---------|-------------------|
| Resume Data Model | Stores parsed resume information for reuse | [Resume Data Model](user-resume.md) |
| Job Description Schema | Defines structure for job description input | [Job Description Schema](../schema/job-description-schema.md) |
| Generated Resume Schema | Validates generated resume output | [Generated Resume Schema](../schema/generated-resume-schema.md) |

## 9. Error Handling

The feature handles the following error scenarios:

- **Invalid Job Description**: User is prompted to provide a valid job description
- **Job Description Parsing Validation Failure**: System identifies schema violations in parsed job description data and prompts user to re-enter
- **No Stored Resume Data**: System informs user that no parsed resumes are available for generation
- **LLM Connection Failure**: System reports connection issues and suggests checking LLM configuration
- **Schema Validation Failure**: System identifies specific schema violations in generated content
- **Markdown Rendering Failure**: System reports rendering errors and prevents corrupted output files
- **Output Folder Creation Failure**: System informs user if folder cannot be created due to permissions or other OS restrictions

## 12. References

- [System Architecture](../../../architecture.md)
- [Functional Requirements](../../../requirements.md)
- [General System Rules](docs/system-rules.md)
- [Feature Overview Format Rules](docs/rules/format/system-rules.md)
- [Resume Generation Process](processes/resume-generation-process.md)
