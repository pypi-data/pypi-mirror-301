# jj-district42

⚠️ This package has been renamed to [jj-d42](https://pypi.org/project/jj-d42/). The [jj-district42](https://pypi.org/project/jj-district42/) package on PyPI is no longer maintained. For updates and improvements, please use [jj-d42](https://pypi.org/project/jj-d42/) going forward.

[![PyPI](https://img.shields.io/pypi/v/jj-district42.svg?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/jj-district42?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)
[![Python Version](https://img.shields.io/pypi/pyversions/jj-district42.svg?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)


## Installation

```sh
pip3 install jj-district42
```

## Usage

```python
import jj
import httpx
from jj.mock import mocked
from jj_district42 import HistorySchema
from valera import validate_or_fail


matcher = jj.match("GET", "/users")
response = jj.Response(status=200, json=[])

with mocked(matcher, response) as mock:
    resp = httpx.get("http://localhost:8080/users", params={"user_id": 1})

assert validate_or_fail(
    HistorySchema % [
        {
            "request": {
                "method": "GET",
                "path": "/users",
                "params": {"user_id": "1"},
            }
        }
    ],
    mock.history
)
```
