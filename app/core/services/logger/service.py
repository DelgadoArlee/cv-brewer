from collections.abc import Sequence

from core.services.logger.models import LoggerError, LogEntry
from core.services.logger.port import LogSink


class LoggerService:
    def __init__(self, sinks: Sequence[LogSink]) -> None:
        self._sinks = tuple(sinks)

    def emit(self, entry: LogEntry) -> None:
        failures: list[Exception] = []
        for sink in self._sinks:
            try:
                sink.write(entry)
            except Exception as exc:
                failures.append(exc)
        if failures:
            raise LoggerError(
                f"Failed to write log entry to {len(failures)} of "
                f"{len(self._sinks)} sink(s)."
            ) from failures[0]
