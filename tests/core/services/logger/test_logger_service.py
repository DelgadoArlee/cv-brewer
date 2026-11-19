from datetime import datetime

import pytest
from core.services.logger import (
    LogEntry,
    LogError,
    LogPerformance,
    LoggerError,
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
        status="success",
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


def test_emit_reports_failure_after_trying_every_sink() -> None:
    first = _RecordingSink(RuntimeError("first failed"))
    second = _RecordingSink()

    with pytest.raises(LoggerError):
        LoggerService([first, second]).emit(_entry())

    assert second.entries[0].id == "log-1"


def test_performance_measurement_captures_timing_and_memory() -> None:
    measurement = PerformanceMeasurement.start()

    performance = measurement.finish()

    assert performance.completed_at is not None
    assert performance.duration_ms is not None
    assert performance.duration_ms >= 0
    assert performance.memory_before_bytes is not None
    assert performance.memory_after_bytes is not None
    assert performance.memory_peak_bytes is not None
    assert performance.memory_delta_bytes is not None
