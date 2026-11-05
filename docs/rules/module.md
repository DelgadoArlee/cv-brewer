# Module Technical Specification Format Rules

## 1. Purpose

This document defines the documentation standards for Module Technical Specifications within CVBrewer.

A Module Technical Specification documents the internal technical structure of an individual module, including its functions, objects, classes, interfaces, and other relevant code elements.

It serves as a technical reference for developers and AI agents when understanding, maintaining, or modifying a module.

## 2. Document Structure

Each Module Technical Specification must follow this structure:

### 2.1 Purpose

Describe the purpose and primary responsibility of the module.

Keep the description concise and focused on what the module does.

### 2.2 Code Elements

Document the relevant functions, objects, classes, interfaces, constants, types, and other code elements within the module.

Each documented element should include:

- **Name:** Name of the function, object, class, or other code element.
- **Type:** Function, Class, Object, Interface, Constant, Type, Enum, etc.
- **Description:** What the element does and its responsibility.
- **Arguments / Parameters:** Inputs accepted by the element, including their names, types, and descriptions.
- **Return Value / Result:** What the element returns or produces, including its type and description.
- **Notes:** Additional behavior, constraints, or relevant implementation details, when necessary.

Example:

| Element            | Type     | Description                        | Arguments / Parameters                     | Return Value / Result                                |
| ------------------ | -------- | ---------------------------------- | ------------------------------------------ | ---------------------------------------------------- |
| `validateResume()` | Function | Validates the uploaded resume PDF. | `filePath: string` – Path to the PDF file. | `ValidationResult` – Validation outcome and details. |
| `Resume`           | Class    | Represents the parsed resume data. | `data: ResumeData` – Resume information.   | `Resume` instance.                                   |

Document only elements relevant to understanding the module. Do not document every trivial implementation detail.

### 2.3 Dependencies

List the module's internal and external dependencies.

For each dependency, provide:

- **Name:** Name of the dependency.
- **Type:** Internal Module, External Library, Package, or other relevant type.
- **Purpose:** Why the module depends on it.

Use links to the corresponding technical documentation when available.

### 2.4 Architecture Decision Log (ADL)

List architecture and implementation decisions that affect the module's internal structure or behavior.

Use the following table:

| Date       | Decision / Description             | Affected Code Elements                | Reference             |
| ---------- | ---------------------------------- | ------------------------------------- | --------------------- |
| MM/DD/YYYY | Brief description of the decision. | `validateResume()`, `ResumeValidator` | [ADL Reference](link) |

The **Affected Code Elements** column must identify the specific functions, objects, classes, interfaces, or other elements affected by the decision.

For new elements, indicate whether they were added. For modified or removed elements, identify the affected elements accordingly.

Only include decisions relevant to the module. Refer to the original ADL for the complete decision details.

### 2.5 References

List relevant documentation and resources used by or related to the module.

References may include:

- Parent system or component technical specifications.
- Related module documentation.
- Architecture Decision Records (ADR).
- Architecture Decision Logs (ADL).
- Data schemas and models.
- External library documentation.
- Relevant standards and technical specifications.

Use descriptive links rather than raw URLs.

## 3. Documentation Guidelines

1. Each module must have its own Module Technical Specification.
2. Document only code elements relevant to understanding the module.
3. Function arguments and return values must include their types and descriptions.
4. Document optional parameters, default values, and possible errors when relevant.
5. Dependencies must identify both internal and external dependencies.
6. ADL entries must identify the specific code elements affected by each decision.
7. Keep documentation consistent with the actual implementation.
8. Update the specification whenever relevant module structures or documented code elements change.
9. Avoid duplicating detailed explanations already available in referenced documentation.
