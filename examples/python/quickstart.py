"""NexaLayer Python quickstart.

Creates a dynamic session, reports telemetry, reads health, and always
terminates the session in cleanup. This can create a real paid session.
"""

import os
import time
import uuid

import requests
from nexalayer import NexaLayerClient


def unwrap(response):
    return response.get("data", response)


def pick_dynamic_product(client: NexaLayerClient) -> str:
    override = os.getenv("NEXALAYER_PRODUCT_NO")
    if override:
        return override
    products = unwrap(client.get_products(type="dynamic"))
    for item in products.get("items", []):
        if item.get("product_no"):
            return item["product_no"]
    raise RuntimeError("No dynamic product available")


def wait_for_active(client: NexaLayerClient, session_id: str) -> dict:
    for _ in range(60):
        session = unwrap(client.get_session(session_id))
        if session.get("status") == "active":
            return session
        if session.get("status") in {"failed", "error"}:
            raise RuntimeError(f"Session failed: {session}")
        time.sleep(2)
    raise TimeoutError("Session did not become active within 120s")


def main():
    api_key = os.getenv("NEXALAYER_API_KEY")
    if not api_key:
        raise RuntimeError("Set NEXALAYER_API_KEY")

    client = NexaLayerClient(
        api_key=api_key,
        base_url=os.getenv("NEXALAYER_BASE_URL", "https://api.nexalayer.net/v1"),
    )
    session_id = None

    try:
        product_no = pick_dynamic_product(client)
        session = client.create_session(
            session_type="dynamic",
            product_no=product_no,
            quantity=1,
            protocol="socks5",
            rotation_mode="on_demand",
            idempotency_key=f"sdk-py-{uuid.uuid4()}",
        )
        session_id = session.session_id
        print("session_id:", session_id)

        active = wait_for_active(client, session_id)
        proxy_url = active.get("proxy", {}).get("full_url")
        if not proxy_url:
            raise RuntimeError("Active session did not include proxy.full_url")

        try:
            res = requests.get(
                "https://httpbin.org/ip",
                proxies={"http": proxy_url, "https": proxy_url},
                timeout=30,
            )
            event_type = "success" if res.ok else "http_error"
            status_code = res.status_code
            print("httpbin:", res.text[:120])
        except requests.Timeout:
            event_type = "timeout"
            status_code = 0

        client.report_event(
            session_id,
            event_type=event_type,
            status_code=status_code,
            target_host="httpbin.org",
        )
        print("health:", client.get_session_health(session_id))
    finally:
        if session_id:
            client.terminate_session(session_id)
            print("terminated:", session_id)


if __name__ == "__main__":
    main()
