/**
 * NexaLayer Node quickstart — create client and session (stub).
 * Run: npx ts-node quickstart.ts (or tsx) from examples/node with parent SDK built.
 */

import { NexaLayerClient } from '../../node/src';

async function main() {
  const apiKey = process.env.NEXALAYER_API_KEY ?? 'your-api-key';
  const baseUrl =
    process.env.NEXALAYER_BASE_URL ?? 'https://api.nexalayer.net/v1';

  const client = new NexaLayerClient({ apiKey, baseUrl });
  const session = await client.createSession({
    type: 'dynamic',
    config: { product_no: 'out_dynamic_1', traffic_gb: 1 },
  });
  console.log('Session created:', session.sessionId);

  const resp = await session.get('https://httpbin.org/ip');
  console.log('IP check status:', resp.status);
}

main().catch(console.error);
