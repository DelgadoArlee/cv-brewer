## 1. Purpose

This document defines the functional requirements for CVBrewer, an AI-powered resume generation application.

The application allows users to upload and parse existing resumes, provide a Job Description, select an LLM, and generate a tailored resume using their stored resume data.

For implementation details, component responsibilities, and architectural constraints, refer to system-rules.md.

## 2. Functional Requirements

### 2.1 Resume Upload and Parsing

- The system must allow users to provide PDF resumes for processing.
- The system must validate uploaded files before accepting them for processing.
- The system must extract readable content from valid PDF resumes.
- The system must parse extracted resume content into structured resume data.
- The system must validate parsed resume data against the Resume JSON schema.
- The system must store successfully parsed resume data for future reuse.
- The system must make stored resume data available for resume generation.

### 2.2 Job Description Processing

- The system must require a Job Description before generating a resume.
- The system must allow users to provide a Job Description for processing.
- The system must validate the provided Job Description.
- The system must parse the Job Description into structured data.
- The system must validate parsed Job Description data against the Job Description JSON schema.

### 2.3 LLM Selection

- The system must allow users to select which supported LLM handles resume generation.

### 2.4 Resume Generation

- The system must generate a tailored resume using the user's stored resume data and a valid Job Description.
- The system must use the selected LLM to perform resume generation.
- The system must validate generated resume data against the Generated Resume JSON schema.

## 3. System Constraints and Rules

### 3.1 Resume Validation

- Only PDF resumes that are not encrypted or password-protected are accepted for processing.
- A PDF resume must contain sufficient readable content to support parsing.
- A resume must pass PDF validation before it is accepted for processing.
- Parsed resume data must conform to the Resume JSON schema before it is stored.

### 3.2 Job Description Validation

- A Job Description must be provided before resume generation can begin.
- A Job Description must pass validation and conform to the Job Description JSON schema before it is used for generation.

### 3.3 Resume Generation Constraints

- Generated resume content must be based exclusively on the user's stored resume data.
- The Job Description may guide the selection, prioritization, and presentation of relevant resume information but must not be treated as a source of facts about the user.
- Generated resume data must conform to the Generated Resume JSON schema.

## 4. Data Management

### 4.1 Data Categories

The system shall distinguish between:

- **Original resume files:** PDF files placed in the input folder by the user.
- **Parsed resume data:** Structured resume data stored locally for reuse.
- **Job description data:** Validated and structured information derived from a provided job description.
- **Generated resume data:** Structured output produced by the Core and validated against the Generated Resume JSON schema.
- **Generated resume documents:** Rendered Markdown files saved in the output folder.


## 5. Deployment Requirements

### 5.1 LLM Deployment

- CLI operation shall use a locally served LLM.
- The CLI shall not require an external cloud-based LLM service for normal operation.
- The LLM service and model files shall be deployed separately from the CLI/Core executable bundle.

## 6. Version Control

- The project shall follow a monorepo version control strategy.
- The repository shall contain the CLI, Core, LLM, and other project components defined by the architecture.
- The repository shall maintain clear separation of component responsibilities.

## 7. References

- For implementation details, component responsibilities, and architectural constraints: system-rules.md
- For JSON schema definitions: schema/README.md (to be created)
- For feature documentation: docs/1.0.0/features/