# Core Processing Engine Component Technical Specification

## 1. Purpose

This document defines the technical organization of the Core Processing Engine component within CVBrewer. It describes how the Core is structured and bounded so resume processing and generation workflows can operate without coupling to specific database or LLM implementations. The Core owns the application-level resume data operations and delegates database-specific work to the Database component.

## 2. Objective

- Provide a central processing boundary for CVBrewer's resume-related workflows.
- Validate uploaded files and PDF content before processing.
- Extract, parse, and validate resume data against approved schemas.
- Generate and validate tailored resume data using stored resume data and a job description.
- Render generated resume content as Markdown for the MVP.
- Own application-level resume data operations and record definitions as the Database Service.
- Depend on the LLM Service interface rather than a concrete implementation.
- Remain part of the single Python distribution used by the application.

## 3. Scope

### In Scope

- The Core component package and its internal subpackages.
- File-type signature verification and PDF validation.
- Metadata extraction and deduplication of uploaded resumes.
- Text extraction from validated PDF resumes.
- Deterministic and LLM-assisted resume data extraction and parsing.
- Resume, job description, and generated resume schema validation.
- Application-level resume data operations, record definitions, and repository contracts.
- Generation of tailored resume data from stored resume data and a job description.
- Resume template mapping and Markdown rendering.
- Coordination with the Database Service and LLM Service.
- Component technical documentation.

### Out of Scope

- CLI user interaction, input and output folder management, and file discovery.
- Database-specific connections, ORM behavior, queries, transactions, migrations, and error translation, which belong to the Database Adapter.
- LLM service communication and service-specific error handling, which belong to the LLM Adapter.
- Management of original PDF files and generated Markdown files.
- Data model and schema definitions, which are documented separately.
- System technical documentation.
- Implementation code and test cases.

## 4. Rules & Constraints

- The Core must perform file-type signature verification and PDF validation; the CLI must not filter files by type.
- The Core must operate on file bytes supplied by the CLI and must not access the file system directly.
- The Core must not import SQLAlchemy or SQLite directly and must perform database operations through the Database Service.
- The Core must not import database adapters; adapters implement Core-owned repository contracts.
- The Core must communicate with LLMs through the LLM Service and must not depend on a specific LLM implementation.
- Only PDF resumes that are not encrypted or password-protected and that contain sufficient readable content may be processed.
- Parsed resume data must conform to the Resume JSON schema before storage.
- Job description data must conform to the Job Description JSON schema before generation.
- Generated resume data must conform to the Generated Resume JSON schema before rendering.
- Generated resume content must be based exclusively on the user's stored resume data; the job description may guide selection, prioritization, and presentation but must not introduce facts about the user.
- Generated resume data must not be stored in the database; rendered Markdown output is saved in the output folder by the CLI.
- The Core must not be independently deployed and must remain part of the combined CLI/Core executable.

## 5. Architectural & Design Approaches

### 5.1. Interface-Based Component Boundaries

- **Name:** Interface-based component boundaries.
- **Description:** The Core interacts with persistence and language-processing capabilities through application-level interfaces.
- **Application:** The Core owns the Database Service for structured data operations and uses the LLM Service for language-processing tasks, without depending on their concrete implementations.

### 5.2. Validation-First Processing

- **Name:** Validation-first processing.
- **Description:** Inputs and generated outputs are validated before they proceed through processing or are accepted.
- **Application:** File-type and PDF validation occur before extraction and parsing, and schema validation occurs before storage, generation, and rendering.

### 5.3. Byte-Oriented Processing Boundary

- **Name:** Byte-oriented processing boundary.
- **Description:** File discovery and file-system access are separated from content processing.
- **Application:** The CLI discovers files and supplies their bytes to the Core, and the Core performs all file-type and PDF validation on the supplied content.

### 5.4. Single-Project Internal Packaging

- **Name:** Single-project internal packaging.
- **Description:** The Core is maintained as a module within the single application Python project.
- **Application:** Core packages are organized under `app/core/` and packaged with the other components by the `app/` project.

### 5.5. Responsibility-Based Package Organization

- **Name:** Responsibility-based package organization.
- **Description:** Core code is organized by architectural responsibility so that orchestration, reusable processing services, validation, and data models remain distinct.
- **Application:** Pipeline processes use `pipeline/`, each processing module and its validation functions use its own `services/<service-name>/service.py`, resume-specific service code uses `services/resume/`, validation models and schemas use the owning service's `services/<service-name>/validation/`, non-validation models use `models/`, and shared errors use `core/errors.py`.

## 6. Systems

| System | Description | Specification |
| --- | --- | --- |
| Resume Processing | Validates uploaded files and PDFs, extracts and parses resume data, and validates it against the Resume JSON schema. | [Resume Processing](systems/resume-processing/overview.md) |
| Database Service | Defines application-level resume data operations and delegates persistence to a Database Adapter. | [Database Service](systems/database-service/overview.md) |
| Resume Generation | Generates and validates tailored resume data from stored resume data and a job description, then renders Markdown output. | Not yet documented |

## 7. File Structure

````text
app/core/
├── README.md               Component README file.
├── docs/
│   ├── technical-specification.md
│   ├── guidelines.md
│   ├── adr/
│   │   ├── ADL.md
│   │   ├── 11-12-26/
│   │   │   ├── core-package-structure.md
│   │   │   └── resume-processing-foundation.md
│   │   ├── 11-13-26/
│   │   │   ├── processing-service-packages.md
│   │   │   └── resume-service-package.md
│   │   └── 11-14-26/
│   │       └── processing-and-validation-service-packages.md
│   └── systems/
│       ├── database-service/
│       │   ├── overview.md
│       │   └── processes/
│       │       ├── retrieve-resume.md
│       │       └── store-resume.md
│       └── resume-processing/
│           ├── overview.md
│           └── processes/
│               ├── resume-processing.md
│               ├── 1-file-type-verification.md
│               ├── 2-metadata-extraction.md
│               ├── 3-deduplication.md
│               ├── 4-pdf-validation.md
│               ├── 5-pdf-extraction.md
│               ├── 6-data-parsing.md
│               └── 7-schema-validation.md
├── __init__.py
├── errors.py
├── models/
│   ├── __init__.py
│   └── resume.py
├── pipeline/
│   ├── __init__.py
│   └── resume_processing.py
├── services/
│   ├── __init__.py
│   ├── metadata/
│   │   ├── __init__.py
│   │   └── service.py
│   ├── parsing/
│   │   ├── __init__.py
│   │   └── service.py
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── service.py
│   └── resume/
│       ├── __init__.py
│       ├── models.py
│       ├── repository.py
│       ├── service.py
│       └── validation/
│           ├── __init__.py
│           ├── models/
│           │   ├── __init__.py
│           │   └── resume.py
│           └── schemas/
│               ├── __init__.py
│               └── resume.json
````

## 8. Deployment

- The Core is included in the single CLI/Core executable and is not independently deployable.
- The Python runtime and dependencies are bundled into per-OS executables built with PyInstaller.
- The Core includes the Database Service and uses the LLM Service within the application; the LLM service itself is installed and operated separately by the user.

## 9. References

- [System Architecture](../../../docs/architecture.md)
- [Repository Architecture](../../README.md)
- [Tech Stack](../../../docs/tech-stack.md)
- [Requirements](../../../docs/requirements.md)
- [General System Rules](../../../docs/system-rules.md)
- [Resume Processing System Overview](../../../docs/system/resume-processing/overview.md)
- [Resume Processing Technical System Specification](systems/resume-processing/overview.md)
- [Resume Processing Technical Process](systems/resume-processing/processes/resume-processing.md)
- [Database Service Technical System Specification](systems/database-service/overview.md)
- [Database Service System Overview](../../../docs/system/database-service/overview.md)
- [Move the Database Service into Core](../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md)
- [Establish the resume service package](adr/11-13-26/resume-service-package.md)
- [Organize processing modules as services](adr/11-13-26/processing-service-packages.md)
- [Organize processing and validation code by service packages](adr/11-14-26/processing-and-validation-service-packages.md)
- [Resume Generation System Overview](../../../docs/system/resume-generation/overview.md)
- [Use Python and uv for the CVBrewer implementation](../../../docs/adr/Architecture/2026-11-04/python-runtime-and-tooling.md)
- [Package CVBrewer as per-OS single executables with PyInstaller](../../../docs/adr/Architecture/2026-11-04/cross-platform-packaging.md)
- [Use pypdf and pdfplumber for PDF processing](../../../docs/adr/Architecture/2026-11-04/pdf-processing.md)
- [Use JSON Schema and Pydantic for data validation](../../../docs/adr/Architecture/2026-11-04/schema-validation.md)
- [Integrate local LLMs through a native Ollama adapter](../../../docs/adr/Architecture/2026-11-04/llm-integration.md)
- [Generate Markdown resumes for the MVP](../../../docs/adr/Architecture/2026-11-04/markdown-output-mvp.md)
- [Core owns file-type and PDF validation](../../../docs/adr/Architecture/2026-11-04/validation-responsibilities.md)
