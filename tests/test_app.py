import zlib
import pytest

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

    @flask_app.route('/', methods=['POST'])
    def echo():
        print(g)
        return g.decompressed_body

    with open('./tests/data/test1.json', 'r') as f:
        original_data = f.read()
        compressed_data = zlib.compress(original_data.encode('utf8'))

    with flask_app.test_client() as client:
        response = client.post(
            '/',
            data=compressed_data,
            headers=dict({'Content-Encoding': 'gzip'}))
        assert response.data == compressed_data
