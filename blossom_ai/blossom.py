import asyncio
import inspect
from typing import Optional

from .generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
    AudioGenerator, AsyncAudioGenerator
)


def _is_running_in_async_loop() -> bool:
    """Checks if the code is running in an asyncio event loop."""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def _run_async_from_sync(coro):
    """Runs a coroutine from synchronous code using asyncio.run()"""
    if _is_running_in_async_loop():
        # Если мы внутри async контекста, нельзя использовать asyncio.run
        raise RuntimeError(
            "Cannot run async code from sync when an event loop is already running. "
            "Consider using `await` or ensuring the call is from a truly synchronous context."
        )

    # Всегда используем asyncio.run() для изоляции
    # Это создает новый event loop, выполняет корутину и закрывает loop
    return asyncio.run(coro)


class HybridGenerator:
    """Base class for hybrid generators that work in sync and async contexts."""

    def __init__(self, sync_gen, async_gen):
        self._sync = sync_gen
        self._async = async_gen

    def _call(self, method_name: str, *args, **kwargs):
        """Dynamically calls the sync or async version of a method."""
        if _is_running_in_async_loop():
            # We are in an async context, return the coroutine
            return getattr(self._async, method_name)(*args, **kwargs)
        else:
            # We are in a sync context, run the coroutine and block
            async_method = getattr(self._async, method_name)
            coro = async_method(*args, **kwargs)
            return _run_async_from_sync(coro)


class HybridImageGenerator(HybridGenerator):
    """Hybrid image generator."""

    def generate(self, prompt: str, **kwargs) -> bytes:
        return self._call("generate", prompt, **kwargs)

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        return self._call("save", prompt, filename, **kwargs)

    def models(self) -> list:
        return self._call("models")


class HybridTextGenerator(HybridGenerator):
    """Hybrid text generator."""

    def generate(self, prompt: str, **kwargs) -> str:
        return self._call("generate", prompt, **kwargs)

    def chat(self, messages: list, **kwargs) -> str:
        return self._call("chat", messages, **kwargs)

    def models(self) -> list:
        return self._call("models")


class HybridAudioGenerator(HybridGenerator):
    """Hybrid audio generator."""

    def generate(self, text: str, **kwargs) -> bytes:
        return self._call("generate", text, **kwargs)

    def save(self, text: str, filename: str, **kwargs) -> str:
        return self._call("save", text, filename, **kwargs)

    def voices(self) -> list:
        return self._call("voices")


class Blossom:
    """Universal Blossom AI client for both sync and async use."""

    def __init__(self, timeout: int = 30, debug: bool = False, api_token: Optional[str] = None):
        # Create both sync and async generators
        sync_image = ImageGenerator(timeout=timeout, api_token=api_token)
        async_image = AsyncImageGenerator(timeout=timeout, api_token=api_token)

        sync_text = TextGenerator(timeout=timeout, api_token=api_token)
        async_text = AsyncTextGenerator(timeout=timeout, api_token=api_token)

        sync_audio = AudioGenerator(timeout=timeout, api_token=api_token)
        async_audio = AsyncAudioGenerator(timeout=timeout, api_token=api_token)

        # Create hybrid wrappers
        self.image = HybridImageGenerator(sync_image, async_image)
        self.text = HybridTextGenerator(sync_text, async_text)
        self.audio = HybridAudioGenerator(sync_audio, async_audio)

        self._async_generators = [async_image, async_text, async_audio]
        self._sync_generators = [sync_image, sync_text, sync_audio]
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __enter__(self):
        """Sync context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager support"""
        self._cleanup_sync()
        return False

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self._cleanup_sync()
        except Exception:
            pass

    def _cleanup_sync(self):
        """Clean up sync session resources"""
        for gen in self._sync_generators:
            if hasattr(gen, 'session') and gen.session:
                try:
                    gen.session.close()
                except Exception:
                    pass

    async def close(self):
        """Closes all async generator sessions."""
        for gen in self._async_generators:
            if hasattr(gen, "_close_session") and inspect.iscoroutinefunction(gen._close_session):
                try:
                    await gen._close_session()
                except Exception:
                    pass

    def __repr__(self) -> str:
        token_status = "with token" if self.api_token else "without token"
        return f"<Blossom AI Client (timeout={self.timeout}s, {token_status})>"