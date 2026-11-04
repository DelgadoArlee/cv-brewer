# Process Format Rules

## Purpose

Define the standard structure and level of detail for process documentation. Process documents must describe high-level system workflows, responsibilities, and behavior without specifying implementation details.

Follow these rules when creating or updating a process document.

## Required Sections

Every process document must contain sections 1, and 2 in the specified order.

### 1. Purpose / Summary

- Explain what the process does and why it exists.
- Identify its main responsibility within the system.
- Describe its overall outcome.
- Use one short paragraph.

### 2. Process Flow

- Describe the process using a Mermaid diagram.
- Always wrap Mermaid diagrams in a `mermaid` code block and is indented by 4 spaces.
- Use quadruple backticks for codeblocks (````)
- Use `flowchart` for sequential steps, decisions, and conditions.
- Use `sequenceDiagram` for interactions between services or components.
- Use valid Mermaid syntax with clearly defined nodes and connections.
- Represent the major stages, decisions, and transitions of the process.
- Include important success, failure, and stopping paths.
- Keep diagrams simple and readable.
- Describe system-level activities rather than individual operations or implementation steps.

Example:

```` mermaid
flowchart TD
    A([Start]) --> B[Perform Step]
    B --> C{Condition Met?}
    C -->|Yes| D[Continue]
    C -->|No| E[Stop]
````

### 3. Rules

- Use a bulleted list.
- Describe required system behavior using clear statements.
- Use **must** for mandatory behavior.
- Include relevant validation, decision, success, and error-handling requirements.
- Define important conditions and expected outcomes.
- Keep rules at the system level.
- Do not specify algorithms, libraries, data structures, API contracts, or other implementation details.
- Do not repeat the diagram step by step.

### 4. Constraints (Optional)

- Use a bulleted list.
- Document limitations and prohibited behavior.
- Include relevant permission, scope, and responsibility boundaries.
- Describe constraints on system behavior rather than implementation choices.
- Do not repeat rules already covered in Section 3.

### 5. References (Optional)

- Use a bulleted list.
- Format references as `[Title](relative/path)`.
- Include only relevant documentation.
- Do not invent references.

## General Rules

- Use Markdown for documentation and Mermaid for diagrams.
- Keep explanations concise and easy to understand.
- Maintain a high-level system perspective throughout the document.
- Document what the system does, not how the system implements it.
- Represent logical activities and responsibilities without prescribing their technical execution.
- Do not include implementation-specific details such as algorithms, libraries, frameworks, database technologies, file formats, or internal code structures.
- Do not duplicate detailed requirements or rules owned by other documents. Reference them instead.
- Do not invent requirements, behavior, or references.
- Preserve existing project conventions and terminology.
- If information is missing, ask for clarification.
- Make sure that the process is part of the workflow defined in `feature-overview.md`.

## Level of Detail Guidelines

Process documentation must describe system behavior at the logical workflow level.

**Appropriate details:**

- Receiving user input.
- Validating provided information.
- Checking whether required conditions are met.
- Processing and transforming information.
- Interacting with another system component.
- Persisting or retrieving information.
- Returning results.
- Handling unsuccessful outcomes.

**Avoid implementation details:**

- Specific algorithms or processing techniques.
- Specific libraries, frameworks, or third-party tools.
- Database queries, schemas, or storage mechanisms.
- Internal class, function, or method responsibilities.
- API endpoints, request payloads, or response structures.
- Low-level file operations and technical validation mechanisms.

Implementation details belong in the appropriate architecture, component, service, data, or technical documentation.

## File Editing Rules

- Write the entire process document in its designated file.
- Sections 1, 2, and 3 are mandatory.
- Sections 4 and 5 are optional when relevant.
- Keep all sections in the same file.
- Never create additional files for individual sections, Mermaid diagrams, or rules.
- Do not treat Mermaid node names, diagram labels, or section headings as filenames.
- The Mermaid diagram must be embedded directly under Section 2. Process Flow in the designated process document.
- Mermaid diagrams must be written inside a Markdown fenced code block using the `mermaid` language identifier.
- Do not create separate `.mmd`, `.mermaid`, or other files for process diagrams.
- Treat Mermaid diagrams as content within the process document, not as standalone documentation files.
- Always preserve the document's required section structure when writing or updating its content.
