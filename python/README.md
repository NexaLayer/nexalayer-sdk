# NexaLayer Python SDK

Install from the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

The package is not documented as published to PyPI yet. Use source install until an official release is available.

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
