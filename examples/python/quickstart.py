"""NexaLayer Python quickstart — create client and session (stub)."""

import os
from nexalayer import NexaLayerClient

def main():
    api_key = os.environ.get("NEXALAYER_API_KEY", "your-api-key")
    base_url = os.environ.get("NEXALAYER_BASE_URL", "https://api.nexalayer.net/v1")

    client = NexaLayerClient(api_key=api_key, base_url=base_url)
    session = client.create_session(
        type="dynamic",
        config={"product_no": "out_dynamic_1", "traffic_gb": 1},
    )
    print(f"Session created: {session.session_id}")

    # Placeholder: real proxy not applied yet
    resp = session.get("https://httpbin.org/ip")
    print(f"IP check status: {resp.status_code}")

if __name__ == "__main__":
    main()
