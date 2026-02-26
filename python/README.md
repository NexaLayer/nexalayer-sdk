# NexaLayer Python SDK

Install in development mode from the **repository root**:

```bash
pip install -e ".[dev]"
```

Or from this directory (parent must have pyproject.toml):

```bash
pip install -e "..[dev]"
```

## Usage

```python
from nexalayer import NexaLayerClient

client = NexaLayerClient(api_key="your-api-key", base_url="https://api.nexalayer.net/v1")
session = client.create_session(type="dynamic", config={"product_no": "out_dynamic_1"})
resp = session.get("https://httpbin.org/ip")
```

## Tests

```bash
pytest -v
```

Run from repo root or from `python/` with `PYTHONPATH=.. pytest -v`.
