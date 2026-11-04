# Package CVBrewer as per-OS single executables with PyInstaller

## Date

2026-11-04

## Status

Accepted

## Context

The architecture requires the CLI and Core to be deployed as a single executable. Windows and macOS are required for the first release; Linux is optional. The packaging tool must support Python 3.12 and the selected libraries. PyInstaller and Nuitka were considered.

## Decision

Use PyInstaller to produce a one-file executable for each target operating system. Build each artifact on its target operating system through CI; PyInstaller does not cross-compile.

macOS artifacts are code-signed and notarized. Windows signing is optional. Linux artifacts are optional and may be distributed as a standalone binary or archive. Keep a one-directory build available for development and debugging.

## Consequences

- PyInstaller is mature and has broad library support, reducing first-release packaging risk.
- One-file executables extract to a temporary directory at startup, which can increase startup time.
- Windows antivirus tools may flag one-file executables; signing reduces this risk.
- Hidden imports and data files must be declared for Pydantic, SQLAlchemy, Jinja2, and PDF libraries.
- Nuitka can be reconsidered later if startup time or artifact size becomes a problem.
