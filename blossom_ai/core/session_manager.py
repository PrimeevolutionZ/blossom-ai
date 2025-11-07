"""
Blossom AI - Session Manager
"""

import asyncio
import atexit
import threading
import weakref
from typing import Dict, Optional, Final
from contextlib import contextmanager, asynccontextmanager

import aiohttp
import requests


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class SessionConfig:
    """Configuration for session managers"""
    # Sync session settings
    SYNC_POOL_CONNECTIONS: Final[int] = 20
    SYNC_POOL_MAXSIZE: Final[int] = 50
    SYNC_POOL_BLOCK: Final[bool] = False

    # Async session settings
    ASYNC_LIMIT_TOTAL: Final[int] = 100
    ASYNC_LIMIT_PER_HOST: Final[int] = 30
    ASYNC_TTL_DNS_CACHE: Final[int] = 300
    ASYNC_CONNECT_TIMEOUT: Final[int] = 30
    ASYNC_SOCK_READ_TIMEOUT: Final[int] = 30
    # Common settings
    USER_AGENT: Final[str] = "blossom-ai/0.4.3-fixed"


# ==============================================================================
# SYNC SESSION MANAGER
# ==============================================================================

class SyncSessionManager:
    """
    Manages synchronous HTTP sessions with connection pooling

    """

    def __init__(self):
        self._session: Optional[requests.Session] = None
        self._closed = False
        self._lock = threading.Lock()

    def get_session(self) -> requests.Session:
        """Get or create an optimized requests session"""
        if self._closed:
            raise RuntimeError("SessionManager has been closed")

        with self._lock:
            if self._session is None:
                self._session = self._create_session()

        return self._session

    def _create_session(self) -> requests.Session:
        """Create and configure a new session"""
        session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=SessionConfig.SYNC_POOL_CONNECTIONS,
            pool_maxsize=SessionConfig.SYNC_POOL_MAXSIZE,
            max_retries=0,
            pool_block=SessionConfig.SYNC_POOL_BLOCK
        )

        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.headers.update({
            'Connection': 'keep-alive',
            'User-Agent': SessionConfig.USER_AGENT
        })

        session.verify = True

        return session

    def close(self) -> None:
        """Close the session and release resources"""
        with self._lock:
            if self._session is not None and not self._closed:
                try:
                    self._session.close()
                except Exception:
                    pass
                finally:
                    self._session = None
                    self._closed = True

    def is_closed(self) -> bool:
        """Check if manager is closed"""
        return self._closed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __del__(self):
        """Ensure cleanup on deletion"""
        if not self._closed:
            self.close()


# ==============================================================================
# ASYNC SESSION MANAGER (FIXED)
# ==============================================================================

class AsyncSessionManager:
    """
    Manages asynchronous HTTP sessions across event loops

    """

    # FIX: Use WeakValueDictionary to prevent memory leaks
    _global_sessions: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
    _global_lock = threading.Lock()
    _cleanup_registered = False

    def __init__(self):
        self._sessions: Dict[int, aiohttp.ClientSession] = {}
        self._closed = False
        self._lock: Optional[asyncio.Lock] = None

        # Register cleanup on first instantiation
        self._ensure_cleanup_registered()

    @classmethod
    def _ensure_cleanup_registered(cls):
        """
        Register global cleanup handler (once)

        """
        with cls._global_lock:
            if not cls._cleanup_registered:
                # FIX: Don't use atexit for async cleanup
                # Instead, rely on __del__ and weakref
                cls._cleanup_registered = True

    @classmethod
    def _sync_cleanup_session(cls, session: aiohttp.ClientSession):
        """
        Synchronous cleanup for a single session


        """
        try:
            if not session.closed and session.connector:
                # Close connector synchronously (doesn't need event loop)
                if hasattr(session.connector, '_close'):
                    session.connector._close()
        except Exception:
            pass

    async def _get_lock(self) -> asyncio.Lock:
        """Get or create async lock for current event loop"""
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    def _is_session_valid(self, session: aiohttp.ClientSession) -> bool:
        """Check if session is still valid"""
        try:
            return (
                not session.closed
                and session.connector is not None
                and not session.connector.closed
            )
        except Exception:
            return False

    async def get_session(self) -> aiohttp.ClientSession:
        """
        Get or create session for current event loop


        """
        if self._closed:
            raise RuntimeError("AsyncSessionManager has been closed")

        try:
            loop = asyncio.get_running_loop()
            loop_id = id(loop)
        except RuntimeError:
            raise RuntimeError("No event loop is running")

        lock = await self._get_lock()

        async with lock:
            # FIX: Prune dead sessions from global cache
            self._prune_dead_sessions()

            # Check existing session
            if loop_id in self._sessions:
                session = self._sessions[loop_id]
                if self._is_session_valid(session):
                    return session

                # Clean up invalid session
                await self._cleanup_session(loop_id)

            # Create new session
            session = self._create_session()
            self._sessions[loop_id] = session

            # FIX: Register globally with weakref
            with self._global_lock:
                self._global_sessions[loop_id] = session

            return session

    def _prune_dead_sessions(self):
        """
        Remove dead sessions from local cache
        """
        dead_loops = []

        for loop_id, session in list(self._sessions.items()):
            if not self._is_session_valid(session):
                dead_loops.append(loop_id)

        for loop_id in dead_loops:
            del self._sessions[loop_id]

    def _create_session(self) -> aiohttp.ClientSession:
        """Create and configure a new async session"""
        connector = aiohttp.TCPConnector(
            limit=SessionConfig.ASYNC_LIMIT_TOTAL,
            limit_per_host=SessionConfig.ASYNC_LIMIT_PER_HOST,
            ttl_dns_cache=SessionConfig.ASYNC_TTL_DNS_CACHE,
            enable_cleanup_closed=True,
            force_close=True,
            # FIX: Ensure SSL verification
            ssl=True
        )

        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=SessionConfig.ASYNC_CONNECT_TIMEOUT,
            sock_read=SessionConfig.ASYNC_SOCK_READ_TIMEOUT
        )

        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            raise_for_status=False,
            headers={'User-Agent': SessionConfig.USER_AGENT}
        )

    async def _cleanup_session(self, loop_id: int):
        """Cleanup a specific session"""
        if loop_id in self._sessions:
            session = self._sessions[loop_id]
            try:
                if not session.closed:
                    await session.close()
            except Exception:
                pass
            finally:
                del self._sessions[loop_id]

                with self._global_lock:
                    # Weakref dict will auto-remove when object is gone
                    if loop_id in self._global_sessions:
                        del self._global_sessions[loop_id]

    async def close(self):
        """Close all sessions managed by this instance"""
        if self._closed:
            return

        lock = await self._get_lock()

        async with lock:
            for loop_id in list(self._sessions.keys()):
                await self._cleanup_session(loop_id)

            self._closed = True

    def is_closed(self) -> bool:
        """Check if manager is closed"""
        return self._closed

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __del__(self):
        """
        Cleanup on deletion
        
        """
        for session in list(self._sessions.values()):
            self._sync_cleanup_session(session)
        self._sessions.clear()


# ==============================================================================
# CONVENIENCE CONTEXT MANAGERS
# ==============================================================================

@contextmanager
def get_sync_session():
    """
    Convenience context manager for sync sessions

    Usage:
        with get_sync_session() as session:
            response = session.get(url)
    """
    manager = SyncSessionManager()
    try:
        yield manager.get_session()
    finally:
        manager.close()


@asynccontextmanager
async def get_async_session():
    """
    Convenience context manager for async sessions

    Usage:
        async with get_async_session() as session:
            response = await session.get(url)
    """
    manager = AsyncSessionManager()
    try:
        yield await manager.get_session()
    finally:
        await manager.close()