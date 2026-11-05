# Component-Level ADR / ADL Format Rules

## 1. Purpose

This document defines the documentation standards for Component-Level Architecture Decision Records (ADR) and the Architecture Decision Log (ADL) within CVBrewery.

These documents track low-level planning discussions, technical decisions, and implementation agreements made between the developer and AI within an individual component.

They serve as a reference for understanding the component's internal technical direction and guiding its implementation and future maintenance.

Component-level ADRs and ADLs must remain consistent with the project's high-level architecture and decisions documented in the root `docs/adr/` directory.

## 2. Component-Level Architecture Decision Record (ADR)

A component-level ADR documents an individual technical or implementation decision made during the planning and development of a component.

### 2.1 Documentation Requirements

Each ADR must contain the following sections:

1. **Title** - A short description of the technical decision.
    
2. **Date** - The date the decision was made.
    
3. **Status** - The current status of the decision (Proposed, Accepted, Rejected, or Superseded).
    
4. **Context** - A brief explanation of the technical problem, discussion, or circumstances that led to the decision.
    
5. **Decision** - The agreed-upon technical or implementation decision.
    
6. **Consequences** - The expected impact, trade-offs, and implications of the decision on the component.
    

### 2.2 Documentation Scope

- ADRs must focus on component-level technical decisions and implementation specifics.
    
- Decisions must be limited to the internal responsibilities and concerns of the component.
    
- Decisions may cover internal structure, module responsibilities, service interactions, data handling, processing logic, algorithms, libraries, frameworks, dependencies, interfaces, and technical configurations.
    
- Include relevant technical reasoning and trade-offs when they help explain why a decision was made.
    
- Keep documentation concise and focused on the decision.
    
- Do not document every technical discussion. Only record discussions that result in a meaningful decision.
    
- Do not use component-level ADRs to establish or modify project-wide architectural direction.
    
- Detailed implementation procedures, API references, code documentation, and operational instructions should be documented separately when necessary.
    

### 2.3 Alignment with High-Level Decisions

- Component-level decisions must comply with the project's high-level architecture and accepted ADRs.
    
- Do not duplicate high-level ADRs within component documentation.
    
- Reference relevant high-level ADRs when they provide context or constraints for a component-level decision.
    
- Component-level ADRs may define how a high-level decision is implemented within the component, but must not redefine the original decision.
    
- If a technical decision requires changing or contradicting a high-level decision, the developer must review and agree on the proposed change at the project level first.
    
- Once a high-level decision changes, review affected component-level ADRs and update them when necessary.
    

### 2.4 File Organization

Each component-level ADR must have its own Markdown file.

**Path:**

`<component>/docs/adr/<MM-DD-YY>/<topic>.md`

**Example:**

```
core/
└── docs/
    └── adr/
        ├── 11-04-26/
        │   ├── pdf-text-extraction.md
        │   └── resume-parser-strategy.md
        └── 11-05-26/
            └── schema-validation.md

cli/
└── docs/
    └── adr/
        └── 11-05-26/
            └── input-folder-discovery.md
```

- Use the decision date as the directory name.
    
- Use the `MM-DD-YY` date format.
    
- Use lowercase, hyphen-separated filenames.
    
- Each file must represent one individual decision.
    
- If a decision is revised, update its existing ADR status and create a new ADR documenting the replacement decision when appropriate.
    
- A superseded ADR must remain available for historical reference.
    

## 3. Component-Level Architecture Decision Log (ADL)

The component-level ADL serves as the central index of all ADRs belonging to an individual component.

### 3.1 Documentation Requirements

The ADL must:

- Contain links to every individual ADR within the component.
    
- Provide a brief description of each decision.
    
- Display the decision date.
    
- Display the current decision status.
    
- Organize entries chronologically, with the newest decisions first.
    
- Reflect changes to ADR statuses when decisions are updated or superseded.
    
- Include relevant references to high-level ADRs when applicable.
    

### 3.2 Documentation Scope

- The ADL must only summarize and reference individual component-level ADRs.
    
- Do not duplicate the full contents of ADRs.
    
- Do not introduce new technical or implementation decisions within the ADL.
    
- Do not include ADRs belonging to other components.
    
- Keep the log concise and easy to navigate.
    

### 3.3 File Organization

Each component must maintain its own ADL in a single Markdown file.

**Path:**

`<component>/docs/adr/ADL.md`

**Example:**

```
core/
└── docs/
    └── adr/
        ├── ADL.md
        ├── 11-04-26/
        │   ├── pdf-text-extraction.md
        │   └── resume-parser-strategy.md
        └── 11-05-26/
            └── schema-validation.md
```

All individual ADRs belonging to the component must be linked from its ADL.

## 4. General Rules

- Component-level ADRs and ADLs must remain focused on the technical and implementation concerns of their respective components.
    
- Decisions must reflect agreements made during planning discussions, not assumptions made by the AI.
    
- The AI must not independently establish or change technical decisions without developer agreement.
    
- Decisions must remain consistent with the project's high-level architecture and accepted ADRs.
    
- When a decision changes, preserve the historical record and clearly identify the latest accepted decision.
    
- Keep documentation simple, concise, and understandable.
    
- Use component-level ADRs as implementation planning references, not as replacements for component overviews, feature documentation, process documentation, technical specifications, or code documentation.
    
- Each component must maintain its own ADR directory and ADL. Component-level decisions must not be mixed into the root project's ADR/ADL.