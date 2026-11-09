# CLI Paths Module Technical Specification

## 1. Purpose

Provides the filesystem locations used during application startup. The module defines a shared layout for the database file and the resume input and generated output folders under a supplied data directory, and provides the development-only locations under the CLI component.

## 2. Code Elements

| Element                       | Type      | Description                                                        | Arguments / Parameters                                                                                                     | Return Value / Result                                                                                           |
| ----------------------------- | --------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `StartupPaths`                | Dataclass | Holds the paths required during startup.                           | `database: Path` – Database file path. `resumes: Path` – Resume input folder. `generated: Path` – Generated output folder. | `StartupPaths` instance.                                                                                        |
| `startup_paths()`             | Function  | Builds the startup paths for a supplied data directory.           | `data_dir: Path` – Root directory for startup data.                                                                        | `StartupPaths` instance using `cvbrewer.db`, `local/resumes`, and `local/generated` under `data_dir`.             |
| `development_startup_paths()` | Function  | Builds the development-only startup paths under the CLI component. | None.                                                                                                                      | `StartupPaths` instance using `cli/data/cvbrewer.db`, `cli/data/local/resumes`, and `cli/data/local/generated`. |

## 3. Dependencies

| Name          | Type                    | Purpose                                       |
| ------------- | ----------------------- | --------------------------------------------- |
| `pathlib`     | Python standard library | Provides filesystem path handling.            |
| `dataclasses` | Python standard library | Defines the immutable startup path container. |

## 4. Architecture Decision Log (ADL)

| Date       | Decision / Description                                      | Affected Code Elements                        | Reference                                                                       |
| ---------- | ----------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| 11/07/2026 | Added development-only startup locations under `cli/data/` and a shared startup path factory. | `StartupPaths`, `startup_paths()`, `development_startup_paths()` | [Development application startup](../adr/11-07-26/development-startup-paths.md) |

## 5. References

- [CLI Component Technical Specification](../technical-specification.md)
- [Application Startup Technical Process](../processes/application-startup.md)
- [Development Application Startup Decision](../adr/11-07-26/development-startup-paths.md)
- [CLI Component ADL](../adr/ADL.md)
