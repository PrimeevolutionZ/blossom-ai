"""
Blossom AI – Generators (v0.5.4)
Single implementation for sync/async via generic ImageGen/AudioGen.
"""

from __future__ import annotations
import asyncio
import json
from typing import (
    Any,Final, AsyncIterator, Dict, Iterator, List, Optional, Union, TypeVar, Generic,
)
from urllib.parse import quote

from blossom_ai.core.config import DEFAULTS, ENDPOINTS, LIMITS
from blossom_ai.core.errors import BlossomError, ErrorType, print_warning, print_debug
from blossom_ai.core.models import DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, ImageModel, TextModel
from blossom_ai.generators.base_generator import BaseGenerator, SyncGenerator, AsyncGenerator
from blossom_ai.generators.streaming_mixin import StreamingMixin
from blossom_ai.generators.parameter_builder import ImageParamsV2, ChatParamsV2, ParameterValidator

T = TypeVar("T", bound=BaseGenerator)

# --------------------------------------------------------------------------- #
# Image – generic sync/async
# --------------------------------------------------------------------------- #

class _ImageBase(Generic[T]):
    fallback_models = DEFAULT_IMAGE_MODELS

    @staticmethod
    def validate_prompt(prompt: str) -> None:
        ParameterValidator.prompt_length(prompt, LIMITS.MAX_IMAGE_PROMPT_LENGTH, "prompt")

    def _make_url(self, base_url: str, prompt: str, params: ImageParamsV2) -> str:
        encoded = quote(prompt)
        url = f"{base_url.rstrip('/')}/{encoded}"
        qs = params.to_query()
        return f"{url}?{qs}" if qs else url

    def _extract_models(self, payload: Any) -> List[str]:
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
        return models or self.fallback_models

class ImageGen(Generic[T], _ImageBase[T]):
    """Generic image generator (sync or async)."""
    def __init__(self, gen: T) -> None:
        self.gen = gen

    # ---------- generate ----------
    def generate(self, prompt: str, **kw: Any) -> Union[bytes, Any]:
        self.validate_prompt(prompt)
        model = ImageModel.from_string(kw.pop("model", DEFAULTS.IMAGE_MODEL))
        params = ImageParamsV2(model=model, **kw)
        url = self._make_url(self.gen.base_url, prompt, params)

        if isinstance(self.gen, AsyncGenerator):
            return self._agenerate(url)
        return self._sgenerate(url)

    def _sgenerate(self, url: str) -> bytes:
        resp = self.gen._make_request("GET", url)
        return resp.content

    async def _agenerate(self, url: str) -> bytes:
        async with await self.gen._amake_request("GET", url) as resp:
            return await resp.read()

    # ---------- generate_url ----------
    def generate_url(self, prompt: str, **kw: Any) -> str:
        self.validate_prompt(prompt)
        model = ImageModel.from_string(kw.pop("model", DEFAULTS.IMAGE_MODEL))
        params = ImageParamsV2(model=model, **kw)
        return self._make_url(self.gen.base_url, prompt, params)

    # ---------- save ----------
    def save(self, prompt: str, filename: str, **kw: Any) -> str:
        data = self.generate(prompt, **kw)
        if asyncio.iscoroutine(data):
            return asyncio.run_coroutine_threadsafe(self._asave(data, filename), asyncio.get_event_loop()).result()  # type: ignore
        with open(filename, "wb") as fh:
            fh.write(data)  # type: ignore
        return filename

    async def _asave(self, coro: Any, filename: str) -> str:
        data = await coro
        with open(filename, "wb") as fh:
            fh.write(data)
        return filename

    # ---------- models ----------
    def models(self) -> Union[List[str], Any]:
        if isinstance(self.gen, AsyncGenerator):
            return self._amodels()
        return self._smodels()

    def _smodels(self) -> List[str]:
        try:
            resp = self.gen._make_request("GET", ENDPOINTS.IMAGE_MODELS)
            payload = resp.json()
            models = self._extract_models(payload)
            ImageModel.update_known_values(models)
            return models
        except Exception as exc:
            print_warning(f"Failed to fetch image models: {exc}")
            return self.fallback_models

    async def _amodels(self) -> List[str]:
        try:
            async with await self.gen._amake_request("GET", ENDPOINTS.IMAGE_MODELS) as resp:
                payload = await resp.json()
                models = self._extract_models(payload)
                ImageModel.update_known_values(models)
                return models
        except Exception as exc:
            print_warning(f"Failed to fetch image models: {exc}")
            return self.fallback_models

# --------------------------------------------------------------------------- #
# Text – generic sync/async
# --------------------------------------------------------------------------- #

class _TextBase(Generic[T]):
    fallback_models = DEFAULT_TEXT_MODELS

    @staticmethod
    def validate_prompt(prompt: str) -> None:
        ParameterValidator.prompt_length(prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "prompt")

    @staticmethod
    def normalize_messages(
        prompt: str, system: Optional[str], messages: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
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
        # strip unsupported audio keys
        kw.pop("audio", None)
        kw.pop("modalities", None)
        model = TextModel.from_string(model or DEFAULTS.TEXT_MODEL)
        return ChatParamsV2(model=model, messages=messages, stream=stream, **kw)

    def _extract_text(self, payload: Dict[str, Any]) -> str:
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
        return models or self.fallback_models

class TextGen(Generic[T], _TextBase[T], StreamingMixin):
    def __init__(self, gen: T) -> None:
        self.gen = gen

    # ---------- generate ----------
    def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        **kw: Any,
    ) -> Union[str, Iterator[str], AsyncIterator[str]]:
        self.validate_prompt(prompt)
        msgs = self.normalize_messages(prompt, system, messages)
        return self.chat(messages=msgs, stream=stream, **kw)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        stream: bool = False,
        **kw: Any,
    ) -> Union[str, Iterator[str], AsyncIterator[str]]:
        params = self._make_params(messages, model=kw.pop("model", DEFAULTS.TEXT_MODEL), stream=stream, **kw)
        body = params.to_body()
        headers = {"Content-Type": "application/json"}

        if isinstance(self.gen, AsyncGenerator):
            return self._achat(body, headers, stream)
        return self._schat(body, headers, stream)

    def _schat(self, body: Dict[str, Any], headers: Dict[str, str], stream: bool) -> Union[str, Iterator[str]]:
        resp = self.gen._make_request("POST", ENDPOINTS.TEXT, json=body, headers=headers, stream=stream)
        if stream:
            return self.stream_sse(resp.iter_lines(decode_unicode=True))
        return self._extract_text(resp.json())

    async def _achat(self, body: Dict[str, Any], headers: Dict[str, str], stream: bool) -> Union[str, AsyncIterator[str]]:
        if stream:
            async def _inner():
                async with await self.gen._amake_request("POST", ENDPOINTS.TEXT, json=body, headers=headers) as resp:
                    async for chunk in self.astream_sse(resp.content):
                        yield chunk
            return _inner()
        async with await self.gen._amake_request("POST", ENDPOINTS.TEXT, json=body, headers=headers) as resp:
            payload = await resp.json()
            return self._extract_text(payload)

    # ---------- models ----------
    def models(self) -> Union[List[str], Any]:
        if isinstance(self.gen, AsyncGenerator):
            return self._amodels()
        return self._smodels()

    def _smodels(self) -> List[str]:
        try:
            resp = self.gen._make_request("GET", ENDPOINTS.TEXT_MODELS)
            payload = resp.json()
            models = self._extract_models(payload)
            TextModel.update_known_values(models)
            return models
        except Exception as exc:
            print_warning(f"Failed to fetch text models: {exc}")
            return self.fallback_models

    async def _amodels(self) -> List[str]:
        try:
            async with await self.gen._amake_request("GET", ENDPOINTS.TEXT_MODELS) as resp:
                payload = await resp.json()
                models = self._extract_models(payload)
                TextModel.update_known_values(models)
                return models
        except Exception as exc:
            print_warning(f"Failed to fetch text models: {exc}")
            return self.fallback_models

# --------------------------------------------------------------------------- #
# Audio – generic sync/async (no auth)
# --------------------------------------------------------------------------- #

class _AudioBase(Generic[T]):
    AUDIO_BASE_URL: Final = "https://text.pollinations.ai"
    VALID_VOICES: Final = ("alloy", "echo", "fable", "onyx", "nova", "shimmer")

    @staticmethod
    def validate_prompt(prompt: str) -> None:
        ParameterValidator.prompt_length(prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "audio prompt")

    def validate_voice(self, voice: str) -> None:
        if voice not in self.VALID_VOICES:
            raise BlossomError(
                message=f"Invalid voice: {voice}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Use one of: {', '.join(self.VALID_VOICES)}",
            )

    def _make_url(self, text: str, voice: str) -> str:
        encoded = quote(text)
        url = f"{self.AUDIO_BASE_URL}/{encoded}"
        return url

    def _params(self, voice: str) -> Dict[str, Any]:
        return {"model": "openai-audio", "voice": voice}

class AudioGen(Generic[T], _AudioBase[T]):
    def __init__(self, gen: T) -> None:
        self.gen = gen

    # ---------- generate ----------
    def generate(self, text: str, voice: str = "alloy") -> Union[bytes, Any]:
        self.validate_prompt(text)
        self.validate_voice(voice)
        url = self._make_url(text, voice)
        params = self._params(voice)

        if isinstance(self.gen, AsyncGenerator):
            return self._agenerate(url, params)
        return self._sgenerate(url, params)

    def _sgenerate(self, url: str, params: Dict[str, Any]) -> bytes:
        resp = self.gen._make_request("GET", url, params=params)
        return resp.content

    async def _agenerate(self, url: str, params: Dict[str, Any]) -> bytes:
        async with await self.gen._amake_request("GET", url, params=params) as resp:
            return await resp.read()

    # ---------- save ----------
    def save(self, text: str, filename: str, voice: str = "alloy") -> Union[str, Any]:
        data = self.generate(text, voice)
        if asyncio.iscoroutine(data):
            return asyncio.run_coroutine_threadsafe(self._asave(data, filename), asyncio.get_event_loop()).result()  # type: ignore
        with open(filename, "wb") as fh:
            fh.write(data)  # type: ignore
        return filename

    async def _asave(self, coro: Any, filename: str) -> str:
        data = await coro
        with open(filename, "wb") as fh:
            fh.write(data)
        return filename

# --------------------------------------------------------------------------- #
# Ready-made sync instances
# --------------------------------------------------------------------------- #

class ImageGenerator(ImageGen[SyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(SyncGenerator(ENDPOINTS.IMAGE, timeout, api_token))

class TextGenerator(TextGen[SyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(SyncGenerator(ENDPOINTS.BASE, timeout, api_token))

class AudioGenerator(AudioGen[SyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(SyncGenerator(_AudioBase.AUDIO_BASE_URL, timeout, api_token=None))

# --------------------------------------------------------------------------- #
# Ready-made async instances
# --------------------------------------------------------------------------- #

class AsyncImageGenerator(ImageGen[AsyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(AsyncGenerator(ENDPOINTS.IMAGE, timeout, api_token))

class AsyncTextGenerator(TextGen[AsyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(AsyncGenerator(ENDPOINTS.BASE, timeout, api_token))

class AsyncAudioGenerator(AudioGen[AsyncGenerator]):
    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        super().__init__(AsyncGenerator(_AudioBase.AUDIO_BASE_URL, timeout, api_token=None))