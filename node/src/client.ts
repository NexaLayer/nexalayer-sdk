/** NexaLayer API client — auth, account, billing, products, sessions, stats. */

import { Session } from './session';
import { APIError, AuthError } from './errors';
import type {
  SessionConfigInput,
  TokenResponse,
  CreateSessionOptions,
} from './types';

const DEFAULT_BASE_URL = 'https://api.nexalayer.net/v1';

export interface NexaLayerClientOptions {
  apiKey?: string;
  bearerToken?: string;
  apiSecret?: string;
  baseUrl?: string;
}

export class NexaLayerClient {
  private baseUrl: string;
  private apiKey?: string;
  private bearerToken?: string;
  private apiSecret?: string;

  constructor(options: NexaLayerClientOptions = {}) {
    this.baseUrl = (options.baseUrl ?? DEFAULT_BASE_URL).replace(/\/$/, '');
    this.apiKey = options.apiKey;
    this.bearerToken = options.bearerToken;
    this.apiSecret = options.apiSecret;
  }

  private headers(): Record<string, string> {
    const h: Record<string, string> = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };
    if (this.bearerToken) {
      h['Authorization'] = `Bearer ${this.bearerToken}`;
    } else if (this.apiKey) {
      h['X-API-Key'] = this.apiKey;
    }
    return h;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: object
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const res = await fetch(url, {
      method,
      headers: this.headers(),
      body: body ? JSON.stringify(body) : undefined,
    });
    if (res.status >= 400) {
      throw new APIError(
        `API error: ${res.status}`,
        res.status,
        await res.text()
      );
    }
    const text = await res.text();
    return (text ? JSON.parse(text) : {}) as T;
  }

  async getToken(apiKey?: string, apiSecret?: string): Promise<TokenResponse> {
    const key = apiKey ?? this.apiKey;
    const secret = apiSecret ?? this.apiSecret;
    if (!key || !secret) {
      throw new AuthError('api_key and api_secret required for getToken');
    }
    // TODO: real POST /auth/token
    const data = await this.request<{ data?: { access_token?: string } }>(
      'POST',
      '/auth/token',
      { api_key: key, api_secret: secret }
    );
    const token = data?.data?.access_token ?? 'mock-token';
    return { access_token: token, token_type: 'Bearer' };
  }

  async register(params: {
    name: string;
    contact_email: string;
    referral_code?: string;
    [k: string]: unknown;
  }): Promise<unknown> {
    // TODO: implement real POST /account/register
    const { referral_code, ...rest } = params;
    const body: Record<string, unknown> = { ...rest };
    if (referral_code != null) {
      body.referral_code = referral_code;
    }
    return this.request('POST', '/account/register', body);
  }

  async getBalance(): Promise<unknown> {
    // TODO: GET /billing/balance
    return this.request('GET', '/billing/balance');
  }

  async recharge(params: {
    amount: number;
    currency?: string;
    [k: string]: unknown;
  }): Promise<unknown> {
    // TODO: POST /billing/recharge
    const { amount, currency, ...rest } = params;
    return this.request('POST', '/billing/recharge', {
      amount,
      currency: currency ?? 'USD',
      ...rest,
    });
  }

  async getProducts(): Promise<unknown> {
    // TODO: GET /products
    return this.request('GET', '/products');
  }

  async recommendProducts(criteria: object): Promise<unknown> {
    // TODO: POST /products/recommend
    return this.request('POST', '/products/recommend', criteria);
  }

  async createSession(options: CreateSessionOptions): Promise<Session> {
    const { type = 'dynamic', config = {} } = options;
    // TODO: real POST /sessions
    const data = await this.request<{
      data?: {
        session_id?: string;
        status?: string;
        proxy_config?: Record<string, unknown>;
      };
    }>('POST', '/sessions', { type, config });
    const inner = data?.data ?? (data as Record<string, unknown>);
    const sessionId =
      (inner.session_id as string) ?? 'mock-session-id';
    const status = (inner.status as string) ?? 'active';
    const proxyConfig =
      (inner.proxy_config as Record<string, unknown>) ?? {};
    return new Session(this, sessionId, proxyConfig);
  }

  async getSession(sessionId: string): Promise<unknown> {
    // TODO: GET /sessions/{session_id}
    return this.request('GET', `/sessions/${sessionId}`);
  }

  async rotateSession(sessionId: string): Promise<unknown> {
    // TODO: POST /sessions/{session_id}/rotate
    return this.request('POST', `/sessions/${sessionId}/rotate`);
  }

  async getSessionUsage(sessionId: string): Promise<unknown> {
    // TODO: GET /sessions/{session_id}/usage
    return this.request('GET', `/sessions/${sessionId}/usage`);
  }

  async getStatsOverview(): Promise<unknown> {
    // TODO: GET /stats/overview
    return this.request('GET', '/stats/overview');
  }
}
