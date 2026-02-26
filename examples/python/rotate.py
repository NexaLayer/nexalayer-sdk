"""NexaLayer Python rotate example — create session and rotate (stub)."""

import os
from nexalayer import NexaLayerClient

def main():
    api_key = os.environ.get("NEXALAYER_API_KEY", "your-api-key")
    base_url = os.environ.get("NEXALAYER_BASE_URL", "https://api.nexalayer.net/v1")

    client = NexaLayerClient(api_key=api_key, base_url=base_url)
    session = client.create_session(
        type="dynamic",
        config={"product_no": "out_dynamic_1"},
    )
    print(f"Session: {session.session_id}")

    # Rotate proxy for this session
    result = session.rotate()
    print(f"Rotate result: {result}")

    usage = session.usage()
    print(f"Usage: {usage}")

if __name__ == "__main__":
    main()
