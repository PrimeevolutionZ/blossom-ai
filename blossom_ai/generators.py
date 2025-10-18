"""
Blossom AI - Generators (с поддержкой streaming)
"""

from typing import Optional, List, Dict, Any, Iterator, Union
import json

from .base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from .errors import BlossomError, ErrorType, print_warning
from .models import (
    ImageModel, TextModel, Voice,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, DEFAULT_VOICES
)


# ============================================================================
# STREAMING UTILITIES
# ============================================================================

class StreamChunk:
    """Представляет chunk из streaming ответа"""
    def __init__(self, content: str, done: bool = False):
        self.content = content
        self.done = done

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"StreamChunk(content={self.content!r}, done={self.done})"


def _parse_sse_line(line: str) -> Optional[dict]:
    """Парсит SSE строку"""
    if not line.strip():
        return None

    if line.startswith('data: '):
        data_str = line[6:].strip()
        if data_str == '[DONE]':
            return {'done': True}
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            return None
    return None


# ============================================================================
# IMAGE GENERATOR (без изменений)
# ============================================================================

class ImageGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI (Synchronous)"""

    MAX_PROMPT_LENGTH = 200

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://image.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {self.MAX_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

    def generate(
        self,
        prompt: str,
        model: str = "flux",
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False
    ) -> bytes:
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        params = {
            "model": self._validate_model(model),
            "width": width,
            "height": height,
        }

        if seed is not None:
            params["seed"] = seed
        if nologo:
            params["nologo"] = "true"
        if private:
            params["private"] = "true"
        if enhance:
            params["enhance"] = "true"
        if safe:
            params["safe"] = "true"

        response = self._make_request("GET", url, params=params)
        return response.content

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        image_data = self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    def models(self) -> list:
        if self._models_cache is None:
            models = self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


class AsyncImageGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI (Asynchronous)"""

    MAX_PROMPT_LENGTH = 200

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, "https://image.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {self.MAX_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

    async def generate(
        self,
        prompt: str,
        model: str = "flux",
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False
    ) -> bytes:
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        params = {
            "model": self._validate_model(model),
            "width": width,
            "height": height,
        }

        if seed is not None:
            params["seed"] = seed
        if nologo:
            params["nologo"] = "true"
        if private:
            params["private"] = "true"
        if enhance:
            params["enhance"] = "true"
        if safe:
            params["safe"] = "true"

        return await self._make_request("GET", url, params=params)

    async def save(self, prompt: str, filename: str, **kwargs) -> str:
        image_data = await self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    async def models(self) -> list:
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# TEXT GENERATOR (С ПОДДЕРЖКОЙ STREAMING)
# ============================================================================

class TextGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate text using Pollinations.AI (Synchronous) with streaming support"""

    MAX_PROMPT_LENGTH = 10000

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {self.MAX_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

    def generate(
        self,
        prompt: str,
        model: str = "openai",
        system: Optional[str] = None,
        seed: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False,
        private: bool = False,
        stream: bool = False
    ) -> Union[str, Iterator[str]]:
        """
        Generate text from a prompt

        Args:
            stream: If True, returns an iterator that yields text chunks in real-time

        Returns:
            str if stream=False, Iterator[str] if stream=True
        """
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(encoded_prompt)

        params = {"model": self._validate_model(model)}

        if system:
            params["system"] = system
        if seed is not None:
            params["seed"] = seed
        if temperature is not None:
            params["temperature"] = temperature
        if json_mode:
            params["json"] = "true"
        if private:
            params["private"] = "true"
        if stream:
            params["stream"] = "true"

        response = self._make_request("GET", url, params=params, stream=stream)

        if stream:
            return self._stream_response(response)
        else:
            return response.text

    def _stream_response(self, response) -> Iterator[str]:
        """
        Обрабатывает streaming ответ (SSE)
        Yields текстовые chunks по мере их получения
        """
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.strip():
                    continue

                parsed = _parse_sse_line(line)
                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                # Извлекаем content из OpenAI формата
                if 'choices' in parsed and len(parsed['choices']) > 0:
                    delta = parsed['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        yield content
        finally:
            response.close()

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai",
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ) -> Union[str, Iterator[str]]:
        """
        Chat completion using OpenAI-compatible endpoint

        Args:
            stream: If True, returns an iterator that yields text chunks

        Returns:
            str if stream=False, Iterator[str] if stream=True
        """
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "stream": stream
        }

        if temperature is not None and temperature != 1.0:
            print_warning(f"Temperature {temperature} not supported. Using default 1.0")
        body["temperature"] = 1.0

        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if private:
            body["private"] = private

        try:
            response = self._make_request(
                "POST",
                url,
                json=body,
                headers={"Content-Type": "application/json"},
                stream=stream
            )

            if stream:
                return self._stream_response(response)
            else:
                result = response.json()
                return result["choices"][0]["message"]["content"]

        except Exception:
            # Fallback to GET method (без streaming)
            user_msg = next((m["content"] for m in messages if m.get("role") == "user"), None)
            system_msg = next((m["content"] for m in messages if m.get("role") == "system"), None)

            if user_msg:
                return self.generate(
                    prompt=user_msg,
                    model=model,
                    system=system_msg,
                    json_mode=json_mode,
                    private=private,
                    stream=False  # Fallback без streaming
                )
            raise

    def models(self) -> List[str]:
        if self._models_cache is None:
            models = self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


class AsyncTextGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate text using Pollinations.AI (Asynchronous) with streaming support"""

    MAX_PROMPT_LENGTH = 10000

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {self.MAX_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

    async def generate(
        self,
        prompt: str,
        model: str = "openai",
        system: Optional[str] = None,
        seed: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False,
        private: bool = False,
        stream: bool = False
    ):
        """
        Generate text from a prompt

        Returns:
            str if stream=False
            AsyncIterator[str] if stream=True
        """
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(encoded_prompt)

        params = {"model": self._validate_model(model)}

        if system:
            params["system"] = system
        if seed is not None:
            params["seed"] = seed
        if temperature is not None:
            params["temperature"] = temperature
        if json_mode:
            params["json"] = "true"
        if private:
            params["private"] = "true"
        if stream:
            params["stream"] = "true"

        if stream:
            return self._stream_response(url, params)
        else:
            data = await self._make_request("GET", url, params=params)
            return data.decode('utf-8')

    async def _stream_response(self, url: str, params: dict):
        """
        Async generator для streaming ответа
        """
        session = await self._get_session()

        # Добавляем auth
        params = self._add_auth_params(params, 'GET')
        headers = self._get_auth_headers('GET')

        async with session.get(url, params=params, headers=headers) as response:
            if response.status >= 400:
                raise BlossomError(
                    message=f"HTTP {response.status}",
                    error_type=ErrorType.API
                )

            async for line in response.content:
                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue

                parsed = _parse_sse_line(line_str)
                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                if 'choices' in parsed and len(parsed['choices']) > 0:
                    delta = parsed['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        yield content

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai",
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ):
        """
        Chat completion

        Returns:
            str if stream=False
            AsyncIterator[str] if stream=True
        """
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "stream": stream
        }

        if temperature is not None and temperature != 1.0:
            print_warning(f"Temperature {temperature} not supported. Using default 1.0")
        body["temperature"] = 1.0

        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if private:
            body["private"] = private

        if stream:
            return self._stream_chat_response(url, body)
        else:
            try:
                data = await self._make_request(
                    "POST",
                    url,
                    json=body,
                    headers={"Content-Type": "application/json"}
                )
                result = json.loads(data.decode('utf-8'))
                return result["choices"][0]["message"]["content"]
            except Exception:
                # Fallback to GET
                user_msg = next((m["content"] for m in messages if m.get("role") == "user"), None)
                system_msg = next((m["content"] for m in messages if m.get("role") == "system"), None)

                if user_msg:
                    return await self.generate(
                        prompt=user_msg,
                        model=model,
                        system=system_msg,
                        json_mode=json_mode,
                        private=private,
                        stream=False
                    )
                raise

    async def _stream_chat_response(self, url: str, body: dict):
        """Async generator для streaming chat ответа"""
        session = await self._get_session()

        headers = {"Content-Type": "application/json"}
        headers.update(self._get_auth_headers('POST'))

        async with session.post(url, json=body, headers=headers) as response:
            if response.status >= 400:
                raise BlossomError(
                    message=f"HTTP {response.status}",
                    error_type=ErrorType.API
                )

            async for line in response.content:
                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue

                parsed = _parse_sse_line(line_str)
                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                if 'choices' in parsed and len(parsed['choices']) > 0:
                    delta = parsed['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        yield content

    async def models(self) -> List[str]:
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# AUDIO GENERATOR (без изменений)
# ============================================================================

class AudioGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate audio using Pollinations.AI (Synchronous)"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        pass

    def generate(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "openai-audio"
    ) -> bytes:
        text = text.rstrip('.!?;:,')
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)
        }

        response = self._make_request("GET", url, params=params)
        return response.content

    def save(self, text: str, filename: str, **kwargs) -> str:
        audio_data = self.generate(text, **kwargs)
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return str(filename)

    def voices(self) -> List[str]:
        if self._models_cache is None:
            voices = self._fetch_list("voices", self._fallback_models)
            self._update_known_models(voices)
        return self._models_cache or self._fallback_models


class AsyncAudioGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate audio using Pollinations.AI (Asynchronous)"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        pass

    async def generate(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "openai-audio"
    ) -> bytes:
        text = text.rstrip('.!?;:,')
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)
        }

        return await self._make_request("GET", url, params=params)

    async def save(self, text: str, filename: str, **kwargs) -> str:
        audio_data = await self.generate(text, **kwargs)
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return str(filename)

    async def voices(self) -> List[str]:
        if self._models_cache is None:
            voices = await self._fetch_list("voices", self._fallback_models)
            self._update_known_models(voices)
        return self._models_cache or self._fallback_models