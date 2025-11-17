"""
Blossom AI - Configuration (v0.5.1)
V2 API Only (enter.pollinations.ai)
"""

from __future__ import annotations

import os
from types import SimpleNamespace
from typing import Optional, Final

# ==============================================================================
# HELPERS
# ==============================================================================

def _safe_int(key: str, default: int) -> int:
    val = os.getenv(key)
    try:
        return int(val) if val else default
    except ValueError:
        return default

def _safe_float(key: str, default: float) -> float:
    val = os.getenv(key)
    try:
        return float(val) if val else default
    except ValueError:
        return default

def _validate_url(url: str) -> str:
    if not isinstance(url, str) or not url.startswith("http"):
        raise ValueError(f"Invalid URL: {url}")
    return url

def _validate_positive(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value

# ==============================================================================
# CONSTANTS
# ==============================================================================

BASE_URL = "https://enter.pollinations.ai/api"

ENDPOINTS = SimpleNamespace(
    BASE=BASE_URL,
    TEXT=f"{BASE_URL}/generate/v1/chat/completions",
    TEXT_MODELS=f"{BASE_URL}/generate/v1/models",
    IMAGE=f"{BASE_URL}/generate/image",
    IMAGE_MODELS=f"{BASE_URL}/generate/image/models",
    AUTH="https://auth.pollinations.ai",
)

LIMITS = SimpleNamespace(
    MAX_IMAGE_PROMPT_LENGTH=200,
    MAX_TEXT_PROMPT_LENGTH=90000,
    MAX_FILE_SIZE_MB=10,
    DEFAULT_TIMEOUT=30,
    CONNECT_TIMEOUT=10,
    READ_TIMEOUT=30,
    STREAM_CHUNK_TIMEOUT=30,
    MAX_RETRIES=3,
    RETRY_MIN_WAIT=4,
    RETRY_MAX_WAIT=10,
    RETRY_EXPONENTIAL_BASE=2.0,
    RATE_LIMIT_BURST=3,
    RATE_LIMIT_REFILL=15,
)

DEFAULTS = SimpleNamespace(
    IMAGE_MODEL="flux",
    TEXT_MODEL="openai",
    IMAGE_WIDTH=1024,
    IMAGE_HEIGHT=1024,
    IMAGE_SEED=42,
    IMAGE_QUALITY="medium",
    IMAGE_NEGATIVE_PROMPT="worst quality, blurry",
    TEMPERATURE=1.0,
    MAX_TOKENS=None,
    TOP_P=1.0,
    FREQUENCY_PENALTY=0.0,
    PRESENCE_PENALTY=0.0,
    STREAM=False,
    AUDIO_VOICE="alloy",
    AUDIO_FORMAT="wav",
    REASONING_EFFORT="medium",
)

AUDIO = SimpleNamespace(
    VOICES=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
    FORMATS=["wav", "mp3", "flac", "opus", "pcm16"],
    DEFAULT_VOICE="alloy",
    DEFAULT_FORMAT="wav",
)

REASONING = SimpleNamespace(
    EFFORTS=["low", "medium", "high"],
    DEFAULT_EFFORT="medium",
)

# ==============================================================================
# VALIDATION
# ==============================================================================

def validate_config() -> None:
    """Validate all constants"""
    for key, url in ENDPOINTS.__dict__.items():
        if key.isupper() or key.startswith("_"):
            continue
        _validate_url(url)

    for key, value in LIMITS.__dict__.items():
        if isinstance(value, (int, float)):
            _validate_positive(value, key)

    if not (0.0 <= DEFAULTS.TEMPERATURE <= 2.0):
        raise ValueError("Temperature must be between 0.0 and 2.0")
    if not (0.0 <= DEFAULTS.TOP_P <= 1.0):
        raise ValueError("Top P must be between 0.0 and 1.0")
    if DEFAULTS.IMAGE_WIDTH <= 0 or DEFAULTS.IMAGE_HEIGHT <= 0:
        raise ValueError("Image dimensions must be positive")

# ==============================================================================
# MUTABLE CONFIG
# ==============================================================================

class Config:
    def __init__(
        self,
        api_token: Optional[str] = None,
        debug: bool = False,
    ) -> None:
        self.api_token = api_token or os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
        self.debug = debug

    def update_from_env(self) -> None:
        self.api_token = os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
        self.debug = os.getenv("BLOSSOM_DEBUG", "").lower() in ("1", "true", "yes")

    def validate(self) -> None:
        validate_config()

# ==============================================================================
# GLOBAL CONFIG
# ==============================================================================

class _ConfigLazy:
    def __init__(self) -> None:
        self._instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = Config()
            self._instance.validate()
        return self._instance

    def set(self, config: Config) -> None:
        config.validate()
        self._instance = config

    def reset(self) -> None:
        self._instance = None

_get_config = _ConfigLazy()

get_config = _get_config
set_config = _get_config.set
reset_config = _get_config.reset