"""
Blossom AI – Universal Client (v0.5.4)
Single hybrid facade, no manual proxying, keeps public API 100 % intact.
"""

from __future__ import annotations

import asyncio
import inspect
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from typing import (
    Any, Awaitable, Callable, Dict, Iterator, AsyncIterator,
    Optional, TypeVar, Union, cast,
)

# импортируем уже отрефакторенные генераторы
from blossom_ai.generators.generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
    AudioGenerator, AsyncAudioGenerator,
)

# --------------------------------------------------------------------------- #
# utils
# --------------------------------------------------------------------------- #

def _is_inside_event_loop() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

T = TypeVar("T")

def _ensure_sync(coro: Awaitable[T]) -> T:
    if _is_inside_event_loop():
        raise RuntimeError(
            "Cannot run async code from sync when an event loop is already running. "
            "Use `await` instead of synchronous call, or run from a truly synchronous context."
        )
    return asyncio.run(coro)

# --------------------------------------------------------------------------- #
# Universal dual-caller (internal)
# --------------------------------------------------------------------------- #

class _DualCaller:
    __slots__ = ("_sync", "_async", "_name")

    def __init__(self, sync_obj: Any, async_obj: Any, name: str = "") -> None:
        self._sync = sync_obj
        self._async = async_obj
        self._name = name

    def _pick(self) -> Any:
        return self._async if _is_inside_event_loop() else self._sync

    def __getattr__(self, name: str) -> Callable[..., Any]:
        target = self._pick()
        method = getattr(target, name)
        if inspect.isgeneratorfunction(method) or name == "models":
            # генераторы / итераторы отдаём как есть
            return method

        def _wrapper(*args: Any, **kw: Any) -> Any:
            result = method(*args, **kw)
            if inspect.iscoroutine(result):
                if _is_inside_event_loop():
                    return result  # в Jupyter – возвращаем корутину
                return _ensure_sync(result)  # вне цикла – синхронно
            return result

        return _wrapper

# --------------------------------------------------------------------------- #
# Hybrid facades
# --------------------------------------------------------------------------- #

class HybridImageGenerator:
    def __init__(self, sync_gen: ImageGenerator, async_gen: AsyncImageGenerator):
        self._caller = _DualCaller(sync_gen, async_gen, "image")

    # публичное API проксируется динамически
    generate = property(lambda self: self._caller.generate)
    generate_url = property(lambda self: self._caller.generate_url)
    save = property(lambda self: self._caller.save)
    models = property(lambda self: self._caller.models)


class HybridTextGenerator:
    def __init__(self, sync_gen: TextGenerator, async_gen: AsyncTextGenerator):
        self._caller = _DualCaller(sync_gen, async_gen, "text")

    generate = property(lambda self: self._caller.generate)
    chat = property(lambda self: self._caller.chat)
    models = property(lambda self: self._caller.models)


class HybridAudioGenerator:
    def __init__(self, sync_gen: AudioGenerator, async_gen: AsyncAudioGenerator):
        self._caller = _DualCaller(sync_gen, async_gen, "audio")

    generate = property(lambda self: self._caller.generate)
    save = property(lambda self: self._caller.save)


# --------------------------------------------------------------------------- #
# Main universal client
# --------------------------------------------------------------------------- #

class Blossom(AbstractContextManager, AbstractAsyncContextManager):
    """
    Universal Blossom AI client (V2 API).
    Works both in synchronous and asynchronous mode without changing the caller's code.
    """

    def __init__(
        self,
        *,
        timeout: int = 30,
        debug: bool = False,
        api_token: Optional[str] = None,
    ) -> None:
        self.timeout = timeout
        self.debug = debug
        self._api_token = api_token

        # гибридные генераторы
        self.image = HybridImageGenerator(
            ImageGenerator(timeout=timeout, api_token=api_token),
            AsyncImageGenerator(timeout=timeout, api_token=api_token),
        )
        self.text = HybridTextGenerator(
            TextGenerator(timeout=timeout, api_token=api_token),
            AsyncTextGenerator(timeout=timeout, api_token=api_token),
        )
        self.audio = HybridAudioGenerator(
            AudioGenerator(timeout=timeout, api_token=api_token),
            AsyncAudioGenerator(timeout=timeout, api_token=api_token),
        )

        # для закрытия
        self._sync_gens = (
            self.image._caller._sync,
            self.text._caller._sync,
            self.audio._caller._sync,
        )
        self._async_gens = (
            self.image._caller._async,
            self.text._caller._async,
            self.audio._caller._async,
        )

    # ---------- sync context ----------
    def __enter__(self) -> Blossom:
        return self

    def __exit__(self, *_: Any) -> None:
        self._close_sync()

    # ---------- async context ----------
    async def __aenter__(self) -> Blossom:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._close_async()

    # ---------- resource cleanup ----------
    def _close_sync(self) -> None:
        for gen in self._sync_gens:
            if hasattr(gen, "close") and callable(gen.close):
                try:
                    gen.close()
                except Exception:
                    pass  # noqa: S110

    async def _close_async(self) -> None:
        for gen in self._async_gens:
            if hasattr(gen, "close"):
                if inspect.iscoroutinefunction(gen.close):
                    try:
                        await gen.close()
                    except Exception:
                        pass
                else:
                    try:
                        gen.close()
                    except Exception:
                        pass

    # ---------- repr ----------
    def __repr__(self) -> str:
        token_info = "with token" if self._api_token else "without token"
        return f"<Blossom AI v0.5.4 (V2 API, {self.timeout}s, {token_info})>"


# --------------------------------------------------------------------------- #
# Factory
# --------------------------------------------------------------------------- #

def create_client(api_token: Optional[str] = None, **kw: Any) -> Blossom:
    """One-line factory."""
    return Blossom(api_token=api_token, **kw)