# NexaLayer SDK

**The Network Execution Layer for AI Agents.**

Official Python and Node.js SDKs for [NexaLayer](https://nexalayer.com)—session-based proxy abstraction for dynamic and static proxies, built for agent-first workflows.

## Features

- **Session abstraction**: Create, rotate, and manage proxy sessions via a unified API.
- **Dual auth**: API Key/Secret token exchange or direct Bearer token.
- **Typed clients**: Lightweight request/response models and structured errors.
- **Python & Node**: Same concepts across both runtimes.

## Quick start

### Python

```bash
pip install nexalayer
```

```python
from nexalayer import NexaLayerClient

client = NexaLayerClient(api_key="your-api-key")
session = client.create_session(type="dynamic", config={"product_no": "out_dynamic_1"})
# Use session for outbound requests through proxy
response = session.get("https://httpbin.org/ip")
```

### Node

```bash
npm install nexalayer
```

```typescript
import { NexaLayerClient } from 'nexalayer';

const client = new NexaLayerClient({ apiKey: 'your-api-key' });
const session = await client.createSession({ type: 'dynamic', config: { product_no: 'out_dynamic_1' } });
const response = await session.get('https://httpbin.org/ip');
```

## Documentation

- [Full documentation](https://docs.nexalayer.com)
- [API reference](https://docs.nexalayer.com/api-reference/openapi)
- [Quickstart](https://docs.nexalayer.com/quickstart)

## Repository layout

- `python/` — Python package and tests
- `node/` — Node/TypeScript package
- `examples/python/` — Python quickstart and rotate examples
- `examples/node/` — Node quickstart and rotate examples

## License

MIT. See [LICENSE](LICENSE).
