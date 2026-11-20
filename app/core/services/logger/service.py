import logging
from collections.abc import Sequence

from core.services.logger.models import LogEntry
from core.services.logger.port import LogSink

_LOGGER = logging.getLogger(__name__)


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
            _LOGGER.error(
                "Failed to write log entry %s to %d of %d sink(s).",
                entry.id,
                len(failures),
                len(self._sinks),
                exc_info=failures[0],
            )
