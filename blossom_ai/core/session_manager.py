"""
Blossom AI – Session Manager (v0.5.3-clean)
Ultra-fast, leak-free sync & async HTTP-pools
"""

from __future__ import annotations

import atexit
import asyncio
import threading
from contextlib import asynccontextmanager, contextmanager
from typing import Optional, Dict, Final

import aiohttp
import requests


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class _Cfg:
    SYNC_POOL_MAXSIZE: Final      = 50
    SYNC_POOL_CONNECTIONS: Final  = 20
    SYNC_POOL_BLOCK: Final        = False

    ASYNC_LIMIT_TOTAL: Final      = 100
    ASYNC_LIMIT_PER_HOST: Final   = 30
    ASYNC_TTL_DNS_CACHE: Final    = 300
    ASYNC_TIMEOUT_CONNECT: Final  = 30
    ASYNC_TIMEOUT_SOCK_READ: Final = 30

    USER_AGENT: Final = "blossom-ai/0.5.3"


# ==============================================================================
# SYNC SESSION MANAGER
# ==============================================================================

class SyncSessionManager:
    __slots__ = ("_session", "_lock", "_closed")

    def __init__(self) -> None:
        self._session: Optional[requests.Session] = None
        self._lock   = threading.Lock()
        self._closed = False

    # --------------------
    def get_session(self) -> requests.Session:
        if self._closed:
            raise RuntimeError("SyncSessionManager closed")
        if (session := self._session) is not None:
            return session
        with self._lock:
            if self._session is None:
                self._session = self._create_session()
            return self._session

    # --------------------
    def _create_session(self) -> requests.Session:
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=_Cfg.SYNC_POOL_CONNECTIONS,
            pool_maxsize=_Cfg.SYNC_POOL_MAXSIZE,
            max_retries=0,
            pool_block=_Cfg.SYNC_POOL_BLOCK,
        )
        sess = requests.Session()
        sess.mount("http://", adapter)
        sess.mount("https://", adapter)
        sess.headers["User-Agent"] = _Cfg.USER_AGENT
        sess.headers["Connection"] = "keep-alive"
        sess.verify = True
        return sess

    # --------------------
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

    # --------------------
    def __enter__(self) -> SyncSessionManager:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


# ==============================================================================
# ASYNC SESSION MANAGER
# ==============================================================================

class AsyncSessionManager:
    __slots__ = ("_sessions", "_lock", "_closed")

    _global_sessions: Dict[int, aiohttp.ClientSession] = {}
    _global_lock = threading.Lock()

    def __init__(self) -> None:
        self._sessions: Dict[int, aiohttp.ClientSession] = {}
        self._lock: Optional[asyncio.Lock] = None
        self._closed = False

    # --------------------
    async def get_session(self) -> aiohttp.ClientSession:
        if self._closed:
            raise RuntimeError("AsyncSessionManager closed")

        loop = asyncio.get_running_loop()
        loop_id = id(loop)

        # fast-path
        if (session := self._sessions.get(loop_id)) and self._is_alive(session):
            return session

        # slow-path
        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            session = self._sessions.get(loop_id)
            if session and self._is_alive(session):
                return session
            if session:  # dead
                await self._close_one(loop_id)

            new_sess = self._create_session()
            self._sessions[loop_id] = new_sess
            with self._global_lock:
                self._global_sessions[loop_id] = new_sess
            return new_sess

    # --------------------
    def _create_session(self) -> aiohttp.ClientSession:
        connector = aiohttp.TCPConnector(
            limit=_Cfg.ASYNC_LIMIT_TOTAL,
            limit_per_host=_Cfg.ASYNC_LIMIT_PER_HOST,
            ttl_dns_cache=_Cfg.ASYNC_TTL_DNS_CACHE,
            ssl=True,
            enable_cleanup_closed=True,
            force_close=False,
        )
        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=_Cfg.ASYNC_TIMEOUT_CONNECT,
            sock_read=_Cfg.ASYNC_TIMEOUT_SOCK_READ,
        )
        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": _Cfg.USER_AGENT},
            raise_for_status=False,
        )

    # --------------------
    @staticmethod
    def _is_alive(session: aiohttp.ClientSession) -> bool:
        return not session.closed and bool(session.connector and not session.connector.closed)

    # --------------------
    async def _close_one(self, loop_id: int) -> None:
        session = self._sessions.pop(loop_id, None)
        if session and not session.closed:
            await session.close()
        with self._global_lock:
            self._global_sessions.pop(loop_id, None)

    # --------------------
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

    # --------------------
    async def __aenter__(self) -> AsyncSessionManager:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # --------------------
    @classmethod
    def close_all_global(cls) -> None:
        with cls._global_lock:
            loops = list(cls._global_sessions.items())
            cls._global_sessions.clear()
        for loop_id, session in loops:
            if not session.closed:
                if session.connector:
                    session.connector._close()


# ==============================================================================
# Утилиты-контекст-менеджеры
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


# ==============================================================================
# Регистрация очистки при выгрузке
# ==============================================================================

atexit.register(AsyncSessionManager.close_all_global)