import logging
from datetime import datetime

import pytest
from core.services.logger import (
    LogEntry,
    LogError,
    LogPerformance,
    LoggerService,
    LogSink,
    PerformanceMeasurement,
)


class _RecordingSink(LogSink):
    def __init__(self, failure: Exception | None = None) -> None:
        self.entries: list[LogEntry] = []
        self.failure = failure

    def write(self, entry: LogEntry) -> None:
        if self.failure is not None:
            raise self.failure
        self.entries.append(entry)


def _entry() -> LogEntry:
    return LogEntry(
        id="log-1",
        operation="generate_structured",
        status="SUCCESS",
        performance=LogPerformance(started_at=datetime(2026, 11, 19, 10, 0)),
        error=LogError(),
        created_at=datetime(2026, 11, 19, 10, 0, 1),
    )


def test_emit_delivers_unchanged_entry_to_one_sink() -> None:
    sink = _RecordingSink()
    entry = _entry()

    LoggerService([sink]).emit(entry)

    assert sink.entries == [entry]


def test_emit_delivers_unchanged_entry_to_every_sink() -> None:
    first = _RecordingSink()
    second = _RecordingSink()

    LoggerService([first, second]).emit(_entry())

    assert first.entries == second.entries


def test_emit_succeeds_without_sinks() -> None:
    LoggerService([]).emit(_entry())


def test_emit_reports_failure_after_trying_every_sink(
    caplog: pytest.LogCaptureFixture,
) -> None:
    first = _RecordingSink(RuntimeError("first failed"))
    second = _RecordingSink()

    with caplog.at_level(logging.ERROR):
        LoggerService([first, second]).emit(_entry())

    assert second.entries[0].id == "log-1"
    assert "Failed to write log entry log-1" in caplog.text


def test_performance_measurement_captures_timing_memory_and_cpu() -> None:
    measurement = PerformanceMeasurement.start()

    performance = measurement.finish()

    assert performance.completed_at is not None
    assert performance.duration_ms is not None
    assert performance.duration_ms >= 0
    assert performance.start_memory_mb is not None
    assert performance.end_memory_mb is not None
    assert performance.peak_memory_mb is not None
    assert performance.memory_delta_mb is not None
    assert performance.sample_count >= 0
