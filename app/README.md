# CVBrewer Application

## 1. Purpose

This document defines the directory and file structure of the CVBrewery monorepository. It provides an overview of the application components and how source code, component documentation, and project-wide documentation are organized.

## 2. Components

| Component | Description |
|---|---|
| CLI | Handles user interaction, local file management, workflow coordination, and result reporting. |
| Core | Handles resume processing, job description processing, validation, resume generation, and application-level resume data and language-model operations. |
| Database | Implements database-specific operations and adapters for Core-owned data contracts. |
| LLM | Implements language-model-service-specific operations and adapters for Core-owned LLM contracts. |

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
│   │   ├── logger_app.py
│   │   ├── data/
│   │   ├── docs/
│   │   │   ├── technical-specification.md
│   │   │   ├── guidelines.md
│   │   │   ├── adr/
│   │   │   ├── processes/
│   │   │   └── system/
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── context.py
│   │   │   ├── logger_context.py
│   │   │   ├── logger_records.py
│   │   │   └── paths.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── all_logs.py
│   │   │   ├── application_startup.py
│   │   │   ├── delete_resumes.py
│   │   │   ├── entry_page.py
│   │   │   ├── error_logs.py
│   │   │   ├── llm_logs.py
│   │   │   ├── llm_menu.py
│   │   │   ├── menu.py
│   │   │   ├── options.py
│   │   │   ├── processing_runs.py
│   │   │   ├── processing_steps.py
│   │   │   ├── resume_upload.py
│   │   │   └── resume_upload_menu.py
│   │   └── ui/
│   │       ├── __init__.py
│   │       ├── delete_resumes.py
│   │       ├── entry_page.py
│   │       ├── html_reports.py
│   │       ├── llm_logs.py
│   │       ├── log_overview.py
│   │       ├── logger_menus.py
│   │       ├── logger_sources.py
│   │       ├── performance.py
│   │       ├── processing_runs.py
│   │       ├── processing_steps.py
│   │       ├── progress.py
│   │       ├── resume_upload.py
│   │       └── selection.py
│   ├── core/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── docs/
│   │   │   ├── technical-specification.md
│   │   │   ├── guidelines.md
│   │   │   ├── adr/
│   │   │   └── system/
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
│   │   │   ├── llm/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── log_models.py
│   │   │   │   ├── logger.py
│   │   │   │   ├── log_port.py
│   │   │   │   ├── models.py
│   │   │   │   ├── port.py
│   │   │   │   └── service.py
│   │   │   ├── logger/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── performance.py
│   │   │   │   ├── port.py
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
│   │   │   └── system/
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
│   │           ├── llm_log/
│   │           └── resume/
│   └── llm/
│       ├── README.md
│       ├── __init__.py
│       ├── docs/
│       │   ├── technical-specification.md
│       │   ├── guidelines.md
│       │   ├── adr/
│       │   └── system/
│       └── adapters/
│           ├── __init__.py
│           ├── logging/
│           └── ollama/
│               ├── __init__.py
│               ├── adapter.py
│               ├── config.py
│               └── errors.py
├── tests/
│   ├── conftest.py
│   ├── data/
│   ├── fixtures/
│   ├── cli/
│   ├── core/
│   ├── database/
│   ├── llm/
│   └── e2e/
├── scripts/
│   ├── clear-logs.sh
│   ├── query-test-logs.sh
│   └── query_test_logs.py
├── logs/
├── docs/
├── main.py
├── logger_main.py
├── run.sh
├── logger.sh
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
|`app/cli/docs/system/`|Contains CLI component system documentation.|
|`app/cli/app.py`|Defines the Typer application and no-command main menu callback.|
|`app/cli/logger_app.py`|Defines the separate logger CLI Typer application.|
|`app/cli/modules/context.py`|Defines the injected CLI dependencies and resume-listing and deletion capabilities.|
|`app/cli/modules/logger_context.py`|Defines the injected logger CLI dependencies and LLM log and processing log query capabilities.|
|`app/cli/modules/logger_records.py`|Normalizes LLM logs and processing runs for combined log views.|
|`app/cli/commands/llm_menu.py`|Coordinates the four-option logger CLI menu and routes to the selected log view.|
|`app/cli/commands/logger_menu.py`|Selects an available log source and prepares its logger CLI dependencies.|
|`app/cli/commands/llm_logs.py`|Coordinates querying LLM activity logs and generating HTML reports.|
|`app/cli/commands/resume_upload_menu.py`|Coordinates the `view runs` and `view steps` child menu.|
|`app/cli/commands/processing_runs.py`|Coordinates processing run queries and HTML reports for `view runs`.|
|`app/cli/commands/processing_steps.py`|Coordinates run selection, step queries, and HTML reports for `view steps`.|
|`app/cli/commands/error_logs.py`|Coordinates error queries and HTML reports across LLM logs and processing runs.|
|`app/cli/commands/all_logs.py`|Coordinates the merged newest-first query and HTML report across LLM logs and processing runs.|
|`app/cli/ui/html_reports.py`|Builds escaped HTML documents, writes report files, and coordinates browser opening.|
|`app/cli/ui/llm_logs.py`|Defines LLM activity log report columns and rows.|
|`app/cli/ui/log_overview.py`|Defines the shared newest-first overview report columns and rows.|
|`app/cli/ui/logger_menus.py`|Renders the logger and resume-upload menu panels.|
|`app/cli/ui/processing_runs.py`|Defines processing run report columns and rows.|
|`app/cli/ui/processing_steps.py`|Renders the run picker and defines processing step report columns and rows.|
|`app/cli/modules/paths.py`|Defines shared and development startup locations.|
|`app/cli/commands/application_startup.py`|Coordinates database initialization and folder preparation during startup.|
|`app/cli/commands/delete_resumes.py`|Coordinates confirmation and deletion of all imported resumes.|
|`app/cli/commands/entry_page.py`|Coordinates the CLI entry page workflow.|
|`app/cli/commands/menu.py`|Coordinates the CLI main menu and action routing.|
|`app/cli/commands/options.py`|Coordinates the CLI Options menu and imported resume actions.|
|`app/cli/commands/resume_upload.py`|Coordinates resume folder preparation, discovery, and Core delegation.|
|`app/cli/ui/`|Contains all CLI UI-related code.|
|`app/cli/ui/selection.py`|Provides shared menu-selection helpers used by both CLI entry points.|
|`app/cli/ui/logger_sources.py`|Renders the logger CLI log source selection prompt.|
|`app/cli/ui/performance.py`|Provides shared CPU and memory performance columns and value formatting for HTML reports.|
|`app/core/`|Contains the Core Processing Engine component module.|
|`app/core/README.md`|Provides the Core component overview.|
|`app/core/docs/`|Contains Core component technical documentation.|
|`app/core/docs/adr/`|Contains Core component-level architecture decisions.|
|`app/core/models/`|Contains non-validation Core models.|
|`app/core/pipeline/`|Contains resume-processing pipeline orchestration.|
|`app/core/services/metadata/`|Contains the resume metadata service.|
|`app/core/services/parsing/`|Contains the resume parsing service.|
|`app/core/services/llm/`|Contains LLM-specific records, the LLM port contract, LLM service operations, and LLM logging.|
|`app/core/services/logger/`|Contains generic log records, performance measurement, the sink contract, and logging operations.|
|`app/core/services/pdf/`|Contains the PDF processing and validation service.|
|`app/core/services/resume/`|Contains resume-specific records, repository contracts, service operations, and validation functions.|
|`app/core/services/resume/validation/`|Contains resume validation models and JSON Schemas.|
|`app/database/`|Contains the Database component module.|
|`app/database/README.md`|Provides the Database component overview.|
|`app/database/docs/`|Contains database component technical documentation.|
|`app/database/docs/adr/`|Contains database component-level architecture decisions.|
|`app/database/adapters/`|Contains database adapter implementations.|
|`app/database/adapters/sqlite/`|Contains the SQLite adapter implementation and migrations.|
|`app/database/adapters/sqlite/llm_log/`|Contains the SQLite LLM activity log repository and ORM model.|
|`app/llm/`|Contains the LLM component module.|
|`app/llm/README.md`|Provides the LLM component overview.|
|`app/llm/docs/`|Contains LLM component technical documentation.|
|`app/llm/docs/adr/`|Contains LLM component-level architecture decisions.|
|`app/llm/docs/system/`|Contains LLM component system documentation.|
|`app/llm/adapters/`|Contains LLM adapter implementations.|
|`app/llm/adapters/ollama/`|Contains the Ollama adapter implementation.|
|`app/llm/adapters/logging/`|Contains the LLM port logging wrapper.|
|`tests/`|Contains all test code. Non-end-to-end tests are grouped by component and mirror the package structure under `app/`; end-to-end tests reside under `tests/e2e/`.|
|`tests/data/`|Contains generated test environment data; reset at test session start and ignored by version control.|
|`scripts/`|Contains test runner, test-inspection, and report-cleanup scripts.|
|`scripts/clear-logs.sh`|Deletes the generated report directory at `./logs`.|
|`logs/`|Contains generated HTML log reports grouped by log source; ignored by version control.|
|`scripts/query-test-logs.sh`|Queries LLM activity logs from the test database.|
|`scripts/query_test_logs.py`|Reads and prints LLM activity log records from the test database as JSON.|
|`main.py`|Application composition root that wires startup, services, and CLI dependencies.|
|`logger_main.py`|Composition root that resolves available log sources and wires startup, log query capabilities, report output directory, and browser opener for the logger CLI.|
|`run.sh`|Starts the application with `uv run python main.py`.|
|`logger.sh`|Starts the logger CLI with `uv run python logger_main.py`.|
|`docs/`|Contains project-wide documentation.|
|`pyproject.toml`|Defines the root uv workspace, test tooling, and pytest configuration.|
|`uv.lock`|Locks dependencies for the root workspace.|
|`.python-version`|Selects Python 3.12 for the root workspace.|
|`README.md`|Provides the repository overview and entry point.|
|`AGENTS.md`|Contains instructions for AI agents working in the repository.|
|`.gitignore`|Defines files and directories excluded from version control.|

## 5. References

- [System Architecture](/docs/architecture.md)
