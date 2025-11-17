"""
Blossom AI – Generators (v0.5.2)
V2 API only (enter.pollinations.ai)
"""

from __future__ import annotations

import json
from typing import (
    Any, AsyncIterator, Dict, Iterator, List, Optional, Union, cast
)
from urllib.parse import urlencode, quote

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
from blossom_ai.core.errors import print_warning, print_debug, BlossomError, ErrorType
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
    """Synchronous image generator with 520 error handling."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        SyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, self._fallback_models)

    def _validate_prompt(self, prompt: str) -> None:
        _ImageBase._validate_prompt(prompt)

    def generate(self, prompt: str, **kw: Any) -> bytes:
        """Generate image with automatic retry on 520 errors."""
        self._validate_prompt(prompt)
        params = ImageParamsV2(
            model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)),
            **kw
        )
        url = self._make_url(self.base_url, prompt, params)

        # Try with retry logic for 520 errors
        max_attempts = 3
        last_error = None

        for attempt in range(max_attempts):
            try:
                resp = self._make_request("GET", url)
                return resp.content
            except Exception as e:
                last_error = e
                # Check if it's a 520 error
                if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                    if e.response.status_code == 520 and attempt < max_attempts - 1:
                        print_warning(f"520 error on attempt {attempt + 1}, retrying...")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                raise

        raise last_error

    def generate_url(self, prompt: str, **kw: Any) -> str:
        self._validate_prompt(prompt)
        params = ImageParamsV2(
            model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)),
            **kw
        )
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
    """Asynchronous image generator with 520 error handling."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        AsyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, self._fallback_models)

    def _validate_prompt(self, prompt: str) -> None:
        _ImageBase._validate_prompt(prompt)

    async def generate(self, prompt: str, **kw: Any) -> bytes:
        """Generate image with automatic retry on 520 errors."""
        self._validate_prompt(prompt)
        params = ImageParamsV2(
            model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)),
            **kw
        )
        url = self._make_url(self.base_url, prompt, params)

        # Try with retry logic for 520 errors
        max_attempts = 3
        last_error = None

        for attempt in range(max_attempts):
            try:
                data = await self._make_request("GET", url)
                return cast(bytes, data)
            except Exception as e:
                last_error = e
                # Check if it's a 520 error (aiohttp)
                if hasattr(e, 'status') and e.status == 520 and attempt < max_attempts - 1:
                    print_warning(f"520 error on attempt {attempt + 1}, retrying...")
                    import asyncio
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        raise last_error

    async def generate_url(self, prompt: str, **kw: Any) -> str:
        self._validate_prompt(prompt)
        params = ImageParamsV2(
            model=self._validate_model(kw.pop("model", DEFAULTS.IMAGE_MODEL)),
            **kw
        )
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
        """Build ChatParamsV2 with REMOVED audio/modalities (unsupported by API)."""

        # CRITICAL FIX: Remove unsupported parameters
        removed_audio = kw.pop("audio", None)
        removed_modalities = kw.pop("modalities", None)

        if removed_audio or removed_modalities:
            print_warning(
                "⚠️  WARNING: 'audio' and 'modalities' parameters are NOT supported by Pollinations API!\n"
                "   For audio generation, use the separate audio endpoint:\n"
                "   ai.audio.generate(text, voice='alloy')\n"
                "   These parameters have been removed from your request."
            )

        # Validate model is set
        if not model:
            model = DEFAULTS.TEXT_MODEL

        # Validate model
        validated_model = self._validate_model(model)

        # Build params - ALWAYS include model
        params = ChatParamsV2(
            model=validated_model,
            messages=messages,
            stream=stream,
            **kw,
        )

        return params

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
    """Synchronous text generator with vision support (NO AUDIO IN CHAT)."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        SyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, self._fallback_models)
        self._sse = SSEParser()

    def _validate_prompt(self, prompt: str) -> None:
        _TextBase._validate_prompt(prompt)

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
        params = self._make_params(
            messages,
            model=kw.pop("model", DEFAULTS.TEXT_MODEL),
            stream=stream,
            **kw
        )

        body = params.to_body()



        # 🔍 DEBUG OUTPUT ( не включать кроме как для дебага / ONLY DEBUG)
        #print(f"\n🔍 DEBUG REQUEST BODY:")
        #print(json.dumps(body, indent=2, ensure_ascii=False))
        #print(f"🔍 Body keys: {list(body.keys())}\n")

        headers = {"Content-Type": "application/json"}
        resp = self._make_request(
            "POST",
            ENDPOINTS.TEXT,
            json=body,
            headers=headers,
            stream=stream,
        )

        if stream:
            return self._stream_sse_chunked(resp, self._sse)
        return self._extract_text(resp.json())

    def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            resp = self._make_request("GET", ENDPOINTS.TEXT_MODELS)
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
    """Asynchronous text generator with vision support (NO AUDIO IN CHAT)."""

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        AsyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, self._fallback_models)
        self._sse = SSEParser()

    def _validate_prompt(self, prompt: str) -> None:
        _TextBase._validate_prompt(prompt)

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
            async def _stream_wrapper():
                async for chunk in self.chat(messages=msgs, stream=True, **kw):
                    yield chunk
            return _stream_wrapper()
        return await self.chat_text(messages=msgs, stream=False, **kw)

    async def chat_text(
        self,
        messages: List[Dict[str, Any]],
        *,
        stream: bool = False,
        **kw: Any,
    ) -> str:
        params = self._make_params(
            messages,
            model=kw.pop("model", DEFAULTS.TEXT_MODEL),
            stream=False,
            **kw
        )

        body = params.to_body()

        # 🔍 DEBUG OUTPUT async ( не включать кроме как для дебага/ ONLY DEBUG)
        #print(f"\n🔍 ASYNC DEBUG REQUEST BODY:")
        #print(json.dumps(body, indent=2, ensure_ascii=False))
        #print(f"🔍 Body keys: {list(body.keys())}\n")

        data = await self._make_request(
            "POST",
            ENDPOINTS.TEXT,
            json=body,
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
        params = self._make_params(
            messages,
            model=kw.pop("model", DEFAULTS.TEXT_MODEL),
            stream=True,
            **kw
        )

        body = params.to_body()

        # 🔍 DEBUG OUTPUT для streaming
        print(f"\n🔍 ASYNC STREAM DEBUG REQUEST BODY:")
        print(json.dumps(body, indent=2, ensure_ascii=False))
        print(f"🔍 Body keys: {list(body.keys())}\n")

        resp = await self._make_request(
            "POST",
            ENDPOINTS.TEXT,
            json=body,
            headers={"Content-Type": "application/json"},
            stream=True,
        )
        async for chunk in self._stream_sse_chunked(resp, self._sse):
            yield chunk

    async def models(self) -> List[str]:
        if self._models_cache:
            return self._models_cache
        try:
            data = await self._make_request("GET", ENDPOINTS.TEXT_MODELS)
            self._models_cache = self._extract_models(json.loads(data.decode()))
            self._update_known_models(self._models_cache)
        except Exception as exc:
            print_warning(f"Failed to fetch text models: {exc}")
            self._models_cache = self._fallback_models
        return self._models_cache


# --------------------------------------------------------------------------- #
# NEW: Audio Generator (Separate TTS endpoint) - NO AUTH REQUIRED
# --------------------------------------------------------------------------- #
class AudioGenerator(SyncGenerator):
    """
    Synchronous audio (TTS) generator using Pollinations text.pollinations.ai endpoint.
    Note: This endpoint does NOT require authentication (works without API key).
    """

    AUDIO_BASE_URL = "https://text.pollinations.ai"
    VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        # Audio endpoint doesn't need auth, but we keep the parameter for consistency
        super().__init__(self.AUDIO_BASE_URL, timeout, api_token=None)  # Force None

    def _validate_prompt(self, prompt: str) -> None:
        """Audio prompts use same limits as text."""
        ParameterValidator.prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "audio prompt"
        )

    def _validate_voice(self, voice: str) -> None:
        """Validate voice parameter."""
        if voice not in self.VALID_VOICES:
            raise BlossomError(
                message=f"Invalid voice: {voice}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Use one of: {', '.join(self.VALID_VOICES)}"
            )

    def generate(self, text: str, voice: str = "alloy") -> bytes:
        """
        Generate MP3 audio from text using Pollinations TTS.
        Note: This endpoint does NOT require authentication.

        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)

        Returns:
            MP3 audio data as bytes
        """
        self._validate_prompt(text)
        self._validate_voice(voice)

        # Build URL: https://text.pollinations.ai/{text}?model=openai-audio&voice={voice}
        url = f"{self.base_url}/{quote(text)}"
        params = {
            "model": "openai-audio",
            "voice": voice
        }

        print_debug(f"Generating audio: voice={voice}, text_len={len(text)}")
        resp = self._make_request("GET", url, params=params)
        return resp.content

    def save(self, text: str, filename: str, voice: str = "alloy") -> str:
        """
        Generate and save audio to file.

        Args:
            text: Text to convert to speech
            filename: Output filename (will be MP3)
            voice: Voice to use

        Returns:
            Path to saved file
        """
        audio_data = self.generate(text, voice)
        with open(filename, "wb") as f:
            f.write(audio_data)
        print_debug(f"Saved audio to {filename} ({len(audio_data)} bytes)")
        return filename


class AsyncAudioGenerator(AsyncGenerator):
    """
    Asynchronous audio (TTS) generator using Pollinations text.pollinations.ai endpoint.
    Note: This endpoint does NOT require authentication.
    """

    AUDIO_BASE_URL = "https://text.pollinations.ai"
    VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def __init__(
        self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None
    ) -> None:
        # Audio endpoint doesn't need auth
        super().__init__(self.AUDIO_BASE_URL, timeout, api_token=None)  # Force None

    def _validate_prompt(self, prompt: str) -> None:
        ParameterValidator.prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "audio prompt"
        )

    def _validate_voice(self, voice: str) -> None:
        if voice not in self.VALID_VOICES:
            raise BlossomError(
                message=f"Invalid voice: {voice}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Use one of: {', '.join(self.VALID_VOICES)}"
            )

    async def generate(self, text: str, voice: str = "alloy") -> bytes:
        """Generate MP3 audio from text (async). No authentication required."""
        self._validate_prompt(text)
        self._validate_voice(voice)

        url = f"{self.base_url}/{quote(text)}"
        params = {
            "model": "openai-audio",
            "voice": voice
        }

        print_debug(f"Generating audio (async): voice={voice}, text_len={len(text)}")
        data = await self._make_request("GET", url, params=params)
        return cast(bytes, data)

    async def save(self, text: str, filename: str, voice: str = "alloy") -> str:
        """Generate and save audio to file (async)."""
        audio_data = await self.generate(text, voice)
        with open(filename, "wb") as f:
            f.write(audio_data)
        print_debug(f"Saved audio to {filename} ({len(audio_data)} bytes)")
        return filename