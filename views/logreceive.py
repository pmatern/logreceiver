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
    log_entries = strip_excluded(log_entries)

    for log_entry in log_entries:
        remove_dots_from_keys(log_entry)

    send_to_mongo(log_entries)

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

def remove_dots_from_keys(log_entry):
    bad_keys = []

    for key, value in log_entry.items():
        if isinstance(value, dict):
            remove_dots_from_keys(value)

        if "." in key:
            bad_keys.append(key)
            new_key = key.replace(".", "_")
            log_entry[new_key] = value

    for key in bad_keys:
        del log_entry[key]


def send_to_mongo(json_logs):
    if json_logs:
        client = MongoClient(app.config["DB_HOST"], app.config["DB_PORT"])
        db = client.metric_logs
        collection = db.wal
        collection.insert(json_logs)


def build_int(four_bytes):
    return int(four_bytes.encode('hex'), 16)
