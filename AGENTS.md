# AGENTS.md

## Repository state

- Docs-only repo: no source code, manifests, build, test, lint, or typecheck commands. Do not invent or run them.
- Planned product is a monorepo with a CLI and Core bundled into one executable, plus Database Service/Adapter and LLM Provider/Adapter. The LLM is an external, user-installed service. See `docs/architecture.md`.
- No implementation stack is committed in an ADR. Confirm the stack with the user and record it in an ADR before adding code.

## Source of truth

- Read `docs/guidelines.md`, `docs/requirements.md`, `docs/architecture.md`, and `docs/system-rules.md` before changing behavior.
- Follow Documentation-Driven Development: docs are the primary project context, and must be created/updated before or alongside the implementation they describe.
- Root `docs/` is high-level only: no code behavior, algorithms, function references, or implementation procedures. Implementation/component docs belong outside root `docs/` (none exist yet).
- Never invent requirements, references, systems, or decisions. ADRs record developer-agreed decisions only.

## Documentation conventions

- Markdown only; kebab-case for file and directory names; relative Markdown links.
- Follow the matching rule in `docs/rules/` for every new/edited doc: `feature.md`, `system.md`, `data.md`, `process.md`, `validation.md`, `adr.md`.
- Current tree differs from `docs/guidelines.md`: it uses `docs/system/` (singular) and flat files in `docs/features/` and `docs/data/`. Match the current layout unless asked to migrate.
- Existing docs are inconsistent with the rules (feature docs omit the required User Journey; `user-resume.md` uses snake_case despite the camelCase rule; several relative links are broken). Do not mass-rename or restructure without asking; apply the rules to new content.
- New process docs: use the `docs/rules/process.md` Mermaid format (quadruple backticks, indented 4 spaces). Existing process files vary.
- ADRs: individual files at `docs/adr/<YYYY-MM-DD>/<topic>.md`, indexed from `docs/adr/ADL.md`. Currently only an empty `docs/adr/architecure-decision-log.md` exists, so create the dated directory and ADL intentionally.

## Verification

- No automated checks exist. Manually verify required section order, Mermaid fences, and relative links when editing docs.
- `.obsidian/`, `.DS_Store`, and other editor/tooling artifacts are not project documentation.
