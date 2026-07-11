# NexaLayer Node SDK

Build from source:

```bash
cd node
npm install
npm run build
```

The package is not documented as published to npm yet. Use the source package until an official release is available.

## Usage

```typescript
import { NexaLayerClient } from "./src";

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
