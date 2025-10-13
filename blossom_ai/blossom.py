"""
Blossom AI - Hybrid Client (Sync + Async)
"""

import asyncio
import inspect
from typing import Optional, Callable, Any
from functools import wraps

from .generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
    AudioGenerator, AsyncAudioGenerator
)


def _is_async_context() -> bool:
    """Проверяет, вызван ли код из async контекста"""
    try:
        asyncio.current_task()
        return True
    except RuntimeError:
        return False


def _run_async(coro):
    """Запускает корутину в синхронном контексте"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Мы внутри async контекста - возвращаем корутину
            return coro
        else:
            # Синхронный контекст - запускаем
            return loop.run_until_complete(coro)
    except RuntimeError:
        # Нет event loop - создаём новый
        return asyncio.run(coro)


class HybridGenerator:
    """Базовый класс для гибридных генераторов"""

    def __init__(self, sync_gen, async_gen):
        self._sync = sync_gen
        self._async = async_gen

    def _call(self, method_name: str, *args, **kwargs):
        """Универсальный вызов метода"""
        if _is_async_context():
            # Async контекст - возвращаем корутину
            return getattr(self._async, method_name)(*args, **kwargs)
        else:
            # Sync контекст - вызываем синхронно
            async_method = getattr(self._async, method_name)
            if inspect.iscoroutinefunction(async_method):
                return _run_async(async_method(*args, **kwargs))
            else:
                # Fallback на sync версию
                return getattr(self._sync, method_name)(*args, **kwargs)


class HybridImageGenerator(HybridGenerator):
    """Гибридный генератор изображений"""

    def generate(self, prompt: str, **kwargs) -> bytes:
        """
        Generate an image from a text prompt
        Works in both sync and async contexts!

        Sync usage:
            ai = Blossom()
            image = ai.image.generate("sunset")

        Async usage:
            ai = Blossom()
            image = await ai.image.generate("sunset")
        """
        return self._call('generate', prompt, **kwargs)

    def save(self, prompt: str, filename: str, **kwargs) -> str:
        """Generate and save image to file"""
        return self._call('save', prompt, filename, **kwargs)

    def models(self) -> list:
        """Get list of available image models"""
        return self._call('models')


class HybridTextGenerator(HybridGenerator):
    """Гибридный генератор текста"""

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt
        Works in both sync and async contexts!
        """
        return self._call('generate', prompt, **kwargs)

    def chat(self, messages: list, **kwargs) -> str:
        """Chat completion"""
        return self._call('chat', messages, **kwargs)

    def models(self) -> list:
        """Get list of available text models"""
        return self._call('models')


class HybridAudioGenerator(HybridGenerator):
    """Гибридный генератор аудио"""

    def generate(self, text: str, **kwargs) -> bytes:
        """
        Generate speech audio from text
        Works in both sync and async contexts!
        """
        return self._call('generate', text, **kwargs)

    def save(self, text: str, filename: str, **kwargs) -> str:
        """Generate and save audio to file"""
        return self._call('save', text, filename, **kwargs)

    def voices(self) -> list:
        """Get list of available voices"""
        return self._call('voices')


class Blossom:
    """
    Universal Blossom AI client - works in BOTH sync and async contexts!

    Synchronous usage (no await needed):
        ai = Blossom()
        image = ai.image.generate("sunset")
        text = ai.text.generate("explain AI")
        audio = ai.audio.generate("Hello")

    Asynchronous usage (with await):
        ai = Blossom()
        image = await ai.image.generate("sunset")
        text = await ai.text.generate("explain AI")
        audio = await ai.audio.generate("Hello")

    Context manager for async (auto cleanup):
        async with Blossom() as ai:
            image = await ai.image.generate("sunset")
    """

    def __init__(self, timeout: int = 30, debug: bool = False, api_token: Optional[str] = None):
        """
        Initialize Blossom AI client

        Args:
            timeout: Request timeout in seconds
            debug: Enable debug mode
            api_token: Your Pollinations.AI API token
        """
        # Создаём обе версии генераторов
        sync_image = ImageGenerator(timeout=timeout, api_token=api_token)
        async_image = AsyncImageGenerator(timeout=timeout, api_token=api_token)

        sync_text = TextGenerator(timeout=timeout, api_token=api_token)
        async_text = AsyncTextGenerator(timeout=timeout, api_token=api_token)

        sync_audio = AudioGenerator(timeout=timeout, api_token=api_token)
        async_audio = AsyncAudioGenerator(timeout=timeout, api_token=api_token)

        # Создаём гибридные обёртки
        self.image = HybridImageGenerator(sync_image, async_image)
        self.text = HybridTextGenerator(sync_text, async_text)
        self.audio = HybridAudioGenerator(sync_audio, async_audio)

        self._async_generators = [async_image, async_text, async_audio]
        self.api_token = api_token
        self.timeout = timeout
        self.debug = debug

    async def __aenter__(self):
        """Context manager entry for async usage"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically closes async sessions"""
        await self.close()
        return False

    async def close(self):
        """Close all async sessions (only needed in async context)"""
        for gen in self._async_generators:
            await gen._close_session()

    def __repr__(self) -> str:
        token_status = "with token" if self.api_token else "without token"
        return f"<Blossom AI Client (timeout={self.timeout}s, {token_status})>"


# Обратная совместимость
class AsyncBlossom(Blossom):
    """
    Alias for Blossom (for backward compatibility)

    Note: The main Blossom class now works in both sync and async contexts,
    so using AsyncBlossom is optional.
    """
    pass