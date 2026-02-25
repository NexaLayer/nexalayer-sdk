/** NexaLayer SDK error classes. */

export class NexaLayerError extends Error {
  statusCode?: number;
  body?: string;

  constructor(
    message: string,
    statusCode?: number,
    body?: string
  ) {
    super(message);
    this.name = 'NexaLayerError';
    this.statusCode = statusCode;
    this.body = body;
  }
}

export class AuthError extends NexaLayerError {
  constructor(message: string) {
    super(message);
    this.name = 'AuthError';
  }
}

export class APIError extends NexaLayerError {
  constructor(message: string, statusCode?: number, body?: string) {
    super(message, statusCode, body);
    this.name = 'APIError';
  }
}

export class SessionError extends NexaLayerError {
  constructor(message: string) {
    super(message);
    this.name = 'SessionError';
  }
}
