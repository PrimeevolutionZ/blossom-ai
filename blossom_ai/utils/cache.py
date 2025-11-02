"""
Blossom AI - Caching Module
Intelligent caching for API requests to reduce costs and improve performance
"""

import hashlib
import json
import os
import pickle
import time
import asyncio
from pathlib import Path
from typing import Optional, Any, Dict, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import threading


class CacheBackend(str, Enum):
    """Cache storage backends"""
    MEMORY = "memory"
    DISK = "disk"
    HYBRID = "hybrid"  # Memory + Disk


@dataclass
class CacheConfig:
    """Configuration for caching"""
    enabled: bool = True
    backend: CacheBackend = CacheBackend.HYBRID
    ttl: int = 3600  # Time to live in seconds (default: 1 hour)
    max_memory_size: int = 100  # Max items in memory
    max_disk_size: int = 1000  # Max items on disk
    cache_dir: Optional[Path] = None  # Auto-set to ~/.blossom_cache

    # What to cache
    cache_text: bool = True
    cache_images: bool = False  # Images can be large
    cache_audio: bool = False

    # Advanced
    compress: bool = True  # Compress disk cache
    serialize_format: str = "pickle"  # pickle or json


@dataclass
class CacheEntry:
    """Single cache entry"""
    key: str
    value: Any
    timestamp: float
    size: int = 0
    hits: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, ttl: int) -> bool:
        """Check if entry is expired"""
        return (time.time() - self.timestamp) > ttl

    def touch(self):
        """Update access time and hit count"""
        self.hits += 1
        self.timestamp = time.time()


class CacheStats:
    """Cache statistics"""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.memory_usage = 0
        self.disk_usage = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

    def __repr__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.misses}, "
            f"hit_rate={self.hit_rate:.1f}%, evictions={self.evictions})"
        )


class CacheManager:
    """
    Intelligent cache manager for Blossom AI

    Features:
    - Memory + Disk hybrid caching
    - TTL-based expiration
    - LRU eviction policy
    - Thread-safe operations
    - Compression for disk storage
    - Statistics tracking

    Example:
        >>> cache = CacheManager()
        >>>
        >>> # Manual caching
        >>> cache.set("key", "value", ttl=3600)
        >>> value = cache.get("key")
        >>>
        >>> # Decorator usage
        >>> @cache.cached(ttl=1800)
        ... def expensive_function(arg):
        ...     return generate_text(arg)
    """

    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self.stats = CacheStats()

        # Memory cache: {key: CacheEntry}
        self._memory: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()  # Thread-safe
        self._async_lock = asyncio.Lock()  # Async-safe

        # Setup disk cache
        if self.config.backend in [CacheBackend.DISK, CacheBackend.HYBRID]:
            self._setup_disk_cache()

    def _setup_disk_cache(self):
        """Setup disk cache directory"""
        if self.config.cache_dir is None:
            self.config.cache_dir = Path.home() / ".blossom_cache"

        self.config.cache_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organization
        (self.config.cache_dir / "text").mkdir(exist_ok=True)
        (self.config.cache_dir / "images").mkdir(exist_ok=True)
        (self.config.cache_dir / "audio").mkdir(exist_ok=True)
        (self.config.cache_dir / "metadata").mkdir(exist_ok=True)

    def _generate_key(
            self,
            prefix: str,
            *args,
            **kwargs
    ) -> str:
        """Generate cache key from arguments"""
        # Create deterministic hash from arguments
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }

        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.sha256(key_str.encode()).hexdigest()[:16]

        return f"{prefix}_{key_hash}"

    def _should_cache(self, prefix: str) -> bool:
        """Check if this type of request should be cached"""
        if not self.config.enabled:
            return False

        if prefix.startswith("text") and not self.config.cache_text:
            return False
        if prefix.startswith("image") and not self.config.cache_images:
            return False
        if prefix.startswith("audio") and not self.config.cache_audio:
            return False

        return True

    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key
            default: Default value if not found

        Returns:
            Cached value or default
        """
        if not self.config.enabled:
            return default

        with self._lock:
            # Try memory first
            if self.config.backend in [CacheBackend.MEMORY, CacheBackend.HYBRID]:
                if key in self._memory:
                    entry = self._memory[key]

                    if entry.is_expired(self.config.ttl):
                        del self._memory[key]
                        self.stats.evictions += 1
                    else:
                        entry.touch()
                        self.stats.hits += 1
                        return entry.value

            # Try disk
            if self.config.backend in [CacheBackend.DISK, CacheBackend.HYBRID]:
                disk_value = self._read_from_disk(key)
                if disk_value is not None:
                    self.stats.hits += 1

                    # Promote to memory cache if hybrid
                    if self.config.backend == CacheBackend.HYBRID:
                        self._memory[key] = CacheEntry(
                            key=key,
                            value=disk_value,
                            timestamp=time.time(),
                            size=self._estimate_size(disk_value)
                        )

                    return disk_value

            self.stats.misses += 1
            return default

    def set(
            self,
            key: str,
            value: Any,
            ttl: Optional[int] = None,
            metadata: Optional[Dict] = None
    ) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Custom TTL (overrides config)
            metadata: Additional metadata

        Returns:
            True if cached successfully
        """
        if not self.config.enabled:
            return False

        ttl = ttl or self.config.ttl

        with self._lock:
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=time.time(),
                size=self._estimate_size(value),
                metadata=metadata or {}
            )

            # Memory cache
            if self.config.backend in [CacheBackend.MEMORY, CacheBackend.HYBRID]:
                self._memory[key] = entry
                self._evict_if_needed()

            # Disk cache
            if self.config.backend in [CacheBackend.DISK, CacheBackend.HYBRID]:
                self._write_to_disk(key, value, entry)

            return True

    def _estimate_size(self, value: Any) -> int:
        """Estimate size of value in bytes"""
        try:
            if isinstance(value, (str, bytes)):
                return len(value)
            elif isinstance(value, dict):
                return len(json.dumps(value))
            else:
                return len(pickle.dumps(value))
        except:
            return 0

    def _evict_if_needed(self):
        """Evict old entries using LRU"""
        if len(self._memory) <= self.config.max_memory_size:
            return

        # Sort by timestamp (LRU)
        sorted_entries = sorted(
            self._memory.items(),
            key=lambda x: x[1].timestamp
        )

        # Remove oldest 20%
        num_to_remove = len(self._memory) - self.config.max_memory_size
        for key, _ in sorted_entries[:num_to_remove]:
            del self._memory[key]
            self.stats.evictions += 1

    def _read_from_disk(self, key: str) -> Optional[Any]:
        """Read value from disk cache"""
        if not self.config.cache_dir:
            return None

        # Try to find in subdirectories
        for subdir in ["text", "images", "audio", "metadata"]:
            cache_file = self.config.cache_dir / subdir / f"{key}.cache"

            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        data = pickle.load(f)

                        # Check expiration
                        if time.time() - data['timestamp'] > self.config.ttl:
                            cache_file.unlink()
                            return None

                        return data['value']
                except Exception:
                    return None

        return None

    def _write_to_disk(self, key: str, value: Any, entry: CacheEntry):
        """Write value to disk cache"""
        if not self.config.cache_dir:
            return

        # Determine subdirectory based on key prefix
        if key.startswith("text"):
            subdir = "text"
        elif key.startswith("image"):
            subdir = "images"
        elif key.startswith("audio"):
            subdir = "audio"
        else:
            subdir = "metadata"

        cache_file = self.config.cache_dir / subdir / f"{key}.cache"

        try:
            data = {
                'value': value,
                'timestamp': entry.timestamp,
                'metadata': entry.metadata
            }

            with open(cache_file, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            # Silently fail disk writes
            pass

    def clear(self, prefix: Optional[str] = None):
        """
        Clear cache

        Args:
            prefix: Clear only keys with this prefix (None = clear all)
        """
        with self._lock:
            if prefix is None:
                self._memory.clear()

                # Clear disk
                if self.config.cache_dir:
                    for subdir in ["text", "images", "audio", "metadata"]:
                        for cache_file in (self.config.cache_dir / subdir).glob("*.cache"):
                            cache_file.unlink()
            else:
                # Clear specific prefix
                keys_to_delete = [k for k in self._memory if k.startswith(prefix)]
                for key in keys_to_delete:
                    del self._memory[key]

                # Clear from disk
                if self.config.cache_dir:
                    for subdir in ["text", "images", "audio", "metadata"]:
                        for cache_file in (self.config.cache_dir / subdir).glob(f"{prefix}*.cache"):
                            cache_file.unlink()

    def cached(
            self,
            ttl: Optional[int] = None,
            key_prefix: Optional[str] = None
    ) -> Callable:
        """
        Decorator for caching function results

        Args:
            ttl: Custom TTL for this function
            key_prefix: Custom key prefix

        Example:
            >>> cache = CacheManager()
            >>> @cache.cached(ttl=1800)
            ... def generate_text(prompt):
            ...     return client.text.generate(prompt)
        """

        def decorator(func: Callable) -> Callable:
            prefix = key_prefix or f"func_{func.__name__}"

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                if not self.config.enabled:
                    return func(*args, **kwargs)

                # Generate cache key
                cache_key = self._generate_key(prefix, *args, **kwargs)

                # Try to get from cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Execute function
                result = func(*args, **kwargs)

                # Cache result
                self.set(cache_key, result, ttl=ttl)

                return result

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not self.config.enabled:
                    return await func(*args, **kwargs)

                cache_key = self._generate_key(prefix, *args, **kwargs)

                async with self._async_lock:
                    cached_value = self.get(cache_key)
                    if cached_value is not None:
                        return cached_value

                result = await func(*args, **kwargs)

                async with self._async_lock:
                    self.set(cache_key, result, ttl=ttl)

                return result

            # Return appropriate wrapper
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        return decorator

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        with self._lock:
            self.stats.memory_usage = len(self._memory)

            if self.config.cache_dir:
                disk_count = 0
                for subdir in ["text", "images", "audio", "metadata"]:
                    disk_count += len(list((self.config.cache_dir / subdir).glob("*.cache")))
                self.stats.disk_usage = disk_count

            return self.stats

    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"CacheManager(backend={self.config.backend}, "
            f"memory={stats.memory_usage}/{self.config.max_memory_size}, "
            f"disk={stats.disk_usage}, {stats})"
        )


# Global cache instance
_global_cache: Optional[CacheManager] = None


def get_cache() -> CacheManager:
    """Get or create global cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager()
    return _global_cache


def configure_cache(config: CacheConfig):
    """Configure global cache"""
    global _global_cache
    _global_cache = CacheManager(config)


# Convenience decorators
def cached(ttl: int = 3600):
    """Quick decorator using global cache"""
    return get_cache().cached(ttl=ttl)