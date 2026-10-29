"""Validasi payload, umur dan urutan telemetri."""
from __future__ import annotations

import json
import math
import time


class PayloadValidator:
    def __init__(self, max_age_seconds: float = 15):
        self.max_age = max_age_seconds
        self.last_sequence: dict[str, int] = {}

    def parse(self, device: str, payload: bytes | str, now: float | None = None) -> dict:
        try:
            item = json.loads(payload)
        except (ValueError, TypeError, UnicodeDecodeError) as exc:
            raise ValueError("JSON tidak valid") from exc
        if not isinstance(item, dict) or item.get("device_id") != device:
            raise ValueError("device_id tidak cocok")
        if item.get("mode") not in {"REAL", "SIMULATION"}:
            raise ValueError("mode harus REAL atau SIMULATION")
        seq, stamp = item.get("sequence"), item.get("timestamp")
        if isinstance(seq, bool) or not isinstance(seq, int) or seq <= self.last_sequence.get(device, 0):
            raise ValueError("sequence duplikat atau out-of-order")
        if isinstance(stamp, bool) or not isinstance(stamp, (int, float)) or not math.isfinite(stamp):
            raise ValueError("timestamp tidak valid")
        age = (time.time() if now is None else now) - stamp
        if age < -5 or age > self.max_age:
            raise ValueError("timestamp masa depan atau data stale")
        key = "noise_dbfs" if device == "audio" else "lux_avg"
        value = item.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{key} harus numerik dan finite")
        if device == "audio" and not -120 <= value <= 0:
            raise ValueError("noise_dbfs di luar rentang -120..0")
        if device == "light" and value < 0:
            raise ValueError("lux_avg tidak boleh negatif")
        self.last_sequence[device] = seq
        item["age_seconds"] = max(0.0, age)
        return item
