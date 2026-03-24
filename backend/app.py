import json
import os
import time
from collections import deque

import paho.mqtt.client as mqtt


BROKER_HOST = os.getenv("MQTT_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_PORT", "1883"))
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "hand-mirror-backend")
TOPIC_IN = os.getenv("MQTT_TOPIC_IN", "hand/raw")
TOPIC_OUT = os.getenv("MQTT_TOPIC_OUT", "hand/filtered")


class LowPassFilter:
    def __init__(self, window_size=6):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def update(self, value):
        self.buffer.append(value)
        return sum(self.buffer) / len(self.buffer)


def parse_payload(payload):
    try:
        data = json.loads(payload)
        return float(data.get("position", 0.0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("MQTT connected.")
        client.subscribe(TOPIC_IN, qos=1)
    else:
        print(f"MQTT connection failed with code {rc}.")


def on_message(client, userdata, msg):
    value = parse_payload(msg.payload.decode("utf-8"))
    if value is None:
        return

    filtered = userdata["filter"].update(value)
    payload = json.dumps(
        {
            "position": round(filtered, 4),
            "latency_ms": int((time.time() - userdata["last_tick"]) * 1000),
        }
    )
    client.publish(TOPIC_OUT, payload=payload, qos=1)
    userdata["last_tick"] = time.time()


def main():
    state = {"filter": LowPassFilter(window_size=5), "last_tick": time.time()}

    client = mqtt.Client(client_id=CLIENT_ID)
    client.user_data_set(state)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=30)
    print(f"Listening on {BROKER_HOST}:{BROKER_PORT} | {TOPIC_IN} -> {TOPIC_OUT}")
    client.loop_forever()


if __name__ == "__main__":
    main()
