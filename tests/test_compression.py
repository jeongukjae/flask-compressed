import pytest

from flask_compressed.compression import Compression, Gzip, Deflate


def test_compression():
    with pytest.raises(NotImplementedError):
        Compression.compress(None)

    with pytest.raises(NotImplementedError):
        Compression.decompress(None)


def test_gzip():
    with pytest.raises(ValueError):
        Gzip.compress('hello')

    with pytest.raises(ValueError):
        Gzip.decompress('hello')

    compressed_hello = Gzip.compress(b'hello')

    assert type(compressed_hello) is bytes
    assert b'hello' == Gzip.decompress(compressed_hello)


def test_zlib():
    with pytest.raises(ValueError):
        Deflate.compress('hello')

    with pytest.raises(ValueError):
        Deflate.decompress('hello')

    compressed_hello = Deflate.compress(b'hello')

    assert type(compressed_hello) is bytes
    assert b'hello' == Deflate.decompress(compressed_hello)
