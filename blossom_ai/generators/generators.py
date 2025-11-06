"""
Blossom AI - Generators V1 (Refactored)
Clean implementation with separation of concerns
"""

from typing import Optional, List, Dict, Any, Iterator, Union, AsyncIterator
from urllib.parse import urlencode
import json

from blossom_ai.generators.base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from blossom_ai.generators.streaming_mixin import (
    SyncStreamingMixin, AsyncStreamingMixin, SSEParser
)
from blossom_ai.generators.parameter_builder import (
    ImageParams, TextParams, ChatParams, AudioParams, ParameterValidator
)
from blossom_ai.core.config import ENDPOINTS, LIMITS, DEFAULTS
from blossom_ai.core.errors import print_warning
from blossom_ai.core.models import (
    ImageModel, TextModel, Voice,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, DEFAULT_VOICES
)


# ============================================================================
# IMAGE GENERATOR (V1)
# ============================================================================

class ImageGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI V1 API (Synchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt length"""
        ParameterValidator.validate_prompt_length(
            prompt, LIMITS.MAX_IMAGE_PROMPT_LENGTH, "prompt"
        )

    def generate(
        self,
        prompt: str,
        model: str = DEFAULTS.IMAGE_MODEL,
        width: int = DEFAULTS.IMAGE_WIDTH,
        height: int = DEFAULTS.IMAGE_HEIGHT,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False
    ) -> bytes:
        """
        Generate an image and return raw bytes

        Args:
            prompt: Text description of the image
            model: Model to use for generation (default: flux)
            width: Image width in pixels (default: 1024)
            height: Image height in pixels (default: 1024)
            seed: Random seed for reproducibility
            nologo: Remove Pollinations watermark
            private: Make generation private
            enhance: Enhance prompt automatically
            safe: Enable safety filter

        Returns:
            bytes: Image data

        Example:
            >>> gen = ImageGenerator()
            >>> img_data = gen.generate("a beautiful sunset", seed=42)
            >>> with open("sunset.png", "wb") as f:
            ...     f.write(img_data)
        """
        self._validate_prompt(prompt)

        # Build parameters using parameter builder
        params = ImageParams(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance,
            safe=safe
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        response = self._make_request("GET", url, params=params.to_dict())
        return response.content

    def generate_url(
        self,
        prompt: str,
        model: str = DEFAULTS.IMAGE_MODEL,
        width: int = DEFAULTS.IMAGE_WIDTH,
        height: int = DEFAULTS.IMAGE_HEIGHT,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        referrer: Optional[str] = None
    ) -> str:
        """
        Generate image URL without downloading the image

        Args:
            prompt: Text description of the image
            model: Model to use for generation
            width: Image width in pixels
            height: Image height in pixels
            seed: Random seed for reproducibility
            nologo: Remove Pollinations watermark
            private: Make generation private
            enhance: Enhance prompt automatically
            safe: Enable safety filter
            referrer: Optional referrer parameter

        Returns:
            str: Full URL of the generated image

        Security Note:
            API tokens are NEVER included in URLs for security reasons.
            URLs can be safely shared publicly.
        """
        self._validate_prompt(prompt)

        # Build parameters
        params = ImageParams(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance,
            safe=safe,
            referrer=referrer
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        # Security: NEVER include tokens in URLs
        query_string = urlencode(params.to_dict())
        return f"{url}?{query_string}"

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        """
        Generate and save image to file

        Args:
            prompt: Text description
            filename: Path where to save the image
            **kwargs: Additional parameters for generate()

        Returns:
            str: Path to saved file
        """
        image_data = self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    def models(self) -> List[str]:
        """Get list of available image models"""
        if self._models_cache is None:
            models = self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


class AsyncImageGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI V1 API (Asynchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt length"""
        ParameterValidator.validate_prompt_length(
            prompt, LIMITS.MAX_IMAGE_PROMPT_LENGTH, "prompt"
        )

    async def generate(
        self,
        prompt: str,
        model: str = DEFAULTS.IMAGE_MODEL,
        width: int = DEFAULTS.IMAGE_WIDTH,
        height: int = DEFAULTS.IMAGE_HEIGHT,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False
    ) -> bytes:
        """Generate an image asynchronously"""
        self._validate_prompt(prompt)

        params = ImageParams(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance,
            safe=safe
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        return await self._make_request("GET", url, params=params.to_dict())

    async def generate_url(
        self,
        prompt: str,
        model: str = DEFAULTS.IMAGE_MODEL,
        width: int = DEFAULTS.IMAGE_WIDTH,
        height: int = DEFAULTS.IMAGE_HEIGHT,
        seed: Optional[int] = None,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        referrer: Optional[str] = None
    ) -> str:
        """Generate image URL without downloading (async version)"""
        self._validate_prompt(prompt)

        params = ImageParams(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance,
            safe=safe,
            referrer=referrer
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(f"prompt/{encoded_prompt}")

        query_string = urlencode(params.to_dict())
        return f"{url}?{query_string}"

    async def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file (async)"""
        image_data = await self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    async def models(self) -> List[str]:
        """Get list of available image models (async)"""
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# TEXT GENERATOR (V1)
# ============================================================================

class TextGenerator(SyncGenerator, SyncStreamingMixin, ModelAwareGenerator):
    """Generate text using Pollinations.AI V1 API (Synchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.TEXT, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)
        self._sse_parser = SSEParser()

    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt length"""
        ParameterValidator.validate_prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "prompt"
        )

    def generate(
        self,
        prompt: str,
        model: str = DEFAULTS.TEXT_MODEL,
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
            prompt: Input text prompt
            model: Model to use (default: openai)
            system: System prompt
            seed: Random seed
            temperature: Temperature for sampling
            json_mode: Enable JSON output mode
            private: Make generation private
            stream: Enable streaming (yields text chunks)

        Returns:
            str if stream=False, Iterator[str] if stream=True

        Example:
            >>> gen = TextGenerator()
            >>> # Non-streaming
            >>> result = gen.generate("Write a poem about AI")
            >>> print(result)

            >>> # Streaming
            >>> for chunk in gen.generate("Tell me a story", stream=True):
            ...     print(chunk, end="", flush=True)
        """
        self._validate_prompt(prompt)

        params = TextParams(
            model=self._validate_model(model),
            system=system,
            seed=seed,
            temperature=temperature,
            json_mode=json_mode,
            private=private,
            stream=stream
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(encoded_prompt)

        response = self._make_request(
            "GET", url, params=params.to_dict(), stream=stream
        )

        if stream:
            return self._stream_sse_response(response, self._sse_parser)
        else:
            return response.text

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ) -> Union[str, Iterator[str]]:
        """
        Chat completion using OpenAI-compatible endpoint

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use
            temperature: Temperature (note: may not be supported by all models)
            stream: Enable streaming
            json_mode: Enable JSON output
            private: Make generation private

        Returns:
            str if stream=False, Iterator[str] if stream=True

        Example:
            >>> gen = TextGenerator()
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant"},
            ...     {"role": "user", "content": "Hello!"}
            ... ]
            >>> response = gen.chat(messages)
            >>> print(response)
        """
        if temperature is not None and temperature != DEFAULTS.TEMPERATURE:
            print_warning(f"Temperature {temperature} may not be supported. Using default.")

        params = ChatParams(
            model=self._validate_model(model),
            messages=messages,
            temperature=DEFAULTS.TEMPERATURE,
            stream=stream,
            json_mode=json_mode,
            private=private
        )

        url = self._build_url("openai")

        try:
            response = self._make_request(
                "POST",
                url,
                json=params.to_body(),
                headers={"Content-Type": "application/json"},
                stream=stream
            )

            if stream:
                return self._stream_sse_response(response, self._sse_parser)
            else:
                result = response.json()
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            # Fallback to GET method
            print_warning(f"Chat endpoint failed, falling back to GET method: {e}")
            user_msg = next((m["content"] for m in messages if m.get("role") == "user"), None)
            system_msg = next((m["content"] for m in messages if m.get("role") == "system"), None)

            if user_msg:
                return self.generate(
                    prompt=user_msg,
                    model=model,
                    system=system_msg,
                    json_mode=json_mode,
                    private=private,
                    stream=False
                )
            raise

    def models(self) -> List[str]:
        """Get list of available text models"""
        if self._models_cache is None:
            models = self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


class AsyncTextGenerator(AsyncGenerator, AsyncStreamingMixin, ModelAwareGenerator):
    """Generate text using Pollinations.AI V1 API (Asynchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.TEXT, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)
        self._sse_parser = SSEParser()

    def _validate_prompt(self, prompt: str) -> None:
        """Validate prompt length"""
        ParameterValidator.validate_prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "prompt"
        )

    async def generate(
        self,
        prompt: str,
        model: str = DEFAULTS.TEXT_MODEL,
        system: Optional[str] = None,
        seed: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False,
        private: bool = False,
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        """Generate text from a prompt (async)"""
        self._validate_prompt(prompt)

        params = TextParams(
            model=self._validate_model(model),
            system=system,
            seed=seed,
            temperature=temperature,
            json_mode=json_mode,
            private=private,
            stream=stream
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = self._build_url(encoded_prompt)

        if stream:
            response = await self._make_request(
                "GET", url, params=params.to_dict(), stream=True
            )
            return self._stream_sse_response(response, self._sse_parser)
        else:
            data = await self._make_request("GET", url, params=params.to_dict())
            return data.decode('utf-8')

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        """Chat completion (async)"""
        if temperature is not None and temperature != DEFAULTS.TEMPERATURE:
            print_warning(f"Temperature {temperature} may not be supported. Using default.")

        params = ChatParams(
            model=self._validate_model(model),
            messages=messages,
            temperature=DEFAULTS.TEMPERATURE,
            stream=stream,
            json_mode=json_mode,
            private=private
        )

        url = self._build_url("openai")

        try:
            if stream:
                response = await self._make_request(
                    "POST",
                    url,
                    json=params.to_body(),
                    headers={"Content-Type": "application/json"},
                    stream=True
                )
                return self._stream_sse_response(response, self._sse_parser)
            else:
                data = await self._make_request(
                    "POST",
                    url,
                    json=params.to_body(),
                    headers={"Content-Type": "application/json"}
                )
                result = json.loads(data.decode('utf-8'))
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            print_warning(f"Chat endpoint failed, falling back to GET method: {e}")
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

    async def models(self) -> List[str]:
        """Get list of available text models (async)"""
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# AUDIO GENERATOR (V1)
# ============================================================================

class AudioGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate audio using Pollinations.AI (Synchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.AUDIO, timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        pass  # No specific validation for audio

    def generate(
        self,
        text: str,
        voice: str = DEFAULTS.AUDIO_VOICE,
        model: str = DEFAULTS.AUDIO_MODEL
    ) -> bytes:
        """
        Generate audio from text

        Args:
            text: Text to convert to speech
            voice: Voice to use (default: alloy)
            model: Model to use (default: openai-audio)

        Returns:
            bytes: Audio data

        Example:
            >>> gen = AudioGenerator()
            >>> audio = gen.generate("Hello world", voice="alloy")
            >>> with open("hello.mp3", "wb") as f:
            ...     f.write(audio)
        """
        text = text.rstrip('.!?;:,')

        params = AudioParams(
            voice=self._validate_model(voice),
            model=model
        )

        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        response = self._make_request("GET", url, params=params.to_dict())
        return response.content

    def save(self, text: str, filename: str, **kwargs) -> str:
        """Generate and save audio to file"""
        audio_data = self.generate(text, **kwargs)
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return str(filename)

    def voices(self) -> List[str]:
        """Get list of available voices"""
        if self._models_cache is None:
            voices = self._fetch_list("voices", self._fallback_models)
            self._update_known_models(voices)
        return self._models_cache or self._fallback_models


class AsyncAudioGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate audio using Pollinations.AI (Asynchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.AUDIO, timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        pass  # No specific validation for audio

    async def generate(
        self,
        text: str,
        voice: str = DEFAULTS.AUDIO_VOICE,
        model: str = DEFAULTS.AUDIO_MODEL
    ) -> bytes:
        """Generate audio from text (async)"""
        text = text.rstrip('.!?;:,')

        params = AudioParams(
            voice=self._validate_model(voice),
            model=model
        )

        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        return await self._make_request("GET", url, params=params.to_dict())

    async def save(self, text: str, filename: str, **kwargs) -> str:
        """Generate and save audio to file (async)"""
        audio_data = await self.generate(text, **kwargs)
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return str(filename)

    async def voices(self) -> List[str]:
        """Get list of available voices (async)"""
        if self._models_cache is None:
            voices = await self._fetch_list("voices", self._fallback_models)
            self._update_known_models(voices)
        return self._models_cache or self._fallback_models


# ============================================================================
# STREAM CHUNK (для обратной совместимости)
# ============================================================================

class StreamChunk:
    """Represents chunk from streaming response"""
    def __init__(self, content: str, done: bool = False, error: Optional[str] = None):
        self.content = content
        self.done = done
        self.error = error

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"StreamChunk(content={self.content!r}, done={self.done}, error={self.error!r})"