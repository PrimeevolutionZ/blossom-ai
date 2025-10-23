"""
Blossom AI - Session Manager (Enhanced)
Enhanced session lifecycle management with better error handling
"""

import asyncio
import weakref
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
            # Set reasonable defaults
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
        if self._session is not None:
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

    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.close()
        except Exception:
            pass


class AsyncSessionManager:
    """Manages asynchronous aiohttp sessions across event loops"""

    def __init__(self):
        self._sessions: Dict[int, aiohttp.ClientSession] = {}
        self._lock = asyncio.Lock()
        self._closed = False
        self._cleanup_registered = False

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session for current event loop"""
        if self._closed:
            raise RuntimeError("AsyncSessionManager has been closed")

        try:
            loop = asyncio.get_running_loop()
            loop_id = id(loop)
        except RuntimeError:
            raise RuntimeError("No event loop is running")

        async with self._lock:
            # Check if session exists and is valid
            if loop_id in self._sessions:
                session = self._sessions[loop_id]
                try:
                    # Verify session is actually usable
                    if not session.closed and session.connector is not None:
                        return session
                except Exception:
                    pass

                # Remove broken session
                del self._sessions[loop_id]

            # Create new session with optimized settings
            connector = aiohttp.TCPConnector(
                limit=100,  # Total connection limit
                limit_per_host=30,  # Per-host limit
                ttl_dns_cache=300,  # DNS cache TTL in seconds
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

            self._sessions[loop_id] = session

            # Register cleanup on first session creation
            if not self._cleanup_registered:
                self._register_cleanup()
                self._cleanup_registered = True

            return session

    def _register_cleanup(self):
        """Register cleanup handler using weakref"""
        # Store reference to sessions dict for cleanup
        sessions_dict = self._sessions

        def cleanup(ref):
            """Called when manager is garbage collected"""
            try:
                # Create temporary event loop for cleanup
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                async def close_all():
                    for session in list(sessions_dict.values()):
                        if not session.closed:
                            try:
                                await session.close()
                            except Exception:
                                pass

                loop.run_until_complete(close_all())
                loop.close()
            except Exception:
                pass

        # Use weakref.finalize on self
        weakref.finalize(self, cleanup, None)

    async def close(self):
        """Close all sessions"""
        async with self._lock:
            for loop_id, session in list(self._sessions.items()):
                if not session.closed:
                    try:
                        await session.close()
                    except Exception:
                        pass

            self._sessions.clear()
            self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __del__(self):
        """Cleanup on destruction"""
        # weakref.finalize will handle cleanup if possible
        pass