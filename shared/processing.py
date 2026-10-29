"""Processing murni untuk agregat sensor."""
from __future__ import annotations

import math
import statistics
from collections.abc import Iterable


def audio_rms(samples: Iterable[int | float], full_scale: float = 32768.0) -> tuple[float, float]:
    values = [float(x) for x in samples]
    if not values or full_scale <= 0 or any(not math.isfinite(x) for x in values):
        raise ValueError("Sampel audio kosong atau tidak valid")
    if any(abs(x) > full_scale for x in values):
        raise ValueError("Sampel melewati rentang PCM")
    rms = math.sqrt(sum(x * x for x in values) / len(values))
    dbfs = 20 * math.log10(rms / full_scale) if rms else -120.0
    return rms, max(-120.0, dbfs)


def average_lux(samples: Iterable[int | float]) -> float:
    values = [float(x) for x in samples]
    if not values or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("Sampel lux kosong, negatif, atau tidak valid")
    return statistics.fmean(values)


def moving_average(previous: float | None, current: float, weight: float = 0.5) -> float:
    if not math.isfinite(current) or current < 0 or not 0 < weight <= 1:
        raise ValueError("Nilai smoothing tidak valid")
    return current if previous is None else weight * current + (1 - weight) * previous
