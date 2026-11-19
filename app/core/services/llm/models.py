from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class ModelInfo:
    name: str


@dataclass(frozen=True, slots=True)
class StructuredGenerationRequest:
    model: str
    messages: list[ChatMessage]
    json_schema: dict[str, Any]


@dataclass(frozen=True, slots=True)
class GenerationUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class GenerationResult:
    content: dict[str, Any]
    response_content: str
    finish_reason: str | None = None
    usage: GenerationUsage = field(default_factory=GenerationUsage)
