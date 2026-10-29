"""Adapter Termux API. Keluaran hardware tidak disimulasikan bila gagal."""
from __future__ import annotations

import json
import os
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

from shared.processing import audio_rms, average_lux


def _run(args, timeout=20):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip() or f"Perintah gagal: {args[0]}")
    return result.stdout


def read_audio_window(seconds=1):
    """Rekam satu jendela WAV pendek via Termux API, hitung level, hapus file."""
    fd, name = tempfile.mkstemp(prefix="studyguard-", suffix=".wav")
    os.close(fd)
    path = Path(name)
    try:
        # No codec is forced: Termux:API encoders vary by version/device.
        # The following parser accepts only verified PCM WAV and otherwise fails.
        _run(["termux-microphone-record", "-f", str(path), "-l", str(seconds)], timeout=seconds + 20)
        with wave.open(str(path), "rb") as wav:
            if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getcomptype() != "NONE":
                raise RuntimeError("Audio harus WAV PCM 16-bit mono; periksa dukungan format HP")
            raw = wav.readframes(wav.getnframes())
            if not raw:
                raise RuntimeError("Rekaman audio kosong")
            count = len(raw) // 2
            samples = struct.unpack("<" + "h" * count, raw[:count * 2])
            _rms, dbfs = audio_rms(samples)
            return dbfs
    finally:
        path.unlink(missing_ok=True)


def _collect_numbers(obj, sensor_name):
    found = []
    if isinstance(obj, dict):
        identity = " ".join(str(obj.get(key, "")) for key in ("name", "type", "type_name"))
        if sensor_name.lower() in identity.lower() and "values" in obj:
            vals = obj["values"]
            vals = vals if isinstance(vals, list) else [vals]
            try:
                found.extend(float(x) for x in vals)
            except (TypeError, ValueError):
                pass
        for key, value in obj.items():
            if sensor_name.lower() in str(key).lower():
                if isinstance(value, dict) and "values" in value:
                    vals = value["values"]
                    vals = vals if isinstance(vals, list) else [vals]
                    found.extend(float(x) for x in vals)
            found.extend(_collect_numbers(value, sensor_name))
    elif isinstance(obj, list):
        for value in obj:
            found.extend(_collect_numbers(value, sensor_name))
    return found



def read_light_average(sensor_name, count=5):
    output = _run(
        ["termux-sensor", "-s", sensor_name, "-n", str(count)],
        timeout=30
    )

    decoder = json.JSONDecoder()
    readings = []
    position = 0

    while position < len(output):
        remaining = output[position:].lstrip()

        if not remaining:
            break

        data, consumed = decoder.raw_decode(remaining)
        position = len(output) - len(remaining) + consumed

        sensor = data.get(sensor_name, {})
        values = sensor.get("values", [])

        if values:
            lux = float(values[0])
            if lux >= 0:
                readings.append(lux)

    if not readings:
        raise RuntimeError(
            f"Tidak ada pembacaan cahaya valid dari '{sensor_name}'"
        )

    return average_lux(readings)

