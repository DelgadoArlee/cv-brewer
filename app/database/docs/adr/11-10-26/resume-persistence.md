# Establish Resume Persistence

## Date

2026-11-10

## Status

Superseded by [Retain Database Adapters as the Database Component Boundary](../11-13-26/adapter-only-boundary.md).

## Context

The database component contains the SQLite adapter foundation and an empty Database Service package. Resume processing requires validated resume data to be stored for later retrieval and generation. The user resume data model defines nested metadata, parsed resume content, validation status, and processing history.

The Database Service must expose application-level operations while the Database Adapter owns SQLAlchemy models, SQLite queries, transactions, and migrations. The component coding guidelines require service modules under `database_service/modules/` and organize adapter repositories and models by class under `adapters/<adapter-name>/<class-name>/`.

## Decision

- Persist resume data using a hybrid relational schema.
- Store resume root data, personal information, metadata, and validation status on the `resumes` table.
- Store experience, education, certifications, skills, and processing history in ordered child tables.
- Enforce a unique `content_fingerprint` on resume records.
- Include a nullable `deleted_at` column as defined by the user resume data model.
- Define resume operations in the Database Service module `database_service/modules/resume/`.
- Implement persistence in `adapters/sqlite/resume/repository.py`.
- Organize SQLAlchemy models under `adapters/sqlite/resume/models/`.
- Generate a UUID and creation timestamp in the Database Service when the caller does not provide them.
- Provide initial operations for saving a resume, retrieving by ID, finding by content fingerprint, and listing resumes.

## Consequences

- Resume data maps to explicit relational tables and preserves child ordering.
- Duplicate content fingerprints are rejected by the database.
- The Database Service remains independent of SQLAlchemy and SQLite details.
- Adapter persistence code is grouped by class, with the repository at the class directory root and models under `models/`.
- Delete-all behavior and the hard-delete documentation remain outside this decision.
- Future database adapters must provide compatible resume repository implementations.
