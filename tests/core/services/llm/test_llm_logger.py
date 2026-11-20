from datetime import datetime

from core.services.logger import LogError, LogPerformance, LoggerService, LogSink
from core.services.llm import (
    ChatMessage,
    GenerationResult,
    GenerationUsage,
    LLMTimeoutError,
    StructuredGenerationRequest,
)
from core.services.llm.logger import LLMLogger
from core.services.logger.models import LogEntry


class _RecordingSink(LogSink):
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def write(self, entry: LogEntry) -> None:
        self.entries.append(entry)


def _request() -> StructuredGenerationRequest:
    return StructuredGenerationRequest(
        model="llama3.1",
        messages=[
            ChatMessage(role="system", content="Extract resume data."),
            ChatMessage(role="user", content="Resume text."),
        ],
        json_schema={"type": "object"},
    )


def _performance() -> LogPerformance:
    return LogPerformance(
        started_at=datetime(2026, 11, 19, 10, 0),
        completed_at=datetime(2026, 11, 19, 10, 0, 1),
        duration_ms=1000.0,
        start_memory_mb=100.0,
        peak_memory_mb=250.0,
        end_memory_mb=200.0,
        memory_delta_mb=100.0,
        cpu_avg_percent=12.5,
        cpu_peak_percent=20.0,
        sample_count=2,
    )


def _result() -> GenerationResult:
    return GenerationResult(
        content={"name": "Ada"},
        response_content='{"name": "Ada"}',
        finish_reason="stop",
        usage=GenerationUsage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
    )


def test_record_generation_captures_success_details() -> None:
    sink = _RecordingSink()
    logger = LLMLogger("ollama", LoggerService([sink]))

    record = logger.record_generation(
        _request(),
        _performance(),
        result=_result(),
        processing_step_id="step-1",
    )

    assert record.status == "SUCCESS"
    assert record.processing_step_id == "step-1"
    assert record.provider == "ollama"
    assert record.model == "llama3.1"
    assert record.request.system_prompt == "Extract resume data."
    assert record.request.prompt == "Resume text."
    assert record.request.parameters.temperature is None
    assert record.request.parameters.top_p is None
    assert record.request.parameters.top_k is None
    assert record.request.parameters.num_ctx is None
    assert record.request.parameters.max_tokens is None
    assert record.response.content == '{"name": "Ada"}'
    assert record.response.finish_reason == "stop"
    assert record.usage.input_tokens == 10
    assert record.usage.output_tokens == 5
    assert record.usage.total_tokens == 15
    assert record.error == LogError()
    assert sink.entries == [record]


def test_record_generation_maps_timeout_errors() -> None:
    sink = _RecordingSink()
    logger = LLMLogger("ollama", LoggerService([sink]))
    error = LLMTimeoutError("timed out")

    record = logger.record_generation(_request(), _performance(), error=error)

    assert record.status == "TIMEOUT"
    assert record.error.type == "LLMTimeoutError"
    assert record.error.message == "timed out"
    assert record.response.content is None
    assert record.usage.total_tokens is None


def test_record_generation_maps_other_errors() -> None:
    sink = _RecordingSink()
    logger = LLMLogger("ollama", LoggerService([sink]))

    record = logger.record_generation(
        _request(),
        _performance(),
        error=RuntimeError("generation failed"),
    )

    assert record.status == "FAILED"
    assert record.error.type == "RuntimeError"
