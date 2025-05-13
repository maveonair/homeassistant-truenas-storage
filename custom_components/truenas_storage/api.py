import requests


class TrueNASAPI:
    def __init__(self, host: str, port: int, api_key: str, verify_ssl: bool = True):
        self.base_url = f"https://{host}:{port}/api/v2.0"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.verify_ssl = verify_ssl

    def get_pools(self):
        response = requests.get(
            f"{self.base_url}/pool", headers=self.headers, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()
