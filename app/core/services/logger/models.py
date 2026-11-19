from dataclasses import dataclass
from datetime import datetime, timezone


class LogStatus:
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


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
    memory_before_bytes: int | None = None
    memory_after_bytes: int | None = None
    memory_peak_bytes: int | None = None
    memory_delta_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class LogEntry:
    id: str
    operation: str
    status: str
    performance: LogPerformance
    error: LogError
    created_at: datetime
