"""
Blossom AI – Configuration (v0.5.4)
Frozen constants + immutable SessionConfig + public singleton DEFAULT_CONFIG.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional, Final

# --------------------------------------------------------------------------- #
# Low-level helpers
# --------------------------------------------------------------------------- #

def _safe_int(key: str, default: int) -> int:
    val = os.getenv(key)
    try:
        return int(val) if val else default
    except (ValueError, TypeError):
        return default

def _validate_url(url: str) -> str:
    if not isinstance(url, str) or not url.startswith("http"):
        raise ValueError(f"Invalid URL: {url}")
    return url

# --------------------------------------------------------------------------- #
# Frozen constants
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class _Endpoints:
    BASE: str = field(default_factory=lambda: _validate_url("https://enter.pollinations.ai/api"))
    TEXT: str = field(init=False)
    TEXT_MODELS: str = field(init=False)
    IMAGE: str = field(default_factory=lambda: _validate_url("https://image.pollinations.ai/prompt"))
    IMAGE_MODELS: str = field(default_factory=lambda: _validate_url("https://image.pollinations.ai/models"))
    AUTH: str = field(default_factory=lambda: _validate_url("https://auth.pollinations.ai"))

    def __post_init__(self) -> None:
        object.__setattr__(self, "TEXT", f"{self.BASE}/generate/v1/chat/completions")
        object.__setattr__(self, "TEXT_MODELS", f"{self.BASE}/generate/v1/models")

ENDPOINTS: Final = _Endpoints()

@dataclass(frozen=True, slots=True)
class _Limits:
    MAX_IMAGE_PROMPT_LENGTH: int = 200
    MAX_TEXT_PROMPT_LENGTH: int = 90_000
    MAX_FILE_SIZE_MB: int = 10
    DEFAULT_TIMEOUT: int = 30
    CONNECT_TIMEOUT: int = 10
    READ_TIMEOUT: int = 30
    STREAM_CHUNK_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_MIN_WAIT: int = 4
    RETRY_MAX_WAIT: int = 10
    RETRY_EXPONENTIAL_BASE: float = 2.0
    RATE_LIMIT_BURST: int = 3
    RATE_LIMIT_REFILL: int = 15

LIMITS: Final = _Limits()

@dataclass(frozen=True, slots=True)
class _Defaults:
    IMAGE_MODEL: str = "flux"
    TEXT_MODEL: str = "openai"
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 1024
    IMAGE_SEED: int = 42
    IMAGE_QUALITY: str = "medium"
    IMAGE_NEGATIVE_PROMPT: str = "worst quality, blurry"
    TEMPERATURE: float = 1.0
    MAX_TOKENS: Optional[int] = None
    TOP_P: float = 1.0
    FREQUENCY_PENALTY: float = 0.0
    PRESENCE_PENALTY: float = 0.0
    STREAM: bool = False
    AUDIO_VOICE: str = "alloy"
    AUDIO_FORMAT: str = "wav"
    REASONING_EFFORT: str = "medium"

DEFAULTS: Final = _Defaults()

@dataclass(frozen=True, slots=True)
class _Audio:
    VOICES: tuple[str, ...] = ("alloy", "echo", "fable", "onyx", "nova", "shimmer")
    FORMATS: tuple[str, ...] = ("wav", "mp3", "flac", "opus", "pcm16")
    DEFAULT_VOICE: str = "alloy"
    DEFAULT_FORMAT: str = "wav"

AUDIO: Final = _Audio()

@dataclass(frozen=True, slots=True)
class _Reasoning:
    EFFORTS: tuple[str, ...] = ("low", "medium", "high")
    DEFAULT_EFFORT: str = "medium"

REASONING: Final = _Reasoning()

# --------------------------------------------------------------------------- #
# Immutable session-level configuration
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
# User config (mutable, but validated)
# --------------------------------------------------------------------------- #

@dataclass(slots=True)
class Config:
    api_token: Optional[str] = field(default=None)
    debug: bool = False

    def __post_init__(self) -> None:
        # env override
        self.api_token = self.api_token or os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
        self.debug = self.debug or os.getenv("BLOSSOM_DEBUG", "").lower() in ("1", "true", "yes")

    def validate(self) -> None:
        # frozen константы уже валидированы при импорте
        if self.debug and not self.api_token:
            import warnings
            warnings.warn("Debug mode without API token – some endpoints may fail", stacklevel=2)

# --------------------------------------------------------------------------- #
# Global singleton (lazy)
# --------------------------------------------------------------------------- #

import threading

class _ConfigLazy:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = Config()
                    self._instance.validate()
        return self._instance

    def set(self, config: Config) -> None:
        config.validate()
        with self._lock:
            self._instance = config

    def reset(self) -> None:
        with self._lock:
            self._instance = None

_get_config = _ConfigLazy()
get_config = _get_config
set_config = _get_config.set
reset_config = _get_config.reset