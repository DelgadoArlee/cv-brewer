# Repository Architecture

## 1. Purpose

This document defines the directory and file structure of the CVBrewery monorepository. It provides an overview of how project components, source code, and documentation are organized.

## 2. Repository Structure

The project follows a **monorepo** structure. All application components and project documentation are maintained within a single repository.

```
cvbrewery/
├── cli/
│   ├── data/               Development-only data (ignored by version control).
│   ├── docs/
│   │   ├── technical-specification.md
│   │   ├── guidelines.md
│   │   ├── adr/
│   │   ├── modules/
│   │   └── processes/
│   └── src/
│       └── cli/
│           ├── __init__.py
│           ├── app.py
│           ├── modules/
│           │   ├── __init__.py
│           │   └── paths.py
│           ├── processes/
│           │   ├── __init__.py
│           │   ├── application_startup.py
│           │   └── entry_page.py
│           └── ui/
│               ├── __init__.py
│               └── entry_page.py
├── core/
├── database/
│   ├── pyproject.toml
│   ├── README.md
│   ├── .python-version
│   ├── docs/
│   │   ├── technical-specification.md
│   │   ├── adr/
│   │   └── modules/
│   └── src/
│       └── database/
│           ├── __init__.py
│           ├── database_service/
│           │   └── __init__.py
│           └── adapters/
│               ├── __init__.py
│               └── sqlite/
│                   ├── __init__.py
│                   ├── alembic.ini
│                   ├── config.py
│                   ├── engine.py
│                   ├── errors.py
│                   ├── migrations.py
│                   └── migrations/
├── llm/
│   ├── pyproject.toml
│   ├── README.md
│   ├── .python-version
│   ├── docs/
│   │   ├── technical-specification.md
│   │   ├── guidelines.md
│   │   ├── adr/
│   │   ├── modules/
│   │   └── systems/
│   └── src/
│       └── llm/
│           ├── __init__.py
│           ├── llm_service/
│           │   ├── __init__.py
│           │   └── modules/
│           │       └── generation/
│           │           ├── __init__.py
│           │           ├── models.py
│           │           ├── adapter.py
│           │           └── service.py
│           └── adapters/
│               ├── __init__.py
│               └── ollama/
│                   ├── __init__.py
│                   ├── adapter.py
│                   ├── config.py
│                   └── errors.py
├── tests/
│   ├── conftest.py
│   ├── data/               Generated test environment data (ignored by version control).
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
```

## 3. Directory Description

|Directory / File|Description|
|---|---|
|`cli/`|Contains the Command-Line Interface component.|
|`cli/data/`|Contains development-only database and local folder data; ignored by version control.|
|`cli/docs/adr/`|Contains CLI component-level architecture decisions.|
|`cli/docs/guidelines.md`|Contains CLI component-specific coding guidelines.|
|`cli/docs/modules/`|Contains CLI component module documentation.|
|`cli/docs/processes/`|Contains CLI component application-level process documentation.|
|`cli/src/cli/app.py`|Defines the Typer application and no-command entry page callback.|
|`cli/src/cli/modules/paths.py`|Defines shared and development startup locations.|
|`cli/src/cli/processes/application_startup.py`|Coordinates database initialization and folder preparation during startup.|
|`cli/src/cli/processes/entry_page.py`|Coordinates the CLI entry page workflow.|
|`cli/src/cli/ui/`|Contains all CLI UI-related code.|
|`core/`|Contains the Core Processing Engine component.|
|`database/`|Contains the database component as a single Python project.|
|`database/docs/`|Contains database component technical documentation.|
|`database/docs/adr/`|Contains database component-level architecture decisions.|
|`database/docs/modules/`|Contains database component module documentation.|
|`database/src/database/database_service/`|Contains the Database Service package.|
|`database/src/database/adapters/`|Contains database adapter implementations.|
|`database/src/database/adapters/sqlite/`|Contains the SQLite adapter implementation and migrations.|
|`llm/`|Contains the LLM component as a single Python project.|
|`llm/docs/`|Contains LLM component technical documentation.|
|`llm/docs/adr/`|Contains LLM component-level architecture decisions.|
|`llm/docs/modules/`|Contains LLM component module documentation.|
|`llm/docs/systems/`|Contains LLM component system documentation.|
|`llm/src/llm/llm_service/`|Contains the LLM Service package.|
|`llm/src/llm/adapters/`|Contains LLM adapter implementations.|
|`llm/src/llm/adapters/ollama/`|Contains the Ollama adapter implementation.|
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

## 4. References

- [System Architecture](../architecture.md)