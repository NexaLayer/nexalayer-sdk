import requests

class Client:
    def __init__(self, api_key, base_url="https://api.nexalayer.com"):
        self.api_key = api_key
        self.base_url = base_url

    def create_session(self, **kwargs):
        response = requests.post(
            f"{self.base_url}/v1/sessions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=kwargs
        )
        response.raise_for_status()
        return response.json()
