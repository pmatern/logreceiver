import snappy
import json
from pymongo import MongoClient
from flask import Blueprint, request
from flask import current_app as app

logreceive = Blueprint('logreceive', __name__)

@logreceive.route('/log/receive/events', methods=['POST'])
def receive_events():
    store(parse_log_entries(request.data))
    return "OK", 200

@logreceive.route('/log/receive/events/snappy', methods=['POST'])
def receive_snappy_compressed_events():
    store(parse_log_entries(snappy.uncompress(request.data)))
    return "OK", 200

def store(log_entries):
    send_to_mongo(strip_excluded(log_entries))

def parse_log_entries(entry_bytes):
    idx = 0
    msgs = []

    while idx < len(entry_bytes):
        size = build_int(entry_bytes[idx : idx + 4])
        idx += 4
        if size < 0 or size > len(entry_bytes) - idx:
            raise IndexError(size)
        json_bytes = entry_bytes[idx : idx + size]
        idx += size

        json_object = json.loads(json_bytes)
        msgs.append(json_object)

    return msgs

def strip_excluded(log_entries):
    excluded = app.config["EXCLUDED_NAMES"]
    stripped = []
    for log_entry in log_entries:
        if log_entry["name"] not in excluded:
            stripped.append(log_entry)

    return stripped


def send_to_mongo(json_logs):
    if json_logs:
        client = MongoClient(app.config["DB_HOST"], app.config["DB_PORT"])
        db = client.metric_logs
        collection = db.wal
        collection.insert(json_logs)


def build_int(four_bytes):
    return int(four_bytes.encode('hex'), 16)
