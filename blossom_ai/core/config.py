"""
Blossom AI - Configuration
Refactored version with validation, environment support, and better structure
"""

import os
from dataclasses import dataclass, field
from typing import Final, Optional, Literal
from enum import Enum


# ==============================================================================
# API VERSIONS
# ==============================================================================

class APIVersion(str, Enum):
    """Supported API versions"""
    V1 = "v1"  # Legacy API
    V2 = "v2"  # New enter.pollinations.ai API


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@dataclass(frozen=True)
class APIEndpoints:
    """
    API endpoint URLs with validation

    Improvements:
    - Grouped by version
    - Validation on creation
    - Type hints
    """

    # Legacy API (v1) - image.pollinations.ai, text.pollinations.ai
    V1_IMAGE: str = "https://image.pollinations.ai"
    V1_TEXT: str = "https://text.pollinations.ai"
    V1_AUDIO: str = "https://text.pollinations.ai"

    # New API (v2) - enter.pollinations.ai
    V2_BASE: str = "https://enter.pollinations.ai/api"
    V2_IMAGE: str = "https://enter.pollinations.ai/api/generate/image"
    V2_TEXT: str = "https://enter.pollinations.ai/api/generate/text"
    V2_CHAT: str = "https://enter.pollinations.ai/api/generate/v1/chat/completions"
    V2_IMAGE_MODELS: str = "https://enter.pollinations.ai/api/generate/image/models"
    V2_TEXT_MODELS: str = "https://enter.pollinations.ai/api/generate/v1/models"

    # Auth
    AUTH: str = "https://auth.pollinations.ai"

    def __post_init__(self):
        """Validate all endpoints are valid URLs"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.startswith('http'):
                raise ValueError(f"Invalid endpoint URL for {field_name}: {value}")

    def get_endpoint(self, version: APIVersion, resource: str) -> str:
        """
        Get endpoint URL for a specific version and resource

        Args:
            version: API version (v1 or v2)
            resource: Resource type (image, text, audio, etc.)

        Returns:
            Endpoint URL

        Raises:
            ValueError: If combination is invalid
        """
        resource = resource.lower()

        if version == APIVersion.V1:
            if resource == "image":
                return self.V1_IMAGE
            elif resource == "text":
                return self.V1_TEXT
            elif resource == "audio":
                return self.V1_AUDIO

        elif version == APIVersion.V2:
            if resource == "image":
                return self.V2_IMAGE
            elif resource == "text":
                return self.V2_TEXT
            elif resource == "chat":
                return self.V2_CHAT

        raise ValueError(f"Invalid combination: version={version}, resource={resource}")


# ==============================================================================
# LIMITS & CONSTRAINTS
# ==============================================================================

@dataclass(frozen=True)
class Limits:
    """
    API limits and constraints

    Improvements:
    - Better organization
    - Additional limits
    - Validation
    """

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
    RATE_LIMIT_BURST: int = 3  # Requests per burst (publishable keys)
    RATE_LIMIT_REFILL: int = 15  # Seconds between refills

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
    """
    Default values for API parameters

    Improvements:
    - Organized by category
    - Environment variable support
    - Validation
    """

    # Model defaults
    IMAGE_MODEL: str = "flux"
    TEXT_MODEL: str = "openai"
    AUDIO_MODEL: str = "openai-audio"
    AUDIO_VOICE: str = "alloy"

    # Image generation defaults
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 1024
    IMAGE_ENHANCE: bool = False
    IMAGE_NOLOGO: bool = True

    # Text generation defaults
    TEMPERATURE: float = 1.0
    MAX_TOKENS: Optional[int] = None
    TOP_P: float = 1.0
    FREQUENCY_PENALTY: float = 0.0
    PRESENCE_PENALTY: float = 0.0

    # API configuration
    API_VERSION: APIVersion = APIVersion.V2
    STREAM: bool = False

    def __post_init__(self):
        """Validate default values"""
        # Image dimensions
        if self.IMAGE_WIDTH <= 0 or self.IMAGE_HEIGHT <= 0:
            raise ValueError("Image dimensions must be positive")

        # Temperature
        if not 0.0 <= self.TEMPERATURE <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")

        # Top P
        if not 0.0 <= self.TOP_P <= 1.0:
            raise ValueError("Top P must be between 0.0 and 1.0")

    @classmethod
    def from_env(cls) -> "Defaults":
        """
        Create Defaults from environment variables

        Environment variables:
            BLOSSOM_API_VERSION: API version (v1 or v2)
            BLOSSOM_IMAGE_MODEL: Default image model
            BLOSSOM_TEXT_MODEL: Default text model
            BLOSSOM_TEMPERATURE: Default temperature
            etc.
        """
        return cls(
            IMAGE_MODEL=os.getenv("BLOSSOM_IMAGE_MODEL", "flux"),
            TEXT_MODEL=os.getenv("BLOSSOM_TEXT_MODEL", "openai"),
            AUDIO_MODEL=os.getenv("BLOSSOM_AUDIO_MODEL", "openai-audio"),
            AUDIO_VOICE=os.getenv("BLOSSOM_AUDIO_VOICE", "alloy"),
            IMAGE_WIDTH=int(os.getenv("BLOSSOM_IMAGE_WIDTH", "1024")),
            IMAGE_HEIGHT=int(os.getenv("BLOSSOM_IMAGE_HEIGHT", "1024")),
            TEMPERATURE=float(os.getenv("BLOSSOM_TEMPERATURE", "1.0")),
            API_VERSION=APIVersion(os.getenv("BLOSSOM_API_VERSION", "v2"))
        )


# ==============================================================================
# CONFIGURATION
# ==============================================================================

@dataclass
class Config:
    """
    Mutable configuration instance

    Allows runtime configuration changes while providing defaults
    """

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
            # Validate endpoints
            self.endpoints.__post_init__()

            # Validate limits
            self.limits.__post_init__()

            # Validate defaults
            self.defaults.__post_init__()

            return True
        except Exception as e:
            raise ValueError(f"Invalid configuration: {e}")


# ==============================================================================
# SINGLETON INSTANCES
# ==============================================================================

# Immutable singletons for backward compatibility
ENDPOINTS: Final[APIEndpoints] = APIEndpoints()
LIMITS: Final[Limits] = Limits()
DEFAULTS: Final[Defaults] = Defaults()

# Auth URL (deprecated, use ENDPOINTS.AUTH)
AUTH_URL: Final[str] = ENDPOINTS.AUTH


# ==============================================================================
# GLOBAL CONFIG INSTANCE
# ==============================================================================

# Mutable global config
_global_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get global configuration instance

    Returns:
        Global Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def set_config(config: Config):
    """
    Set global configuration instance

    Args:
        config: New Config instance
    """
    global _global_config
    config.validate()
    _global_config = config


def reset_config():
    """Reset global configuration to defaults"""
    global _global_config
    _global_config = Config()