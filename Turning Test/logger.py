import datetime
import json

def log(event_type: str, payload: dict):
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "payload": payload
    }
    print(json.dumps(entry, ensure_ascii=False))
