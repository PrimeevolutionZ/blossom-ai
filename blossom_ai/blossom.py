
"""
Blossom AI - Main Client
"""

from typing import Optional

from .generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
    AudioGenerator, AsyncAudioGenerator
)



class Blossom:
    """
    Main Blossom AI client for synchronous operations.

    Usage:
        ai = Blossom(api_token="your_token_here")

        # Generate image
        image = ai.image.generate("a beautiful sunset")

        # Generate text
        text = ai.text.generate("explain AI in simple terms")

        # Generate audio
        audio = ai.audio.generate("Hello world")
    """

    def __init__(self, timeout: int = 30, debug: bool = False, api_token: Optional[str] = None):
        """
        Initialize Blossom AI client

        Args:
            timeout: Request timeout in seconds
            debug: Enable debug mode for verbose output (currently not used)
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


class AsyncBlossom:
    """
    Main Blossom AI client for asynchronous operations.

    Usage:
        async def main():
            ai = AsyncBlossom(api_token="your_token_here")

            # Generate image asynchronously
            image = await ai.image.generate("a beautiful sunset")

            # Generate text asynchronously
            text = await ai.text.generate("explain AI in simple terms")

            # Generate audio asynchronously
            audio = await ai.audio.generate("Hello world")

            # Don't forget to close sessions
            await ai.close()

        if __name__ == "__main__":
            import asyncio
            asyncio.run(main())
    """

    def __init__(self, timeout: int = 30, debug: bool = False, api_token: Optional[str] = None):
        """
        Initialize Async Blossom AI client

        Args:
            timeout: Request timeout in seconds
            debug: Enable debug mode for verbose output (currently not used)
            api_token: Your Pollinations.AI API token
        """
        self.image = AsyncImageGenerator(timeout=timeout, api_token=api_token)
        self.text = AsyncTextGenerator(timeout=timeout, api_token=api_token)
        self.audio = AsyncAudioGenerator(timeout=timeout, api_token=api_token)
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

    async def close(self):
        """Close all underlying aiohttp client sessions."""
        await self.image._close_session()
        await self.text._close_session()
        await self.audio._close_session()

    def __repr__(self) -> str:
        token_status = "with token" if self.api_token else "without token"
        return f"<Async Blossom AI Client (timeout={self.timeout}s, debug={self.debug}, {token_status})>"

