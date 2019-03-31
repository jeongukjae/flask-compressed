# flask-compressed

[![Build Status](https://travis-ci.com/jeongukjae/flask-compressed.svg?branch=master)](https://travis-ci.com/jeongukjae/flask-compressed) [![codecov](https://codecov.io/gh/jeongukjae/flask-compressed/branch/master/graph/badge.svg)](https://codecov.io/gh/jeongukjae/flask-compressed) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-compressed.svg)](https://pypi.org/project/flask-compressed/)

A simple libary to send request and get response with gzip, zlib encodings.

## Usage

### Installation

```shell
pip install flask-compressed
```

### Codes

```python
from flask import Flask
from flask_compressed import FlaskCompressed

flask_app = Flask(__name__)
FlaskCompressed(flask_app)

@flask_app.route('/')
def echo():
    return g.body
```
