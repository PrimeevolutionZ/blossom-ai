"""
Blossom AI - Universal Client (v0.5.0)
V2 API Only (enter.pollinations.ai)
"""

import asyncio
import inspect
from typing import Optional, Iterator, Union

from blossom_ai.generators.generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator
)


def _is_running_in_async_loop() -> bool:
    """Checks if the code is running in an asyncio event loop"""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def _run_async_from_sync(coro):
    """Runs a coroutine from synchronous code using asyncio.run()"""
    if _is_running_in_async_loop():
        raise RuntimeError(
            "Cannot run async code from sync when an event loop is already running. "
            "Consider using `await` or ensuring the call is from a truly synchronous context."
        )
    return asyncio.run(coro)


class HybridGenerator:
    """Base class for hybrid generators that work in sync and async contexts"""

    def __init__(self, sync_gen, async_gen):
        self._sync = sync_gen
        self._async = async_gen

    def _call(self, method_name: str, *args, **kwargs):
        """Dynamically calls the sync or async version of a method"""
        if _is_running_in_async_loop():
            return getattr(self._async, method_name)(*args, **kwargs)
        else:
            sync_method = getattr(self._sync, method_name)
            result = sync_method(*args, **kwargs)

            if inspect.isgenerator(result) or isinstance(result, Iterator):
                return result

            if inspect.iscoroutine(result):
                return _run_async_from_sync(result)

            return result


class HybridImageGenerator(HybridGenerator):
    """Hybrid image generator with URL generation support"""

    def generate(self, prompt: str, **kwargs) -> bytes:
        """Generate an image and return raw bytes"""
        return self._call("generate", prompt, **kwargs)

    def generate_url(self, prompt: str, **kwargs) -> str:
        """Generate image URL without downloading the image"""
        return self._call("generate_url", prompt, **kwargs)

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file"""
        return self._call("save", prompt, filename, **kwargs)

    def models(self) -> list:
        """Get list of available image models"""
        return self._call("models")


class HybridTextGenerator(HybridGenerator):
    """Hybrid text generator"""

    def generate(self, prompt: str, **kwargs) -> Union[str, Iterator[str]]:
        """Generate text from a prompt"""
        return self._call("generate", prompt, **kwargs)

    def chat(self, messages: list, **kwargs) -> Union[str, Iterator[str]]:
        """Chat completion"""
        return self._call("chat", messages, **kwargs)

    def models(self) -> list:
        """Get list of available text models"""
        return self._call("models")


class Blossom:
    """
    Universal Blossom AI client for both sync and async use

    Uses V2 API (enter.pollinations.ai) with OpenAI-compatible endpoints

    Args:
        timeout: Request timeout in seconds (default: 30)
        debug: Enable debug logging (default: False)
        api_token: API token from enter.pollinations.ai

    Examples:
        # Sync usage
        >>> client = Blossom(api_token="your_token")
        >>> image = client.image.generate("a sunset")
        >>> text = client.text.generate("Write a poem")

        # Async usage
        >>> async with Blossom(api_token="your_token") as client:
        ...     image = await client.image.generate("a sunset")
        ...     text = await client.text.generate("Write a poem")

        # Streaming
        >>> for chunk in client.text.generate("Tell a story", stream=True):
        ...     print(chunk, end="", flush=True)

    Note:
        Version 0.5.0+ uses V2 API only.
        V1 API support removed (discontinued by Pollinations).
    """

    def __init__(
        self,
        timeout: int = 30,
        debug: bool = False,
        api_token: Optional[str] = None
    ):
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

        # Initialize generators
        sync_image = ImageGenerator(timeout=timeout, api_token=api_token)
        async_image = AsyncImageGenerator(timeout=timeout, api_token=api_token)
        sync_text = TextGenerator(timeout=timeout, api_token=api_token)
        async_text = AsyncTextGenerator(timeout=timeout, api_token=api_token)

        self.image = HybridImageGenerator(sync_image, async_image)
        self.text = HybridTextGenerator(sync_text, async_text)

        self._async_generators = [async_image, async_text]
        self._sync_generators = [sync_image, sync_text]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_sync()
        return False

    def close_sync(self):
        """
        Close sync session resources
        Safe to call from __exit__ or manually
        """
        for gen in self._sync_generators:
            if gen is None:
                continue
            if hasattr(gen, '_session_manager'):
                try:
                    gen._session_manager.close()
                except Exception:
                    pass
            elif hasattr(gen, 'close'):
                try:
                    gen.close()
                except Exception:
                    pass

    async def close(self):
        """
        Close all async generator sessions
        Must be called from async context
        """
        for gen in self._async_generators:
            if gen is None:
                continue
            if hasattr(gen, '_session_manager'):
                try:
                    await gen._session_manager.close()
                except Exception:
                    pass
            elif hasattr(gen, "close") and inspect.iscoroutinefunction(gen.close):
                try:
                    await gen.close()
                except Exception:
                    pass

    def __repr__(self) -> str:
        token_status = "with token" if self.api_token else "without token"
        return f"<Blossom AI Client v0.5.0 (V2 API, timeout={self.timeout}s, {token_status})>"


# Convenience factory function
def create_client(api_token: Optional[str] = None, **kwargs) -> Blossom:
    """
    Factory function to create Blossom client

    Args:
        api_token: Your API token from enter.pollinations.ai
        **kwargs: Additional arguments for Blossom()

    Returns:
        Blossom client instance

    Example:
        >>> client = create_client(api_token="your_token")
        >>> image = client.image.generate("a sunset", quality="hd")
    """
    return Blossom(api_token=api_token, **kwargs)