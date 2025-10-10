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

    def __init__(self, base_url: str, timeout: int = 30, api_token: Optional[str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.api_token = api_token
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

            # Добавляем токен в заголовки или параметры
            if self.api_token:
                # Для POST-запросов используем заголовок Authorization
                if method.upper() == 'POST':
                    if 'headers' not in kwargs:
                        kwargs['headers'] = {}
                    kwargs['headers']['Authorization'] = f'Bearer {self.api_token}'
                # Для GET-запросов добавляем токен как параметр
                else:
                    if 'params' not in kwargs:
                        kwargs['params'] = {}
                    kwargs['params']['token'] = self.api_token

            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            # Проверяем специфичные ошибки API
            if isinstance(e, requests.exceptions.HTTPError):
                status_code = e.response.status_code

                # Обработка 402 Payment Required
                if status_code == 402:
                    try:
                        error_data = e.response.json()
                        error_msg = error_data.get('error', str(e))
                        raise BlossomError(
                            message=f"Payment Required: {error_msg}",
                            error_type=ErrorType.API,
                            suggestion="Your current tier may not support this feature. Visit https://auth.pollinations.ai to upgrade or check your API token."
                        )
                    except json.JSONDecodeError:
                        raise BlossomError(
                            message=f"Payment Required (402). Your tier may not support this feature.",
                            error_type=ErrorType.API,
                            suggestion="Visit https://auth.pollinations.ai to upgrade."
                        )

                # Повторяем попытку для 502
                if status_code == 502:
                    print_info(f"Retrying 502 error for {url}...")
                    raise

            # Повторяем попытку для ChunkedEncodingError
            if isinstance(e, requests.exceptions.ChunkedEncodingError):
                print_info(f"Retrying ChunkedEncodingError for {url}...")
                raise

            # Для остальных ошибок используем общий обработчик
            raise handle_request_error(e, f"making {method} request to {url}")


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
        # Validate prompt length
        MAX_PROMPT_LENGTH = 200
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

        # Build parameters
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

        Uses GET endpoint with model=openai-audio for text-to-speech generation.

        Args:
            text: Text to synthesize
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: Model to use (must be "openai-audio" for TTS)

        Returns:
            Audio data as bytes (MP3 format)
        """
        # Build URL with encoded text
        encoded_text = quote(text)
        url = f"{self.base_url}/{encoded_text}"

        # Build parameters for GET request
        params = {
            "model": model,
            "voice": voice
        }

        # Make GET request
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
        try:
            audio_data = self.generate(text, voice=voice)
        except BlossomError as e:
            # If TTS fails, provide helpful message
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
        # Common voices for OpenAI TTS
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


# ============================================================================
# MAIN BLOSSOM CLASS
# ============================================================================

class Blossom:
    """
    Main Blossom AI client

    Usage:
        ai = Blossom(api_token="your_token_here")

        # Generate image
        image = ai.image("a beautiful sunset")

        # Generate text
        text = ai.text("explain AI in simple terms")

        # Generate audio
        audio = ai.audio("Hello world")
    """

    def __init__(self, timeout: int = 30, debug: bool = False, api_token: Optional[str] = None):
        """
        Initialize Blossom AI client

        Args:
            timeout: Request timeout in seconds
            debug: Enable debug mode for verbose output
            api_token: Your Pollinations.AI API token
        """
        self.image = ImageGenerator(timeout=timeout, api_token=api_token)
        self.text = TextGenerator(timeout=timeout, api_token=api_token)
        self.audio = AudioGenerator(timeout=timeout, api_token=api_token)
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

    def __repr__(self) -> str:
        token_status = "with token" if self.api_token else "without token"
        return f"<Blossom AI Client (timeout={self.timeout}s, debug={self.debug}, {token_status})>"