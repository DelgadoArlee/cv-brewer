# Repository Architecture

## 1. Purpose

This document defines the directory and file structure of the CVBrewery monorepository. It provides an overview of how project components, source code, and documentation are organized.

## 2. Repository Structure

The project follows a **monorepo** structure. All application components and project documentation are maintained within a single repository.

```
cvbrewery/
├── cli/
├── core/
├── database/
│   ├── pyproject.toml
│   ├── README.md
│   ├── .python-version
│   ├── docs/
│   │   └── technical-specification.md
│   └── src/
│       └── database/
│           ├── __init__.py
│           ├── database_service/
│           │   └── __init__.py
│           └── adapters/
│               └── __init__.py
├── llm/
│   └── adapters/
├── docs/
├── README.md
├── AGENTS.md
└── .gitignore
```

## 3. Directory Description

|Directory / File|Description|
|---|---|
|`cli/`|Contains the Command-Line Interface component.|
|`core/`|Contains the Core Processing Engine component.|
|`database/`|Contains the database component as a single Python project.|
|`database/docs/`|Contains database component technical documentation.|
|`database/src/database/database_service/`|Contains the Database Service package.|
|`database/src/database/adapters/`|Contains database adapter implementations.|
|`llm/`|Contains LLM integration components.|
|`llm/adapters/`|Contains LLM adapter implementations.|
|`docs/`|Contains project-wide documentation.|
|`README.md`|Provides the repository overview and entry point.|
|`AGENTS.md`|Contains instructions for AI agents working in the repository.|
|`.gitignore`|Defines files and directories excluded from version control.|

## 4. References

- [System Architecture](docs/architecture/system-architecture.md)