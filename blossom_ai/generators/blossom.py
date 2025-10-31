"""
Blossom AI - Universal Client (Updated with V2 API Support)
Supports both legacy and new enter.pollinations.ai API
"""

import asyncio
import inspect
from typing import Optional, Iterator, Union, Literal

from blossom_ai.generators.generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
    AudioGenerator, AsyncAudioGenerator
)

# Import V2 generators
try:
    from blossom_ai.generators.generators_v2 import (
        ImageGeneratorV2, AsyncImageGeneratorV2,
        TextGeneratorV2, AsyncTextGeneratorV2
    )
    V2_AVAILABLE = True
except ImportError:
    V2_AVAILABLE = False


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
        return self._call("generate", prompt, **kwargs)

    def chat(self, messages: list, **kwargs) -> Union[str, Iterator[str]]:
        return self._call("chat", messages, **kwargs)

    def models(self) -> list:
        return self._call("models")


class HybridAudioGenerator(HybridGenerator):
    """Hybrid audio generator"""

    def generate(self, text: str, **kwargs) -> bytes:
        return self._call("generate", text, **kwargs)

    def save(self, text: str, filename: str, **kwargs) -> str:
        return self._call("save", text, filename, **kwargs)

    def voices(self) -> list:
        return self._call("voices")


class Blossom:
    """
    Universal Blossom AI client for both sync and async use

    Supports both API versions:
    - v1 (legacy): image.pollinations.ai, text.pollinations.ai
    - v2 (new): enter.pollinations.ai/api

    Args:
        timeout: Request timeout in seconds
        debug: Enable debug logging
        api_token: API token from enter.pollinations.ai
        api_version: API version to use ("v1" or "v2", default: "v1")

    Examples:
        # Legacy API (v1)
        >>> client = Blossom(api_token="your_token")
        >>> image = client.image.generate("a sunset")

        # New API (v2) with more features
        >>> client = Blossom(api_token="your_token", api_version="v2")
        >>> image = client.image.generate("a sunset", quality="hd", guidance_scale=7.5)

        # Async usage
        >>> async with Blossom(api_version="v2") as client:
        ...     image = await client.image.generate("a sunset")
    """

    def __init__(
        self,
        timeout: int = 30,
        debug: bool = False,
        api_token: Optional[str] = None,
        api_version: Literal["v1", "v2"] = "v1"
    ):
        self.api_version = api_version
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

        # Initialize generators based on API version
        if api_version == "v2":
            if not V2_AVAILABLE:
                raise ImportError(
                    "V2 API generators not available. "
                    "Make sure generators_v2.py is present."
                )

            sync_image = ImageGeneratorV2(timeout=timeout, api_token=api_token)
            async_image = AsyncImageGeneratorV2(timeout=timeout, api_token=api_token)
            sync_text = TextGeneratorV2(timeout=timeout, api_token=api_token)
            async_text = AsyncTextGeneratorV2(timeout=timeout, api_token=api_token)

            # V2 doesn't have audio endpoint yet, use V1
            sync_audio = AudioGenerator(timeout=timeout, api_token=api_token)
            async_audio = AsyncAudioGenerator(timeout=timeout, api_token=api_token)

        else:  # v1 (legacy)
            sync_image = ImageGenerator(timeout=timeout, api_token=api_token)
            async_image = AsyncImageGenerator(timeout=timeout, api_token=api_token)
            sync_text = TextGenerator(timeout=timeout, api_token=api_token)
            async_text = AsyncTextGenerator(timeout=timeout, api_token=api_token)
            sync_audio = AudioGenerator(timeout=timeout, api_token=api_token)
            async_audio = AsyncAudioGenerator(timeout=timeout, api_token=api_token)

        self.image = HybridImageGenerator(sync_image, async_image)
        self.text = HybridTextGenerator(sync_text, async_text)
        self.audio = HybridAudioGenerator(sync_audio, async_audio)

        self._async_generators = [async_image, async_text, async_audio]
        self._sync_generators = [sync_image, sync_text, sync_audio]

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
        This is safe to call from __exit__ or manually
        """
        for gen in self._sync_generators:
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
        return (
            f"<Blossom AI Client (api_version={self.api_version}, "
            f"timeout={self.timeout}s, {token_status})>"
        )


# Convenience factory functions
def create_client(
    api_version: Literal["v1", "v2"] = "v1",
    api_token: Optional[str] = None,
    **kwargs
) -> Blossom:
    """
    Factory function to create Blossom client

    Args:
        api_version: "v1" (legacy) or "v2" (new enter.pollinations.ai)
        api_token: Your API token
        **kwargs: Additional arguments for Blossom()

    Returns:
        Blossom client instance

    Example:
        >>> # Use new V2 API
        >>> client = create_client("v2", api_token="your_token")
        >>> image = client.image.generate("a sunset", quality="hd")
    """
    return Blossom(api_version=api_version, api_token=api_token, **kwargs)