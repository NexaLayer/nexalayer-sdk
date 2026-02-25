/** Session abstraction — perform requests through proxy config (placeholder). */

import type { NexaLayerClient } from './client';

export class Session {
  constructor(
    private client: NexaLayerClient,
    public readonly sessionId: string,
    public readonly proxyConfig: Record<string, unknown> = {}
  ) {}

  async get(url: string, options?: RequestInit): Promise<Response> {
    // TODO: use proxyConfig to route via proxy when available
    return fetch(url, { ...options, method: 'GET' });
  }

  async post(
    url: string,
    body?: string | object,
    options?: RequestInit
  ): Promise<Response> {
    const opts: RequestInit = { ...options, method: 'POST' };
    if (body !== undefined) {
      opts.body =
        typeof body === 'string' ? body : JSON.stringify(body);
      if (typeof body === 'object' && !opts.headers) {
        (opts as Record<string, unknown>).headers = {
          'Content-Type': 'application/json',
        };
      }
    }
    return fetch(url, opts);
  }

  async rotate(): Promise<unknown> {
    return this.client.rotateSession(this.sessionId);
  }

  async usage(): Promise<unknown> {
    return this.client.getSessionUsage(this.sessionId);
  }
}
