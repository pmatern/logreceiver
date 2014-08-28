import snappy
import json
from pymongo import MongoClient
from flask import Blueprint, request

logreceive = Blueprint('logreceive', __name__)

@logreceive.route('/log/receive/events', methods=['POST'])
def receive_events():
    parse_and_store(request.data)
    return "OK", 200

@logreceive.route('/log/receive/events/snappy', methods=['POST'])
def receive_snappy_compressed_events():
    parse_and_store(snappy.uncompress(request.data))
    return "OK", 200

def parse_and_store(entry_bytes):
    send_to_mongo(parse_log_entries(entry_bytes))

def parse_log_entries(entry_bytes):
    idx = 0
    msgs = []

    while idx < len(entry_bytes):
        size = build_int(entry_bytes[idx : idx + 4])
        idx += 4
        json_bytes = entry_bytes[idx : idx + size]
        idx += size

        json_object = json.loads(json_bytes)
        msgs.append(json_object)

    return msgs


def send_to_mongo(json_logs):
    client = MongoClient("localhost", 27017) # yeah I know
    db = client.metric_logs # yeah I know
    collection = db.wal
    collection.insert(json_logs)


def build_int(four_bytes):
    return int(four_bytes.encode('hex'), 16)
