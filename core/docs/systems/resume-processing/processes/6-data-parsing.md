# Data Parsing Technical Process

## 1. Purpose

Define how the Core Processing Engine turns extracted resume text into a structured resume payload.

## 2. Objective

- Produce a deterministic draft from resume text.
- Enhance the draft with the first available LLM model.
- Merge deterministic and LLM values into one payload.

## 3. Scope

### In Scope

- LLM availability checks and model selection.
- Deterministic extraction of personal information, summary, and skills.
- Structured LLM generation using the Resume JSON Schema.
- Merging deterministic and LLM payloads.

### Out of Scope

- PDF validation and text extraction.
- Schema validation of the merged payload.
- LLM transport and provider-specific communication.
- Storage.

## 4. Rules & Constraints

- Check LLM availability before processing.
- Use the first model returned by the LLM Service.
- Reject processing when the LLM service is unavailable or no models exist.
- Run deterministic extraction before LLM enhancement.
- Fall back to an empty deterministic draft when extraction fails.
- Always invoke LLM enhancement after deterministic extraction.
- Instruct the LLM to return only schema-compliant JSON and not invent facts.
- Merge values by preferring non-empty deterministic values and combining list values.

## 5. Workflow

### Diagram

````mermaid
flowchart TD
    Start([Resume text]) --> Available{LLM available?}
    Available -->|No| LlmFailure[Raise LLM processing error]
    Available -->|Yes| Models{Models available?}
    Models -->|No| LlmFailure
    Models -->|Yes| Deterministic[Extract deterministic draft]
    Deterministic --> Enhance[Generate structured LLM payload]
    Enhance -->|Failure| LlmFailure
    Enhance --> Merge[Merge deterministic and LLM payloads]
    Merge --> Return[Return structured payload]
````

### Steps

1. Verify the LLM Service is available.
2. List models and select the first model.
3. Reject processing when no model is available.
4. Extract deterministic personal information, summary, and skills from the text.
5. Use an empty draft when deterministic extraction fails.
6. Request a schema-constrained structured response from the LLM.
7. Reject non-object responses as LLM processing failures.
8. Merge deterministic and LLM values into the final payload.

## 6. Modules

- `core/src/core/modules/parsing.py` — Implements model selection, deterministic extraction, LLM enhancement, and merging.
- `core/src/core/pipeline/resume_processing.py` — Invokes parsing after text extraction.
- `core/src/core/errors.py` — Defines the LLM processing error.
- `llm/src/llm/llm_service/modules/generation/service.py` — Provides availability, model listing, and structured generation.
- `llm/src/llm/llm_service/modules/generation/models.py` — Defines generation request records.

## 7. Data

- [Resume JSON Schema](../../../../src/core/validation/schemas/resume.json) — Defines the structured payload requested from the LLM.

## 8. Testing

### 8.1 Test Level

This process should be tested at the **Process** level according to the testing strategy.

### 8.2 Test Scenarios

| Scenario ID | Given | When | Then |
|-------------|-------|------|------|
| RP-PARSE-001 | Resume text and an available LLM model. | Parsing runs. | A merged structured payload is returned. |
| RP-PARSE-002 | No available LLM model. | Parsing runs. | An LLM processing error is raised. |
| RP-PARSE-003 | Deterministic extraction fails. | Parsing runs. | LLM enhancement still runs with an empty draft. |
| RP-PARSE-004 | The LLM returns a non-object value. | Parsing runs. | An LLM processing error is raised. |

## 9. References

- [Resume Processing Technical Process](resume-processing.md)
- [Resume Processing System Overview](../overview.md)
- [Core Component Technical Specification](../../../technical-specification.md)
- [Establish the resume-processing foundation](../../../adr/11-12-26/resume-processing-foundation.md)
