# CVBrewer Application

## 1. Purpose

This document defines the directory and file structure of the CVBrewery monorepository. It provides an overview of the application components and how source code, component documentation, and project-wide documentation are organized.

## 2. Components

| Component | Description |
|---|---|
| CLI | Handles user interaction, local file management, workflow coordination, and result reporting. |
| Core | Handles resume processing, job description processing, validation, resume generation, and application-level resume data operations. |
| Database | Implements database-specific operations and adapters for Core-owned data contracts. |
| LLM | Provides application-level language-model operations through pluggable LLM adapters. |

## 3. Repository Structure

The project follows a **monorepo** structure. All application components are maintained within the `app/` directory as modules of a single Python project. Project-wide documentation and tests remain at the repository root.

````text
cv-brewer/
├── app/
│   ├── README.md
│   ├── pyproject.toml
│   ├── cli/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── data/
│   │   ├── docs/
│   │   │   ├── technical-specification.md
│   │   │   ├── guidelines.md
│   │   │   ├── adr/
│   │   │   ├── processes/
│   │   │   └── systems/
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   └── paths.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── application_startup.py
│   │   │   ├── entry_page.py
│   │   │   ├── menu.py
│   │   │   ├── options.py
│   │   │   └── resume_upload.py
│   │   └── ui/
│   │       ├── __init__.py
│   │       ├── entry_page.py
│   │       └── resume_upload.py
│   ├── core/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── docs/
│   │   │   ├── technical-specification.md
│   │   │   ├── guidelines.md
│   │   │   ├── adr/
│   │   │   └── systems/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── resume.py
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   └── resume_processing.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── metadata/
│   │   │   │   ├── __init__.py
│   │   │   │   └── service.py
│   │   │   ├── parsing/
│   │   │   │   ├── __init__.py
│   │   │   │   └── service.py
│   │   │   ├── pdf/
│   │   │   │   ├── __init__.py
│   │   │   │   └── service.py
│   │   │   └── resume/
│   │   │       ├── __init__.py
│   │   │       ├── models.py
│   │   │       ├── repository.py
│   │   │       ├── service.py
│   │   │       └── validation/
│   │   │           ├── __init__.py
│   │   │           ├── models/
│   │   │           │   ├── __init__.py
│   │   │           │   └── resume.py
│   │   │           └── schemas/
│   │   │               ├── __init__.py
│   │   │               └── resume.json
│   ├── database/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── docs/
│   │   │   ├── technical-specification.md
│   │   │   ├── guidelines.md
│   │   │   ├── adr/
│   │   │   ├── sqlite/
│   │   │   └── systems/
│   │   └── adapters/
│   │       ├── __init__.py
│   │       └── sqlite/
│   │           ├── __init__.py
│   │           ├── alembic.ini
│   │           ├── config.py
│   │           ├── engine.py
│   │           ├── errors.py
│   │           ├── migrations.py
│   │           ├── migrations/
│   │           └── resume/
│   └── llm/
│       ├── README.md
│       ├── __init__.py
│       ├── docs/
│       │   ├── technical-specification.md
│       │   ├── guidelines.md
│       │   ├── adr/
│       │   └── systems/
│       ├── llm_service/
│       │   ├── __init__.py
│       │   └── modules/
│       │       └── generation/
│       │           ├── __init__.py
│       │           ├── models.py
│       │           ├── adapter.py
│       │           └── service.py
│       └── adapters/
│           ├── __init__.py
│           └── ollama/
│               ├── __init__.py
│               ├── adapter.py
│               ├── config.py
│               └── errors.py
├── tests/
│   ├── conftest.py
│   ├── data/
│   ├── fixtures/
│   ├── features/
│   ├── systems/
│   ├── processes/
│   └── e2e/
├── docs/
├── main.py
├── run.sh
├── pyproject.toml
├── uv.lock
├── .python-version
├── README.md
├── AGENTS.md
└── .gitignore
````

## 4. Directory Description

|Directory / File|Description|
|---|---|
|`app/`|Contains the single Python project and all application component modules.|
|`app/README.md`|Provides the application component summary and repository structure.|
|`app/pyproject.toml`|Defines the `cv-brewer` project, dependencies, and build configuration.|
|`app/cli/`|Contains the Command-Line Interface component module.|
|`app/cli/data/`|Contains development-only database and local folder data; ignored by version control.|
|`app/cli/README.md`|Provides the CLI component overview.|
|`app/cli/docs/`|Contains CLI component technical documentation.|
|`app/cli/docs/adr/`|Contains CLI component-level architecture decisions.|
|`app/cli/docs/guidelines.md`|Contains CLI component-specific coding guidelines.|
|`app/cli/docs/processes/`|Contains CLI component application-level and UI process documentation.|
|`app/cli/docs/systems/`|Contains CLI component system documentation.|
|`app/cli/app.py`|Defines the Typer application and no-command main menu callback.|
|`app/cli/modules/paths.py`|Defines shared and development startup locations.|
|`app/cli/commands/application_startup.py`|Coordinates database initialization and folder preparation during startup.|
|`app/cli/commands/entry_page.py`|Coordinates the CLI entry page workflow.|
|`app/cli/commands/menu.py`|Coordinates the CLI main menu and action routing.|
|`app/cli/commands/options.py`|Coordinates the CLI Options menu and imported resume display.|
|`app/cli/commands/resume_upload.py`|Coordinates resume folder preparation, discovery, and Core delegation.|
|`app/cli/ui/`|Contains all CLI UI-related code.|
|`app/core/`|Contains the Core Processing Engine component module.|
|`app/core/README.md`|Provides the Core component overview.|
|`app/core/docs/`|Contains Core component technical documentation.|
|`app/core/docs/adr/`|Contains Core component-level architecture decisions.|
|`app/core/models/`|Contains non-validation Core models.|
|`app/core/pipeline/`|Contains resume-processing pipeline orchestration.|
|`app/core/services/metadata/`|Contains the resume metadata service.|
|`app/core/services/parsing/`|Contains the resume parsing service.|
|`app/core/services/pdf/`|Contains the PDF processing and validation service.|
|`app/core/services/resume/`|Contains resume-specific records, repository contracts, service operations, and validation functions.|
|`app/core/services/resume/validation/`|Contains resume validation models and JSON Schemas.|
|`app/database/`|Contains the Database component module.|
|`app/database/README.md`|Provides the Database component overview.|
|`app/database/docs/`|Contains database component technical documentation.|
|`app/database/docs/adr/`|Contains database component-level architecture decisions.|
|`app/database/adapters/`|Contains database adapter implementations.|
|`app/database/adapters/sqlite/`|Contains the SQLite adapter implementation and migrations.|
|`app/llm/`|Contains the LLM component module.|
|`app/llm/README.md`|Provides the LLM component overview.|
|`app/llm/docs/`|Contains LLM component technical documentation.|
|`app/llm/docs/adr/`|Contains LLM component-level architecture decisions.|
|`app/llm/docs/systems/`|Contains LLM component system documentation.|
|`app/llm/llm_service/`|Contains the LLM Service package.|
|`app/llm/adapters/`|Contains LLM adapter implementations.|
|`app/llm/adapters/ollama/`|Contains the Ollama adapter implementation.|
|`tests/`|Contains all test code organized by testing level (features, systems, processes, e2e).|
|`tests/data/`|Contains generated test environment data; reset at test session start and ignored by version control.|
|`main.py`|Application composition root that wires CLI startup and the CLI entry page.|
|`run.sh`|Starts the application with `uv run python main.py`.|
|`docs/`|Contains project-wide documentation.|
|`pyproject.toml`|Defines the root uv workspace, test tooling, and pytest configuration.|
|`uv.lock`|Locks dependencies for the root workspace.|
|`.python-version`|Selects Python 3.12 for the root workspace.|
|`README.md`|Provides the repository overview and entry point.|
|`AGENTS.md`|Contains instructions for AI agents working in the repository.|
|`.gitignore`|Defines files and directories excluded from version control.|

## 5. References

- [System Architecture](../docs/architecture.md)
