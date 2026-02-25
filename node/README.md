# NexaLayer Node SDK

Install from repository root (or publish from this package):

```bash
cd node && npm install && npm run build
```

## Usage

```typescript
import { NexaLayerClient } from 'nexalayer';

const client = new NexaLayerClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.nexalayer.com/v1',
});
const session = await client.createSession({
  type: 'dynamic',
  config: { product_no: 'out_dynamic_1' },
});
const response = await session.get('https://httpbin.org/ip');
```

## Tests

```bash
npm test
```
