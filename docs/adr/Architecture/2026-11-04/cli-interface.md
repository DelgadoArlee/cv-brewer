# Use Typer and Rich for a hybrid CLI

## Date

2026-11-04

## Status

Accepted

## Context

The CLI handles user interaction, input and output folder management, file discovery, workflow coordination, and result reporting. The documented user journeys are menu-oriented, while direct commands are useful for automation and testing. The CLI and Core are bundled together but have separate responsibilities.

## Decision

Use Typer for command definitions and Rich for prompts, tables, progress, and error output. Provide direct subcommands and an interactive menu when `cvbrewer` is run without a command.

Keep the CLI orchestration-only: it discovers files, reads file bytes, passes immutable file payloads to the Core, and reports outcomes. The CLI does not perform file-type validation, parsing, schema validation, database access, LLM access, or rendering. Destructive actions require explicit confirmation. Support non-interactive flags for automation.

## Consequences

- Users get both guided and scriptable workflows.
- Typer and Rich add dependencies but improve usability and testing.
- The menu and subcommands must remain behaviorally consistent.
- Passing file bytes keeps the Core independent of the file system; resume files are small enough for this to be practical.
- The CLI must not duplicate Core validation or processing logic.
