# NexaLayer SDK

Managed network sessions for Playwright, Browser Use, AI agents, and automation scripts.

**Keep using proxies. Stop managing them.**  
中文：代理继续使用，代理管理交给 NexaLayer。

This repository contains the Python and Node/TypeScript SDK source. The packages are not yet published to PyPI or npm from this workspace, so install from source until an official release is announced.

## Status

| Runtime | Source | Package registry status |
| --- | --- | --- |
| Python | `python/` | Source install supported; PyPI publication not confirmed |
| Node / TypeScript | `node/` | Source build supported; npm publication not confirmed |

## Installation

Python from repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Node from repository root:

```bash
cd node
npm install
npm run build
```

## Authentication

```bash
export NEXALAYER_BASE_URL=https://api.nexalayer.net/v1
export NEXALAYER_API_KEY=agk_your_key
```

The SDK uses `X-API-Key` for Agent requests.

## 60-second Python example

This example auto-selects a dynamic product, creates a session, reports telemetry, reads health, and terminates the session in cleanup.

```python
import os
import time
import uuid

import requests
from nexalayer import NexaLayerClient

api_key = os.environ["NEXALAYER_API_KEY"]
client = NexaLayerClient(api_key=api_key)
session_id = None

def data(resp):
    return resp.get("data", resp)

try:
    products = data(client.get_products(type="dynamic"))
    product = next(p for p in products.get("items", []) if p.get("product_no"))

    session = client.create_session(
        session_type="dynamic",
        product_no=product["product_no"],
        quantity=1,
        protocol="socks5",
        rotation_mode="on_demand",
        idempotency_key=f"py-{uuid.uuid4()}",
    )
    session_id = session.session_id

    for _ in range(60):
        current = data(client.get_session(session_id))
        if current.get("status") == "active":
            proxy_url = current["proxy"]["full_url"]
            break
        time.sleep(2)
    else:
        raise TimeoutError("Session did not become active")

    res = requests.get(
        "https://httpbin.org/ip",
        proxies={"http": proxy_url, "https": proxy_url},
        timeout=30,
    )
    client.report_event(
        session_id,
        event_type="success" if res.ok else "http_error",
        status_code=res.status_code,
        target_host="httpbin.org",
    )
    print(client.get_session_health(session_id))
finally:
    if session_id:
        client.terminate_session(session_id)
```

## Dynamic Session

Use a dynamic session when your automation can rotate after errors such as timeout, 403, 429, or explicit blocks.

```python
session = client.create_session(
    session_type="dynamic",
    product_no="selected_from_products_api",
    quantity=1,
    protocol="socks5",
    rotation_mode="on_demand",
)
```

## Static Session

Use a static session when you need fixed network identity for a longer-lived task.

```python
session = client.create_session(
    session_type="static",
    product_no="selected_from_products_api",
    quantity=1,
    duration=30,
    protocol="socks5",
)
```

## Telemetry

```python
client.report_event(
    session_id,
    event_type="timeout",
    status_code=0,
    target_host="example.com",
)
```

## Health

```python
health = client.get_session_health(session_id)
```

`timeout`, `captcha`, `block`, and repeated HTTP errors are not neutral noise; report them so NexaLayer can score the session and recommend rotate or pause.

## Cleanup

Always terminate sessions you no longer need:

```python
try:
    ...
finally:
    if session_id:
        client.terminate_session(session_id)
```

## Playwright

Use the public Playwright examples:

- Chinese: https://github.com/NexaLayer/nexalayer-examples/tree/main/playwright/basic-session
- English: https://github.com/NexaLayer/nexalayer-examples/tree/main/playwright/basic-session

## 中文文档

- 中文快速开始: https://docs.nexalayer.net/zh/quick-start
- Playwright 中文 Demo: https://docs.nexalayer.net/zh/examples
- API 文档: https://docs.nexalayer.net/api-reference/openapi

## Error handling

- Check `backend_ready=true` before creating paid sessions after registration.
- Use `Idempotency-Key` for create, rotate, renew, and recharge operations.
- Do not log `proxy.full_url` in production without redaction because it can contain proxy credentials.
- Respect target website terms and applicable law.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Do not open public issues with API keys, cookies, account passwords, proxy credentials, or target-site secrets. See [SECURITY.md](SECURITY.md).
