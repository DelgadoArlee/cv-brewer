# Generate Markdown resumes for the MVP

## Date

2026-11-04

## Status

Accepted

## Context

The current requirements and architecture describe generated PDF files. The developer selected Markdown output for the initial implementation to reduce rendering complexity. The output format must still be produced from validated generated resume data and saved in the output folder.

## Decision

Generate resume output as Markdown for the MVP using Jinja2 templates. Keep rendering behind a replaceable renderer boundary so PDF rendering can be added later without changing the Core workflow.

Update the requirements, architecture, feature, system, and process documentation to describe Markdown output instead of PDF output. PDF rendering is deferred to a future decision.

## Consequences

- The MVP avoids the complexity and packaging cost of a PDF rendering engine.
- Users receive Markdown files instead of PDFs in the output folder.
- Requirements and architecture documentation must change to match the decision.
- A future PDF renderer will require a new decision and may need additional dependencies.
- Template design remains simpler, but output appearance depends on the user's Markdown viewer.
