"""
Blossom AI - Core Classes
"""

import requests
from urllib.parse import quote
from typing import Optional, Dict, Any, List
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .errors import (
    BlossomError,
    ErrorType,
    handle_request_error,
    print_success,
    print_info,
    print_warning
)


# ============================================================================
# BASE API CLIENT
# ============================================================================

class BaseAPI:
    """Base class for API interactions"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.exceptions.HTTPError) | retry_if_exception_type(requests.exceptions.ChunkedEncodingError),
        reraise=True
    )
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling and retry logic"""
        try:
            kwargs.setdefault("timeout", self.timeout)
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            # Only re-raise if it's not a retryable error or after all retries are exhausted
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 502:
                print_info(f"Retrying 502 error for {url}...")
                raise  # Re-raise to trigger retry
            elif isinstance(e, requests.exceptions.ChunkedEncodingError):
                print_info(f"Retrying ChunkedEncodingError for {url}...")
                raise  # Re-raise to trigger retry
            else:
                raise handle_request_error(e, f"making {method} request to {url}")


# ============================================================================
# IMAGE GENERATOR
# ============================================================================

class ImageGenerator(BaseAPI):
    """Generate images using Pollinations.AI"""

    def __init__(self, timeout: int = 30):
        super().__init__("https://image.pollinations.ai", timeout)

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
        # Validate prompt length
        MAX_PROMPT_LENGTH = 200  # This is an arbitrary limit, adjust as needed
        if len(prompt) > MAX_PROMPT_LENGTH:
            raise BlossomError(
                message=f"Prompt exceeds maximum allowed length of {MAX_PROMPT_LENGTH} characters.",
                error_type=ErrorType.INVALID_PARAM,
                suggestion="Please shorten your prompt."
            )

        # Build URL
        encoded_prompt = quote(prompt)

        url = f"{self.base_url}/prompt/{encoded_prompt}"

        # Build parameters
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

        # Make request
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


# ============================================================================
# TEXT GENERATOR
# ============================================================================

class TextGenerator(BaseAPI):
    """Generate text using Pollinations.AI"""

    def __init__(self, timeout: int = 30):
        super().__init__("https://text.pollinations.ai", timeout)

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

        Args:
            prompt: Text prompt for the AI
            model: Model to use (default: openai)
            system: System prompt to guide AI behavior
            temperature: Controls randomness (0.0 to 3.0) - NOTE: Not supported in GET API
            seed: Seed for reproducible results
            json_mode: Return response as JSON
            stream: Enable streaming (returns generator)
            private: Keep response private

        Returns:
            Generated text

        Note:
            The GET endpoint does not support temperature parameter.
            If you need temperature control, consider using the chat() method
            or use the API without temperature.
        """
        # Warn about unsupported parameters
        if temperature is not None:
            print_warning("Temperature parameter is not supported in GET endpoint and will be ignored")

        # Build URL with encoded prompt
        encoded_prompt = quote(prompt)
        url = f"{self.base_url}/{encoded_prompt}"

        # Build parameters - only include supported ones
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

        # Make GET request
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

        Note: POST endpoint may have issues. If it fails and use_get_fallback=True,
        will automatically try GET endpoint with the last user message.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use
            temperature: Controls randomness
            stream: Enable streaming
            json_mode: Return JSON response
            private: Keep response private
            use_get_fallback: If True, falls back to GET on POST failure

        Returns:
            Generated response text
        """
        url = f"{self.base_url}/openai"

        # Build request body
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
            # Try POST request
            response = self._make_request(
                "POST",
                url,
                json=body,
                headers={"Content-Type": "application/json"}
            )

            # Parse OpenAI-style response
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            # If POST fails and fallback is enabled
            if use_get_fallback:
                # Extract the last user message
                user_message = None
                system_message = None

                for msg in messages:
                    if msg.get("role") == "user":
                        user_message = msg.get("content")
                    elif msg.get("role") == "system":
                        system_message = msg.get("content")

                if user_message:
                    # Try GET fallback
                    return self.generate(
                        prompt=user_message,
                        model=model,
                        system=system_message,
                        temperature=temperature,
                        json_mode=json_mode,
                        private=private
                    )

            # Re-raise if no fallback or fallback not applicable
            raise

    def models(self) -> List[str]:
        """Get list of available text models"""
        url = f"{self.base_url}/models"
        response = self._make_request("GET", url)
        return response.json()


# ============================================================================
# AUDIO GENERATOR
# ============================================================================

class AudioGenerator(BaseAPI):
    """Generate audio using Pollinations.AI"""

    def __init__(self, timeout: int = 30):
        super().__init__("https://text.pollinations.ai", timeout)

    def generate(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "openai-audio"
    ) -> bytes:
        """
        Generate speech audio from text (Text-to-Speech)

        Args:
            text: Text to synthesize
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: Model to use (default: openai-audio)

        Returns:
            Audio data as bytes (MP3 format)
        """
        # Build URL
        encoded_text = quote(text)
        url = f"{self.base_url}/{encoded_text}"

        # Build parameters
        params = {
            "model": model,
            "voice": voice
        }

        # Make request
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

        Args:
            text: Text to synthesize
            filename: Path to save the audio
            voice: Voice to use

        Returns:
            Path to saved file
        """
        audio_data = self.generate(text, voice=voice)

        with open(filename, 'wb') as f:
            f.write(audio_data)

        return filename

    def voices(self) -> List[str]:
        """Get list of available voices"""
        # Common voices for OpenAI TTS
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


# ============================================================================
# MAIN BLOSSOM CLASS
# ============================================================================

class Blossom:
    """
    Main Blossom AI client

    Usage:
        ai = Blossom()

        # Generate image
        image = ai.image("a beautiful sunset")

        # Generate text
        text = ai.text("explain AI in simple terms")

        # Generate audio
        audio = ai.audio("Hello world")
    """

    def __init__(self, timeout: int = 30, debug: bool = False):
        """
        Initialize Blossom AI client

        Args:
            timeout: Request timeout in seconds
            debug: Enable debug mode for verbose output
        """
        self.image = ImageGenerator(timeout)
        self.text = TextGenerator(timeout)
        self.audio = AudioGenerator(timeout)
        self.timeout = timeout
        self.debug = debug

    def __repr__(self) -> str:
        return f"<Blossom AI Client (timeout={self.timeout}s, debug={self.debug})>"

