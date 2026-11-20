from dataclasses import dataclass
from datetime import datetime, timezone


class LogStatus:
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    SKIPPED = "SKIPPED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


class LoggerError(Exception):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@dataclass(frozen=True, slots=True)
class LogError:
    type: str | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class LogPerformance:
    started_at: datetime
    completed_at: datetime | None = None
    duration_ms: float | None = None
    start_memory_mb: float | None = None
    peak_memory_mb: float | None = None
    end_memory_mb: float | None = None
    memory_delta_mb: float | None = None
    cpu_avg_percent: float | None = None
    cpu_peak_percent: float | None = None
    sample_count: int = 0


@dataclass(frozen=True, slots=True)
class LogEntry:
    id: str
    operation: str
    status: str
    performance: LogPerformance
    error: LogError
    created_at: datetime
    processing_step_id: str | None = None
