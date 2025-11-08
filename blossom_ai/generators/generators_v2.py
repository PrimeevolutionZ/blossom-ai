"""
Blossom AI - V2 Generators (Fixed with generate_url)
enter.pollinations.ai API with clean architecture
"""

from typing import Optional, List, Dict, Any, Iterator, Union, AsyncIterator
from urllib.parse import urlencode
import json

from blossom_ai.generators.base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from blossom_ai.generators.streaming_mixin import (
    SyncStreamingMixin, AsyncStreamingMixin, SSEParser
)
from blossom_ai.generators.parameter_builder import (
    ImageParamsV2, ChatParamsV2, ParameterValidator
)
from blossom_ai.core.config import ENDPOINTS, LIMITS, DEFAULTS
from blossom_ai.core.errors import print_warning
from blossom_ai.core.models import (
    ImageModel, TextModel,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS
)


# ============================================================================
# V2 IMAGE GENERATOR
# ============================================================================

class ImageGeneratorV2(SyncGenerator, ModelAwareGenerator):
    """Generate images using V2 API (enter.pollinations.ai)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.V2_IMAGE, timeout, api_token)
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
        """
        Generate image using V2 API with extended features

        Args:
            prompt: Text description
            model: Model to use
            width: Image width
            height: Image height
            seed: Random seed (default: 42)
            enhance: Enhance prompt
            negative_prompt: Negative prompt for guidance
            private: Private generation
            nologo: Remove watermark
            nofeed: Don't add to public feed
            safe: Enable safety filter
            quality: Image quality (low/medium/high/hd)
            image: Input image URL for img2img
            transparent: Generate with transparent background
            guidance_scale: Guidance scale for generation

        Returns:
            bytes: Image data
        """
        self._validate_prompt(prompt)

        params = ImageParamsV2(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            enhance=enhance,
            negative_prompt=negative_prompt,
            private=private,
            nologo=nologo,
            nofeed=nofeed,
            safe=safe,
            quality=quality,
            image=image,
            transparent=transparent,
            guidance_scale=guidance_scale
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        response = self._make_request("GET", url, params=params.to_dict())
        return response.content

    def generate_url(
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
    ) -> str:
        """
        Generate image URL without downloading (V2)

        Security Note:
            API tokens are NEVER included in URLs for security reasons.
            URLs can be safely shared publicly.
        """
        self._validate_prompt(prompt)

        params = ImageParamsV2(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            enhance=enhance,
            negative_prompt=negative_prompt,
            private=private,
            nologo=nologo,
            nofeed=nofeed,
            safe=safe,
            quality=quality,
            image=image,
            transparent=transparent,
            guidance_scale=guidance_scale
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        # Security: NEVER include tokens in URLs
        query_string = urlencode(params.to_dict())
        return f"{url}?{query_string}"

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file"""
        image_data = self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    def models(self) -> List[str]:
        """Get available image models from V2 API"""
        if self._models_cache is None:
            try:
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

        params = ImageParamsV2(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            enhance=enhance,
            negative_prompt=negative_prompt,
            private=private,
            nologo=nologo,
            nofeed=nofeed,
            safe=safe,
            quality=quality,
            image=image,
            transparent=transparent,
            guidance_scale=guidance_scale
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        return await self._make_request("GET", url, params=params.to_dict())

    async def generate_url(
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
    ) -> str:
        """Generate image URL without downloading (async)"""
        self._validate_prompt(prompt)

        params = ImageParamsV2(
            model=self._validate_model(model),
            width=width,
            height=height,
            seed=seed,
            enhance=enhance,
            negative_prompt=negative_prompt,
            private=private,
            nologo=nologo,
            nofeed=nofeed,
            safe=safe,
            quality=quality,
            image=image,
            transparent=transparent,
            guidance_scale=guidance_scale
        )

        encoded_prompt = self._encode_prompt(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        query_string = urlencode(params.to_dict())
        return f"{url}?{query_string}"

    async def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file (async)"""
        image_data = await self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

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

class TextGeneratorV2(SyncGenerator, SyncStreamingMixin, ModelAwareGenerator):
    """Generate text using V2 API (OpenAI-compatible)"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.V2_BASE, timeout, api_token)
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
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """
        Generate text using V2 OpenAI-compatible endpoint

        Args:
            prompt: Input prompt
            model: Model to use
            system: System prompt
            temperature: Temperature (0-2)
            max_tokens: Max tokens in response
            stream: Enable streaming
            json_mode: Enable JSON output
            tools: Function calling tools
            **kwargs: Additional parameters

        Returns:
            str if stream=False, Iterator[str] if stream=True
        """
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
        thinking: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """
        Chat using V2 OpenAI-compatible API

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use
            temperature: Temperature (0-2)
            max_tokens: Max tokens in response
            stream: Enable streaming
            json_mode: Enable JSON output
            tools: Function calling tools
            tool_choice: Tool selection strategy
            frequency_penalty: Frequency penalty (-2 to 2)
            presence_penalty: Presence penalty (-2 to 2)
            top_p: Top-p sampling
            n: Number of completions
            thinking: Native reasoning config
            **kwargs: Additional parameters

        Returns:
            str if stream=False, Iterator[str] if stream=True
        """
        params = ChatParamsV2(
            model=self._validate_model(model),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            json_mode=json_mode,
            tools=tools,
            tool_choice=tool_choice,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
            n=n,
            thinking=thinking,
            extra_params=kwargs
        )

        chat_url = f"{self.base_url}/generate/v1/chat/completions"

        response = self._make_request(
            "POST",
            chat_url,
            json=params.to_body(),
            headers={"Content-Type": "application/json"},
            stream=stream
        )

        if stream:
            return self._stream_sse_chunked(response, self._sse_parser)
        else:
            result = response.json()
            return result["choices"][0]["message"]["content"]

    def models(self) -> List[str]:
        """Get available text models from V2 API"""
        if self._models_cache is None:
            try:
                models_url = f"{self.base_url}/generate/v1/models"
                response = self._make_request("GET", models_url)
                data = response.json()

                models = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name')
                            if name:
                                models.append(name)
                                # Add aliases
                                if 'aliases' in item and isinstance(item['aliases'], list):
                                    models.extend(item['aliases'])

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


class AsyncTextGeneratorV2(AsyncGenerator, AsyncStreamingMixin, ModelAwareGenerator):
    """Async text generator for V2 API"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.V2_BASE, timeout, api_token)
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
        thinking: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """Chat using V2 API (async) with optional native reasoning"""
        params = ChatParamsV2(
            model=self._validate_model(model),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            json_mode=json_mode,
            tools=tools,
            tool_choice=tool_choice,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
            n=n,
            thinking=thinking,
            extra_params=kwargs
        )

        chat_url = f"{self.base_url}/generate/v1/chat/completions"

        if stream:
            response = await self._make_request(
                "POST",
                chat_url,
                json=params.to_body(),
                headers={"Content-Type": "application/json"},
                stream=True
            )
            return self._stream_sse_chunked(response, self._sse_parser)
        else:
            data = await self._make_request(
                "POST",
                chat_url,
                json=params.to_body(),
                headers={"Content-Type": "application/json"}
            )
            result = json.loads(data.decode('utf-8'))
            return result["choices"][0]["message"]["content"]

    async def models(self) -> List[str]:
        """Get available text models from V2 API (async)"""
        if self._models_cache is None:
            try:
                models_url = f"{self.base_url}/generate/v1/models"
                data = await self._make_request("GET", models_url)
                parsed = json.loads(data.decode('utf-8'))

                models = []
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict):
                            name = item.get('name')
                            if name:
                                models.append(name)
                                # Add aliases
                                if 'aliases' in item and isinstance(item['aliases'], list):
                                    models.extend(item['aliases'])

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch V2 models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache