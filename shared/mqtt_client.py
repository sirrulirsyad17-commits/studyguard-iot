"""Pembuatan klien MQTT dengan TLS eksplisit."""
from __future__ import annotations


def create_client(config, client_id: str):
    try:
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise RuntimeError("Dependensi belum ada. Jalankan python -m pip install -r requirements.txt") from exc
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    if config["username"]:
        client.username_pw_set(config["username"], config["password"])
    if config["tls"]:
        client.tls_set()
    return client


def topics(config):
    base = f"studyguard/{config['project_id']}"
    return {"audio": f"{base}/edge/audio/telemetry",
            "light": f"{base}/edge/light/telemetry", "status": f"{base}/status"}
