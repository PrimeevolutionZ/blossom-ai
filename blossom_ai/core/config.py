"""
Blossom AI - Configuration
Centralized configuration for API endpoints and constants
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class APIEndpoints:
    """API endpoint URLs"""
    IMAGE: str = "https://image.pollinations.ai"
    TEXT: str = "https://text.pollinations.ai"
    AUDIO: str = "https://text.pollinations.ai"  # Audio uses text endpoint


@dataclass(frozen=True)
class Limits:
    """API limits and constraints"""
    MAX_IMAGE_PROMPT_LENGTH: int = 200
    MAX_TEXT_PROMPT_LENGTH: int = 10000
    STREAM_CHUNK_TIMEOUT: int = 30  # seconds without data
    DEFAULT_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_MIN_WAIT: int = 4  # seconds
    RETRY_MAX_WAIT: int = 10  # seconds


@dataclass(frozen=True)
class Defaults:
    """Default values for API parameters"""
    IMAGE_MODEL: str = "flux"
    TEXT_MODEL: str = "openai"
    AUDIO_MODEL: str = "openai-audio"
    AUDIO_VOICE: str = "alloy"
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 1024
    TEMPERATURE: float = 1.0


# Singleton instances
ENDPOINTS: Final = APIEndpoints()
LIMITS: Final = Limits()
DEFAULTS: Final = Defaults()


# Auth configuration
AUTH_URL: Final[str] = "https://auth.pollinations.ai"