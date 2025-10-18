"""
Blossom AI - Base Generator Classes
Unified base classes for all generators with retry logic and error handling
"""

import json
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from urllib.parse import quote

import requests
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .session_manager import SyncSessionManager, AsyncSessionManager
from .errors import BlossomError, ErrorType, handle_request_error, print_info, print_warning
from .models import DynamicModel


class BaseGenerator(ABC):
    """Abstract base class for all generators"""

    MAX_PROMPT_LENGTH = 10000  # Default, can be overridden

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.api_token = api_token

    @abstractmethod
    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt before making request"""
        pass

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return f"{self.base_url}/{endpoint}".rstrip('/')

    def _encode_prompt(self, prompt: str) -> str:
        """URL encode prompt"""
        return quote(prompt)

    def _add_auth_params(self, params: Dict[str, Any], method: str = 'GET') -> Dict[str, Any]:
        """Add authentication parameters based on method"""
        if not self.api_token:
            return params

        if method.upper() == 'POST':
            # POST uses Bearer token in headers (handled separately)
            return params
        else:
            # GET uses token in query params
            params['token'] = self.api_token
            return params

    def _get_auth_headers(self, method: str = 'GET') -> Dict[str, str]:
        """Get authentication headers"""
        if not self.api_token or method.upper() != 'POST':
            return {}

        return {'Authorization': f'Bearer {self.api_token}'}


class SyncGenerator(BaseGenerator):
    """Base class for synchronous generators"""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        super().__init__(base_url, timeout, api_token)
        self._session_manager = SyncSessionManager()

    @property
    def session(self) -> requests.Session:
        """Get requests session"""
        return self._session_manager.get_session()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.exceptions.HTTPError) |
              retry_if_exception_type(requests.exceptions.ChunkedEncodingError),
        reraise=True
    )
    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with retry logic"""
        try:
            kwargs.setdefault("timeout", self.timeout)

            # Add auth
            if params is None:
                params = {}
            params = self._add_auth_params(params, method)

            headers = kwargs.get('headers', {})
            headers.update(self._get_auth_headers(method))
            kwargs['headers'] = headers

            response = self.session.request(method, url, params=params, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 402:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', str(e))
                except json.JSONDecodeError:
                    error_msg = "Payment Required"

                raise BlossomError(
                    message=f"Payment Required: {error_msg}",
                    error_type=ErrorType.API,
                    suggestion="Visit https://auth.pollinations.ai to upgrade or check your API token."
                )

            if e.response.status_code == 502:
                print_info(f"Retrying 502 error for {url}...")
                raise

            raise handle_request_error(e, f"making {method} request to {url}")

        except requests.exceptions.ChunkedEncodingError:
            print_info(f"Retrying ChunkedEncodingError for {url}...")
            raise

        except requests.exceptions.RequestException as e:
            raise handle_request_error(e, f"making {method} request to {url}")

    def _fetch_list(self, endpoint: str, fallback: list) -> list:
        """Fetch list from API endpoint with fallback"""
        try:
            url = self._build_url(endpoint)
            response = self._make_request("GET", url)
            data = response.json()

            # API может возвращать как список строк, так и список словарей
            if isinstance(data, list):
                result = []
                for item in data:
                    if isinstance(item, dict):
                        # Извлечь имя из словаря
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
        """Close session"""
        self._session_manager.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


class AsyncGenerator(BaseGenerator):
    """Base class for asynchronous generators"""

    def __init__(self, base_url: str, timeout: int, api_token: Optional[str] = None):
        super().__init__(base_url, timeout, api_token)
        self._session_manager = AsyncSessionManager()

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get aiohttp session"""
        return await self._session_manager.get_session()

    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        max_retries: int = 3,
        **kwargs
    ) -> bytes:
        """Make async HTTP request with retry logic"""
        session = await self._get_session()

        retry_count = 0
        last_exception = None

        while retry_count < max_retries:
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)

                # Prepare headers and params
                headers = kwargs.pop('headers', {})
                if params is None:
                    params = {}

                # Add authentication
                params = self._add_auth_params(params, method)
                headers.update(self._get_auth_headers(method))

                async with session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    **kwargs
                ) as response:
                    data = await response.read()

                    if response.status >= 400:
                        if response.status == 402:
                            try:
                                error_data = json.loads(data.decode('utf-8'))
                                error_msg = error_data.get('error', 'Payment Required')
                            except json.JSONDecodeError:
                                error_msg = 'Payment Required'

                            raise BlossomError(
                                message=f"Payment Required: {error_msg}",
                                error_type=ErrorType.API,
                                suggestion="Visit https://auth.pollinations.ai to upgrade."
                            )

                        if response.status == 502 and retry_count < max_retries - 1:
                            retry_count += 1
                            print_info(f"Retrying 502 error for {url}... ({retry_count}/{max_retries})")
                            await asyncio.sleep(2 ** retry_count)
                            continue

                        error_text = data.decode('utf-8', errors='replace')
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=error_text
                        )

                    return data

            except aiohttp.ClientError as e:
                last_exception = e
                if isinstance(e, aiohttp.ClientResponseError) and e.status == 502:
                    if retry_count < max_retries - 1:
                        retry_count += 1
                        print_info(f"Retrying ClientError 502 for {url}... ({retry_count}/{max_retries})")
                        await asyncio.sleep(2 ** retry_count)
                        continue

                raise handle_request_error(e, f"making {method} request to {url}")

            except asyncio.TimeoutError:
                raise BlossomError(
                    message=f"Request timeout after {self.timeout}s",
                    error_type=ErrorType.NETWORK,
                    suggestion="Try increasing timeout or check your connection."
                )

        # Max retries exceeded
        if last_exception:
            raise handle_request_error(last_exception, f"making {method} request (max retries)")

        raise BlossomError(
            message=f"Max retries exceeded for {method} request to {url}",
            error_type=ErrorType.NETWORK,
            suggestion="The API may be temporarily unavailable."
        )

    async def _fetch_list(self, endpoint: str, fallback: list) -> list:
        """Fetch list from API endpoint with fallback"""
        try:
            url = self._build_url(endpoint)
            data = await self._make_request("GET", url)
            parsed = json.loads(data.decode('utf-8'))

            # API может возвращать как список строк, так и список словарей
            if isinstance(parsed, list):
                result = []
                for item in parsed:
                    if isinstance(item, dict):
                        # Извлечь имя из словаря
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
        """Close session"""
        await self._session_manager.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __del__(self):
        """Background cleanup on destruction"""
        if hasattr(self, '_session_manager'):
            # Let the session manager handle cleanup
            pass


class ModelAwareGenerator:
    """Mixin for generators that work with dynamic models"""

    def __init__(self, model_class: type[DynamicModel], fallback_models: list):
        self._model_class = model_class
        self._fallback_models = fallback_models
        self._models_cache: Optional[list] = None

    def _update_known_models(self, models: list):
        """Update known models in model class"""
        self._model_class.update_known_values(models)
        self._models_cache = models

    def _validate_model(self, model: str) -> str:
        """Validate and normalize model name"""
        return self._model_class.from_string(model)