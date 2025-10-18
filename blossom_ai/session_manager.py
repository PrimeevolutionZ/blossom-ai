"""
Blossom AI - Session Manager
Centralized session lifecycle management for sync and async HTTP clients
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
                if not session.closed:
                    return session
                else:
                    # Remove closed session
                    del self._sessions[loop_id]

            # Create new session
            session = aiohttp.ClientSession()
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
                            await session.close()

                loop.run_until_complete(close_all())
                loop.close()
            except Exception:
                pass

        # Use weakref.finalize on self, not on dict
        weakref.finalize(self, cleanup, None)

    async def close(self):
        """Close all sessions"""
        async with self._lock:
            for session in self._sessions.values():
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
        # Don't create threads during interpreter shutdown
        # weakref.finalize will handle cleanup if possible
        pass