"""NexaLayer Python rotate example.

Creates a dynamic session, rotates it, reads usage, and terminates it.
This can create a real paid session.
"""

import os
import uuid

from nexalayer import NexaLayerClient


def unwrap(response):
    return response.get("data", response)


def pick_dynamic_product(client):
    override = os.getenv("NEXALAYER_PRODUCT_NO")
    if override:
        return override
    products = unwrap(client.get_products(type="dynamic"))
    for item in products.get("items", []):
        if item.get("product_no"):
            return item["product_no"]
    raise RuntimeError("No dynamic product available")


def main():
    api_key = os.getenv("NEXALAYER_API_KEY")
    if not api_key:
        raise RuntimeError("Set NEXALAYER_API_KEY")
    client = NexaLayerClient(api_key=api_key)
    session_id = None
    try:
        session = client.create_session(
            session_type="dynamic",
            product_no=pick_dynamic_product(client),
            quantity=1,
            protocol="socks5",
            rotation_mode="on_demand",
            idempotency_key=f"sdk-rotate-{uuid.uuid4()}",
        )
        session_id = session.session_id
        print("Session:", session_id)
        print("Rotate result:", session.rotate())
        print("Usage:", session.usage())
    finally:
        if session_id:
            client.terminate_session(session_id)
            print("Terminated:", session_id)


if __name__ == "__main__":
    main()
