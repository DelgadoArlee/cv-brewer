# Core Processing Engine Component Technical Specification

## 1. Purpose

This document defines the technical organization of the Core Processing Engine component within CVBrewer. It describes how the Core is structured and bounded so resume processing and generation workflows can operate without coupling to specific database or LLM implementations.

## 2. Objective

- Provide a central processing boundary for CVBrewer's resume-related workflows.
- Validate uploaded files and PDF content before processing.
- Extract, parse, and validate resume data against approved schemas.
- Generate and validate tailored resume data using stored resume data and a job description.
- Render generated resume content as Markdown for the MVP.
- Depend on the Database Service and LLM Service interfaces rather than concrete implementations.
- Remain part of the single Python distribution used by the application.

## 3. Scope

### In Scope

- The Core component package and its internal subpackages.
- File-type signature verification and PDF validation.
- Metadata extraction and deduplication of uploaded resumes.
- Text extraction from validated PDF resumes.
- Deterministic and LLM-assisted resume data extraction and parsing.
- Resume, job description, and generated resume schema validation.
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
- System and module technical documentation.
- Implementation code and test cases.

## 4. Rules & Constraints

- The Core must perform file-type signature verification and PDF validation; the CLI must not filter files by type.
- The Core must operate on file bytes supplied by the CLI and must not access the file system directly.
- The Core must not import SQLAlchemy or SQLite directly and must perform database operations through the Database Service.
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
- **Application:** The Core uses the Database Service for structured data operations and the LLM Service for language-processing tasks, without depending on their concrete implementations.

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
- **Description:** The Core is maintained as one Python project containing internal packages.
- **Application:** Core packages are organized under `core/src/core/` within the single application distribution.

### 5.5. Responsibility-Based Package Organization

- **Name:** Responsibility-based package organization.
- **Description:** Core code is organized by architectural responsibility so that orchestration, reusable processing, validation, and data models remain distinct.
- **Application:** Pipeline processes use `pipeline/`, non-validation modules use `modules/`, validation modules, models, and schemas use `validation/`, non-validation models use `models/`, and shared errors use `core/errors.py`.

## 6. Systems

| System | Description | Specification |
| --- | --- | --- |
| Resume Processing | Validates uploaded files and PDFs, extracts and parses resume data, and validates it against the Resume JSON schema. | [Resume Processing](systems/resume-processing/overview.md) |
| Resume Generation | Generates and validates tailored resume data from stored resume data and a job description, then renders Markdown output. | Not yet documented |

## 7. File Structure

````text
core/
├── pyproject.toml          Project configuration and package metadata.
├── README.md               Package README file.
├── .python-version         Python version selection.
├── docs/
│   ├── technical-specification.md
│   ├── guidelines.md
│   ├── adr/
│   │   ├── ADL.md
│   │   └── 11-12-26/
│   │       ├── core-package-structure.md
│   │       └── resume-processing-foundation.md
│   ├── modules/
│   │   ├── resume-processing/
│   │   │   ├── metadata.md
│   │   │   ├── parsing.md
│   │   │   └── pdf-processing.md
│   │   ├── validation/
│   │   │   ├── file-validation.md
│   │   │   ├── schema-validation.md
│   │   │   └── validation-models.md
│   │   ├── pipelines/
│   │   │   └── processor.md
│   │   └── models/
│   │       └── models.md
│   └── systems/
│       └── resume-processing/
│           └── overview.md
└── src/
    └── core/
        ├── __init__.py
        ├── errors.py
        ├── models/
        │   ├── __init__.py
        │   └── resume.py
        ├── modules/
        │   ├── __init__.py
        │   ├── metadata.py
        │   ├── parsing.py
        │   └── pdf_processing.py
        ├── pipeline/
        │   ├── __init__.py
        │   └── resume_processing.py
        └── validation/
            ├── __init__.py
            ├── file_validation.py
            ├── schema_validation.py
            ├── models/
            │   ├── __init__.py
            │   └── resume.py
            └── schemas/
                ├── __init__.py
                └── resume.json
````

## 8. Deployment

- The Core is included in the single CLI/Core executable and is not independently deployable.
- The Python runtime and dependencies are bundled into per-OS executables built with PyInstaller.
- The Core uses the Database Service and LLM Service within the application; the LLM service itself is installed and operated separately by the user.

## 9. References

- [System Architecture](../../docs/architecture.md)
- [Repository Architecture](../../docs/repository/architecture.md)
- [Tech Stack](../../docs/tech-stack.md)
- [Requirements](../../docs/requirements.md)
- [General System Rules](../../docs/system-rules.md)
- [Resume Processing System Overview](../../docs/system/resume-processing/overview.md)
- [Resume Generation System Overview](../../docs/system/resume-generation/overview.md)
- [Use Python and uv for the CVBrewer implementation](../../docs/adr/Architecture/2026-11-04/python-runtime-and-tooling.md)
- [Package CVBrewer as per-OS single executables with PyInstaller](../../docs/adr/Architecture/2026-11-04/cross-platform-packaging.md)
- [Use pypdf and pdfplumber for PDF processing](../../docs/adr/Architecture/2026-11-04/pdf-processing.md)
- [Use JSON Schema and Pydantic for data validation](../../docs/adr/Architecture/2026-11-04/schema-validation.md)
- [Integrate local LLMs through a native Ollama adapter](../../docs/adr/Architecture/2026-11-04/llm-integration.md)
- [Generate Markdown resumes for the MVP](../../docs/adr/Architecture/2026-11-04/markdown-output-mvp.md)
- [Core owns file-type and PDF validation](../../docs/adr/Architecture/2026-11-04/validation-responsibilities.md)
