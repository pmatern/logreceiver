from flask import Blueprint, request

logreceive = Blueprint('logreceive', __name__)


@logreceive.route('/log/receive/events/snappy', methods=['POST'])
def snappy_compressed_events():
    request.stream

    pass
