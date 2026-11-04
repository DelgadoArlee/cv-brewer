# Core owns file-type and PDF validation

## Date

2026-11-04

## Status

Accepted

## Context

The architecture previously stated that the CLI performs file-type checks, while the resume-upload system assigned file-type validation to the Core. Performing checks in both places would duplicate logic and create inconsistent outcomes. The CLI and Core are parts of one executable, not separate frontend and backend services.

## Decision

The CLI performs file discovery only and passes every discovered file to the Core. The Core performs file signature verification, PDF encryption and structure validation, readable-content checks, text extraction, and parsing.

The CLI reports the Core's outcomes and does not filter files by type. Update the architecture and resume-upload documentation to reflect this single validation boundary.

## Consequences

- File-type and PDF validation have one source of truth.
- The CLI remains simple and free of processing logic.
- Non-PDF files reach the Core and are rejected there without creating resume records.
- The Core operates on file bytes supplied by the CLI and does not need direct file-system access.
- The architecture and upload documentation must be updated to remove the conflicting CLI responsibility.
