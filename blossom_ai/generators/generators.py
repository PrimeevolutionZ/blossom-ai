"""
Blossom AI – Generators (v0.5.0-hotfix)
V2 API only (enter.pollinations.ai)
"""

from __future__ import annotations

import json
from typing import (
    Any, AsyncIterator, Dict, Iterator, List, Optional, Union, cast
)
from urllib.parse import urlencode

from blossom_ai.generators.base_generator import (
    AsyncGenerator, SyncGenerator, ModelAwareGenerator
)
from blossom_ai.generators.streaming_mixin import (
    AsyncStreamingMixin, SyncStreamingMixin, SSEParser
)
from blossom_ai.generators.parameter_builder import (
    ChatParamsV2, ImageParamsV2, MessageBuilder, ParameterValidator
)
from blossom_ai.core.config import DEFAULTS, ENDPOINTS, LIMITS
from blossom_ai.core.errors import print_warning
from blossom_ai.core.models import (
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, ImageModel, TextModel
)

# --------------------------------------------------------------------------- #
# Image – internal helpers
# --------------------------------------------------------------------------- #
class _ImageBase:
    """Shared logic for sync & async image generators."""

    _fallback_models = DEFAULT_IMAGE_MODELS

    @staticmethod
    def _validate_prompt(prompt: str) -> None:
        ParameterValidator.prompt_length(
            prompt, LIMITS.MAX_IMAGE_PROMPT_LENGTH, "prompt"
        )

    def _make_url(self, base_url: str, prompt: str, params: ImageParamsV2) -> str:
        """Compose *safe* URL (no token)."""
        encoded = self._encode_prompt(prompt)
        url = f"{base_url.rstrip('/')}/{encoded}"
        qs = urlencode(params.to_dict())
        return f"{url}?{qs}" if qs else url

    def _extract_models(self, payload: Any) -> List[str]:
        """Normalize server response to list of names."""
        models: List[str] = []
        if not isinstance(payload, list):
            return models
        for item in payload:
            if isinstance(item, str):
                models.append(item)
            elif isinstance(item, dict):
                name = item.get("name") or item.get("id")
                if name:
                    models.append(name)
        return models or self._fallback_models

# --------------------------------------------------------------------------- #
# Sync Image
# --------------------------------------------------------------------------- #
class ImageGenerator(SyncGenerator, ModelAwareGenerator, _ImageBase):
    """Synchronous image generator."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        SyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, self._fallback_models)

    #  required abstract method
    def _validate_prompt(self, prompt: str) -> None:
        _ImageBase._validate_prompt(prompt)

    #  public high-level API
    def generate(self, prompt: str, **kw: Any) -> bytes:
        self._validate_prompt(prompt)
        params = ImageParamsV2(model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)), **kw)
        url = self._make_url(self.base_url, prompt, params)
        resp = self._make_request("GET", url)
        return resp.content

    def generate_url(self, prompt: str, **kw: Any) -> str:
        self._validate_prompt(prompt)
        params = ImageParamsV2(model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)), **kw)
        return self._make_url(self.base_url, prompt, params)

    def save(self, prompt: str, filename: str, **kw: Any) -> str:
        data = self.generate(prompt, **kw)
        with open(filename, "wb") as fh:
            fh.write(data)
        return filename

    def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            resp = self._make_request("GET", ENDPOINTS.IMAGE_MODELS)
            self._models_cache = self._extract_models(resp.json())
            self._update_known_models(self._models_cache)
        except Exception as exc:
            print_warning(f"Failed to fetch image models: {exc}")
            self._models_cache = self._fallback_models
        return self._models_cache

# --------------------------------------------------------------------------- #
# Async Image
# --------------------------------------------------------------------------- #
class AsyncImageGenerator(AsyncGenerator, ModelAwareGenerator, _ImageBase):
    """Asynchronous image generator."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        AsyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, self._fallback_models)

    #  required abstract method
    def _validate_prompt(self, prompt: str) -> None:
        _ImageBase._validate_prompt(prompt)

    async def generate(self, prompt: str, **kw: Any) -> bytes:
        self._validate_prompt(prompt)
        params = ImageParamsV2(model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)), **kw)
        url = self._make_url(self.base_url, prompt, params)
        return cast(bytes, await self._make_request("GET", url))

    async def generate_url(self, prompt: str, **kw: Any) -> str:
        self._validate_prompt(prompt)
        params = ImageParamsV2(model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)), **kw)
        return self._make_url(self.base_url, prompt, params)

    async def save(self, prompt: str, filename: str, **kw: Any) -> str:
        data = await self.generate(prompt, **kw)
        with open(filename, "wb") as fh:
            fh.write(data)
        return filename

    async def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            data = await self._make_request("GET", ENDPOINTS.IMAGE_MODELS)
            self._models_cache = self._extract_models(json.loads(data.decode()))
            self._update_known_models(self._models_cache)
        except Exception as exc:
            print_warning(f"Failed to fetch image models: {exc}")
            self._models_cache = self._fallback_models
        return self._models_cache

# --------------------------------------------------------------------------- #
# Text – internal helpers
# --------------------------------------------------------------------------- #
class _TextBase:
    """Shared text-logic for sync & async paths."""

    _fallback_models = DEFAULT_TEXT_MODELS
    _chat_endpoint = f"{ENDPOINTS.BASE}/generate/v1/chat/completions"
    _models_endpoint = f"{ENDPOINTS.BASE}/generate/v1/models"

    @staticmethod
    def _validate_prompt(prompt: str) -> None:
        ParameterValidator.prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "prompt"
        )

    @staticmethod
    def _normalize_messages(
        prompt: str, system: Optional[str], messages: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Return OpenAI-style messages list."""
        if messages:
            return messages
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        return msgs

    def _make_params(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str,
        stream: bool,
        **kw: Any,
    ) -> ChatParamsV2:
        """Single place where ChatParamsV2 is built."""
        return ChatParamsV2(
            model=self._validate_model(model),                               # type: ignore
            messages=messages,
            stream=stream,
            **kw,
        )

    def _extract_text(self, payload: Dict[str, Any]) -> str:
        """Grab text from server JSON."""
        return payload["choices"][0]["message"]["content"]

    def _extract_models(self, payload: Any) -> List[str]:
        models: List[str] = []
        if not isinstance(payload, list):
            return models
        for item in payload:
            if isinstance(item, dict):
                name = item.get("name")
                if name:
                    models.append(name)
                    for alias in item.get("aliases", []):
                        models.append(alias)
        return models or self._fallback_models

# --------------------------------------------------------------------------- #
# Sync Text
# --------------------------------------------------------------------------- #
class TextGenerator(
    SyncGenerator, SyncStreamingMixin, ModelAwareGenerator, _TextBase
):
    """Synchronous text generator with vision & audio support."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        SyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, self._fallback_models)
        self._sse = SSEParser()

    #  required abstract method
    def _validate_prompt(self, prompt: str) -> None:
        _TextBase._validate_prompt(prompt)

    #  ----------  public high-level API  ----------
    def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        **kw: Any,
    ) -> Union[str, Iterator[str]]:
        self._validate_prompt(prompt)
        msgs = self._normalize_messages(prompt, system, messages)
        return self.chat(messages=msgs, stream=stream, **kw)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        stream: bool = False,
        **kw: Any,
    ) -> Union[str, Iterator[str]]:
        params = self._make_params(messages, model=kw.pop("model", DEFAULTS.TEXT_MODEL), stream=stream, **kw)
        resp = self._make_request(
            "POST",
            self._chat_endpoint,
            json=params.to_body(),
            headers={"Content-Type": "application/json"},
            stream=stream,
        )
        if stream:
            return self._stream_sse_chunked(resp, self._sse)
        return self._extract_text(resp.json())

    def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            resp = self._make_request("GET", self._models_endpoint)
            self._models_cache = self._extract_models(resp.json())
            self._update_known_models(self._models_cache)
        except Exception as exc:
            print_warning(f"Failed to fetch text models: {exc}")
            self._models_cache = self._fallback_models
        return self._models_cache

# --------------------------------------------------------------------------- #
# Async Text
# --------------------------------------------------------------------------- #
class AsyncTextGenerator(
    AsyncGenerator, AsyncStreamingMixin, ModelAwareGenerator, _TextBase
):
    """Asynchronous text generator with vision & audio support."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        AsyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, self._fallback_models)
        self._sse = SSEParser()

    #  required abstract method
    def _validate_prompt(self, prompt: str) -> None:
        _TextBase._validate_prompt(prompt)

    #  ----------  public high-level API  ----------
    async def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        **kw: Any,
    ) -> Union[str, AsyncIterator[str]]:
        self._validate_prompt(prompt)
        msgs = self._normalize_messages(prompt, system, messages)
        if stream:
            return self.chat(messages=msgs, stream=True, **kw)                                     # type: ignore
        return await self.chat_text(messages=msgs, stream=False, **kw)

    async def chat_text(
        self,
        messages: List[Dict[str, Any]],
        *,
        stream: bool = False,
        **kw: Any,
    ) -> str:
        params = self._make_params(messages, model=kw.pop("model", DEFAULTS.TEXT_MODEL), stream=False, **kw)
        data = await self._make_request(
            "POST",
            self._chat_endpoint,
            json=params.to_body(),
            headers={"Content-Type": "application/json"},
        )
        return self._extract_text(json.loads(data.decode()))

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        stream: bool = False,
        **kw: Any,
    ) -> AsyncIterator[str]:
        params = self._make_params(messages, model=kw.pop("model", DEFAULTS.TEXT_MODEL), stream=True, **kw)
        resp = await self._make_request(
            "POST",
            self._chat_endpoint,
            json=params.to_body(),
            headers={"Content-Type": "application/json"},
            stream=True,
        )
        async for chunk in self._stream_sse_chunked(resp, self._sse):
            yield chunk

    async def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            data = await self._make_request("GET", self._models_endpoint)
            self._models_cache = self._extract_models(json.loads(data.decode()))
            self._update_known_models(self._models_cache)
        except Exception as exc:
            print_warning(f"Failed to fetch text models: {exc}")
            self._models_cache = self._fallback_models
        return self._models_cache