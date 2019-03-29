import gzip
import zlib


class Compression:
    _encoding_name = ''

    @staticmethod
    def compress(content, **kwargs):
        raise NotImplementedError

    @staticmethod
    def decompress(compressed, **kwargs):
        raise NotImplementedError


class Gzip(Compression):
    @staticmethod
    def compress(content, level=5):
        if not isinstance(content, bytes):
            raise ValueError("content must be bytes literal")

        return gzip.compress(content)

    @staticmethod
    def decompress(compressed):
        if not isinstance(compressed, bytes):
            raise ValueError("content must be bytes literal")

        return gzip.decompress(compressed)


class Deflate(Compression):
    @staticmethod
    def compress(content):
        if not isinstance(content, bytes):
            raise ValueError("content must be bytes literal")

        return zlib.compress(content)

    @staticmethod
    def decompress(compressed):
        if not isinstance(compressed, bytes):
            raise ValueError("content must be bytes literal")

        return zlib.decompress(compressed)
