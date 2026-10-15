# NexaLayer Node SDK

Install from npm:

```bash
npm install @nexalayer/sdk
```

The public package is `@nexalayer/sdk`.

## Usage

```typescript
import { NexaLayerClient } from "@nexalayer/sdk";

const client = new NexaLayerClient({
  apiKey: process.env.NEXALAYER_API_KEY,
});

const products = await client.getProducts({ type: "dynamic" });
```

Create sessions with a `product_no` returned by `/products`; do not hardcode old product IDs.

## Tests

```bash
npm test
```
