"""
Blossom AI - Python Client
"""

from .blossom import Blossom
from .errors import (
    BlossomError,
    ErrorType,
    ErrorContext,
    NetworkError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
)
from .models import ImageModel, TextModel, Voice

__version__ = "0.2.1"

__all__ = [
    # Main client
    "Blossom",

    # Base errors
    "BlossomError",
    "ErrorType",
    "ErrorContext",

    # Specific errors
    "NetworkError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",

    # Models (optional, for autocomplete)
    "ImageModel",
    "TextModel",
    "Voice",
]