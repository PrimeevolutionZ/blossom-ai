"""
Blossom AI - V2 Generators (enter.pollinations.ai API)
Support for new API with OpenAI-compatible endpoints
"""

from typing import Optional, List, Dict, Any, Iterator, Union, AsyncIterator
import json

from blossom_ai.generators.base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from blossom_ai.core.config import ENDPOINTS, LIMITS, DEFAULTS
from blossom_ai.core.errors import BlossomError, ErrorType, StreamError, print_warning, print_debug
from blossom_ai.core.models import (
    ImageModel, TextModel, Voice,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, DEFAULT_VOICES
)


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
# V2 IMAGE GENERATOR
# ============================================================================

class ImageGeneratorV2(SyncGenerator, ModelAwareGenerator):
    """Generate images using V2 API (enter.pollinations.ai)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.V2_IMAGE, timeout, api_token)
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
        seed: int = 42,
        enhance: bool = False,
        negative_prompt: str = "worst quality, blurry",
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = "medium",
        image: Optional[str] = None,
        transparent: bool = False,
        guidance_scale: Optional[float] = None
    ) -> bytes:
        """Generate image using V2 API"""
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        params = {
            "model": self._validate_model(model),
            "width": width,
            "height": height,
            "seed": seed,
            "enhance": str(enhance).lower(),
            "negative_prompt": negative_prompt,
            "private": str(private).lower(),
            "nologo": str(nologo).lower(),
            "nofeed": str(nofeed).lower(),
            "safe": str(safe).lower(),
            "quality": quality,
            "transparent": str(transparent).lower(),
        }

        if image:
            params["image"] = image
        if guidance_scale is not None:
            params["guidance_scale"] = guidance_scale

        # DON'T add token to params for V2 - it goes in header via _make_request
        response = self._make_request("GET", url, params=params)
        return response.content

    def models(self) -> List[str]:
        """Get available image models from V2 API"""
        if self._models_cache is None:
            try:
                # Use absolute URL directly, bypass _build_url
                response = self._make_request("GET", ENDPOINTS.V2_IMAGE_MODELS)
                data = response.json()

                models = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            models.append(item)
                        elif isinstance(item, dict):
                            name = item.get('name') or item.get('id')
                            if name:
                                models.append(name)

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 image models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


class AsyncImageGeneratorV2(AsyncGenerator, ModelAwareGenerator):
    """Async image generator for V2 API"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.V2_IMAGE, timeout, api_token)
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
        seed: int = 42,
        enhance: bool = False,
        negative_prompt: str = "worst quality, blurry",
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = "medium",
        image: Optional[str] = None,
        transparent: bool = False,
        guidance_scale: Optional[float] = None
    ) -> bytes:
        """Generate image using V2 API (async)"""
        self._validate_prompt(prompt)
        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        params = {
            "model": self._validate_model(model),
            "width": width,
            "height": height,
            "seed": seed,
            "enhance": str(enhance).lower(),
            "negative_prompt": negative_prompt,
            "private": str(private).lower(),
            "nologo": str(nologo).lower(),
            "nofeed": str(nofeed).lower(),
            "safe": str(safe).lower(),
            "quality": quality,
            "transparent": str(transparent).lower(),
        }

        if image:
            params["image"] = image
        if guidance_scale is not None:
            params["guidance_scale"] = guidance_scale

        return await self._make_request("GET", url, params=params)

    async def models(self) -> List[str]:
        """Get available image models from V2 API (async)"""
        if self._models_cache is None:
            try:
                data = await self._make_request("GET", ENDPOINTS.V2_IMAGE_MODELS)
                parsed = json.loads(data.decode('utf-8'))

                models = []
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, str):
                            models.append(item)
                        elif isinstance(item, dict):
                            name = item.get('name') or item.get('id')
                            if name:
                                models.append(name)

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 image models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


# ============================================================================
# V2 TEXT GENERATOR
# ============================================================================

class TextGeneratorV2(SyncGenerator, ModelAwareGenerator):
    """Generate text using V2 API (OpenAI-compatible)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.V2_OPENAI, timeout, api_token)
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
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """Generate text using V2 OpenAI-compatible endpoint"""
        self._validate_prompt(prompt)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        return self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            json_mode=json_mode,
            tools=tools,
            **kwargs
        )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        top_p: float = 1.0,
        n: int = 1,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """Chat using V2 OpenAI-compatible API"""
        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }

        # Only add optional parameters if they differ from defaults
        if n != 1:
            body["n"] = n
        if top_p != 1.0:
            body["top_p"] = top_p
        if frequency_penalty != 0:
            body["frequency_penalty"] = frequency_penalty
        if presence_penalty != 0:
            body["presence_penalty"] = presence_penalty
        if max_tokens:
            body["max_tokens"] = max_tokens

        if json_mode:
            body["response_format"] = {"type": "json_object"}

        if tools:
            body["tools"] = tools
            if tool_choice:
                body["tool_choice"] = tool_choice

        # Add any additional parameters
        body.update(kwargs)

        response = self._make_request(
            "POST",
            self.base_url,
            json=body,
            headers={"Content-Type": "application/json"},
            stream=stream
        )

        if stream:
            return self._stream_response(response)
        else:
            result = response.json()
            return result["choices"][0]["message"]["content"]

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

    def models(self) -> List[str]:
        """Get available text models from V2 API"""
        if self._models_cache is None:
            try:
                response = self._make_request("GET", ENDPOINTS.V2_TEXT_MODELS)
                data = response.json()

                models = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name')
                            if name:
                                models.append(name)
                                # Also add aliases
                                if 'aliases' in item:
                                    models.extend(item['aliases'])

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


class AsyncTextGeneratorV2(AsyncGenerator, ModelAwareGenerator):
    """Async text generator for V2 API"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.V2_OPENAI, timeout, api_token)
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
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """Generate text using V2 API (async)"""
        self._validate_prompt(prompt)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        return await self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            json_mode=json_mode,
            tools=tools,
            **kwargs
        )

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        top_p: float = 1.0,
        n: int = 1,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """Chat using V2 API (async)"""
        body = {
            "model": self._validate_model(model),
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }

        if n != 1:
            body["n"] = n
        if top_p != 1.0:
            body["top_p"] = top_p
        if frequency_penalty != 0:
            body["frequency_penalty"] = frequency_penalty
        if presence_penalty != 0:
            body["presence_penalty"] = presence_penalty
        if max_tokens:
            body["max_tokens"] = max_tokens

        if json_mode:
            body["response_format"] = {"type": "json_object"}

        if tools:
            body["tools"] = tools
            if tool_choice:
                body["tool_choice"] = tool_choice

        body.update(kwargs)

        if stream:
            return self._stream_response(body)
        else:
            data = await self._make_request(
                "POST",
                self.base_url,
                json=body,
                headers={"Content-Type": "application/json"}
            )
            result = json.loads(data.decode('utf-8'))
            return result["choices"][0]["message"]["content"]

    async def _stream_response(self, body: dict) -> AsyncIterator[str]:
        """Async streaming response"""
        import asyncio

        response = None
        try:
            response = await self._make_request(
                "POST",
                self.base_url,
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
                message=f"Error during async streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and not response.closed:
                await response.close()

    async def models(self) -> List[str]:
        """Get available text models from V2 API (async)"""
        if self._models_cache is None:
            try:
                data = await self._make_request("GET", ENDPOINTS.V2_TEXT_MODELS)
                parsed = json.loads(data.decode('utf-8'))

                models = []
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict):
                            name = item.get('name')
                            if name:
                                models.append(name)
                                if 'aliases' in item:
                                    models.extend(item['aliases'])

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache