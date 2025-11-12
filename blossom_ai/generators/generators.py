"""
Blossom AI - Generators (v0.5.0)
V2 API Only (enter.pollinations.ai)
"""
from typing import AsyncIterator, AsyncGenerator
from typing import Optional, List, Dict, Any, Iterator, Union, AsyncIterator
from urllib.parse import urlencode
import json

from blossom_ai.generators.base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from blossom_ai.generators.streaming_mixin import (
    SyncStreamingMixin, AsyncStreamingMixin, SSEParser
)
from blossom_ai.generators.parameter_builder import (
    ImageParamsV2, ChatParamsV2, ParameterValidator, MessageBuilder
)
from blossom_ai.core.config import ENDPOINTS, LIMITS, DEFAULTS
from blossom_ai.core.errors import print_warning
from blossom_ai.core.models import (
    ImageModel, TextModel,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS
)


# ============================================================================
# IMAGE GENERATOR
# ============================================================================

class ImageGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations AI V2 API (Synchronous)"""

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
        seed: int = DEFAULTS.IMAGE_SEED,
        enhance: bool = False,
        negative_prompt: str = DEFAULTS.IMAGE_NEGATIVE_PROMPT,
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = DEFAULTS.IMAGE_QUALITY,
        image: Optional[str] = None,
        transparent: bool = False,
        guidance_scale: Optional[float] = None
    ) -> bytes:
        """
        Generate image using V2 API with extended features

        Args:
            prompt: Text description of the image
            model: Model to use (default: flux)
            width: Image width in pixels (default: 1024)
            height: Image height in pixels (default: 1024)
            seed: Random seed for reproducibility (default: 42)
            enhance: Enhance prompt automatically
            negative_prompt: Negative prompt for guidance
            private: Make generation private
            nologo: Remove Pollinations watermark
            nofeed: Don't add to public feed
            safe: Enable safety filter
            quality: Image quality (low/medium/high/hd)
            image: Input image URL for img2img
            transparent: Generate with transparent background
            guidance_scale: Guidance scale for generation

        Returns:
            bytes: Image data

        Example:
            >>> gen = ImageGenerator(api_token="your_token")
            >>> img_data = gen.generate(
            ...     "a beautiful sunset over mountains",
            ...     quality="hd",
            ...     seed=42
            ... )
            >>> with open("sunset.png", "wb") as f:
            ...     f.write(img_data)
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
        seed: int = DEFAULTS.IMAGE_SEED,
        enhance: bool = False,
        negative_prompt: str = DEFAULTS.IMAGE_NEGATIVE_PROMPT,
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = DEFAULTS.IMAGE_QUALITY,
        image: Optional[str] = None,
        transparent: bool = False,
        guidance_scale: Optional[float] = None
    ) -> str:
        """
        Generate image URL without downloading the image

        Security Note:
            API tokens are NEVER included in URLs for security reasons.
            URLs can be safely shared publicly.

        Returns:
            str: Full URL of the generated image
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
            try:
                response = self._make_request("GET", ENDPOINTS.IMAGE_MODELS)
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
                print_warning(f"Failed to fetch image models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


class AsyncImageGenerator(AsyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations AI V2 API (Asynchronous)"""

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
        seed: int = DEFAULTS.IMAGE_SEED,
        enhance: bool = False,
        negative_prompt: str = DEFAULTS.IMAGE_NEGATIVE_PROMPT,
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = DEFAULTS.IMAGE_QUALITY,
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
        seed: int = DEFAULTS.IMAGE_SEED,
        enhance: bool = False,
        negative_prompt: str = DEFAULTS.IMAGE_NEGATIVE_PROMPT,
        private: bool = False,
        nologo: bool = False,
        nofeed: bool = False,
        safe: bool = False,
        quality: str = DEFAULTS.IMAGE_QUALITY,
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
        """Get list of available image models (async)"""
        if self._models_cache is None:
            try:
                data = await self._make_request("GET", ENDPOINTS.IMAGE_MODELS)
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
                print_warning(f"Failed to fetch image models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


# ============================================================================
# TEXT GENERATOR (UPDATED WITH VISION & AUDIO)
# ============================================================================

class TextGenerator(SyncGenerator, SyncStreamingMixin, ModelAwareGenerator):
    """Generate text using Pollinations AI V2 API (Synchronous) with Vision & Audio"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
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
        temperature: float = DEFAULTS.TEMPERATURE,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """
        Generate text from a prompt

        Args:
            prompt: Input text prompt
            model: Model to use (default: openai)
            system: System prompt
            temperature: Temperature for sampling (0-2)
            max_tokens: Maximum tokens in response
            stream: Enable streaming (yields text chunks)
            json_mode: Enable JSON output mode
            tools: Function calling tools
            **kwargs: Additional OpenAI-compatible parameters

        Returns:
            str if stream=False, Iterator[str] if stream=True

        Example:
            >>> gen = TextGenerator(api_token="your_token")
            >>> # Non-streaming
            >>> result = gen.generate("Write a poem about AI")
            >>> print(result)

            >>> # Streaming
            >>> for chunk in gen.generate("Tell me a story", stream=True):
            ...     print(chunk, end="", flush=True)
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
        temperature: float = DEFAULTS.TEMPERATURE,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        frequency_penalty: float = DEFAULTS.FREQUENCY_PENALTY,
        presence_penalty: float = DEFAULTS.PRESENCE_PENALTY,
        top_p: float = DEFAULTS.TOP_P,
        n: int = 1,
        thinking: Optional[Dict[str, Any]] = None,
        modalities: Optional[List[str]] = None,
        audio: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[str, Iterator[str]]:
        """
        Chat completion using OpenAI-compatible V2 API with Vision & Audio

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
            modalities: Output modalities ["text", "audio"]
            audio: Audio config with voice: {"voice": "alloy", "format": "wav"}
            **kwargs: Additional parameters

        Returns:
            str if stream=False, Iterator[str] if stream=True

        Example:
            >>> gen = TextGenerator()
            >>> # Text-only chat
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant"},
            ...     {"role": "user", "content": "Hello!"}
            ... ]
            >>> response = gen.chat(messages)

            >>> # Vision (image input)
            >>> messages = [
            ...     MessageBuilder.image_message(
            ...         role="user",
            ...         text="What's in this image?",
            ...         image_path="photo.jpg"
            ...     )
            ... ]
            >>> response = gen.chat(messages, model="openai")

            >>> # Audio output
            >>> messages = [{"role": "user", "content": "Tell me a joke"}]
            >>> response = gen.chat(
            ...     messages,
            ...     modalities=["text", "audio"],
            ...     audio={"voice": "alloy", "format": "wav"}
            ... )
        """
        # Validate modalities if provided
        if modalities:
            ParameterValidator.validate_modalities(modalities)

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
            modalities=modalities,
            audio=audio,
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
        """Get list of available text models"""
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
                print_warning(f"Failed to fetch text models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache


class AsyncTextGenerator(AsyncGenerator, AsyncStreamingMixin, ModelAwareGenerator):
    """Generate text using Pollinations AI V2 API (Asynchronous) with Vision & Audio"""

    def __init__(self, timeout: int = LIMITS.DEFAULT_TIMEOUT, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, ENDPOINTS.BASE, timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)
        self._sse_parser = SSEParser()

    def _validate_prompt(self, prompt: str) -> None:
        ParameterValidator.validate_prompt_length(
            prompt, LIMITS.MAX_TEXT_PROMPT_LENGTH, "prompt"
        )

    # ----------  ЕДИНЫЙ ПУБЛИЧНЫЙ МЕТОД  ----------
    def generate(
        self,
        prompt: str,
        model: str = DEFAULTS.TEXT_MODEL,
        system: Optional[str] = None,
        temperature: float = DEFAULTS.TEMPERATURE,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generate text from a prompt (async)

        Returns:
            str                   if stream=False
            AsyncIterator[str]    if stream=True
        """
        self._validate_prompt(prompt)

        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})

        if stream:
            # возвращаем генератор
            return self._generate_stream(
                msgs, model, temperature, max_tokens, json_mode, tools, **kwargs
            )
        # возвращаем корутину, дающую строку
        return self._generate_text(
            msgs, model, temperature, max_tokens, json_mode, tools, **kwargs
        )

    # ----------  ВНУТРЕННИЕ ПОМОЩНИКИ  ----------
    async def _generate_text(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        json_mode: bool,
        tools: Optional[List[Dict]],
        **kwargs
    ) -> str:
        """Простой текстовый запрос (без стриминга)"""
        return await self.chat_text(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=json_mode,
            tools=tools,
            **kwargs
        )

    async def _generate_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        json_mode: bool,
        tools: Optional[List[Dict]],
        **kwargs
    ) -> AsyncIterator[str]:
        """Стриминговый запрос"""
        async for chunk in self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            json_mode=json_mode,
            tools=tools,
            **kwargs
        ):
            yield chunk

    # ----------  ОСТАЛЬНОЕ БЕЗ ИЗМЕНЕНИЙ  ----------
    async def chat_text(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: float = DEFAULTS.TEMPERATURE,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        frequency_penalty: float = DEFAULTS.FREQUENCY_PENALTY,
        presence_penalty: float = DEFAULTS.PRESENCE_PENALTY,
        top_p: float = DEFAULTS.TOP_P,
        n: int = 1,
        thinking: Optional[Dict[str, Any]] = None,
        modalities: Optional[List[str]] = None,
        audio: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if modalities:
            ParameterValidator.validate_modalities(modalities)

        params = ChatParamsV2(
            model=self._validate_model(model),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
            json_mode=json_mode,
            tools=tools,
            tool_choice=tool_choice,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
            n=n,
            thinking=thinking,
            modalities=modalities,
            audio=audio,
            extra_params=kwargs
        )

        chat_url = f"{self.base_url}/generate/v1/chat/completions"
        data = await self._make_request(
            "POST",
            chat_url,
            json=params.to_body(),
            headers={"Content-Type": "application/json"}
        )
        result = json.loads(data.decode('utf-8'))
        return result["choices"][0]["message"]["content"]

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = DEFAULTS.TEXT_MODEL,
        temperature: float = DEFAULTS.TEMPERATURE,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        json_mode: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        frequency_penalty: float = DEFAULTS.FREQUENCY_PENALTY,
        presence_penalty: float = DEFAULTS.PRESENCE_PENALTY,
        top_p: float = DEFAULTS.TOP_P,
        n: int = 1,
        thinking: Optional[Dict[str, Any]] = None,
        modalities: Optional[List[str]] = None,
        audio: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        if modalities:
            ParameterValidator.validate_modalities(modalities)

        params = ChatParamsV2(
            model=self._validate_model(model),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            json_mode=json_mode,
            tools=tools,
            tool_choice=tool_choice,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            top_p=top_p,
            n=n,
            thinking=thinking,
            modalities=modalities,
            audio=audio,
            extra_params=kwargs
        )

        chat_url = f"{self.base_url}/generate/v1/chat/completions"
        resp = await self._make_request(
            "POST",
            chat_url,
            json=params.to_body(),
            headers={"Content-Type": "application/json"},
            stream=True
        )

        async for chunk in self._stream_sse_chunked(resp, self._sse_parser):
            yield chunk

    async def models(self) -> List[str]:
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
                                if 'aliases' in item and isinstance(item['aliases'], list):
                                    models.extend(item['aliases'])

                self._update_known_models(models if models else self._fallback_models)
                self._models_cache = models if models else self._fallback_models
            except Exception as e:
                print_warning(f"Failed to fetch text models: {e}")
                self._models_cache = self._fallback_models

        return self._models_cache