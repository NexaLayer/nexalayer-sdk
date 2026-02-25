"""NexaLayer API client — auth, account, billing, products, sessions, stats."""

from typing import Any, Optional, Union

import requests

from nexalayer.errors import APIError, AuthError
from nexalayer.session import Session
from nexalayer.types import SessionConfig, SessionCreateResponse, TokenResponse

DEFAULT_BASE_URL = "https://api.nexalayer.com/v1"


class NexaLayerClient:
    """HTTP client for NexaLayer API with auth header injection."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        bearer_token: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._bearer_token = bearer_token
        self._api_secret = api_secret
        self._session = requests.Session()
        if bearer_token:
            self._session.headers["Authorization"] = f"Bearer {bearer_token}"
        elif api_key:
            self._session.headers["X-API-Key"] = api_key

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._bearer_token:
            h["Authorization"] = f"Bearer {self._bearer_token}"
        elif self._api_key:
            h["X-API-Key"] = self._api_key
        return h

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[dict] = None,
        **kwargs: Any,
    ) -> dict:
        url = f"{self.base_url}{path}"
        resp = self._session.request(
            method,
            url,
            json=json,
            headers=self._headers(),
            timeout=kwargs.get("timeout", 30),
        )
        if resp.status_code >= 400:
            raise APIError(
                f"API error: {resp.status_code}",
                status_code=resp.status_code,
                body=resp.text,
            )
        return resp.json() if resp.content else {}

    def get_token(self, api_key: Optional[str] = None, api_secret: Optional[str] = None) -> TokenResponse:
        """POST /auth/token — obtain Bearer token from API Key/Secret."""
        # TODO: call real POST /auth/token when backend is available
        key = api_key or self._api_key
        secret = api_secret or self._api_secret
        if not key or not secret:
            raise AuthError("api_key and api_secret required for get_token")
        payload = {"api_key": key, "api_secret": secret}
        data = self._request("POST", "/auth/token", json=payload)
        # Placeholder; replace with real response parsing
        token = data.get("data", {}).get("access_token") or "mock-token"
        return TokenResponse(access_token=token)

    def register(self, name: str, contact_email: str, **kwargs: Any) -> dict:
        """POST /account/register."""
        # TODO: implement real call
        payload = {"name": name, "contact_email": contact_email, **kwargs}
        return self._request("POST", "/account/register", json=payload)

    def get_balance(self) -> dict:
        """GET /billing/balance."""
        # TODO: implement real call
        return self._request("GET", "/billing/balance")

    def recharge(self, amount: float, currency: str = "USD", **kwargs: Any) -> dict:
        """POST /billing/recharge."""
        # TODO: implement real call
        payload = {"amount": amount, "currency": currency, **kwargs}
        return self._request("POST", "/billing/recharge", json=payload)

    def get_products(self) -> dict:
        """GET /products."""
        # TODO: implement real call
        return self._request("GET", "/products")

    def recommend_products(self, criteria: dict) -> dict:
        """POST /products/recommend."""
        # TODO: implement real call
        return self._request("POST", "/products/recommend", json=criteria)

    def create_session(
        self,
        type: str = "dynamic",
        config: Optional[Union[dict, SessionConfig]] = None,
        **kwargs: Any,
    ) -> Session:
        """POST /sessions — create a session and return a Session object."""
        cfg = config.to_dict() if isinstance(config, SessionConfig) else (config or {})
        payload = {"type": type, "config": cfg, **kwargs}
        data = self._request("POST", "/sessions", json=payload)
        # Placeholder: real API returns session_id, status, proxy_config
        inner = data.get("data", data)
        session_id = inner.get("session_id") or "mock-session-id"
        status = inner.get("status") or "active"
        proxy_config = inner.get("proxy_config") or {}
        resp = SessionCreateResponse(
            session_id=session_id,
            status=status,
            proxy_config=proxy_config,
        )
        return Session(
            client=self,
            session_id=resp.session_id,
            proxy_config=resp.proxy_config,
        )

    def get_session(self, session_id: str) -> dict:
        """GET /sessions/{session_id}."""
        # TODO: implement real call
        return self._request("GET", f"/sessions/{session_id}")

    def rotate_session(self, session_id: str) -> dict:
        """POST /sessions/{session_id}/rotate."""
        # TODO: implement real call
        return self._request("POST", f"/sessions/{session_id}/rotate")

    def get_session_usage(self, session_id: str) -> dict:
        """GET /sessions/{session_id}/usage."""
        # TODO: implement real call
        return self._request("GET", f"/sessions/{session_id}/usage")

    def get_stats_overview(self) -> dict:
        """GET /stats/overview."""
        # TODO: implement real call
        return self._request("GET", "/stats/overview")
