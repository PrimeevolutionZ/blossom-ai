"""
Blossom AI - Base Generator Classes (Refactored)
"""

import json
import asyncio
import time
import uuid
import random
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Iterator, AsyncIterator, Callable, Union
from urllib.parse import quote
from functools import wraps

import requests
import aiohttp

from blossom_ai.core.session_manager import SyncSessionManager, AsyncSessionManager
from blossom_ai.core.config import LIMITS
from blossom_ai.core.errors import (
    AuthenticationError,
    BlossomError, ErrorType, StreamError, RateLimitError,
    handle_request_error, print_info, print_warning, print_debug
)
from blossom_ai.core.models import DynamicModel

# ============================================================================
# CONSTANTS
# ============================================================================

RETRYABLE_HTTP_CODES = {502, 503, 504}
DEFAULT_RETRY_AFTER = 60
MAX_EXPONENTIAL_BACKOFF = 32
MAX_CHUNK_ENCODING_BACKOFF = 16

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _calculate_wait_time(attempt: int, max_backoff: int = MAX_EXPONENTIAL_BACKOFF) -> float:
    """Calculate exponential backoff with jitter."""
    return min(2 ** attempt + random.uniform(0, 1), max_backoff)

def _log_safe_url(url: str) -> str:
    """Return URL without query params for safe logging."""
    return url.split('?')[0]

# ============================================================================
# RETRY DECORATOR (REFACTORED)
# ============================================================================

def with_retry(max_attempts: int = LIMITS.MAX_RETRIES):
    """Unified retry decorator for sync and async functions."""
    def decorator(func: Callable):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = e.retry_after or DEFAULT_RETRY_AFTER
                        print_info(f"Rate limited. Waiting {wait_time}s before retry (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(wait_time)
                        continue
                    raise
                except requests.exceptions.HTTPError as e:
                    last_exception = e
                    if e.response.status_code in RETRYABLE_HTTP_CODES and attempt < max_attempts - 1:
                        wait_time = _calculate_wait_time(attempt)
                        print_info(f"Retrying {e.response.status_code} error (attempt {attempt + 1}/{max_attempts}, waiting {wait_time:.1f}s)...")
                        time.sleep(wait_time)
                        continue
                    raise
                except requests.exceptions.ChunkedEncodingError as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = _calculate_wait_time(attempt, MAX_CHUNK_ENCODING_BACKOFF)
                        print_info(f"Retrying chunked encoding error (attempt {attempt + 1}/{max_attempts})...")
                        time.sleep(wait_time)
                        continue
                    raise
                except Exception:
                    raise
            if last_exception:
                raise last_exception

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = e.retry_after or DEFAULT_RETRY_AFTER
                        print_info(f"Rate limited. Waiting {wait_time}s before retry (attempt {attempt + 1}/{max_attempts})")
                        await asyncio.sleep(wait_time)
                        continue
                    raise
                except aiohttp.ClientResponseError as e:
                    last_exception = e
                    if e.status in RETRYABLE_HTTP_CODES and attempt < max_attempts - 1:
                        wait_time = _calculate_wait_time(attempt)
                        print_info(f"Retrying {e.status} error (attempt {attempt + 1}/{max_attempts}, waiting {wait_time:.1f}s)...")
                        await asyncio.sleep(wait_time)
                        continue
                    raise
                except aiohttp.ClientError as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = _calculate_wait_time(attempt, MAX_CHUNK_ENCODING_BACKOFF)
                        print_info(f"Retrying connection error (attempt {attempt + 1}/{max_attempts})...")
                        await asyncio.sleep(wait_time)
                        continue
                    raise
                except Exception:
                    raise
            if last_exception:
                raise last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator

# ============================================================================
# BASE GENERATOR (REFACTORED)
# ============================================================================

class BaseGenerator(ABC):
    """Abstract base class for all generators."""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._api_token = api_token  # private to avoid accidental exposure

    @abstractmethod
    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt before making request."""
        pass

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _encode_prompt(self, prompt: str) -> str:
        """URL encode prompt."""
        return quote(prompt)

    def _generate_request_id(self) -> str:
        """Generate unique request ID for tracing."""
        return str(uuid.uuid4())

    def _is_v2_api(self) -> bool:
        """Check if this is V2 API."""
        return 'enter.pollinations.ai' in self.base_url

    def _get_auth_headers(self, request_id: Optional[str] = None) -> Dict[str, str]:
        """Get authentication headers."""
        headers = {}
        if self._api_token:
            headers['Authorization'] = f'Bearer {self._api_token}'
        if request_id:
            headers['X-Request-ID'] = request_id
        return headers

    def _handle_http_error(self, status_code: int, response_data: Optional[bytes] = None) -> None:
        """Handle HTTP errors securely."""
        if status_code == 401:
            raise AuthenticationError(
                message="Invalid or missing API token",
                suggestion="Check your API token at https://enter.pollinations.ai"
            )
        if status_code == 402:
            error_msg = "Payment Required"
            if response_data:
                try:
                    decoded = response_data.decode('utf-8')
                    error_data = json.loads(decoded)
                    error_msg = error_data.get('error', error_msg)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    error_msg = response_data.decode('utf-8', errors='ignore')[:200]
            raise BlossomError(
                message=f"Payment Required: {error_msg}",
                error_type=ErrorType.API,
                suggestion="Visit https://auth.pollinations.ai to upgrade or check your API token."
            )
        if status_code == 429:
            retry_after = DEFAULT_RETRY_AFTER
            if response_data:
                try:
                    decoded = response_data.decode('utf-8')
                    error_data = json.loads(decoded)
                    retry_after = error_data.get('retry_after', DEFAULT_RETRY_AFTER)
                except:
                    pass
            raise RateLimitError(message="Rate limit exceeded", retry_after=retry_after)

# ============================================================================
# SYNC GENERATOR (REFACTORED)
# ============================================================================

class SyncGenerator(BaseGenerator):
    """Base class for synchronous generators."""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        super().__init__(base_url, timeout, api_token)
        self._session_manager = SyncSessionManager()

    @property
    def session(self) -> requests.Session:
        return self._session_manager.get_session()

    @with_retry()
    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        stream: bool = False,
        request_id: Optional[str] = None,
        **kwargs
    ) -> requests.Response:
        if request_id is None:
            request_id = self._generate_request_id()

        kwargs.setdefault("timeout", self.timeout)
        kwargs['stream'] = stream
        headers = kwargs.pop('headers', {})
        headers.update(self._get_auth_headers(request_id))
        kwargs['headers'] = headers

        print_debug(f"Request {request_id}: {method} {_log_safe_url(url)}")

        response = self.session.request(method, url, params=params or {}, **kwargs)

        if response.status_code >= 400:
            self._handle_http_error(response.status_code, response.content)
            response.raise_for_status()

        return response

    def _stream_with_timeout(
        self,
        response: requests.Response,
        chunk_timeout: Optional[int] = None
    ) -> Iterator[str]:
        """Stream response with timeout between chunks."""
        if chunk_timeout is None:
            chunk_timeout = LIMITS.STREAM_CHUNK_TIMEOUT

        last_data_time = time.time()
        try:
            for line in response.iter_lines(decode_unicode=True, chunk_size=1024):
                if time.time() - last_data_time > chunk_timeout:
                    raise StreamError(
                        message=f"Stream timeout: no data received for {chunk_timeout}s",
                        suggestion="Check your connection or increase timeout"
                    )
                if line:
                    last_data_time = time.time()
                    yield line
        finally:
            if not response.raw.closed:
                response.close()

    def _fetch_list(self, endpoint: str, fallback: list) -> list:
        """Fetch list from API endpoint with fallback."""
        try:
            url = self._build_url(endpoint)
            response = self._make_request("GET", url)
            data = response.json()

            if isinstance(data, list):
                result = []
                for item in data:
                    if isinstance(item, dict):
                        name = item.get('name') or item.get('id') or item.get('model')
                        if name:
                            result.append(name)
                    elif isinstance(item, str):
                        result.append(item)
                return result if result else fallback
            return fallback

        except (json.JSONDecodeError, ValueError) as e:
            print_warning(f"Failed to parse {endpoint} response: {e}")
            return fallback
        except Exception as e:
            print_warning(f"Failed to fetch {endpoint}: {e}")
            return fallback

    def close(self):
        self._session_manager.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

# ============================================================================
# ASYNC GENERATOR (REFACTORED)
# ============================================================================

class AsyncGenerator(BaseGenerator):
    """Base class for asynchronous generators."""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        super().__init__(base_url, timeout, api_token)
        self._session_manager = AsyncSessionManager()

    async def _get_session(self) -> aiohttp.ClientSession:
        return await self._session_manager.get_session()

    @with_retry()
    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        stream: bool = False,
        request_id: Optional[str] = None,
        **kwargs
    ) -> Union[bytes, aiohttp.ClientResponse]:
        if request_id is None:
            request_id = self._generate_request_id()

        session = await self._get_session()
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        headers = kwargs.pop('headers', {})
        headers.update(self._get_auth_headers(request_id))

        print_debug(f"Async Request {request_id}: {method} {_log_safe_url(url)}")

        if stream:
            response = await session.request(
                method, url, headers=headers, params=params or {},
                timeout=timeout, **kwargs
            )
            if response.status >= 400:
                data = await response.read()
                await response.close()
                self._handle_http_error(response.status, data)
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"HTTP {response.status}"
                )
            return response
        else:
            async with session.request(
                method, url, headers=headers, params=params or {},
                timeout=timeout, **kwargs
            ) as response:
                data = await response.read()
                if response.status >= 400:
                    self._handle_http_error(response.status, data)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=data.decode('utf-8', errors='replace')
                    )
                return data

    async def _fetch_list(self, endpoint: str, fallback: list) -> list:
        """Fetch list from API endpoint with fallback."""
        try:
            url = self._build_url(endpoint)
            data = await self._make_request("GET", url)
            parsed = json.loads(data.decode('utf-8'))

            if isinstance(parsed, list):
                result = []
                for item in parsed:
                    if isinstance(item, dict):
                        name = item.get('name') or item.get('id') or item.get('model')
                        if name:
                            result.append(name)
                    elif isinstance(item, str):
                        result.append(item)
                return result if result else fallback
            return fallback

        except (json.JSONDecodeError, ValueError) as e:
            print_warning(f"Failed to parse {endpoint} response: {e}")
            return fallback
        except Exception as e:
            print_warning(f"Failed to fetch {endpoint}: {e}")
            return fallback

    async def close(self):
        await self._session_manager.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

# ============================================================================
# MODEL AWARE MIXIN (REFACTORED)
# ============================================================================

class ModelAwareGenerator:
    """Mixin for generators that work with dynamic models."""

    def __init__(self, model_class: type[DynamicModel], fallback_models: list):
        self._model_class = model_class
        self._fallback_models = fallback_models
        self._models_cache: Optional[list] = None

    def _update_known_models(self, models: list):
        """Update known models in model class."""
        self._model_class.update_known_values(models)
        self._models_cache = models

    def _validate_model(self, model: str) -> str:
        """Validate and normalize model name."""
        return self._model_class.from_string(model)