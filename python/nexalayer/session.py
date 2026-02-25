"""Session abstraction — perform requests through proxy config (placeholder)."""

from typing import TYPE_CHECKING, Any, Optional

import requests

from nexalayer.errors import SessionError

if TYPE_CHECKING:
    from nexalayer.client import NexaLayerClient


class Session:
    """Represents a NexaLayer proxy session; use get/post to send traffic via proxy."""

    def __init__(
        self,
        client: "NexaLayerClient",
        session_id: str,
        proxy_config: Optional[dict] = None,
    ):
        self.client = client
        self.session_id = session_id
        self.proxy_config = proxy_config or {}
        self._session = requests.Session()
        # TODO: apply real proxy from proxy_config (e.g. http://user:pass@host:port)
        # For now we do not set proxies so requests go direct (stub behavior)
        # self._session.proxies = {"http": ..., "https": ...}

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Perform GET through session proxy (placeholder: direct request)."""
        # TODO: use proxy_config to route via proxy when available
        return self._session.get(url, timeout=kwargs.get("timeout", 30))

    def post(self, url: str, data: Any = None, json: Any = None, **kwargs: Any) -> requests.Response:
        """Perform POST through session proxy (placeholder: direct request)."""
        # TODO: use proxy_config to route via proxy when available
        return self._session.post(url, data=data, json=json, timeout=kwargs.get("timeout", 30))

    def rotate(self) -> dict:
        """POST /sessions/{session_id}/rotate — rotate proxy for this session."""
        return self.client.rotate_session(self.session_id)

    def usage(self) -> dict:
        """GET /sessions/{session_id}/usage."""
        return self.client.get_session_usage(self.session_id)
