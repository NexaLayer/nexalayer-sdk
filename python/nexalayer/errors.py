"""NexaLayer SDK error classes."""

from typing import Optional


class NexaLayerError(Exception):
    """Base exception for NexaLayer SDK."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body


class AuthError(NexaLayerError):
    """Authentication or authorization failed."""


class APIError(NexaLayerError):
    """API returned an error (4xx/5xx)."""


class SessionError(NexaLayerError):
    """Session operation failed (create, rotate, get, etc.)."""
