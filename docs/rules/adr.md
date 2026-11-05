# ADR / ADL Format Rules

## 1. Purpose

This document defines the documentation standards for Architecture Decision Records (ADR) and the Architecture Decision Log (ADL) within CVBrewery.

These documents track high-level planning discussions, decisions, and agreements made between the developer and AI during software planning.

They serve as a reference for understanding the project's architectural direction and guiding future development.

## 2. Architecture Decision Record (ADR)

An ADR documents an individual decision made during project planning.

### 2.1 Documentation Requirements

Each ADR must contain the following sections:

1. **Title** - A short description of the decision.
    
2. **Date** - The date the decision was made.
    
3. **Status** - The current status of the decision (Proposed, Accepted, Rejected, or Superseded).
    
4. **Category** - One of four categories: `release`, `architecture`, `feature`, or `repositories`.
    
5. **Context** - A brief explanation of the problem, discussion, or circumstances that led to the decision.
    
6. **Decision** - The agreed-upon decision.
    
7. **Consequences** - The expected impact and implications of the decision on the project.
    

### 2.2 Documentation Scope

- ADRs must focus on high-level decisions rather than implementation details.
    
- Decisions may affect one or multiple project components.
    
- Decisions may cover architecture, deployment, technology stack, systems, and features.
    
- Include relevant reasoning when it helps explain why a decision was made.
    
- Keep documentation concise and focused on the decision.
    
- Do not document every discussion. Only record discussions that result in a meaningful decision.
    
- Implementation specifications, detailed technical procedures, and code-level decisions should be documented separately when necessary.

### 2.3 Categorization Guidelines

ADR decisions must be classified into one of four categories:

1. **release** - Decisions related to deployment, releases, versioning, and packaging
    
2. **architecture** - Decisions about system architecture, technology stack, data models, and infrastructure
    
3. **feature** - Decisions about specific features, functionality, and user-facing capabilities
    
4. **repositories** - Decisions about repository structure, storage, and data management

### 2.4 File Organization

Each ADR must have its own Markdown file.

**Path:**  
`docs/<category>/<yy-mm-dd>/<topic>.md`

**Example:**

```
docs/
├── release/
│   ├── 2026-11-04/
│   │   ├── monorepo-structure.md
│   │   ├── database-responsibilities.md
│   │   └── llm-integration.md
├── architecture/
│   ├── 2026-11-05/
│   │   └── resume-storage.md
├── feature/
│   └── ...
└── repositories/
    └── ...
```

- Use the decision date as the directory name.
    
- Use lowercase, hyphen-separated filenames.
    
- Each file must represent one individual decision.
    
- If a decision is revised, update its existing ADR status and create a new ADR documenting the replacement decision when appropriate.
    
- A superseded ADR must remain available for historical reference.

## 3. Architecture Decision Log (ADL)

The ADL serves as the central index of all ADRs within CVBrewery.

### 3.1 Documentation Requirements

The ADL must:

- Contain links to every individual ADR.
    
- Provide a brief description of each decision.
    
- Display the decision date.
    
- Display the current decision status.
    
- Display the category (release, architecture, feature, or repositories).
    
- Organize entries chronologically, with the newest decisions first.
    
- Reflect changes to ADR statuses when decisions are updated or superseded.

### 3.2 Documentation Scope

- The ADL must only summarize and reference individual ADRs.
    
- Do not duplicate the full contents of ADRs.
    
- Do not introduce new decisions within the ADL.
    
- Keep the log concise and easy to navigate.

### 3.3 File Organization

The ADL must be maintained in a single Markdown file.

**Path:**  
`docs/deployment/ADL.md`

All individual ADRs must be linked from this file.

## 4. General Rules

- ADRs and the ADL must remain focused on high-level project decisions.
    
- Decisions must reflect agreements made during planning discussions, not assumptions made by the AI.
    
- The AI must not independently establish or change project decisions without developer agreement.
    
- When a decision changes, preserve the historical record and clearly identify the latest accepted decision.
    
- Keep the documentation simple, concise, and understandable without requiring knowledge of specific architectural patterns.
    
- Use ADRs as planning references, not as replacements for feature, system, architecture, or implementation documentation.````