/**
 * NexaLayer Node quickstart.
 *
 * Creates a dynamic session, reports telemetry, reads health, and always
 * terminates the session in cleanup. This can create a real paid session.
 */

import { NexaLayerClient } from '../../node/src';

function unwrap(value: unknown): Record<string, unknown> {
  const obj = value as Record<string, unknown>;
  return (obj.data as Record<string, unknown>) ?? obj;
}

async function pickDynamicProduct(client: NexaLayerClient): Promise<string> {
  if (process.env.NEXALAYER_PRODUCT_NO) {
    return process.env.NEXALAYER_PRODUCT_NO;
  }
  const products = unwrap(await client.getProducts({ type: 'dynamic' }));
  const items = (products.items as Array<Record<string, unknown>>) ?? [];
  const product = items.find((item) => item.product_no);
  if (!product?.product_no) {
    throw new Error('No dynamic product available');
  }
  return String(product.product_no);
}

async function waitForActive(
  client: NexaLayerClient,
  sessionId: string
): Promise<Record<string, unknown>> {
  for (let i = 0; i < 60; i += 1) {
    const session = unwrap(await client.getSession(sessionId));
    if (session.status === 'active') return session;
    if (session.status === 'failed' || session.status === 'error') {
      throw new Error(`Session failed: ${JSON.stringify(session)}`);
    }
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
  throw new Error('Session did not become active within 120s');
}

async function main() {
  const apiKey = process.env.NEXALAYER_API_KEY;
  if (!apiKey) throw new Error('Set NEXALAYER_API_KEY');

  const client = new NexaLayerClient({
    apiKey,
    baseUrl: process.env.NEXALAYER_BASE_URL ?? 'https://api.nexalayer.net/v1',
  });
  let sessionId: string | undefined;

  try {
    const productNo = await pickDynamicProduct(client);
    const session = await client.createSession({
      session_type: 'dynamic',
      product_no: productNo,
      quantity: 1,
      protocol: 'socks5',
      rotation_mode: 'on_demand',
      idempotencyKey: `sdk-node-${Date.now()}`,
    });
    sessionId = session.sessionId;
    console.log('session_id:', sessionId);

    const active = await waitForActive(client, sessionId);
    const proxy = active.proxy as Record<string, unknown> | undefined;
    if (!proxy?.full_url) {
      throw new Error('Active session did not include proxy.full_url');
    }

    await client.reportEvent(sessionId, {
      event_type: 'success',
      status_code: 200,
      target_host: 'httpbin.org',
    });
    console.log('health:', await client.getSessionHealth(sessionId));
  } finally {
    if (sessionId) {
      await client.terminateSession(sessionId);
      console.log('terminated:', sessionId);
    }
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
