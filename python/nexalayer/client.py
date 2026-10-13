"""NexaLayer API client — auth, account, billing, products, sessions, stats."""

from typing import Any, Optional, Union
from urllib.parse import urlencode

import requests

from nexalayer.errors import APIError, AuthError
from nexalayer.session import Session
from nexalayer.types import SessionConfig, SessionCreateResponse, TokenResponse

DEFAULT_BASE_URL = "https://api.nexalayer.net/v1"


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
        headers: Optional[dict] = None,
        **kwargs: Any,
    ) -> dict:
        url = f"{self.base_url}{path}"
        request_headers = self._headers()
        if headers:
            request_headers.update(headers)
        resp = self._session.request(
            method,
            url,
            json=json,
            headers=request_headers,
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

    def register(
        self,
        name: str,
        contact_email: str,
        referral_code: Optional[str] = None,
        **kwargs: Any,
    ) -> dict:
        """POST /account/register."""
        # TODO: implement real call
        payload: dict = {"name": name, "contact_email": contact_email, **kwargs}
        if referral_code is not None:
            payload["referral_code"] = referral_code
        return self._request("POST", "/account/register", json=payload)

    def request_api_key(self, email: str, referral_code: Optional[str] = None) -> dict:
        """POST /account/request-api-key; first-time emails receive trial credit."""
        payload = {"email": email}
        if referral_code:
            payload["referral_code"] = referral_code
        return self._request("POST", "/account/request-api-key", json=payload)

    def get_balance(self) -> dict:
        """GET /billing/balance."""
        # TODO: implement real call
        return self._request("GET", "/billing/balance")

    def recharge(
        self,
        amount: float,
        currency: str = "USD",
        idempotency_key: Optional[str] = None,
        **kwargs: Any,
    ) -> dict:
        """POST /billing/recharge."""
        # TODO: implement real call
        payload = {"amount": amount, "currency": currency, **kwargs}
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._request("POST", "/billing/recharge", json=payload, headers=headers)

    def get_budget(self) -> dict:
        """GET /account/budget."""
        return self._request("GET", "/account/budget")

    def set_budget(
        self,
        *,
        idempotency_key: str,
        key_limit_usd: Optional[float] = None,
        daily_limit_usd: Optional[float] = None,
        pause_on_exceed: bool = True,
        alert_thresholds: Optional[list] = None,
        paused: Optional[bool] = None,
    ) -> dict:
        """PUT /account/budget."""
        if not idempotency_key:
            raise ValueError("idempotency_key is required")
        payload = {
            "key_limit_usd": key_limit_usd,
            "daily_limit_usd": daily_limit_usd,
            "pause_on_exceed": pause_on_exceed,
            "alert_thresholds": alert_thresholds or [50, 80, 100],
        }
        if paused is not None:
            payload["paused"] = paused
        return self._request(
            "PUT",
            "/account/budget",
            json=payload,
            headers={"Idempotency-Key": idempotency_key},
        )

    def get_usage_alerts(self) -> dict:
        """GET /account/usage-alerts."""
        return self._request("GET", "/account/usage-alerts")

    def get_products(self, type: str = "all", country_code: Optional[str] = None) -> dict:
        """GET /products."""
        query = {"type": type}
        if country_code:
            query["country_code"] = country_code
        return self._request("GET", f"/products?{urlencode(query)}")

    def recommend_products(self, criteria: dict) -> dict:
        """POST /products/recommend."""
        # TODO: implement real call
        return self._request("POST", "/products/recommend", json=criteria)

    def create_session(
        self,
        type: Optional[str] = None,
        session_type: Optional[str] = None,
        product_no: Optional[str] = None,
        config: Optional[Union[dict, SessionConfig]] = None,
        idempotency_key: Optional[str] = None,
        **kwargs: Any,
    ) -> Session:
        """POST /sessions — create a session and return a Session object."""
        cfg = config.to_dict() if isinstance(config, SessionConfig) else (config or {})
        resolved_type = session_type or type or cfg.pop("session_type", "dynamic")
        resolved_product = product_no or cfg.pop("product_no", None)
        if not resolved_product:
            raise APIError("product_no is required")
        payload = {
            "session_type": resolved_type,
            "product_no": resolved_product,
            **cfg,
            **kwargs,
        }
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        data = self._request("POST", "/sessions", json=payload, headers=headers)
        inner = data.get("data", data)
        session_id = inner.get("session_id")
        if not session_id:
            raise APIError(f"Session create response missing session_id: {data}")
        status = inner.get("status") or "creating"
        proxy_config = inner.get("proxy") or inner.get("proxy_config") or {}
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

    def rotate_session(self, session_id: str, idempotency_key: Optional[str] = None) -> dict:
        """POST /sessions/{session_id}/rotate."""
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._request("POST", f"/sessions/{session_id}/rotate", headers=headers)

    def terminate_session(self, session_id: str) -> dict:
        """DELETE /sessions/{session_id}."""
        return self._request("DELETE", f"/sessions/{session_id}")

    def report_event(self, session_id: str, **event: Any) -> dict:
        """POST /sessions/{session_id}/report-event."""
        return self._request("POST", f"/sessions/{session_id}/report-event", json=event)

    def get_session_health(self, session_id: str) -> dict:
        """GET /sessions/{session_id}/health."""
        return self._request("GET", f"/sessions/{session_id}/health")

    def get_session_usage(self, session_id: str) -> dict:
        """GET /sessions/{session_id}/usage."""
        # TODO: implement real call
        return self._request("GET", f"/sessions/{session_id}/usage")

    def get_stats_overview(self) -> dict:
        """GET /stats/overview."""
        # TODO: implement real call
        return self._request("GET", "/stats/overview")
