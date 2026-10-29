from __future__ import annotations

import json
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from shared.config import get_config
from shared.mqtt_client import create_client, topics
from shared.rules import classify
from shared.schemas import PayloadValidator

STATE = {"audio": None, "light": None, "connections": {"mqtt": "DISCONNECTED", "audio": "OFFLINE", "light": "OFFLINE"},
         "status": "INCOMPLETE_DATA", "recommendation": "Periksa koneksi dan sensor kedua perangkat.",
         "mode": "UNKNOWN", "updated_at": None, "errors": []}
LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            body = json.dumps(STATE, ensure_ascii=False).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            body = ("<!doctype html><meta charset='utf-8'><title>StudyGuard</title>"
                    "<h1>StudyGuard</h1><pre id='s'>Memuat...</pre>"
                    "<script>async function u(){let r=await fetch('/api/status');"
                    "document.querySelector('#s').textContent=JSON.stringify(await r.json(),null,2)}"
                    "u();setInterval(u,2000)</script>").encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *_args):
        pass


def main():
    cfg = get_config(); topic = topics(cfg); validator = PayloadValidator(cfg["max_age_seconds"])
    client = create_client(cfg, f"sg-detector-{uuid.uuid4().hex[:8]}")
    def on_connect(c, _userdata, _flags, reason_code, _properties):
        if reason_code == 0:
            c.subscribe([(topic["audio"], 1), (topic["light"], 1)])
            with LOCK: STATE["connections"]["mqtt"] = "CONNECTED"
        else:
            with LOCK: STATE["connections"]["mqtt"] = f"ERROR: {reason_code}"
    def on_disconnect(_c, _userdata, _flags, reason_code, _properties):
        with LOCK: STATE["connections"]["mqtt"] = "DISCONNECTED"
        print(f"MQTT terputus: {reason_code}; menunggu reconnect otomatis")
    def on_message(_c, _userdata, msg):
        device = "audio" if msg.topic == topic["audio"] else "light"
        try:
            item = validator.parse(device, msg.payload, time.time())
            with LOCK:
                STATE[device] = item
        except ValueError as exc:
            with LOCK:
                STATE["errors"] = (STATE["errors"] + [f"{device}: {exc}"])[-5:]
            print(f"Payload {device} ditolak: {exc}")
    client.on_connect = on_connect; client.on_disconnect = on_disconnect; client.on_message = on_message
    client.connect(cfg["host"], cfg["port"], cfg["keepalive"]); client.loop_start()
    server = ThreadingHTTPServer((cfg["dashboard_host"], cfg["dashboard_port"]), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Detector aktif. Dashboard opsional: http://<IP-LAN-laptop>:{cfg['dashboard_port']}")
    print("Ambang adalah nilai demo yang dapat dikalibrasi, bukan standar resmi.")
    try:
        while True:
            now = time.time()
            with LOCK:
                items = {k: STATE[k] for k in ("audio", "light")}
                mqtt_connected = STATE["connections"]["mqtt"] == "CONNECTED"
                valid = {}
                for device, item in items.items():
                    if item and now - item["timestamp"] <= cfg["max_age_seconds"]:
                        valid[device] = item
                    STATE["connections"][device] = "CONNECTED" if device in valid else ("STALE" if item else "OFFLINE")
                modes = {x["mode"] for x in valid.values()}
                mixed = len(modes) > 1
                audio = valid.get("audio", {}).get("noise_dbfs")
                light = valid.get("light", {}).get("lux_avg")
                status, rec = classify(audio, light, cfg["noise_threshold_dbfs"], cfg["light_threshold_lux"])
                if mixed:
                    status, rec = "INCOMPLETE_DATA", "Mode REAL/SIMULATION tercampur; samakan sumber data."
                STATE["status"] = status
                STATE["recommendation"] = rec if mqtt_connected else "Koneksi MQTT terputus; periksa broker dan jaringan."
                if not mqtt_connected: STATE["status"] = "INCOMPLETE_DATA"
                STATE["mode"] = next(iter(modes)) if len(modes) == 1 else ("MIXED" if mixed else "UNKNOWN")
                STATE["updated_at"] = now
                snapshot = dict(STATE)
            output = {"timestamp": now, "status": snapshot["status"], "mode": snapshot["mode"],
                      "audio": snapshot["audio"], "light": snapshot["light"],
                      "connections": snapshot["connections"], "recommendation": snapshot["recommendation"]}
            print(json.dumps(output, ensure_ascii=False))
            client.publish(topic["status"], json.dumps(output), qos=1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Detector dihentikan")
    finally:
        server.shutdown(); client.loop_stop(); client.disconnect()


if __name__ == "__main__":
    main()
