/**
 * NexaLayer Node rotate example — create session and rotate (stub).
 * Run: npx ts-node rotate.ts from examples/node with parent SDK built.
 */

import { NexaLayerClient } from '../../node/src';

async function main() {
  const apiKey = process.env.NEXALAYER_API_KEY ?? 'your-api-key';
  const baseUrl =
    process.env.NEXALAYER_BASE_URL ?? 'https://api.nexalayer.com/v1';

  const client = new NexaLayerClient({ apiKey, baseUrl });
  const session = await client.createSession({
    type: 'dynamic',
    config: { product_no: 'out_dynamic_1' },
  });
  console.log('Session:', session.sessionId);

  const result = await session.rotate();
  console.log('Rotate result:', result);

  const usage = await session.usage();
  console.log('Usage:', usage);
}

main().catch(console.error);
