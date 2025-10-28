"""
Blossom AI - Generators (Refactored)
Clean implementation using centralized config and improved error handling
"""

from typing import Optional, List, Dict, Any, Iterator, Union, AsyncIterator
from urllib.parse import urlencode
import json
import asyncio

from blossom_ai.generators.base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from blossom_ai.core.config import ENDPOINTS, LIMITS, DEFAULTS
from blossom_ai.core.errors import BlossomError, ErrorType, StreamError, print_warning, print_debug
from blossom_ai.core.models import (
    ImageModel, TextModel, Voice,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, DEFAULT_VOICES
)


# ============================================================================
# STREAMING UTILITIES
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


def _parse_sse_line(line: str) -> Optional[dict]:
    """Parse SSE line with error handling"""
    if not line.strip():
        return None

    if line.startswith('data: '):
        data_str = line[6:].strip()
        if data_str == '[DONE]':
            return {'done': True}
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as e:
            print_debug(f"Invalid SSE JSON: {data_str[:100]} | Error: {e}")
            return None
    return None


# ============================================================================
# IMAGE GENERATOR
# ============================================================================

class ImageGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI (Synchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > LIMITS.MAX_IMAGE_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {LIMITS.MAX_IMAGE_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
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

        Example:
            >>> gen = ImageGenerator()
            >>> url = gen.generate_url("a beautiful sunset", seed=42, nologo=True)
            >>> print(url)
            https://image.pollinations.ai/prompt/a%20beautiful%20sunset?model=flux&...

        Security Note:
            API tokens are NEVER included in URLs for security reasons.
            URLs can be safely shared publicly. If you need authenticated features,
            use generate() or save() methods instead.
        """
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
        if referrer:
            params["referrer"] = referrer

        # Security: NEVER include tokens in URLs
        query_string = urlencode(params)
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
    """Generate images using Pollinations.AI (Asynchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.IMAGE, timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > LIMITS.MAX_IMAGE_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {LIMITS.MAX_IMAGE_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
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
        if referrer:
            params["referrer"] = referrer

        query_string = urlencode(params)
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
# TEXT GENERATOR
# ============================================================================

class TextGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate text using Pollinations.AI (Synchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.TEXT, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > LIMITS.MAX_TEXT_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {LIMITS.MAX_TEXT_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
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
        """Process streaming response (SSE)"""
        try:
            for line in self._stream_with_timeout(response):
                if not line or not line.strip():
                    continue

                parsed = _parse_sse_line(line)
                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                # Extract content from OpenAI format
                if 'choices' in parsed and len(parsed['choices']) > 0:
                    delta = parsed['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        yield content
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )

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
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "stream": stream
        }

        if temperature is not None and temperature != DEFAULTS.TEMPERATURE:
            print_warning(f"Temperature {temperature} may not be supported. Using default.")
        body["temperature"] = DEFAULTS.TEMPERATURE

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


class AsyncTextGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate text using Pollinations.AI (Asynchronous)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.TEXT, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        if len(prompt) > LIMITS.MAX_TEXT_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum length of {LIMITS.MAX_TEXT_PROMPT_LENGTH} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
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

    async def _stream_response(self, url: str, params: dict) -> AsyncIterator[str]:
        """Async generator for streaming response"""
        response = None
        try:
            response = await self._make_request("GET", url, params=params, stream=True)

            last_data_time = asyncio.get_event_loop().time()

            async for line in response.content:
                current_time = asyncio.get_event_loop().time()

                if current_time - last_data_time > LIMITS.STREAM_CHUNK_TIMEOUT:
                    raise StreamError(
                        message=f"Stream timeout: no data for {LIMITS.STREAM_CHUNK_TIMEOUT}s",
                        suggestion="Check connection or increase timeout"
                    )

                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue

                last_data_time = current_time
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

        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during async streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and not response.closed:
                await response.close()

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
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "stream": stream
        }

        if temperature is not None and temperature != DEFAULTS.TEMPERATURE:
            print_warning(f"Temperature {temperature} may not be supported. Using default.")
        body["temperature"] = DEFAULTS.TEMPERATURE

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

    async def _stream_chat_response(self, url: str, body: dict) -> AsyncIterator[str]:
        """Async generator for streaming chat response"""
        response = None
        try:
            response = await self._make_request(
                "POST",
                url,
                json=body,
                headers={"Content-Type": "application/json"},
                stream=True
            )

            last_data_time = asyncio.get_event_loop().time()

            async for line in response.content:
                current_time = asyncio.get_event_loop().time()

                if current_time - last_data_time > LIMITS.STREAM_CHUNK_TIMEOUT:
                    raise StreamError(
                        message=f"Stream timeout: no data for {LIMITS.STREAM_CHUNK_TIMEOUT}s",
                        suggestion="Check connection or increase timeout"
                    )

                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue

                last_data_time = current_time
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

        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during async chat streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and not response.closed:
                await response.close()

    async def models(self) -> List[str]:
        """Get list of available text models (async)"""
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# AUDIO GENERATOR
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
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)
        }

        response = self._make_request("GET", url, params=params)
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
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)
        }

        return await self._make_request("GET", url, params=params)

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