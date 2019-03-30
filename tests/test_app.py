import gzip
import zlib

from flask import Flask, g

from flask_compressed import FlaskCompressed


def test_flask_compressed():
    flask_app = Flask(__name__)

    FlaskCompressed(flask_app)

    # attached to flask app's hooks
    assert len(flask_app.after_request_funcs) == 1
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
