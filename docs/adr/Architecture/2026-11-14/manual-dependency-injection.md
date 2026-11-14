# Use Manual Dependency Injection with a Single Composition Root

## Date

2026-11-14

## Status

Accepted

## Category

architecture

## Context

CVBrewer components already use constructor injection for service and adapter dependencies. The CLI application, however, stored runtime dependencies in module-level globals and could construct database and LLM services through a lazy accessor. Menu and Options workflows also resolved dependencies through fallback paths, and the Options menu read a private attribute from the resume processor.

These patterns created multiple composition paths, hidden dependencies, globally mutable state, and tests that depended on internal globals. They also risked violating the CLI boundary by constructing database and LLM implementations inside the CLI component.

## Decision

- Use manual dependency injection with explicit constructor and function parameters.
- Keep the application composition root in `main.py` as the only place that constructs concrete database and LLM services and wires the application.
- Pass an immutable `CLIDependencies` value to the CLI application factory.
- Pass a narrow `ResumeLister` capability to the CLI instead of exposing the resume service or processor internals.
- Remove module-level dependency globals, lazy dependency construction, and fallback dependency resolution from the CLI.
- Do not introduce a dependency injection framework or container.

## Consequences

- The CLI receives all runtime dependencies from the composition root and does not locate or construct them itself.
- The CLI no longer imports database or LLM implementations.
- Menu, Options, and Resume Upload workflows require explicit dependencies and no longer rely on global state.
- Tests can construct dependencies directly and no longer need to patch CLI module globals.
- Core, LLM, and Database component boundaries and constructor-injection patterns remain unchanged.
- The application remains small enough that a dependency injection framework is unnecessary.
