# Feature Overview Format Rules

## Purpose

Define the standard structure and documentation requirements for feature overview documents. Feature overviews should describe the purpose, objectives, and user interaction of a feature without going into implementation details.

Follow these rules when creating or updating a feature overview document.

## Required Sections

Every feature overview document must contain sections 1–5 in the specified order.

### 1. Purpose / Summary

Provide a brief, high-level summary of the feature.

- Explain what the feature does.
    
- Describe its general purpose within the application.
    
- Avoid implementation details.
    

### 2. Objective

Describe what the feature aims to achieve.

- Identify the intended outcomes.
    
- Explain what the feature should accomplish for the user or application.
    
- Keep objectives clear and concise.
    

### 3. User Journey

Describe the user's interaction with the feature from beginning to end.

- Represent the journey using a Mermaid diagram.
    
- Focus on user actions and system responses.
    
- Keep the journey simple and high-level.
    
- Include only important decisions and outcomes.
    
- Do not include implementation details, internal processing logic, or technical operations.
    

Use the following format:

```
flowchart TD
    A[User starts] --> B[User performs an action]
    B --> C[System responds]
    C --> D{Successful?}
    D -->|Yes| E[Journey completed]
    D -->|No| F[Show error]
```

Only Mermaid diagrams are permitted for documenting user journeys.

### 4. Systems

List the systems that make up or participate in the feature.

Include a brief, high-level description of each system's responsibility.

Use the following table format:

|System|Description|
|---|---|
|[System Name](path/to/system-overview.md)|Brief description of its responsibility within the feature.|

- Include only relevant systems.
    
- Link each system directly to its corresponding system overview document.
    
- Describe responsibilities rather than implementation details.
    
- Do not duplicate detailed system architecture documentation.
    

### 5. References

List relevant documentation and external references related to the feature.

- Use bullet points.
    
- Include links to related documents, specifications, or resources.
    
- Include only relevant references.
    

## General Rules

- Follow the required section order.
    
- Keep documentation concise and high-level.
    
- Focus on feature behavior and user interaction.
    
- Avoid implementation-specific details.
    
- Refer to dedicated system, process, and technical documentation for lower-level details.