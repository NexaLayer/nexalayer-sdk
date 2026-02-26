# NexaLayer Node SDK

Install from repository root (or publish from this package):

```bash
cd node && npm install && npm run build
```

## Usage

Default base URL: `https://api.nexalayer.net/v1`.

**Register (optional referral_code)**:

```typescript
import { NexaLayerClient } from 'nexalayer';

const client = new NexaLayerClient({ baseUrl: 'https://api.nexalayer.net/v1' });
const reg = await client.register({
  name: 'My Agent',
  contact_email: 'dev@example.com',
  referral_code: '0345', // optional
});
const apiKey = reg?.data?.api_key;
```

**Create session and use proxy**:

```typescript
const sessionClient = new NexaLayerClient({
  apiKey,
  baseUrl: 'https://api.nexalayer.net/v1',
});
const session = await sessionClient.createSession({
  type: 'dynamic',
  config: { product_no: 'out_dynamic_1' },
});
const response = await session.get('https://httpbin.org/ip');
```

## Tests

```bash
npm test
```
