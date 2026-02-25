"""Lightweight request/response types for NexaLayer API."""

from typing import Any, Optional


class SessionConfig:
    """Configuration for creating a session (dynamic or static)."""

    def __init__(
        self,
        product_no: Optional[str] = None,
        traffic_gb: Optional[float] = None,
        protocol: Optional[str] = None,
        country: Optional[str] = None,
        **kwargs: Any,
    ):
        self.product_no = product_no
        self.traffic_gb = traffic_gb
        self.protocol = protocol
        self.country = country
        self.extra = kwargs

    def to_dict(self) -> dict:
        out = {}
        if self.product_no is not None:
            out["product_no"] = self.product_no
        if self.traffic_gb is not None:
            out["traffic_gb"] = self.traffic_gb
        if self.protocol is not None:
            out["protocol"] = self.protocol
        if self.country is not None:
            out["country"] = self.country
        out.update(self.extra)
        return out


class TokenResponse:
    """Response from POST /auth/token."""

    def __init__(self, access_token: str, token_type: str = "Bearer", **kwargs: Any):
        self.access_token = access_token
        self.token_type = token_type
        self.extra = kwargs


class SessionCreateResponse:
    """Response from POST /sessions."""

    def __init__(
        self,
        session_id: str,
        status: str,
        proxy_config: Optional[dict] = None,
        **kwargs: Any,
    ):
        self.session_id = session_id
        self.status = status
        self.proxy_config = proxy_config or {}
        self.extra = kwargs
