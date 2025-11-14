"""
Blossom AI – Session Manager (v0.5.0)
"""

from __future__ import annotations

import asyncio
import threading
from contextlib import asynccontextmanager, contextmanager
from types import SimpleNamespace
from typing import Optional, Dict, Final, Protocol,TypedDict,cast
import aiohttp
import requests

# ==============================================================================
# CONFIGURATION
# ==============================================================================

class _SessionConfig(TypedDict):
    SYNC_POOL_MAXSIZE: int
    SYNC_POOL_CONNECTIONS: int
    SYNC_POOL_BLOCK: bool
    ASYNC_LIMIT_TOTAL: int
    ASYNC_LIMIT_PER_HOST: int
    ASYNC_TTL_DNS_CACHE: int
    ASYNC_TIMEOUT_CONNECT: int
    ASYNC_TIMEOUT_SOCK_READ: int
    USER_AGENT: str
    SSL: bool



SessionConfig = SimpleNamespace(
    SYNC_POOL_MAXSIZE=50,
    SYNC_POOL_CONNECTIONS=20,
    SYNC_POOL_BLOCK=False,
    ASYNC_LIMIT_TOTAL=100,
    ASYNC_LIMIT_PER_HOST=30,
    ASYNC_TTL_DNS_CACHE=300,
    ASYNC_TIMEOUT_CONNECT=30,
    ASYNC_TIMEOUT_SOCK_READ=30,
    USER_AGENT="blossom-ai/0.5.0",
    SSL=True,
)

def validate_session_config() -> None:
    """Validate session configuration values."""
    if SessionConfig.SYNC_POOL_MAXSIZE <= 0:
        raise ValueError("SYNC_POOL_MAXSIZE must be positive")
    if SessionConfig.ASYNC_TIMEOUT_CONNECT <= 0:
        raise ValueError("ASYNC_TIMEOUT_CONNECT must be positive")
    if SessionConfig.ASYNC_LIMIT_TOTAL <= 0:
        raise ValueError("ASYNC_LIMIT_TOTAL must be positive")

# ==============================================================================
# SYNC SESSION MANAGER
# ==============================================================================

class SyncSessionManager:
    __slots__ = ("_session", "_lock", "_closed")

    def __init__(self) -> None:
        validate_session_config()
        self._session: Optional[requests.Session] = None
        self._lock = threading.Lock()
        self._closed = False

    def get_session(self) -> requests.Session:
        if self._closed:
            raise RuntimeError("SyncSessionManager closed")
        if self._session is not None:
            return self._session
        with self._lock:
            if self._session is None:
                self._session = self._create_session()
            return self._session

    @staticmethod
    def _create_session() -> requests.Session:
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=SessionConfig.SYNC_POOL_CONNECTIONS,
            pool_maxsize=SessionConfig.SYNC_POOL_MAXSIZE,
            max_retries=0,
            pool_block=SessionConfig.SYNC_POOL_BLOCK,
        )
        sess = requests.Session()
        sess.mount("http://", adapter)
        sess.mount("https://", adapter)
        sess.headers["User-Agent"] = SessionConfig.USER_AGENT
        sess.headers["Connection"] = "keep-alive"
        sess.verify = SessionConfig.SSL
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

# ==============================================================================
# ASYNC SESSION MANAGER
# ==============================================================================

class AsyncSessionManager:
    __slots__ = ("_sessions", "_lock", "_closed")

    def __init__(self) -> None:
        validate_session_config()
        self._sessions: Dict[int, aiohttp.ClientSession] = {}
        self._lock: Optional[asyncio.Lock] = None
        self._closed = False

    async def get_session(self) -> aiohttp.ClientSession:
        if self._closed:
            raise RuntimeError("AsyncSessionManager closed")

        loop = asyncio.get_running_loop()
        loop_id = id(loop)

        session = self._sessions.get(loop_id)
        if session and self._is_alive(session):
            return session

        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            session = self._sessions.get(loop_id)
            if session and self._is_alive(session):
                return session
            if session:
                await self._close_one(loop_id)

            new_sess = self._create_session()
            self._sessions[loop_id] = new_sess
            return new_sess

    @staticmethod
    def _create_session() -> aiohttp.ClientSession:
        connector = aiohttp.TCPConnector(
            limit=SessionConfig.ASYNC_LIMIT_TOTAL,
            limit_per_host=SessionConfig.ASYNC_LIMIT_PER_HOST,
            ttl_dns_cache=SessionConfig.ASYNC_TTL_DNS_CACHE,
            ssl=SessionConfig.SSL,
            enable_cleanup_closed=True,
            force_close=False,
        )
        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=SessionConfig.ASYNC_TIMEOUT_CONNECT,
            sock_read=SessionConfig.ASYNC_TIMEOUT_SOCK_READ,
        )
        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": SessionConfig.USER_AGENT},
            raise_for_status=False,
        )

    @staticmethod
    def _is_alive(session: aiohttp.ClientSession) -> bool:
        return not session.closed and bool(session.connector and not session.connector.closed)

    async def _close_one(self, loop_id: int) -> None:
        session = self._sessions.pop(loop_id, None)
        if session and not session.closed:
            await session.close()

    async def close(self) -> None:
        if self._closed:
            return
        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            await asyncio.gather(
                *(self._close_one(lid) for lid in list(self._sessions.keys())),
                return_exceptions=True,
            )
            self._closed = True

    def is_closed(self) -> bool:
        return self._closed

    async def __aenter__(self) -> AsyncSessionManager:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

@contextmanager
def get_sync_session():
    mgr = SyncSessionManager()
    try:
        yield mgr.get_session()
    finally:
        mgr.close()

@asynccontextmanager
async def get_async_session():
    mgr = AsyncSessionManager()
    try:
        yield await mgr.get_session()
    finally:
        await mgr.close()