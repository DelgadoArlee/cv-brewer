import threading
import time
from dataclasses import dataclass, field
from datetime import datetime

import psutil

from core.services.logger.models import LogPerformance, utc_now


def _memory_mb() -> float | None:
    try:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


def _cpu_percent(process: psutil.Process) -> float | None:
    try:
        return float(process.cpu_percent(interval=None))
    except Exception:
        return None


def _cpu_aggregate(
    samples: list[float | None],
) -> tuple[float | None, float | None, int]:
    valid = [sample for sample in samples if sample is not None]
    count = len(valid)
    if count == 0:
        return None, None, 0
    return (sum(valid) / count), max(valid), count


def _memory_peak(
    start: float | None,
    end: float | None,
    samples: list[float | None],
) -> float | None:
    values = [value for value in [start, end, *samples] if value is not None]
    return max(values) if values else None


def _memory_delta(start: float | None, end: float | None) -> float | None:
    if start is None or end is None:
        return None
    return end - start


@dataclass(frozen=True, slots=True)
class Sample:
    mono: float
    memory_mb: float | None
    cpu_percent: float | None
    step_id: str | None


@dataclass(slots=True)
class _StepState:
    step_id: str
    started_at: datetime
    start_mono: float
    start_memory_mb: float | None
    completed_at: datetime | None = None
    end_mono: float | None = None
    end_memory_mb: float | None = None


@dataclass(slots=True)
class StepMeasurement:
    step_id: str
    performance: LogPerformance


class RunPerformanceMonitor:
    def __init__(self, interval_seconds: float = 1.0) -> None:
        self._interval = interval_seconds
        self._process = psutil.Process()
        self._samples: list[Sample] = []
        self._steps: dict[str, _StepState] = {}
        self._active_step_id: str | None = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._started_at = utc_now()
        self._start_mono = time.perf_counter()
        try:
            self._process.cpu_percent(interval=None)
        except Exception:
            pass
        self._start_memory_mb = _memory_mb()
        self._completed_at: datetime | None = None
        self._end_mono: float | None = None
        self._end_memory_mb: float | None = None

    @classmethod
    def start(cls, interval_seconds: float = 1.0) -> "RunPerformanceMonitor":
        monitor = cls(interval_seconds=interval_seconds)
        monitor._thread = threading.Thread(target=monitor._run, daemon=True)
        monitor._thread.start()
        return monitor

    def _run(self) -> None:
        next_tick = time.perf_counter() + self._interval
        while not self._stop_event.is_set():
            remaining = next_tick - time.perf_counter()
            if remaining > 0:
                self._stop_event.wait(remaining)
                if self._stop_event.is_set():
                    break
            mono = time.perf_counter()
            sample = Sample(
                mono=mono,
                memory_mb=_memory_mb(),
                cpu_percent=_cpu_percent(self._process),
                step_id=self._active_step_id,
            )
            with self._lock:
                self._samples.append(sample)
            next_tick += self._interval
            if next_tick < mono:
                next_tick = mono + self._interval

    @property
    def start_memory_mb(self) -> float | None:
        return self._start_memory_mb

    @property
    def started_at(self) -> datetime:
        return self._started_at

    def begin_step(self, step_id: str) -> tuple[datetime, float | None]:
        started_at = utc_now()
        start_mono = time.perf_counter()
        start_memory_mb = _memory_mb()
        with self._lock:
            self._active_step_id = step_id
            self._steps[step_id] = _StepState(
                step_id=step_id,
                started_at=started_at,
                start_mono=start_mono,
                start_memory_mb=start_memory_mb,
            )
        return started_at, start_memory_mb

    def end_step(self, step_id: str) -> StepMeasurement:
        completed_at = utc_now()
        end_mono = time.perf_counter()
        end_memory_mb = _memory_mb()
        with self._lock:
            state = self._steps.get(step_id)
            if state is not None:
                state.completed_at = completed_at
                state.end_mono = end_mono
                state.end_memory_mb = end_memory_mb
            if self._active_step_id == step_id:
                self._active_step_id = None
            samples = list(self._samples)
        if state is None:
            performance = LogPerformance(
                started_at=completed_at,
                completed_at=completed_at,
                duration_ms=0.0,
                start_memory_mb=end_memory_mb,
                peak_memory_mb=end_memory_mb,
                end_memory_mb=end_memory_mb,
                memory_delta_mb=0.0,
                cpu_avg_percent=None,
                cpu_peak_percent=None,
                sample_count=0,
            )
            return StepMeasurement(step_id=step_id, performance=performance)

        window_samples = [
            sample
            for sample in samples
            if sample.step_id == step_id
            and state.start_mono <= sample.mono <= end_mono
        ]
        cpu_values = [sample.cpu_percent for sample in window_samples]
        cpu_avg, cpu_peak, sample_count = _cpu_aggregate(cpu_values)
        memory_samples = [
            sample.memory_mb
            for sample in window_samples
            if sample.memory_mb is not None
        ]
        peak_memory_mb = _memory_peak(
            state.start_memory_mb,
            end_memory_mb,
            memory_samples,
        )
        duration_ms = (end_mono - state.start_mono) * 1000
        performance = LogPerformance(
            started_at=state.started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            start_memory_mb=state.start_memory_mb,
            peak_memory_mb=peak_memory_mb,
            end_memory_mb=end_memory_mb,
            memory_delta_mb=_memory_delta(state.start_memory_mb, end_memory_mb),
            cpu_avg_percent=cpu_avg,
            cpu_peak_percent=cpu_peak,
            sample_count=sample_count,
        )
        return StepMeasurement(step_id=step_id, performance=performance)

    def finish(self) -> LogPerformance:
        self._completed_at = utc_now()
        self._end_mono = time.perf_counter()
        self._end_memory_mb = _memory_mb()
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 1.0)
        with self._lock:
            samples = list(self._samples)
        cpu_values = [sample.cpu_percent for sample in samples]
        cpu_avg, cpu_peak, sample_count = _cpu_aggregate(cpu_values)
        memory_samples = [
            sample.memory_mb for sample in samples if sample.memory_mb is not None
        ]
        peak_memory_mb = _memory_peak(
            self._start_memory_mb,
            self._end_memory_mb,
            memory_samples,
        )
        duration_ms = (self._end_mono - self._start_mono) * 1000
        return LogPerformance(
            started_at=self._started_at,
            completed_at=self._completed_at,
            duration_ms=duration_ms,
            start_memory_mb=self._start_memory_mb,
            peak_memory_mb=peak_memory_mb,
            end_memory_mb=self._end_memory_mb,
            memory_delta_mb=_memory_delta(self._start_memory_mb, self._end_memory_mb),
            cpu_avg_percent=cpu_avg,
            cpu_peak_percent=cpu_peak,
            sample_count=sample_count,
        )


class PerformanceMeasurement:
    def __init__(self, interval_seconds: float = 1.0) -> None:
        self._interval = interval_seconds
        self._process = psutil.Process()
        self._samples: list[Sample] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._started_at = utc_now()
        self._start_mono = time.perf_counter()
        try:
            self._process.cpu_percent(interval=None)
        except Exception:
            pass
        self._start_memory_mb = _memory_mb()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    @classmethod
    def start(cls, interval_seconds: float = 1.0) -> "PerformanceMeasurement":
        return cls(interval_seconds=interval_seconds)

    def _run(self) -> None:
        next_tick = time.perf_counter() + self._interval
        while not self._stop_event.is_set():
            remaining = next_tick - time.perf_counter()
            if remaining > 0:
                self._stop_event.wait(remaining)
                if self._stop_event.is_set():
                    break
            sample = Sample(
                mono=time.perf_counter(),
                memory_mb=_memory_mb(),
                cpu_percent=_cpu_percent(self._process),
                step_id=None,
            )
            with self._lock:
                self._samples.append(sample)
            next_tick += self._interval
            if next_tick < sample.mono:
                next_tick = sample.mono + self._interval

    def finish(self) -> LogPerformance:
        completed_at = utc_now()
        end_mono = time.perf_counter()
        end_memory_mb = _memory_mb()
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval + 1.0)
        with self._lock:
            samples = list(self._samples)
        cpu_avg, cpu_peak, sample_count = _cpu_aggregate(
            [sample.cpu_percent for sample in samples]
        )
        return LogPerformance(
            started_at=self._started_at,
            completed_at=completed_at,
            duration_ms=(end_mono - self._start_mono) * 1000,
            start_memory_mb=self._start_memory_mb,
            peak_memory_mb=_memory_peak(
                self._start_memory_mb,
                end_memory_mb,
                [sample.memory_mb for sample in samples],
            ),
            end_memory_mb=end_memory_mb,
            memory_delta_mb=_memory_delta(self._start_memory_mb, end_memory_mb),
            cpu_avg_percent=cpu_avg,
            cpu_peak_percent=cpu_peak,
            sample_count=sample_count,
        )
