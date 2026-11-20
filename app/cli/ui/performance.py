from typing import Protocol


class PerformanceValues(Protocol):
    start_memory_mb: float | None
    peak_memory_mb: float | None
    end_memory_mb: float | None
    memory_delta_mb: float | None
    cpu_avg_percent: float | None
    cpu_peak_percent: float | None
    sample_count: int


PERFORMANCE_COLUMNS: tuple[str, ...] = (
    "Start Mem (MB)",
    "Peak Mem (MB)",
    "End Mem (MB)",
    "Mem Delta (MB)",
    "CPU Avg (%)",
    "CPU Peak (%)",
    "Samples",
)


def _number(value: float | None) -> str:
    return "-" if value is None else f"{value:.1f}"


def performance_values(performance: PerformanceValues) -> tuple[str, ...]:
    return (
        _number(performance.start_memory_mb),
        _number(performance.peak_memory_mb),
        _number(performance.end_memory_mb),
        _number(performance.memory_delta_mb),
        _number(performance.cpu_avg_percent),
        _number(performance.cpu_peak_percent),
        str(performance.sample_count),
    )
