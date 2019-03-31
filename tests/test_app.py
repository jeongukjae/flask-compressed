import gzip
import zlib
import json

from flask import Flask, g
from flask_compressed import FlaskCompressed, compress_as_gzip


def test_flask_compressed():
    flask_app = Flask(__name__)

    FlaskCompressed(flask_app)

    # attached to flask app's hooks
    assert len(flask_app.before_request_funcs) == 1


def test_send_gzip():
    flask_app = Flask(__name__)
    FlaskCompressed(flask_app)

    flask_app.config['TESTING'] = True

    flask_app.route('/', methods=['POST'])(lambda: g.body)

    with open('./tests/data/test1.json', 'r') as f:
        original_data = f.read().encode('utf8')
        compressed_data = gzip.compress(original_data)

    with flask_app.test_client() as client:
        response = client.post(
            '/',
            data=compressed_data,
            headers=dict({'Content-Encoding': 'gzip'}))
        assert response.data == original_data


def test_send_zlib():
    flask_app = Flask(__name__)
    FlaskCompressed(flask_app)

    flask_app.config['TESTING'] = True

    flask_app.route('/', methods=['POST'])(lambda: g.body)

    with open('./tests/data/test1.json', 'r') as f:
        original_data = f.read().encode('utf8')
        compressed_data = zlib.compress(original_data)

    with flask_app.test_client() as client:
        response = client.post(
            '/',
            data=compressed_data,
            headers=dict({'Content-Encoding': 'deflate'}))
        assert response.data == original_data


def test_send_multiple():
    flask_app = Flask(__name__)
    FlaskCompressed(flask_app)

    flask_app.config['TESTING'] = True
    flask_app.route('/', methods=['POST'])(lambda: g.body)

    with open('./tests/data/test1.json', 'r') as f:
        original_data = f.read().encode('utf8')
        compressed_data = zlib.compress(original_data)
        compressed_data = gzip.compress(compressed_data)

    with flask_app.test_client() as client:
        response = client.post(
            '/',
            data=compressed_data,
            headers=dict({'Content-Encoding': 'deflate, gzip'}))
        assert response.data == original_data


def test_response():
    flask_app = Flask(__name__)
    FlaskCompressed(flask_app)
    messages = json.dumps({'message': 'hello'})

    @flask_app.route('/')
    @compress_as_gzip
    def index():
        return messages, 200

    with flask_app.test_client() as client:
        response = client.get('/')
        assert messages.encode('utf8') == gzip.decompress(response.get_data())
