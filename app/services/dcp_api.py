import time

import requests

from app.config import DCP_API_URL, DCP_LOGIN, DCP_PASSWORD


class DcpApi:
    def __init__(self):
        self.base_url = DCP_API_URL
        self.login = DCP_LOGIN
        self.password = DCP_PASSWORD

        self.token = None
        self.expires_at = 0

    def _login(self):
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "login": self.login,
                "password": self.password,
            },
            headers={
                "Accept": "application/json",
            },
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        self.token = data["accessToken"]
        self.expires_at = time.time() + data["expiresIn"] - 30

    def _get_token(self):
        if not self.token or time.time() >= self.expires_at:
            self._login()

        return self.token

    def get_rosters(self):
        token = self._get_token()

        response = requests.get(
            f"{self.base_url}/rosters",
            params={"type": "PARTY"},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()


dcp_api = DcpApi()