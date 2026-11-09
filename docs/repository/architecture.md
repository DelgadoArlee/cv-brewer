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
│   │   ├── adr/
│   │   ├── modules/
│   │   └── processes/
│   └── src/
│       └── cli/
│           ├── __init__.py
│           ├── modules/
│           │   ├── __init__.py
│           │   └── paths.py
│           └── processes/
│               ├── __init__.py
│               └── application_startup.py
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
│   └── adapters/
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
|`cli/docs/modules/`|Contains CLI component module documentation.|
|`cli/docs/processes/`|Contains CLI component application-level process documentation.|
|`cli/src/cli/modules/paths.py`|Defines shared and development startup locations.|
|`cli/src/cli/processes/application_startup.py`|Coordinates database initialization and folder preparation during startup.|
|`core/`|Contains the Core Processing Engine component.|
|`database/`|Contains the database component as a single Python project.|
|`database/docs/`|Contains database component technical documentation.|
|`database/docs/adr/`|Contains database component-level architecture decisions.|
|`database/docs/modules/`|Contains database component module documentation.|
|`database/src/database/database_service/`|Contains the Database Service package.|
|`database/src/database/adapters/`|Contains database adapter implementations.|
|`database/src/database/adapters/sqlite/`|Contains the SQLite adapter implementation and migrations.|
|`llm/`|Contains LLM integration components.|
|`llm/adapters/`|Contains LLM adapter implementations.|
|`tests/`|Contains all test code organized by testing level (features, systems, processes, e2e).|
|`tests/data/`|Contains generated test environment data; reset at test session start and ignored by version control.|
|`main.py`|Application composition root that wires CLI startup to database initialization.|
|`docs/`|Contains project-wide documentation.|
|`pyproject.toml`|Defines the root uv workspace, test tooling, and pytest configuration.|
|`uv.lock`|Locks dependencies for the root workspace.|
|`.python-version`|Selects Python 3.12 for the root workspace.|
|`README.md`|Provides the repository overview and entry point.|
|`AGENTS.md`|Contains instructions for AI agents working in the repository.|
|`.gitignore`|Defines files and directories excluded from version control.|

## 4. References

- [System Architecture](../architecture.md)````