from __future__ import annotations

import json
import time
import uuid

from shared.config import get_config
from shared.mqtt_client import create_client, topics
from shared.processing import moving_average
from edge.android_adapters import read_light_average


def main():
    cfg = get_config()
    client = create_client(cfg, f"sg-light-{uuid.uuid4().hex[:8]}")
    client.connect(cfg["host"], cfg["port"], cfg["keepalive"])
    client.loop_start()
    topic = topics(cfg)["light"]
    seq, smooth = 0, None
    print(f"HP B: sensor cahaya '{cfg['light_sensor_name']}'; mode={cfg['mode']}; topic={topic}")
    try:
        while True:
            value = read_light_average(cfg["light_sensor_name"], 5)
            smooth = moving_average(smooth, value, 0.5)
            seq += 1
            payload = {"device_id": "light", "sequence": seq, "timestamp": time.time(),
                       "lux_avg": round(smooth, 2), "mode": "REAL"}
            info = client.publish(topic, json.dumps(payload), qos=1)
            info.wait_for_publish(timeout=10)
            print(f"cahaya rata-rata/smoothing={smooth:.2f} lux; REAL")
            time.sleep(cfg["interval"])
    except KeyboardInterrupt:
        print("Edge cahaya dihentikan")
    finally:
        client.loop_stop(); client.disconnect()


if __name__ == "__main__":
    main()
