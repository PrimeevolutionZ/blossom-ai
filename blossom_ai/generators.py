"""
Blossom AI - Generators
"""

from urllib.parse import quote
from typing import Optional, Dict, Any, List
import asyncio

from .base_client import BaseAPI, AsyncBaseAPI
from .errors import BlossomError, ErrorType, print_warning


# ============================================================================
# IMAGE GENERATOR
# ============================================================================

class ImageGenerator(BaseAPI):
    """Generate images using Pollinations.AI"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://image.pollinations.ai", timeout, api_token=api_token)

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
            nologo: Remove Pollinations logo (requires registration)
            private: Keep image private
            enhance: Enhance prompt with LLM
            safe: Enable strict NSFW filtering

        Returns:
            Image data as bytes
        """
        MAX_PROMPT_LENGTH = 200
        if len(prompt) > MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum allowed length of {MAX_PROMPT_LENGTH} characters.",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

        encoded_prompt = quote(prompt)
        url = f"{self.base_url}/prompt/{encoded_prompt}"

        params = {
            "model": model,
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

    def save(
            self,
            prompt: str,
            filename: str,
            **kwargs
    ) -> str:
        """
        Generate and save image to file

        Args:
            prompt: Text description of the image
            filename: Path to save the image
            **kwargs: Additional arguments for generate()

        Returns:
            Path to saved file
        """
        image_data = self.generate(prompt, **kwargs)

        with open(filename, 'wb') as f:
            f.write(image_data)

        return filename

    def models(self) -> List[str]:
        """Get list of available image models"""
        url = f"{self.base_url}/models"
        response = self._make_request("GET", url)
        return response.json()


class AsyncImageGenerator(AsyncBaseAPI):
    """Generate images using Pollinations.AI asynchronously"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://image.pollinations.ai", timeout, api_token=api_token)

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
        """
        Generate an image from a text prompt asynchronously
        """
        MAX_PROMPT_LENGTH = 200
        if len(prompt) > MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum allowed length of {MAX_PROMPT_LENGTH} characters.",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

        encoded_prompt = quote(prompt)
        url = f"{self.base_url}/prompt/{encoded_prompt}"

        params = {
            "model": model,
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

        response = await self._make_request("GET", url, params=params)
        return await response.read()

    async def save(
            self,
            prompt: str,
            filename: str,
            **kwargs
    ) -> str:
        """
        Generate and save image to file asynchronously
        """
        image_data = await self.generate(prompt, **kwargs)

        with open(filename, 'wb') as f:
            f.write(image_data)

        return filename

    async def models(self) -> List[str]:
        """
        Get list of available image models asynchronously
        """
        url = f"{self.base_url}/models"
        response = await self._make_request("GET", url)
        return await response.json()


# ============================================================================
# TEXT GENERATOR
# ============================================================================

class TextGenerator(BaseAPI):
    """Generate text using Pollinations.AI"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://text.pollinations.ai", timeout, api_token=api_token)

    def generate(
            self,
            prompt: str,
            model: str = "openai",
            system: Optional[str] = None,
            temperature: Optional[float] = None,
            seed: Optional[int] = None,
            json_mode: bool = False,
            stream: bool = False,
            private: bool = False
    ) -> str:
        """
        Generate text from a prompt (GET method)
        """
        if temperature is not None:
            print_warning("Temperature parameter is not supported in GET endpoint and will be ignored")

        # Убираем trailing пунктуацию
        prompt = prompt.rstrip('.!?;:,')

        encoded_prompt = quote(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        params = {"model": model}

        if system:
            params["system"] = system
        if seed is not None:
            params["seed"] = str(seed)
        if json_mode:
            params["json"] = "true"
        if stream:
            params["stream"] = "true"
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
            private: bool = False,
            use_get_fallback: bool = True
    ) -> str:
        """
        Chat completion using OpenAI-compatible endpoint (POST method)
        """
        url = f"{self.base_url}/openai"

        body = {
            "model": model,
            "messages": messages
        }

        if temperature is not None:
            body["temperature"] = temperature
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

        except Exception as e:
            if use_get_fallback:
                user_message = None
                system_message = None

                for msg in messages:
                    if msg.get("role") == "user":
                        user_message = msg.get("content")
                    elif msg.get("role") == "system":
                        system_message = msg.get("content")

                if user_message:
                    return self.generate(
                        prompt=user_message,
                        model=model,
                        system=system_message,
                        temperature=temperature,
                        json_mode=json_mode,
                        private=private
                    )
            raise

    def models(self) -> List[str]:
        """Get list of available text models"""
        url = f"{self.base_url}/models"
        response = self._make_request("GET", url)
        return response.json()


class AsyncTextGenerator(AsyncBaseAPI):
    """Generate text using Pollinations.AI asynchronously"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://text.pollinations.ai", timeout, api_token=api_token)

    async def generate(
            self,
            prompt: str,
            model: str = "openai",
            system: Optional[str] = None,
            temperature: Optional[float] = None,
            seed: Optional[int] = None,
            json_mode: bool = False,
            stream: bool = False,
            private: bool = False
    ) -> str:
        """
        Generate text from a prompt asynchronously (GET method)
        """
        if temperature is not None:
            print_warning("Temperature parameter is not supported in GET endpoint and will be ignored")

        prompt = prompt.rstrip('.!?;:,')

        encoded_prompt = quote(prompt)

        url = f"{self.base_url}/{encoded_prompt}"

        params = {"model": model}

        if system:
            params["system"] = system
        if seed is not None:
            params["seed"] = str(seed)
        if json_mode:
            params["json"] = "true"
        if stream:
            params["stream"] = "true"
        if private:
            params["private"] = "true"

        response = await self._make_request("GET", url, params=params)
        return await response.text()

    async def chat(
            self,
            messages: List[Dict[str, Any]],
            model: str = "openai",
            temperature: Optional[float] = None,
            stream: bool = False,
            json_mode: bool = False,
            private: bool = False,
            use_get_fallback: bool = True
    ) -> str:
        """
        Chat completion using OpenAI-compatible endpoint asynchronously (POST method)
        """
        url = f"{self.base_url}/openai"

        body = {
            "model": model,
            "messages": messages
        }

        if temperature is not None:
            body["temperature"] = temperature
        if stream:
            body["stream"] = stream
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if private:
            body["private"] = private

        try:
            response = await self._make_request(
                "POST",
                url,
                json=body,
                headers={"Content-Type": "application/json"}
            )

            result = await response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            if use_get_fallback:
                user_message = None
                system_message = None

                for msg in messages:
                    if msg.get("role") == "user":
                        user_message = msg.get("content")
                    elif msg.get("role") == "system":
                        system_message = msg.get("content")

                if user_message:
                    return await self.generate(
                        prompt=user_message,
                        model=model,
                        system=system_message,
                        temperature=temperature,
                        json_mode=json_mode,
                        private=private
                    )
            raise

    async def models(self) -> List[str]:
        """
        Get list of available text models asynchronously
        """
        url = f"{self.base_url}/models"
        response = await self._make_request("GET", url)
        return await response.json()


# ============================================================================
# AUDIO GENERATOR
# ============================================================================

class AudioGenerator(BaseAPI):
    """Generate audio using Pollinations.AI"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://text.pollinations.ai", timeout, api_token=api_token)

    def generate(
            self,
            text: str,
            voice: str = "alloy",
            model: str = "openai-audio"
    ) -> bytes:
        """
        Generate speech audio from text (Text-to-Speech)
        """
        text = text.rstrip('.!?;:,')

        encoded_text = quote(text)
        # ИСПРАВЛЕНО: используем тот же формат что и для текста (БЕЗ /prompt/)
        url = f"{self.base_url}/{encoded_text}"

        params = {
            "model": model,
            "voice": voice
        }

        response = self._make_request("GET", url, params=params)
        return response.content

    def save(
            self,
            text: str,
            filename: str,
            voice: str = "alloy"
    ) -> str:
        """
        Generate and save audio to file
        """
        try:
            audio_data = self.generate(text, voice=voice)
        except BlossomError as e:
            if e.error_type == ErrorType.API and "402" in str(e):
                raise BlossomError(
                    message="Text-to-Speech requires authenticated access (Seed tier or higher).",
                    error_type=ErrorType.API,
                    suggestion="Visit https://auth.pollinations.ai to get your API token and ensure you're logged in."
                )
            raise

        with open(filename, 'wb') as f:
            f.write(audio_data)

        return filename

    def voices(self) -> List[str]:
        """Get list of available voices"""
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class AsyncAudioGenerator(AsyncBaseAPI):
    """Generate audio using Pollinations.AI asynchronously"""

    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        super().__init__("https://text.pollinations.ai", timeout, api_token=api_token)

    async def generate(
            self,
            text: str,
            voice: str = "alloy",
            model: str = "openai-audio"
    ) -> bytes:
        """
        Generate speech audio from text asynchronously (Text-to-Speech)
        """
        text = text.rstrip('.!?;:,')

        encoded_text = quote(text)
        url = f"{self.base_url}/{encoded_text}"

        params = {
            "model": model,
            "voice": voice
        }

        response = await self._make_request("GET", url, params=params)
        return await response.read()

    async def save(
            self,
            text: str,
            filename: str,
            voice: str = "alloy"
    ) -> str:
        """
        Generate and save audio to file asynchronously
        """
        try:
            audio_data = await self.generate(text, voice=voice)
        except BlossomError as e:
            if e.error_type == ErrorType.API and "402" in str(e):
                raise BlossomError(
                    message="Text-to-Speech requires authenticated access (Seed tier or higher).",
                    error_type=ErrorType.API,
                    suggestion="Visit https://auth.pollinations.ai to get your API token and ensure you're logged in."
                )
            raise

        with open(filename, 'wb') as f:
            f.write(audio_data)

        return filename

    async def voices(self) -> List[str]:
        """
        Get list of available voices asynchronously
        """
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]