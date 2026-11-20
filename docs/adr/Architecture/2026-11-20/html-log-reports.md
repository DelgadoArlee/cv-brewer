# Render Logger Reports as HTML

## Date

2026-11-20

## Status

Accepted

## Category

architecture

## Context

The [expanded logger CLI log views decision](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md) established the current four-option logger menu, the `resume-upload` child menu, error predicates, row limits, and Rich table output. Reviewers now need log reports that are easier to scan, share, and retain outside the terminal. The logger remains a read-only review entry point, and its source selection and query capabilities continue to come from the composition root as required by [manual dependency injection](/docs/adr/Architecture/2026-11-14/manual-dependency-injection.md).

## Decision

- Keep the logger CLI menus and prompts in the terminal, but stop rendering log data as CLI tables.
- When a data-view option is selected, generate a standalone HTML report for the selected log source and attempt to open it in the default browser.
- Apply HTML report generation to `llm`, `view runs`, `view steps`, `error`, and `all`.
- Write reports under `./logs/<source>/`, using the available `dev`, `e2e`, and `test` source names as subfolder names.
- Name report files with a full UTC creation timestamp and log type, using the pattern `YYYY-MM-DDTHHMMSSffffffZ-<log-type>.html`.
- Use only Python standard library HTML generation with escaped cell values; do not add an HTML templating dependency.
- Print the generated report path after every successful report creation. If the browser cannot be opened, print a warning and keep the path available.
- Add `logs/` to repository ignore rules and add a repository script that deletes `./logs`.
- Carry forward the accepted menu options, child menu, query behavior, error predicates, 100-row limits, source selection, and read-only constraints. Only the presentation behavior is replaced.
- Make no database schema or query API changes.

## Consequences

- The [expanded logger CLI log views decision](/docs/adr/Architecture/2026-11-20/logger-cli-log-views.md) is superseded for its table-output clauses; its remaining logger behavior is carried forward by this decision.
- The CLI composition root must supply the selected source, report output directory, and browser-opening capability.
- Logger tests must verify generated HTML content, per-source output folders, filenames, path output, and browser-open behavior instead of terminal table rows.
- Report files are generated artifacts and remain excluded from version control.
- Browser and file-system behavior must be injectable so tests do not open real browsers or write outside temporary directories.
