# NexaLayer SDK

Official SDK for NexaLayer – The Network Execution Layer for AI Agents.

---

## What is NexaLayer?

NexaLayer abstracts proxy networking into session-based execution  
so AI agents can operate globally without IP chaos.

Instead of managing IP pools, you manage sessions.

---

## Why NexaLayer?

- Session abstraction over raw IP
- Dynamic & static proxy unification
- Agent-first API design
- Built for AI-native workloads
- Infrastructure, not commodity proxies

---

## Installation

### Python (coming soon)

```bash
pip install nexalayer
```

### Node.js (coming soon)

```bash
npm install nexalayer
```

---

## Quickstart (Python)

```python
import nexalayer

client = nexalayer.Client(api_key="YOUR_API_KEY")

session = client.create_session(
    type="dynamic",
    country="US",
    rotation="timed"
)

response = session.get("https://example.com")
print(response.status_code)
```

---

## Quickstart (Node.js)

```javascript
import NexaLayer from "nexalayer"

const client = new NexaLayer({ apiKey: "YOUR_API_KEY" })

const session = await client.createSession({
  type: "dynamic",
  country: "US",
  rotation: "timed"
})

const response = await session.get("https://example.com")
console.log(response.status)
```

---

## Documentation

Full API reference:
https://nexalayer.com/docs

---

## Roadmap

- [ ] Python SDK v0.1
- [ ] Node SDK v0.1
- [ ] Session auto-rotation helper
- [ ] Async support
- [ ] Retry & failover logic
- [ ] OpenTelemetry support

---

## Vision

AI agents need infrastructure.

NexaLayer provides the network execution layer.
