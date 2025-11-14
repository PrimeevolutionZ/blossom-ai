"""
Blossom AI – Universal Client (v0.5.0)
V2 API only (enter.pollinations.ai)
"""

from __future__ import annotations
from contextlib import AbstractContextManager, AbstractAsyncContextManager
import asyncio
import inspect
from contextlib import AbstractContextManager
from typing import (
    Any, Awaitable, Callable, Dict, Generator, Generic, Iterator,
    Optional, TypeVar, Union, cast
)

from blossom_ai.generators.generators import (
    ImageGenerator, AsyncImageGenerator,
    TextGenerator, AsyncTextGenerator,
)


# --------------------------------------------------------------------------- #
# low-level utils
# --------------------------------------------------------------------------- #
def _is_inside_event_loop() -> bool:
    """Returns True if an event loop is already running."""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def _ensure_sync(coro: Awaitable[T]) -> T:
    """Runs a coroutine synchronously, if safe to do so."""
    if _is_inside_event_loop():
        raise RuntimeError(
            "Cannot run async code from sync when an event loop is already running. "
            "Use `await` or call from a truly synchronous context."
        )
    return asyncio.run(coro)


T = TypeVar("T")
R = TypeVar("R")


class _DualCaller(Generic[T, R]):
    """
    Internal helper: holds sync and async versions of the same object
    and delegates method calls to the correct one based on execution context.
    """

    __slots__ = ("_sync", "_async", "_name")

    def __init__(self, sync_obj: T, async_obj: T, name: str = "") -> None:
        self._sync = sync_obj
        self._async = async_obj
        self._name = name

    def _pick(self) -> T:
        """Returns the appropriate implementation depending on context."""
        return self._async if _is_inside_event_loop() else self._sync

    # universal call dispatcher
    def __call__(self, __method: str, *args: Any, **kw: Any) -> R:
        target = self._pick()
        method: Callable[..., R] = getattr(target, __method)
        result = method(*args, **kw)

        # return generators/iterators as-is
        if inspect.isgenerator(result) or isinstance(result, Iterator):
            return result

        # synchronize coroutine if outside event loop
        if inspect.iscoroutine(result):
            if _is_inside_event_loop():
                return result  # type: ignore
            return _ensure_sync(result)  # type: ignore
        return result


# --------------------------------------------------------------------------- #
# Hybrid wrappers
# --------------------------------------------------------------------------- #
class HybridImageGenerator:
    """Synchronous-asynchronous image generator."""

    def __init__(self, sync_gen: ImageGenerator, async_gen: AsyncImageGenerator):
        self._caller = _DualCaller(sync_gen, async_gen, "image")

    # fmt: off
    def generate(self, prompt: str, **kw: Any) -> bytes:                       return self._caller("generate", prompt, **kw)          # type: ignore
    def generate_url(self, prompt: str, **kw: Any) -> str:                     return self._caller("generate_url", prompt, **kw)      # type: ignore
    def save(self, prompt: str, filename: str, **kw: Any) -> str:              return self._caller("save", prompt, filename, **kw)    # type: ignore
    def models(self) -> list:                                                    return self._caller("models")                            # type: ignore
    # fmt: on


class HybridTextGenerator:
    """Synchronous-asynchronous text generator."""

    def __init__(self, sync_gen: TextGenerator, async_gen: AsyncTextGenerator):
        self._caller = _DualCaller(sync_gen, async_gen, "text")

    # fmt: off
    def generate(self, prompt: str, **kw: Any) -> Union[str, Iterator[str]]:    return self._caller("generate", prompt, **kw)          # type: ignore
    def chat(self, messages: list, **kw: Any) -> Union[str, Iterator[str]]:    return self._caller("chat", messages, **kw)            # type: ignore
    def models(self) -> list:                                                    return self._caller("models")                            # type: ignore
    # fmt: on


# --------------------------------------------------------------------------- #
# Main client
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
        self._api_token = api_token  # private field — excluded from repr

        # instantiate generators
        self.image = HybridImageGenerator(
            ImageGenerator(timeout=timeout, api_token=api_token),
            AsyncImageGenerator(timeout=timeout, api_token=api_token),
        )
        self.text = HybridTextGenerator(
            TextGenerator(timeout=timeout, api_token=api_token),
            AsyncTextGenerator(timeout=timeout, api_token=api_token),
        )

        # for closing sessions
        self._sync_gens = (self.image._caller._sync, self.text._caller._sync)
        self._async_gens = (self.image._caller._async, self.text._caller._async)

    # --- sync context ------------------------------------------------------------
    def __enter__(self) -> Blossom:
        return self

    def __exit__(self, *_: Any) -> None:
        self._close_sync()

    # --- async context -----------------------------------------------------------
    async def __aenter__(self) -> Blossom:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._close_async()

    # --- resource cleanup --------------------------------------------------------
    def _close_sync(self) -> None:
        for gen in self._sync_gens:
            try:
                if hasattr(gen, "close") and callable(gen.close):
                    gen.close()
            except Exception:  # noqa: S110
                pass

    async def _close_async(self) -> None:
        for gen in self._async_gens:
            try:
                if hasattr(gen, "close") and inspect.iscoroutinefunction(gen.close):
                    await gen.close()
                elif hasattr(gen, "_session_manager"):
                    await gen._session_manager.close()
            except Exception:  # noqa: S110
                pass

    # --- debug / repr ------------------------------------------------------------
    def __repr__(self) -> str:
        token_info = "with token" if self._api_token else "without token"
        return f"<Blossom AI v0.5.0 (V2 API, {self.timeout}s, {token_info})>"


# --------------------------------------------------------------------------- #
# Factory
# --------------------------------------------------------------------------- #
def create_client(api_token: Optional[str] = None, **kw: Any) -> Blossom:
    """Instantiates a client in one line."""
    return Blossom(api_token=api_token, **kw)