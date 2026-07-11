/**
 * NexaLayer Node rotate example.
 *
 * Creates a dynamic session, rotates it, reads usage, and terminates it.
 * This can create a real paid session.
 */

import { NexaLayerClient } from '../../node/src';

function unwrap(value: unknown): Record<string, unknown> {
  const obj = value as Record<string, unknown>;
  return (obj.data as Record<string, unknown>) ?? obj;
}

async function pickDynamicProduct(client: NexaLayerClient): Promise<string> {
  if (process.env.NEXALAYER_PRODUCT_NO) return process.env.NEXALAYER_PRODUCT_NO;
  const products = unwrap(await client.getProducts({ type: 'dynamic' }));
  const items = (products.items as Array<Record<string, unknown>>) ?? [];
  const product = items.find((item) => item.product_no);
  if (!product?.product_no) throw new Error('No dynamic product available');
  return String(product.product_no);
}

async function main() {
  const apiKey = process.env.NEXALAYER_API_KEY;
  if (!apiKey) throw new Error('Set NEXALAYER_API_KEY');

  const client = new NexaLayerClient({ apiKey });
  let sessionId: string | undefined;

  try {
    const session = await client.createSession({
      session_type: 'dynamic',
      product_no: await pickDynamicProduct(client),
      quantity: 1,
      protocol: 'socks5',
      rotation_mode: 'on_demand',
      idempotencyKey: `sdk-rotate-${Date.now()}`,
    });
    sessionId = session.sessionId;
    console.log('Session:', sessionId);
    console.log('Rotate result:', await session.rotate());
    console.log('Usage:', await session.usage());
  } finally {
    if (sessionId) {
      await client.terminateSession(sessionId);
      console.log('Terminated:', sessionId);
    }
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
