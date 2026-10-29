"""Konfigurasi sederhana dari environment/.env, tanpa dependency dotenv."""
from __future__ import annotations

import os
from pathlib import Path


def load_env_file(path: str | Path = ".env") -> None:
    file = Path(path)
    if not file.exists():
        return
    for raw in file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_config() -> dict:
    load_env_file()
    mode = os.getenv("PROJECT_MODE", "REAL").strip().upper()
    if mode not in {"REAL", "SIMULATION"}:
        raise ValueError("PROJECT_MODE harus REAL atau SIMULATION")
    return {
        "project_id": os.getenv("PROJECT_ID", "studyguard-demo").strip(),
        "host": os.getenv("MQTT_HOST", "broker.hivemq.com").strip(),
        "port": int(os.getenv("MQTT_PORT", "8883")),
        "tls": os.getenv("MQTT_TLS", "true").lower() in {"1", "true", "yes", "on"},
        "username": os.getenv("MQTT_USERNAME", ""),
        "password": os.getenv("MQTT_PASSWORD", ""),
        "keepalive": int(os.getenv("MQTT_KEEPALIVE", "30")),
        "noise_threshold_dbfs": float(os.getenv("NOISE_THRESHOLD_DBFS", "-35")),
        "light_threshold_lux": float(os.getenv("LIGHT_THRESHOLD_LUX", "300")),
        "max_age_seconds": float(os.getenv("MAX_AGE_SECONDS", "15")),
        "interval": float(os.getenv("SAMPLE_INTERVAL_SECONDS", "5")),
        "mode": mode,
        "light_sensor_name": os.getenv("LIGHT_SENSOR_NAME", "Light"),
        "dashboard_host": os.getenv("DASHBOARD_HOST", "0.0.0.0"),
        "dashboard_port": int(os.getenv("DASHBOARD_PORT", "8000")),
    }
