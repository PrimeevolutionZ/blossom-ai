"""
🌸 Blossom AI - Beautiful Python SDK for Pollinations.AI
Generate images, text, and audio with AI

Version: 0.3.1
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
    FileTooLargeError,
    ImageModel,
    TextModel,
    Voice,
    DEFAULT_IMAGE_MODELS,
    DEFAULT_TEXT_MODELS,
    DEFAULT_VOICES,
)

from blossom_ai.utils import (
    FileContentReader,
    FileContent,
    read_file_for_prompt,
    get_file_info,
    DEFAULT_MAX_FILE_LENGTH,
    DEFAULT_PROMPT_SPACE,
    API_MAX_TOTAL_LENGTH,
    SUPPORTED_TEXT_EXTENSIONS,
)

__version__ = "0.3.2"

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
    "FileTooLargeError",

    # Models
    "ImageModel",
    "TextModel",
    "Voice",
    "DEFAULT_IMAGE_MODELS",
    "DEFAULT_TEXT_MODELS",
    "DEFAULT_VOICES",

    # Utils
    "FileContentReader",
    "FileContent",
    "read_file_for_prompt",
    "get_file_info",
    "DEFAULT_MAX_FILE_LENGTH",
    "DEFAULT_PROMPT_SPACE",
    "API_MAX_TOTAL_LENGTH",
    "SUPPORTED_TEXT_EXTENSIONS",

    # Version
    "__version__",
]