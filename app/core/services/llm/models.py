from dataclasses import dataclass
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
