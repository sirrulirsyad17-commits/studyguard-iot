"""Pengirim data buatan untuk demo logika. Selalu diberi label SIMULATION."""
from __future__ import annotations

import argparse
import json
import time
import uuid

from shared.config import get_config
from shared.mqtt_client import create_client, topics


def main():
    parser = argparse.ArgumentParser(description="Kirim data SIMULATION, bukan sensor fisik")
    parser.add_argument("--noise", type=float, default=-45)
    parser.add_argument("--lux", type=float, default=450)
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    if args.noise < -120 or args.noise > 0 or args.lux < 0:
        parser.error("noise harus -120..0 dBFS dan lux tidak negatif")
    cfg = get_config(); client = create_client(cfg, f"sg-sim-{uuid.uuid4().hex[:8]}")
    client.connect(cfg["host"], cfg["port"], cfg["keepalive"]); client.loop_start()
    topic = topics(cfg); seq = {"audio": 0, "light": 0}
    try:
        for _ in range(args.count):
            now = time.time()
            for device, key, value in (("audio", "noise_dbfs", args.noise), ("light", "lux_avg", args.lux)):
                seq[device] += 1
                payload = {"device_id": device, "sequence": seq[device], "timestamp": now,
                           key: value, "mode": "SIMULATION"}
                client.publish(topic[device], json.dumps(payload), qos=1)
            print(f"SIMULATION: noise={args.noise} dBFS, light={args.lux} lux")
            time.sleep(cfg["interval"])
    finally:
        client.loop_stop(); client.disconnect()


if __name__ == "__main__":
    main()
