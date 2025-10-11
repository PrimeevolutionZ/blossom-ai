"""
Blossom AI - Base API Client
"""

import requests
from typing import Optional, Dict, Any
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import asyncio
import aiohttp

from .errors import BlossomError, handle_request_error, print_info, ErrorType


class BaseAPI:
    """Base class for synchronous API interactions"""

    def __init__(self, base_url: str, timeout: int = 30, api_token: Optional[str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.api_token = api_token
        self.session = requests.Session()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.exceptions.HTTPError) | retry_if_exception_type(requests.exceptions.ChunkedEncodingError),
        reraise=True
    )
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make synchronous HTTP request with error handling and retry logic"""
        try:
            kwargs.setdefault("timeout", self.timeout)

            if self.api_token:
                if method.upper() == 'POST':
                    if 'headers' not in kwargs:
                        kwargs['headers'] = {}
                    kwargs['headers']['Authorization'] = f'Bearer {self.api_token}'
                else:
                    if 'params' not in kwargs:
                        kwargs['params'] = {}
                    kwargs['params']['token'] = self.api_token

            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                status_code = e.response.status_code
                if status_code == 402:
                    try:
                        error_data = e.response.json()
                        error_msg = error_data.get('error', str(e))
                        raise BlossomError(
                            message=f"Payment Required: {error_msg}",
                            error_type=ErrorType.API,
                            suggestion="Your current tier may not support this feature. Visit https://auth.pollinations.ai to upgrade or check your API token."
                        )
                    except json.JSONDecodeError:
                        raise BlossomError(
                            message=f"Payment Required (402). Your tier may not support this feature.",
                            error_type=ErrorType.API,
                            suggestion="Visit https://auth.pollinations.ai to upgrade."
                        )
                if status_code == 502:
                    print_info(f"Retrying 502 error for {url}...")
                    raise
            if isinstance(e, requests.exceptions.ChunkedEncodingError):
                print_info(f"Retrying ChunkedEncodingError for {url}...")
                raise
            raise handle_request_error(e, f"making {method} request to {url}")


# ИСПРАВЛЕНИЕ: Создаем wrapper класс для ответа
class AsyncResponseWrapper:
    """Wrapper for aiohttp response to ensure it's properly closed"""
    def __init__(self, response: aiohttp.ClientResponse, data: bytes):
        self._response = response
        self._data = data

    @property
    def status(self):
        return self._response.status

    @property
    def headers(self):
        return self._response.headers

    @property
    def content(self):
        return self._data

    async def read(self):
        return self._data

    async def text(self, encoding='utf-8'):
        return self._data.decode(encoding)

    async def json(self):
        return json.loads(self._data.decode('utf-8'))


class AsyncBaseAPI:
    """Base class for asynchronous API interactions"""

    def __init__(self, base_url: str, timeout: int = 30, api_token: Optional[str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.api_token = api_token
        self._session = None

    async def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _make_request(self, method: str, url: str, **kwargs) -> AsyncResponseWrapper:
        """Make asynchronous HTTP request with error handling and retry logic"""
        session = await self._get_session()

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)

                headers = kwargs.pop('headers', {})
                params = kwargs.pop('params', {})

                if self.api_token:
                    if method.upper() == 'POST':
                        headers['Authorization'] = f'Bearer {self.api_token}'
                    else:
                        params['token'] = self.api_token

                # ИСПРАВЛЕНИЕ: Используем async with для правильного управления соединением
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    **kwargs
                ) as response:
                    # Читаем данные ВНУТРИ контекста
                    data = await response.read()

                    # Проверяем статус
                    if response.status >= 400:
                        if response.status == 402:
                            try:
                                error_data = json.loads(data.decode('utf-8'))
                                error_msg = error_data.get('error', 'Payment Required')
                                raise BlossomError(
                                    message=f"Payment Required: {error_msg}",
                                    error_type=ErrorType.API,
                                    suggestion="Your current tier may not support this feature. Visit https://auth.pollinations.ai to upgrade or check your API token."
                                )
                            except json.JSONDecodeError:
                                raise BlossomError(
                                    message=f"Payment Required (402). Your tier may not support this feature.",
                                    error_type=ErrorType.API,
                                    suggestion="Visit https://auth.pollinations.ai to upgrade."
                                )

                        if response.status == 502:
                            retry_count += 1
                            if retry_count < max_retries:
                                print_info(f"Retrying 502 error for {url}... (attempt {retry_count}/{max_retries})")
                                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                                continue

                        # Для других ошибок 4xx/5xx
                        error_text = data.decode('utf-8', errors='replace')
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=error_text
                        )

                    # Возвращаем wrapper с уже прочитанными данными
                    return AsyncResponseWrapper(response, data)

            except aiohttp.ClientError as e:
                if isinstance(e, aiohttp.ClientResponseError):
                    if e.status == 502 and retry_count < max_retries - 1:
                        retry_count += 1
                        print_info(f"Retrying on ClientError 502 for {url}... (attempt {retry_count}/{max_retries})")
                        await asyncio.sleep(2 ** retry_count)
                        continue

                raise handle_request_error(e, f"making {method} request to {url}")

            except asyncio.TimeoutError:
                raise BlossomError(
                    message=f"Request timeout after {self.timeout}s when making {method} request to {url}",
                    error_type=ErrorType.NETWORK,
                    suggestion="Try increasing timeout or check your connection."
                )

        # Если все попытки исчерпаны
        raise BlossomError(
            message=f"Max retries exceeded for {method} request to {url}",
            error_type=ErrorType.NETWORK,
            suggestion="The API may be temporarily unavailable. Try again later."
        )