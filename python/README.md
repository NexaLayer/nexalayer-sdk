# NexaLayer Python SDK

Install from PyPI:

```bash
pip install nexalayer
```

The public package is `nexalayer`.

## Usage

```python
import os
from nexalayer import NexaLayerClient

client = NexaLayerClient(api_key=os.environ["NEXALAYER_API_KEY"])
products = client.get_products(type="dynamic")
```

Create sessions with a `product_no` returned by `/products`; do not hardcode old product IDs.

## Tests

```bash
pytest -v
```

Run from repo root or from `python/` with `PYTHONPATH=.. pytest -v`.
