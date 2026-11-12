# Resume Processing Parsing Module Technical Specification

## 1. Purpose

Produces structured resume data using basic deterministic extraction followed by LLM enhancement and merging. The implementation is located at `core/src/core/modules/parsing.py`.

## 2. Code Elements

| Element | Type | Description | Arguments / Parameters | Return Value / Result |
| --- | --- | --- | --- | --- |
| `resolve_parsing_model()` | Function | Verifies LLM availability and returns the first available model name. | `llm_service: LLMService` – LLM Service interface. | `str` – First available model name; raises `LlmProcessingError` when unavailable. |
| `extract_deterministic_data()` | Function | Extracts contact fields and common resume sections with basic heuristics. | `text: str` – Extracted PDF text. | `dict[str, Any]` – Partial resume payload. |
| `merge_resume_payloads()` | Function | Merges deterministic and LLM payloads without overwriting deterministic non-empty values. | `deterministic: dict[str, Any]`, `llm_payload: dict[str, Any]` – Payloads to merge. | `dict[str, Any]` – Merged resume payload. |
| `enhance_with_llm()` | Function | Builds a structured generation request and returns the LLM resume payload. | `text`, `deterministic_payload`, `llm_service`, `model` – Source text, draft payload, LLM Service, and model name. | `dict[str, Any]` – LLM-generated resume payload. |
| `parse_resume_text()` | Function | Runs deterministic extraction, always invokes LLM enhancement, and merges the results. | `text: str`, `llm_service: LLMService`, `model: str` – Extracted text and LLM dependencies. | `dict[str, Any]` – Merged resume payload. |

## 3. Dependencies

| Name | Type | Purpose |
| --- | --- | --- |
| Python `json` | Standard library | Serializes the deterministic draft for the LLM prompt. |
| Python `re` | Standard library | Extracts contact details and date patterns. |
| LLM Service | Internal dependency | Provides model discovery and structured generation. |
| Resume schema module | Internal module | Supplies the Resume JSON Schema for structured generation. |
| Resume processing errors | Internal module | Provides `LlmProcessingError`. |

## 4. Architecture Decision Log

| Date | Decision / Description | Affected Code Elements | Reference |
| --- | --- | --- | --- |
| 11/12/2026 | Use basic deterministic heuristics, the first available model, and always-on LLM enhancement. | `resolve_parsing_model()`, `extract_deterministic_data()`, `parse_resume_text()` | [Resume-processing foundation](../../adr/11-12-26/resume-processing-foundation.md) |

## 5. References

- [Resume Processing Technical System Specification](../../systems/resume-processing/overview.md)
- [Data Parsing Process](../../../../docs/system/resume-processing/processes/6-data-parsing.md)
- [Resume Processing Schema Validation Module](../validation/schema-validation.md)
- [Use an LLM Service abstraction with pluggable LLM adapters](../../../../docs/adr/Architecture/2026-11-11/llm-service-abstraction.md)
