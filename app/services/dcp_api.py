import asyncio
import time
from typing import Any

import aiohttp

from app.config import DCP_API_URL, DCP_LOGIN, DCP_PASSWORD


class DcpApi:
    def __init__(self) -> None:
        self.base_url = DCP_API_URL.rstrip("/") if DCP_API_URL else ""
        self.login = DCP_LOGIN
        self.password = DCP_PASSWORD
        self.token: str | None = None
        self.expires_at = 0.0
        self._token_lock = asyncio.Lock()

    def _validate_config(self) -> None:
        missing = [
            name
            for name, value in (
                ("DCP_API_URL", self.base_url),
                ("DCP_LOGIN", self.login),
                ("DCP_PASSWORD", self.password),
            )
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Missing DCP configuration: {', '.join(missing)}"
            )

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        **kwargs: Any,
    ) -> Any:
        headers = {
            "Accept": "application/json",
            **kwargs.pop("headers", {}),
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                **kwargs,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def _login(self) -> str:
        self._validate_config()
        data = await self._request_json(
            "POST",
            "/auth/login",
            json={
                "login": self.login,
                "password": self.password,
            },
        )
        token = data.get("accessToken")
        if not isinstance(token, str) or not token:
            raise RuntimeError("DCP login response does not contain accessToken")

        expires_in = data.get("expiresIn", 300)
        try:
            expires_seconds = float(expires_in)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("DCP login response contains invalid expiresIn") from exc

        self.token = token
        self.expires_at = time.monotonic() + max(0.0, expires_seconds - 30)
        return token

    async def _get_token(self) -> str:
        if self.token and time.monotonic() < self.expires_at:
            return self.token

        async with self._token_lock:
            if self.token and time.monotonic() < self.expires_at:
                return self.token
            return await self._login()

    async def _get_json(self, path: str, **kwargs: Any) -> Any:
        self._validate_config()
        token = await self._get_token()
        try:
            return await self._request_json(
                "GET",
                path,
                token=token,
                **kwargs,
            )
        except aiohttp.ClientResponseError as exc:
            if exc.status != 401:
                raise

        self.token = None
        token = await self._get_token()
        return await self._request_json(
            "GET",
            path,
            token=token,
            **kwargs,
        )

    async def get_rosters(self) -> list[dict[str, Any]]:
        data = await self._get_json("/rosters", params={"type": "PARTY"})
        if not isinstance(data, list):
            raise RuntimeError("DCP rosters response must be a list")
        return data

    async def get_auctions(self) -> list[dict[str, Any]]:
        data = await self._get_json("/auctions")
        if not isinstance(data, list):
            raise RuntimeError("DCP auctions response must be a list")
        return data

    async def get_targets(self) -> list[dict[str, Any]]:
        data = await self._get_json("/targets")
        if not isinstance(data, list):
            raise RuntimeError("DCP targets response must be a list")
        return data


dcp_api = DcpApi()
