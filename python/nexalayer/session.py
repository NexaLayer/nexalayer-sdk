"""Session abstraction for NexaLayer managed sessions."""

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
        # Transport helpers are intentionally minimal. Production integrations
        # should use proxy.full_url or host/port credentials from GET /sessions.
        # self._session.proxies = {"http": ..., "https": ...}

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Perform GET with the local requests session."""
        # TODO: use proxy_config to route via proxy when available
        return self._session.get(url, timeout=kwargs.get("timeout", 30))

    def post(self, url: str, data: Any = None, json: Any = None, **kwargs: Any) -> requests.Response:
        """Perform POST with the local requests session."""
        # TODO: use proxy_config to route via proxy when available
        return self._session.post(url, data=data, json=json, timeout=kwargs.get("timeout", 30))

    def rotate(self) -> dict:
        """POST /sessions/{session_id}/rotate — rotate proxy for this session."""
        return self.client.rotate_session(self.session_id)

    def usage(self) -> dict:
        """GET /sessions/{session_id}/usage."""
        return self.client.get_session_usage(self.session_id)
