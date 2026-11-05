Documentation Guidelines

1. Purpose

This document defines the purpose, structure, and documentation standards of the docs/ directory within CVBrewer.

The docs/ directory serves as the central repository for high-level project documentation. It provides a shared source of context and reference for both developers and AI agents throughout the planning, design, and development of the project.

Documentation stored here describes the project's decisions, features, systems, and data models without including implementation-specific details.

The project follows a Documentation-Driven Development approach, where documentation guides development and remains aligned with the actual state of the project.

2. Documentation Principles

All documentation within docs/ must follow these principles:

High-Level Documentation: Documents must describe the purpose, responsibilities, relationships, and behavior of project components without going into implementation-specific details.

Single Source of Context: Documentation should provide a consistent reference for developers and AI agents to understand the project.

Documentation-Driven Development: Decisions, features, systems, and implementation work must have corresponding documentation.

Consistency: Every document must follow its corresponding formatting rules.

Clarity: Documents must be concise, structured, and understandable without requiring knowledge of implementation details.

3. Directory Structure

The root docs/ directory is divided into five primary categories:

docs/
├── adr/
├── rules/
├── features/
├── systems/
└── data/

Each category has a distinct documentation responsibility.

3.1 ADR

Purpose: Stores Architectural Decision Records (ADRs).

This directory documents high-level decisions made during project planning and development.

ADRs capture decisions that may affect one or multiple project components, including:

Architecture

Deployment

Technology stack

Systems

Features

ADRs serve as historical references explaining what was decided and the reasoning behind those decisions.

Directory Structure:

docs/adr/<mm-dd-yyyy>/<topic>.md

Each ADR must be stored under its corresponding decision date.

3.2 Rules

Purpose: Stores documentation formatting and writing standards.

This directory defines how AI agents and assistants should create, organize, and maintain project documentation.

Rules establish consistent documentation structures and requirements across the repository.

Examples include:

Feature overview formatting rules

System overview formatting rules

Data model formatting rules

ADR formatting rules

Process documentation formatting rules

Rules must be followed when creating or modifying documents of their corresponding types.

3.3 Features

Purpose: Stores high-level documentation describing the features of CVbrewer.

Feature documentation describes what a feature does, its objectives, user journey, and the systems involved in delivering it.

Feature documents must focus on the feature's purpose and overall behavior rather than its implementation.

Directory Structure:

docs/features/<feature-name>/

Each feature must have its own directory containing its corresponding documentation.

3.4 Systems

Purpose: Stores high-level documentation describing the systems that make up a feature.

System documentation describes the purpose, responsibilities, scope, and relationships of individual systems within the project.

Systems are documented independently to establish clear boundaries and responsibilities, even when multiple systems contribute to the same feature.

Directory Structure:

docs/systems/<system-name>/

Each system must have its own directory containing its corresponding documentation.

3.5 Data

Purpose: Stores high-level documentation describing the data models used by project systems.

Data documentation describes the purpose, structure, properties, and relationships of the data models used throughout CVbrewer.

These documents establish a shared understanding of the information represented and used by the systems.

Directory Structure:

docs/data/<data-name>/

Each data model must have its own directory containing its corresponding documentation.

4. Documentation Standards

All documents stored within the root docs/ directory must follow these standards.

4.1 File Naming

All filenames must use kebab-case.

All documentation files must use the Markdown (.md) format.

Directory names must also use kebab-case.

Names must clearly describe the subject of the document.

Examples:

feature-overview.md
system-overview.md
data-model.md
validation-rules.md

4.2 Formatting Rules

Every document must follow its corresponding formatting rule defined in docs/rules/.

Documents must use consistent headings and section organization.

Mermaid diagrams may be used when they help explain relationships, workflows, or decisions.

References to other project documentation should use relative Markdown links whenever applicable.

Documentation should avoid unnecessary technical details and redundant explanations.

4.3 Documentation Scope

The root docs/ directory is exclusively for high-level project documentation.

The following information belongs here:

Architectural and project-level decisions.

Feature purposes, objectives, and user journeys.

System responsibilities, boundaries, and relationships.

Data model descriptions and structures.

Documentation standards and guidelines.

Implementation-specific documentation, such as detailed code behavior, internal algorithms, function references, and implementation procedures, must not be stored here.

4.4 Component Documentation

Each major project component, such as Core and CLI, must maintain its own documentation directory.

These directories serve as the central location for implementation-specific documentation and component-level decision records.

Component documentation may include:

Implementation-specific architecture and design decisions.

Internal system and module documentation.

Implementation procedures and workflows.

Technical specifications and configurations.

Component-level ADRs or other decision records.

Each component is responsible for maintaining documentation relevant to its own implementation.

Component documentation must remain separate from the root docs/ directory to preserve the distinction between project-wide context and component-specific implementation details.

5. Documentation-Driven Development

CVbrewer follows a Documentation-Driven Development approach.

Documentation is an integral part of the development process, not an optional activity performed after implementation.

The following requirements apply:

Decisions: Significant project-wide architectural and planning decisions must have corresponding ADRs in the root docs/adr/ directory. Component-specific decisions must be documented within the corresponding component documentation directory.

Features: Every feature must have corresponding high-level feature documentation.

Systems: Every system must have corresponding high-level system documentation.

Data: Data models used by systems must have corresponding documentation.

Implementation: Implementation work must be guided by the relevant documentation. Any implementation that changes documented decisions, features, systems, or data models must trigger an update to the affected documentation.

Documentation must be created or updated before or alongside the implementation work it describes.

AI agents and assistants must treat the root documentation and relevant component documentation as the primary project context when planning, discussing, or performing development tasks.
