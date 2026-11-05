# Branching Strategy

## Purpose

This document defines the Git branching strategy and workflow used in the CVBrewery repository. It establishes branch responsibilities, naming conventions, and merging rules to maintain development stability and ensure controlled releases.

## Branch Structure

CVBrewery uses two permanent branches and temporary branches for feature development, bug fixes, and release preparation.

### Permanent Branches

| Branch | Purpose                                                                                                                                                 |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main` | Contains the stable, production-ready version of the application. Changes merged into this branch represent approved releases or production fixes.      |
| `dev`  | Contains the latest integrated development changes. It serves as the primary branch for ongoing development and is deployed separately from production. |

### Temporary Branches

| Branch  | Naming Convention   | Purpose                                                                                        |
| ------- | ------------------- | ---------------------------------------------------------------------------------------------- |
| Feature | `feature/<name>`    | Used to develop new features or functionality.                                                 |
| Fix     | `fix/<name>`        | Used to resolve bugs or issues discovered during development.                                  |
| Hotfix  | `hotfix/<name>`     | Used to address urgent issues affecting the production version.                                |
| Release | `release/<version>` | Used to prepare, test, and stabilize a specific application version before production release. |

Temporary branches are created when needed and removed after their changes have been successfully integrated.

## Branching Rules

### 1. Feature Development

- Feature branches must originate from `dev`.
    
- Each feature or task should have its own branch.
    
- Completed and tested changes must be merged into `dev`.
    
- Feature branches must not be merged directly into `main`.
    
- Feature branches should be removed after successful integration.
    

### 2. Bug Fixes

- Fix branches must originate from `dev`.
    
- Each fix should have its own branch.
    
- Completed and tested fixes must be merged into `dev`.
    
- Fix branches must not be merged directly into `main`, unless the issue affects the production version and requires a hotfix.
    

### 3. Release Preparation

- Release branches must originate from `dev`.
    
- Each release branch represents a specific application version.
    
- Release branches are used for beta testing, final validation, and stabilization.
    
- Only release-related fixes and necessary adjustments should be introduced into a release branch.
    
- Once approved, the release branch must be merged into `main`.
    
- The released version must be identified using a Git tag.
    
- Changes made during release preparation must also be merged back into `dev`.
    
- Release branches should be removed after successful integration.
    

### 4. Production Hotfixes

- Hotfix branches must originate from `main`.
    
- Hotfixes are reserved for urgent issues affecting the production version.
    
- Completed and tested hotfixes must be merged into `main`.
    
- Hotfix changes must also be merged into `dev` to keep both branches synchronized.
    
- Hotfix branches should be removed after successful integration.
    

## Branch Naming Convention

Branch names must:

- Use lowercase letters.
    
- Use hyphens to separate words.
    
- Follow the designated branch prefix.
    
- Clearly describe the feature, task, or issue being addressed.
    
- Include a version number for release branches.
    

Examples:

```
feature/resume-upload
feature/job-description-parser
fix/pdf-validation
fix/resume-duplicate-check
hotfix/file-permission-error
release/1.0.0
release/1.1.0
```

## Release Versioning

CVBrewery uses version tags to identify released application versions.

The version format follows:

`MAJOR.MINOR.PATCH`

|Version Component|Description|
|---|---|
|MAJOR|Introduces incompatible changes.|
|MINOR|Introduces backward-compatible functionality.|
|PATCH|Introduces backward-compatible bug fixes.|

Beta and release candidate versions may use pre-release identifiers.

Examples:

```
v1.0.0-beta.1
v1.0.0-rc.1
v1.0.0
```

## Branch Workflow

### Standard Development Workflow

```
flowchart TD
    A[dev] --> B[Create Feature or Fix Branch]
    B --> C[Development and Testing]
    C --> D[Merge into dev]
    D --> E[Development Deployment]
```

### Release Workflow

```
flowchart TD
    A[dev] --> B[Create Release Branch]
    B --> C[Beta Testing and Validation]
    C --> D{Release Approved?}
    D -->|No| E[Apply Release Fixes]
    E --> C
    D -->|Yes| F[Merge into main]
    F --> G[Create Version Tag]
    G --> H[Production Deployment]
    H --> I[Merge Release Changes Back into dev]
```

### Production Hotfix Workflow

```
flowchart TD
    A[main] --> B[Create Hotfix Branch]
    B --> C[Apply and Test Fix]
    C --> D[Merge into main]
    D --> E[Production Deployment]
    D --> F[Merge Hotfix into dev]
```

## General Rules

- `main` must always represent a stable, production-ready version.
    
- `dev` serves as the primary integration branch for ongoing development.
    
- Direct commits to permanent branches should be avoided; changes should go through the appropriate temporary branches.
    
- Temporary branches must have a clearly defined purpose.
    
- Changes must be tested before merging into permanent branches.
    
- Release branches must only contain changes intended for their corresponding release.
    
- Merging must preserve changes made in other permanent branches to prevent development and production versions from becoming inconsistent.