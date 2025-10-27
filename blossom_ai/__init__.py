"""
🌸 Blossom AI - Beautiful Python SDK for Pollinations.AI
Generate images, text, and audio with AI

Version: 0.2.91
"""

from blossom_ai.generators import (
    Blossom,
    ImageGenerator,
    AsyncImageGenerator,
    TextGenerator,
    AsyncTextGenerator,
    AudioGenerator,
    AsyncAudioGenerator,
    StreamChunk,
)

from blossom_ai.core import (
    BlossomError,
    ErrorType,
    ErrorContext,
    NetworkError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    StreamError,
    ImageModel,
    TextModel,
    Voice,
    DEFAULT_IMAGE_MODELS,
    DEFAULT_TEXT_MODELS,
    DEFAULT_VOICES,
)

__version__ = "0.2.5"

__all__ = [
    # Main client
    "Blossom",

    # Generators
    "ImageGenerator",
    "AsyncImageGenerator",
    "TextGenerator",
    "AsyncTextGenerator",
    "AudioGenerator",
    "AsyncAudioGenerator",
    "StreamChunk",

    # Errors
    "BlossomError",
    "ErrorType",
    "ErrorContext",
    "NetworkError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "StreamError",

    # Models
    "ImageModel",
    "TextModel",
    "Voice",
    "DEFAULT_IMAGE_MODELS",
    "DEFAULT_TEXT_MODELS",
    "DEFAULT_VOICES",

    # Version
    "__version__",
]