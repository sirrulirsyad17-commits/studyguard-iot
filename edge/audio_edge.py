from __future__ import annotations

import json
import time
import uuid

from shared.config import get_config
from shared.mqtt_client import create_client, topics
from edge.android_adapters import read_audio_window


def main():
    cfg = get_config()
    client = create_client(cfg, f"sg-audio-{uuid.uuid4().hex[:8]}")
    client.connect(cfg["host"], cfg["port"], cfg["keepalive"])
    client.loop_start()
    topic = topics(cfg)["audio"]
    seq = 0
    print(f"HP A: sensor mikrofon nyata; mode={cfg['mode']}; topic={topic}")
    try:
        while True:
            # Mode edge nyata sengaja tidak mengubah kegagalan hardware menjadi data simulasi.
            value = read_audio_window(1)
            seq += 1
            payload = {"device_id": "audio", "sequence": seq, "timestamp": time.time(),
                       "noise_dbfs": round(value, 2), "mode": "REAL"}
            info = client.publish(topic, json.dumps(payload), qos=1)
            info.wait_for_publish(timeout=10)
            print(f"audio dBFS relatif={value:.2f}; REAL")
            time.sleep(max(0, cfg["interval"] - 1))
    except KeyboardInterrupt:
        print("Edge audio dihentikan")
    finally:
        client.loop_stop(); client.disconnect()


if __name__ == "__main__":
    main()
