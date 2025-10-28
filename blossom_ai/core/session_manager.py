"""
Blossom AI - Session Manager
Fixed async session cleanup without __del__ anti-patterns
"""

import asyncio
import atexit
from typing import Dict, Optional
import aiohttp
import requests


class SyncSessionManager:
    """Manages synchronous requests sessions"""

    def __init__(self):
        self._session: Optional[requests.Session] = None
        self._closed = False

    def get_session(self) -> requests.Session:
        """Get or create requests session"""
        if self._closed:
            raise RuntimeError("SessionManager has been closed")

        if self._session is None:
            self._session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=10,
                pool_maxsize=20,
                max_retries=0  # We handle retries ourselves
            )
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)

        return self._session

    def close(self):
        """Close the session"""
        if self._session is not None and not self._closed:
            try:
                self._session.close()
            except Exception:
                pass
            finally:
                self._session = None
                self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class AsyncSessionManager:
    """
    Manages asynchronous aiohttp sessions across event loops
    Uses atexit for cleanup instead of __del__ to avoid ResourceWarnings
    """

    # Class-level registry for cleanup at exit
    _global_sessions: Dict[int, aiohttp.ClientSession] = {}
    _cleanup_registered = False

    def __init__(self):
        self._sessions: Dict[int, aiohttp.ClientSession] = {}
        self._closed = False

        # Register global cleanup on first instance
        if not AsyncSessionManager._cleanup_registered:
            AsyncSessionManager._register_global_cleanup()
            AsyncSessionManager._cleanup_registered = True

    @classmethod
    def _register_global_cleanup(cls):
        """Register cleanup at exit to close all sessions"""
        def cleanup_all_sessions():
            """Synchronous cleanup at program exit"""
            if not cls._global_sessions:
                return

            try:
                # Create new event loop for cleanup
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                async def close_all():
                    for session in list(cls._global_sessions.values()):
                        if not session.closed:
                            try:
                                await session.close()
                            except Exception:
                                pass

                loop.run_until_complete(close_all())
                loop.close()
            except Exception:
                pass
            finally:
                cls._global_sessions.clear()

        atexit.register(cleanup_all_sessions)

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session for current event loop"""
        if self._closed:
            raise RuntimeError("AsyncSessionManager has been closed")

        try:
            loop = asyncio.get_running_loop()
            loop_id = id(loop)
        except RuntimeError:
            raise RuntimeError("No event loop is running")

        # Check if session exists and is valid
        if loop_id in self._sessions:
            session = self._sessions[loop_id]
            try:
                if not session.closed and session.connector is not None:
                    return session
            except Exception:
                pass

            # Remove broken session
            del self._sessions[loop_id]
            if loop_id in self._global_sessions:
                del self._global_sessions[loop_id]

        # Create new session with optimized settings
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )

        timeout = aiohttp.ClientTimeout(
            total=None,  # We handle timeout per-request
            connect=30,
            sock_read=30
        )

        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )

        # Store in both registries
        self._sessions[loop_id] = session
        self._global_sessions[loop_id] = session

        return session

    async def close(self):
        """Close all sessions owned by this manager"""
        for loop_id, session in list(self._sessions.items()):
            if not session.closed:
                try:
                    await session.close()
                except Exception:
                    pass

            # Remove from global registry
            if loop_id in self._global_sessions:
                del self._global_sessions[loop_id]

        self._sessions.clear()
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False