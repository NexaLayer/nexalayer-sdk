"""Basic tests for NexaLayerClient (stub/mock behavior)."""

import pytest

from nexalayer import NexaLayerClient
from nexalayer.errors import AuthError


def test_client_init_with_api_key():
    client = NexaLayerClient(api_key="test-key", base_url="https://api.example.com/v1")
    assert client.base_url == "https://api.example.com/v1"
    assert client._api_key == "test-key"


def test_client_init_with_bearer():
    client = NexaLayerClient(bearer_token="token", base_url="https://api.example.com/v1")
    assert client._session.headers.get("Authorization", "").startswith("Bearer ")


def test_get_token_requires_secret():
    client = NexaLayerClient(api_key="key", base_url="https://api.example.com/v1")
    with pytest.raises(AuthError):
        client.get_token(api_key="key")
    with pytest.raises(AuthError):
        client.get_token(api_key="key", api_secret=None)


def test_get_products_sends_current_filters(monkeypatch):
    client = NexaLayerClient(api_key="key", base_url="https://api.example.com/v1")
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update(method=method, path=path, kwargs=kwargs)
        return {"items": []}

    monkeypatch.setattr(client, "_request", fake_request)
    client.get_products(type="dynamic", country="US", in_stock=False, limit=10, cursor="MTA")
    assert captured["method"] == "GET"
    assert captured["path"] == "/products?type=dynamic&in_stock=false&limit=10&country=US&cursor=MTA"
