/** Lightweight request/response types for NexaLayer API. */

export interface SessionConfigInput {
  product_no?: string;
  traffic_gb?: number;
  protocol?: string;
  country?: string;
  [k: string]: unknown;
}

export interface TokenResponse {
  access_token: string;
  token_type?: string;
}

export interface SessionCreateResponse {
  session_id: string;
  status: string;
  proxy_config?: Record<string, unknown>;
}

export interface CreateSessionOptions {
  type: 'dynamic' | 'static';
  config?: SessionConfigInput;
}
