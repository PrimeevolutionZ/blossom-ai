"""
Blossom AI – Base Generator Classes (v0.5.4)
Unified retry via tenacity, single BaseGenerator for sync/async.
"""

from __future__ import annotations

import json
import uuid
from abc import ABC, abstractmethod
from typing import Optional,Final, Dict, Any, Iterator, AsyncIterator, Union
from urllib.parse import quote

import aiohttp
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from blossom_ai.core.config import LIMITS
from blossom_ai.core.errors import (
    AuthenticationError,
    BlossomError,
    RateLimitError,
    handle_request_error,
)
from blossom_ai.core.models import DynamicModel

# --------------------------------------------------------------------------- #
# Retry utils
# --------------------------------------------------------------------------- #

RETRYABLE_HTTP_CODES: Final = {502, 503, 504, 520}
DEFAULT_RETRY_AFTER: Final = 60
_MAX_RETRIES: Final = LIMITS.MAX_RETRIES

def _is_retryable_http(exc: Exception) -> bool:
    """Check if exception is HTTP error with retryable status."""
    if isinstance(exc, requests.exceptions.HTTPError):
        return exc.response.status_code in RETRYABLE_HTTP_CODES
    if isinstance(exc, aiohttp.ClientResponseError):
        return exc.status in RETRYABLE_HTTP_CODES
    return False

_retry_hook = retry(
    stop=stop_after_attempt(_MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=(
        retry_if_exception_type(RateLimitError)
        | retry_if_exception_type((requests.exceptions.HTTPError, aiohttp.ClientResponseError))
    ),
    reraise=True,
)

# --------------------------------------------------------------------------- #
# Base generator (sync/async)
# --------------------------------------------------------------------------- #

class BaseGenerator(ABC):
    """Common logic for sync/async generators."""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._api_token = api_token

    # ---------- helpers ----------
    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _encode_prompt(self, prompt: str) -> str:
        return quote(prompt)

    def _generate_request_id(self) -> str:
        return str(uuid.uuid4())

    def _get_auth_headers(self, request_id: Optional[str] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self._api_token:
            headers["Authorization"] = f"Bearer {self._api_token}"
        if request_id:
            headers["X-Request-ID"] = request_id
        return headers

    def _handle_http_error(self, status: int, body: bytes) -> bool:
        """
        Return True if error should be ignored (e.g. 402 on audio).
        Otherwise raise concrete exception.
        """
        if status == 401:
            raise AuthenticationError(
                message="Invalid or missing API token",
                suggestion="Check your API token at https://enter.pollinations.ai",
            )
        if status == 402:
            # audio endpoint may return 402 but works without auth
            if "text.pollinations.ai" in self.base_url:
                return True  # ignore
            raise BlossomError(
                message="Payment Required",
                error_type="API_ERROR",
                suggestion="Visit https://auth.pollinations.ai to upgrade or check your API token.",
            )
        if status == 429:
            retry_after = DEFAULT_RETRY_AFTER
            try:
                retry_after = int(json.loads(body.decode()).get("retry_after", DEFAULT_RETRY_AFTER))
            except Exception:
                pass
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if status >= 500:
            raise BlossomError(f"Server error {status}", error_type="API_ERROR")
        return False

    # ---------- sync ----------
    @_retry_hook
    def _make_request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
        **kwargs,
    ) -> requests.Response:
        from blossom_ai.core.session_manager import get_sync_session

        hdrs = (headers or {}).copy()
        hdrs.update(self._get_auth_headers())
        with get_sync_session() as session:
            resp = session.request(
                method,
                url,
                params=params,
                headers=hdrs,
                timeout=self.timeout,
                stream=stream,
                **kwargs,
            )
            if resp.status_code >= 400:
                if self._handle_http_error(resp.status_code, resp.content):
                    return resp  # ignored
            resp.raise_for_status()
            return resp

    # ---------- async ----------
    @_retry_hook
    async def _amake_request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        from blossom_ai.core.session_manager import get_async_session

        hdrs = (headers or {}).copy()
        hdrs.update(self._get_auth_headers())
        async with get_async_session() as session:
            resp = await session.request(
            method,
            url,
            params=params,
            headers=hdrs,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            **kwargs,
        )
        if resp.status >= 400:
            body = await resp.read()
            if self._handle_http_error(resp.status, body):
                return resp  # ignored
        resp.raise_for_status()
        return resp

    # ---------- streaming ----------
    def _stream_text(self, response: requests.Response) -> Iterator[str]:
        """Sync SSE streaming stub."""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield line

    async def _astream_text(self, response: aiohttp.ClientResponse) -> AsyncIterator[str]:
        """Async SSE streaming stub."""
        async for line in response.content:
            yield line.decode("utf-8", errors="ignore")

# --------------------------------------------------------------------------- #
# Sync-only mixin
# --------------------------------------------------------------------------- #

class SyncGenerator(BaseGenerator):
    """Sync-specific helpers."""

    def close(self) -> None:
        # manager lives per-thread – не закрываем здесь
        pass

    def __enter__(self) -> SyncGenerator:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

# --------------------------------------------------------------------------- #
# Async-only mixin
# --------------------------------------------------------------------------- #

class AsyncGenerator(BaseGenerator):
    async def close(self) -> None:
        # manager lives per-loop – не закрываем здесь
        pass

    async def __aenter__(self) -> AsyncGenerator:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()