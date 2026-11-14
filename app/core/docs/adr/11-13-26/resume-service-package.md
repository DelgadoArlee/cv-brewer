# Establish the Resume Service Package

## Date

2026-11-13

## Status

Accepted

## Context

The Database Service application layer is now owned by the Core under the [Move the Database Service into the Core application layer](../../../../../docs/adr/Architecture/2026-11-13/database-service-to-core.md) decision. All resume-specific records, the repository contract, and resume service operations previously lived under the database component. Core needs a package location that keeps resume-specific application logic together without reintroducing a generic database abstraction that has no shared use yet.

## Decision

- Place all resume-specific service code under `app/core/services/resume/`.
- Define resume records in `app/core/services/resume/models.py`.
- Define the resume repository contract in `app/core/services/resume/repository.py`.
- Define resume service operations in `app/core/services/resume/service.py`.
- Export the resume records, `ResumeRepository`, and `ResumeService` from `app/core/services/resume/__init__.py`.
- Do not create an `app/core/services/database/` package until a concrete reusable database abstraction is required.

## Consequences

- Core owns all resume-specific application-level data code.
- Database adapters import the Core-owned resume records and repository contract.
- The former `database_service/modules/resume/` package is removed.
- New resume services follow the `services/resume/` package structure.
- Reusable database abstractions are deferred until a shared need exists.
