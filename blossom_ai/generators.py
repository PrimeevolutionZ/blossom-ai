"""
Blossom AI - Generators (Refactored)
Unified generator classes using base classes and dynamic models
"""

from typing import Optional, List, Dict, Any
import json

from .base_generator import SyncGenerator, AsyncGenerator, ModelAwareGenerator
from .errors import BlossomError, ErrorType, print_warning
from .models import (
    ImageModel, TextModel, Voice,
    DEFAULT_IMAGE_MODELS, DEFAULT_TEXT_MODELS, DEFAULT_VOICES
)


# ============================================================================
# IMAGE GENERATOR
# ============================================================================

class ImageGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate images using Pollinations.AI (Synchronous)"""

    MAX_PROMPT_LENGTH = 200

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://image.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, ImageModel, DEFAULT_IMAGE_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        """Validate image prompt"""
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
        """
        Generate an image from a text prompt

        Args:
            prompt: Text description of the image
            model: Model to use (default: flux)
            width: Image width in pixels
            height: Image height in pixels
            seed: Seed for reproducible results
            nologo: Remove Pollinations logo
            private: Keep image private
            enhance: Enhance prompt with LLM
            safe: Enable strict NSFW filtering

        Returns:
            Image data as bytes
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

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file"""
        image_data = self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    def models(self) -> list:
        """Get list of available image models"""
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
        """Validate image prompt"""
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
        """Generate an image from a text prompt asynchronously"""
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
        """Generate and save image to file asynchronously"""
        image_data = await self.generate(prompt, **kwargs)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return str(filename)

    async def models(self) -> list:
        """Get list of available image models asynchronously"""
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# TEXT GENERATOR
# ============================================================================

class TextGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate text using Pollinations.AI (Synchronous)"""

    MAX_PROMPT_LENGTH = 10000

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        """Validate text prompt"""
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
        private: bool = False
    ) -> str:
        """
        Generate text from a prompt

        Args:
            prompt: Text prompt to generate from
            model: Model to use
            system: System message
            seed: Seed for reproducible results
            temperature: Sampling temperature
            json_mode: Force JSON output
            private: Keep generation private

        Returns:
            Generated text
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

        response = self._make_request("GET", url, params=params)
        return response.text

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai",
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ) -> str:
        """Chat completion using OpenAI-compatible endpoint"""
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages
        }

        # API only supports temperature=1.0
        if temperature is not None and temperature != 1.0:
            print_warning(f"Temperature {temperature} not supported. Using default 1.0")
        body["temperature"] = 1.0

        if stream:
            body["stream"] = stream
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if private:
            body["private"] = private

        try:
            response = self._make_request(
                "POST",
                url,
                json=body,
                headers={"Content-Type": "application/json"}
            )
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception:
            # Fallback to GET method
            user_msg = next((m["content"] for m in messages if m.get("role") == "user"), None)
            system_msg = next((m["content"] for m in messages if m.get("role") == "system"), None)

            if user_msg:
                return self.generate(
                    prompt=user_msg,
                    model=model,
                    system=system_msg,
                    json_mode=json_mode,
                    private=private
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

    MAX_PROMPT_LENGTH = 10000

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, TextModel, DEFAULT_TEXT_MODELS)

    def _validate_prompt(self, prompt: str) -> None:
        """Validate text prompt"""
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
        private: bool = False
    ) -> str:
        """Generate text from a prompt asynchronously"""
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

        data = await self._make_request("GET", url, params=params)
        return data.decode('utf-8')

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "openai",
        temperature: Optional[float] = None,
        stream: bool = False,
        json_mode: bool = False,
        private: bool = False
    ) -> str:
        """Chat completion asynchronously"""
        url = self._build_url("openai")

        body = {
            "model": self._validate_model(model),
            "messages": messages
        }

        if temperature is not None and temperature != 1.0:
            print_warning(f"Temperature {temperature} not supported. Using default 1.0")
        body["temperature"] = 1.0

        if stream:
            body["stream"] = stream
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if private:
            body["private"] = private

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
                    private=private
                )
            raise

    async def models(self) -> List[str]:
        """Get list of available text models asynchronously"""
        if self._models_cache is None:
            models = await self._fetch_list("models", self._fallback_models)
            self._update_known_models(models)
        return self._models_cache or self._fallback_models


# ============================================================================
# AUDIO GENERATOR
# ============================================================================

class AudioGenerator(SyncGenerator, ModelAwareGenerator):
    """Generate audio using Pollinations.AI (Synchronous)"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        SyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        """Audio doesn't have strict prompt validation"""
        pass

    def generate(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "openai-audio"
    ) -> bytes:
        """Generate speech audio from text (Text-to-Speech)"""
        text = text.rstrip('.!?;:,')
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)  # Voice validation through model aware
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

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        AsyncGenerator.__init__(self, "https://text.pollinations.ai", timeout, api_token)
        ModelAwareGenerator.__init__(self, Voice, DEFAULT_VOICES)

    def _validate_prompt(self, prompt: str) -> None:
        """Audio doesn't have strict prompt validation"""
        pass

    async def generate(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "openai-audio"
    ) -> bytes:
        """Generate speech audio from text asynchronously"""
        text = text.rstrip('.!?;:,')
        encoded_text = self._encode_prompt(text)
        url = self._build_url(encoded_text)

        params = {
            "model": model,
            "voice": self._validate_model(voice)
        }

        return await self._make_request("GET", url, params=params)

    async def save(self, text: str, filename: str, **kwargs) -> str:
        """Generate and save audio to file asynchronously"""
        audio_data = await self.generate(text, **kwargs)
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return str(filename)

    async def voices(self) -> List[str]:
        """Get list of available voices asynchronously"""
        if self._models_cache is None:
            voices = await self._fetch_list("voices", self._fallback_models)
            self._update_known_models(voices)
        return self._models_cache or self._fallback_models