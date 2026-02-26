# NexaLayer SDK

**The Network Execution Layer for AI Agents.**

Official Python and Node.js SDKs for [NexaLayer](https://nexalayer.com)—session-based proxy abstraction for dynamic and static proxies, built for agent-first workflows.

## Features

- **Session abstraction**: Create, rotate, and manage proxy sessions via a unified API.
- **Dual auth**: API Key/Secret token exchange or direct Bearer token.
- **Typed clients**: Lightweight request/response models and structured errors.
- **Python & Node**: Same concepts across both runtimes.

## Quick start

Base URL: `https://api.nexalayer.net/v1`

### Register (get API key)

Register once to get `api_key` and `api_secret`. Optional `referral_code` assigns the account to a referral agent.

```bash
curl -X POST https://api.nexalayer.net/v1/account/register \
  -H "Content-Type: application/json" \
  -d '{"name":"My Agent","contact_email":"dev@example.com","referral_code":"0345"}'
```

### Python

```bash
pip install nexalayer
```

```python
from nexalayer import NexaLayerClient

# Register (optional referral_code)
client = NexaLayerClient(base_url="https://api.nexalayer.net/v1")
reg = client.register("My Agent", "dev@example.com", referral_code="0345")
api_key = reg["data"]["api_key"]

# Use API key for sessions
client = NexaLayerClient(api_key=api_key, base_url="https://api.nexalayer.net/v1")
session = client.create_session(type="dynamic", config={"product_no": "out_dynamic_1"})
response = session.get("https://httpbin.org/ip")
```

### Node

```bash
npm install nexalayer
```

```typescript
import { NexaLayerClient } from 'nexalayer';

// Register (optional referral_code)
const baseUrl = 'https://api.nexalayer.net/v1';
const client = new NexaLayerClient({ baseUrl });
const reg = await client.register({
  name: 'My Agent',
  contact_email: 'dev@example.com',
  referral_code: '0345',
});
const apiKey = reg?.data?.api_key;

const sessionClient = new NexaLayerClient({ apiKey, baseUrl });
const session = await sessionClient.createSession({
  type: 'dynamic',
  config: { product_no: 'out_dynamic_1' },
});
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
