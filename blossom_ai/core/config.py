"""
Blossom AI - Configuration (v0.5.0)
V2 API Only (enter.pollinations.ai)
"""

import os
from dataclasses import dataclass, field
from typing import Final, Optional
from enum import Enum


# ==============================================================================
# API ENDPOINTS (V2 ONLY)
# ==============================================================================

@dataclass(frozen=True)
class APIEndpoints:
    """
    V2 API endpoints (enter.pollinations.ai)
    """

    # Base V2 API
    BASE = "https://enter.pollinations.ai/api"

    # Generation endpoints
    IMAGE = f"{BASE}/generate/image"
    TEXT = f"{BASE}/generate/v1/chat/completions"

    # Model discovery
    IMAGE_MODELS = f"{BASE}/generate/image/models"
    TEXT_MODELS = f"{BASE}/generate/v1/models"

    # Auth
    AUTH: str = "https://auth.pollinations.ai"

    def __post_init__(self):
        """Validate all endpoints are valid URLs"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.startswith('http'):
                raise ValueError(f"Invalid endpoint URL for {field_name}: {value}")


# ==============================================================================
# LIMITS & CONSTRAINTS
# ==============================================================================

@dataclass(frozen=True)
class Limits:
    """API limits and constraints"""

    # Content limits
    MAX_IMAGE_PROMPT_LENGTH: int = 200
    MAX_TEXT_PROMPT_LENGTH: int = 10000
    MAX_FILE_SIZE_MB: int = 10

    # Timeout settings (seconds)
    DEFAULT_TIMEOUT: int = 30
    CONNECT_TIMEOUT: int = 10
    READ_TIMEOUT: int = 30
    STREAM_CHUNK_TIMEOUT: int = 30

    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_MIN_WAIT: int = 4
    RETRY_MAX_WAIT: int = 10
    RETRY_EXPONENTIAL_BASE: float = 2.0

    # Rate limiting
    RATE_LIMIT_BURST: int = 3
    RATE_LIMIT_REFILL: int = 15

    def __post_init__(self):
        """Validate all limits are positive"""
        for field_name, value in self.__dict__.items():
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(f"{field_name} must be positive, got {value}")

    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


# ==============================================================================
# DEFAULT VALUES
# ==============================================================================

@dataclass(frozen=True)
class Defaults:
    """Default values for API parameters"""

    # Model defaults
    IMAGE_MODEL: str = "flux"
    TEXT_MODEL: str = "openai"

    # Image generation defaults
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 1024
    IMAGE_SEED: int = 42
    IMAGE_QUALITY: str = "medium"
    IMAGE_NEGATIVE_PROMPT: str = "worst quality, blurry"

    # Text generation defaults
    TEMPERATURE: float = 1.0
    MAX_TOKENS: Optional[int] = None
    TOP_P: float = 1.0
    FREQUENCY_PENALTY: float = 0.0
    PRESENCE_PENALTY: float = 0.0

    # Streaming
    STREAM: bool = False

    def __post_init__(self):
        """Validate default values"""
        if self.IMAGE_WIDTH <= 0 or self.IMAGE_HEIGHT <= 0:
            raise ValueError("Image dimensions must be positive")

        if not 0.0 <= self.TEMPERATURE <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")

        if not 0.0 <= self.TOP_P <= 1.0:
            raise ValueError("Top P must be between 0.0 and 1.0")

    @classmethod
    def from_env(cls) -> "Defaults":
        """Create Defaults from environment variables"""
        return cls(
            IMAGE_MODEL=os.getenv("BLOSSOM_IMAGE_MODEL", "flux"),
            TEXT_MODEL=os.getenv("BLOSSOM_TEXT_MODEL", "openai"),
            IMAGE_WIDTH=int(os.getenv("BLOSSOM_IMAGE_WIDTH", "1024")),
            IMAGE_HEIGHT=int(os.getenv("BLOSSOM_IMAGE_HEIGHT", "1024")),
            TEMPERATURE=float(os.getenv("BLOSSOM_TEMPERATURE", "1.0")),
        )


# ==============================================================================
# CONFIGURATION
# ==============================================================================

@dataclass
class Config:
    """Mutable configuration instance"""

    endpoints: APIEndpoints = field(default_factory=APIEndpoints)
    limits: Limits = field(default_factory=Limits)
    defaults: Defaults = field(default_factory=Defaults)

    # Runtime settings
    api_token: Optional[str] = None
    debug: bool = False

    def __post_init__(self):
        """Load API token from environment if not provided"""
        if self.api_token is None:
            self.api_token = os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")

    def update_from_env(self):
        """Update configuration from environment variables"""
        self.defaults = Defaults.from_env()

        if debug_env := os.getenv("BLOSSOM_DEBUG"):
            self.debug = debug_env.lower() in ("1", "true", "yes")

    def validate(self) -> bool:
        """Validate configuration"""
        try:
            self.endpoints.__post_init__()
            self.limits.__post_init__()
            self.defaults.__post_init__()
            return True
        except Exception as e:
            raise ValueError(f"Invalid configuration: {e}")


# ==============================================================================
# SINGLETON INSTANCES
# ==============================================================================

ENDPOINTS: Final[APIEndpoints] = APIEndpoints()
LIMITS: Final[Limits] = Limits()
DEFAULTS: Final[Defaults] = Defaults()

# Auth URL (backward compatibility)
AUTH_URL: Final[str] = ENDPOINTS.AUTH


# ==============================================================================
# GLOBAL CONFIG INSTANCE
# ==============================================================================

_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def set_config(config: Config):
    """Set global configuration instance"""
    global _global_config
    config.validate()
    _global_config = config


def reset_config():
    """Reset global configuration to defaults"""
    global _global_config
    _global_config = Config()