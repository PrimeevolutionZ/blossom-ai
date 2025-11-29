"""
Blossom AI – Session Manager (v0.5.4)
"""

from __future__ import annotations

import asyncio
import threading
import weakref
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from typing import Dict, Optional, ClassVar, Final

import aiohttp
import requests

# --------------------------------------------------------------------------- #
# Immutable configuration
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class SessionConfig:
    SYNC_POOL_MAXSIZE: int = 50
    SYNC_POOL_CONNECTIONS: int = 20
    SYNC_POOL_BLOCK: bool = False
    ASYNC_LIMIT_TOTAL: int = 100
    ASYNC_LIMIT_PER_HOST: int = 30
    ASYNC_TTL_DNS_CACHE: int = 300
    ASYNC_TIMEOUT_CONNECT: int = 30
    ASYNC_TIMEOUT_SOCK_READ: int = 30
    USER_AGENT: str = "blossom-ai/0.5.4"
    SSL: bool = True

    def __post_init__(self) -> None:
        for name in ("SYNC_POOL_MAXSIZE", "ASYNC_LIMIT_TOTAL", "ASYNC_TIMEOUT_CONNECT"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")

# singleton instance
DEFAULT_CONFIG: Final = SessionConfig()

# --------------------------------------------------------------------------- #
# Sync manager – thread-local singleton
# --------------------------------------------------------------------------- #

class SyncSessionManager:
    __slots__ = ("_session", "_lock", "_config", "_closed", "_initialized")

    _INSTANCES: ClassVar[threading.local] = threading.local()

    def __new__(cls, config: SessionConfig = DEFAULT_CONFIG) -> SyncSessionManager:
        if not hasattr(cls._INSTANCES, "data"):
            cls._INSTANCES.data = {}  # type: ignore
        key = id(config)
        if key not in cls._INSTANCES.data:  # type: ignore
            cls._INSTANCES.data[key] = super().__new__(cls)  # type: ignore
        return cls._INSTANCES.data[key]  # type: ignore

    def __init__(self, config: SessionConfig = DEFAULT_CONFIG) -> None:
        if hasattr(self, "_initialized"):
            return
        self._config = config
        self._session: Optional[requests.Session] = None
        self._lock = threading.Lock()
        self._closed = False
        self._initialized = True

    def get_session(self) -> requests.Session:
        if self._closed:
            raise RuntimeError("SyncSessionManager closed")
        if self._session is not None:
            return self._session
        with self._lock:
            if self._session is None:
                self._session = self._create_session()
            return self._session

    def _create_session(self) -> requests.Session:
        cfg = self._config
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=cfg.SYNC_POOL_CONNECTIONS,
            pool_maxsize=cfg.SYNC_POOL_MAXSIZE,
            max_retries=0,
            pool_block=cfg.SYNC_POOL_BLOCK,
        )
        sess = requests.Session()
        sess.mount("http://", adapter)
        sess.mount("https://", adapter)
        sess.headers["User-Agent"] = cfg.USER_AGENT
        sess.headers["Connection"] = "keep-alive"
        sess.verify = cfg.SSL
        return sess

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._session:
                self._session.close()
                self._session = None
            self._closed = True

    def is_closed(self) -> bool:
        return self._closed

    def __enter__(self) -> SyncSessionManager:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

# --------------------------------------------------------------------------- #
# Async manager – per-loop singleton via WeakKeyDictionary
# --------------------------------------------------------------------------- #

class AsyncSessionManager:
    __slots__ = ("_sessions", "_lock", "_config", "_closed", "_initialized")

    _INSTANCES: ClassVar[weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, AsyncSessionManager]] = weakref.WeakKeyDictionary()  # type: ignore

    def __new__(cls, config: SessionConfig = DEFAULT_CONFIG) -> AsyncSessionManager:
        loop = asyncio.get_running_loop()
        if loop not in cls._INSTANCES:
            cls._INSTANCES[loop] = super().__new__(cls)
        return cls._INSTANCES[loop]

    def __init__(self, config: SessionConfig = DEFAULT_CONFIG) -> None:
        if hasattr(self, "_initialized"):
            return
        self._config = config
        self._sessions: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, aiohttp.ClientSession] = weakref.WeakKeyDictionary()
        self._lock = asyncio.Lock()
        self._closed = False
        self._initialized = True

    async def get_session(self) -> aiohttp.ClientSession:
        if self._closed:
            raise RuntimeError("AsyncSessionManager closed")
        loop = asyncio.get_running_loop()
        session = self._sessions.get(loop)
        if session and self._is_alive(session):
            return session
        async with self._lock:
            session = self._sessions.get(loop)
            if session and self._is_alive(session):
                return session
            new_sess = self._create_session()
            self._sessions[loop] = new_sess
            return new_sess

    def _create_session(self) -> aiohttp.ClientSession:
        cfg = self._config
        connector = aiohttp.TCPConnector(
            limit=cfg.ASYNC_LIMIT_TOTAL,
            limit_per_host=cfg.ASYNC_LIMIT_PER_HOST,
            ttl_dns_cache=cfg.ASYNC_TTL_DNS_CACHE,
            ssl=cfg.SSL,
            enable_cleanup_closed=True,
            force_close=False,
        )
        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=cfg.ASYNC_TIMEOUT_CONNECT,
            sock_read=cfg.ASYNC_TIMEOUT_SOCK_READ,
        )
        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": cfg.USER_AGENT},
            raise_for_status=False,
        )

    @staticmethod
    def _is_alive(session: aiohttp.ClientSession) -> bool:
        return not session.closed and bool(session.connector and not session.connector.closed)

    async def close(self) -> None:
        if self._closed:
            return
        async with self._lock:
            await asyncio.gather(
                *(sess.close() for sess in self._sessions.values() if not sess.closed),
                return_exceptions=True,
            )
            self._closed = True

    def is_closed(self) -> bool:
        return self._closed

    async def __aenter__(self) -> AsyncSessionManager:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

# --------------------------------------------------------------------------- #
# Convenience-shared singleton managers
# --------------------------------------------------------------------------- #

@contextmanager
def get_sync_session(config: SessionConfig = DEFAULT_CONFIG):
    mgr = SyncSessionManager(config)
    try:
        yield mgr.get_session()
    finally:
        pass

@asynccontextmanager
async def get_async_session(config: SessionConfig = DEFAULT_CONFIG):
    mgr = AsyncSessionManager(config)
    try:
        yield await mgr.get_session()
    finally:
        pass