import tracemalloc
from dataclasses import dataclass
from datetime import datetime
from time import perf_counter

from core.services.logger.models import LogPerformance, utc_now


def _memory_snapshot() -> tuple[int, int] | None:
    if not tracemalloc.is_tracing():
        return None
    return tracemalloc.get_traced_memory()


@dataclass(slots=True)
class PerformanceMeasurement:
    started_at: datetime
    memory_before_bytes: int | None = None
    completed_at: datetime | None = None
    duration_ms: float | None = None
    memory_after_bytes: int | None = None
    memory_peak_bytes: int | None = None
    memory_delta_bytes: int | None = None
    _started_clock: float = 0.0
    _owns_tracing: bool = False

    @classmethod
    def start(cls) -> "PerformanceMeasurement":
        owns_tracing = not tracemalloc.is_tracing()
        if owns_tracing:
            tracemalloc.start()
        snapshot = _memory_snapshot()
        return cls(
            started_at=utc_now(),
            memory_before_bytes=snapshot[0] if snapshot else None,
            _started_clock=perf_counter(),
            _owns_tracing=owns_tracing,
        )

    def finish(self) -> LogPerformance:
        snapshot = _memory_snapshot()
        self.completed_at = utc_now()
        self.duration_ms = (perf_counter() - self._started_clock) * 1000
        self.memory_after_bytes = snapshot[0] if snapshot else None
        self.memory_peak_bytes = snapshot[1] if snapshot else None
        self.memory_delta_bytes = (
            snapshot[0] - self.memory_before_bytes
            if snapshot and self.memory_before_bytes is not None
            else None
        )
        if self._owns_tracing:
            tracemalloc.stop()
        return self.to_performance()

    def to_performance(self) -> LogPerformance:
        return LogPerformance(
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_ms=self.duration_ms,
            memory_before_bytes=self.memory_before_bytes,
            memory_after_bytes=self.memory_after_bytes,
            memory_peak_bytes=self.memory_peak_bytes,
            memory_delta_bytes=self.memory_delta_bytes,
        )
