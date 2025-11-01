"""
🌸 Blossom AI - Beautiful Python SDK for Pollinations.AI
Generate images, text, and audio with AI

Version: 0.4.0 (V2 API Support)
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

# V2 Generators
try:
    from blossom_ai.generators.generators_v2 import (
        ImageGeneratorV2,
        AsyncImageGeneratorV2,
        TextGeneratorV2,
        AsyncTextGeneratorV2,
    )
    V2_AVAILABLE = True
except ImportError:
    # V2 generators not available
    ImageGeneratorV2 = None
    AsyncImageGeneratorV2 = None
    TextGeneratorV2 = None
    AsyncTextGeneratorV2 = None
    V2_AVAILABLE = False

# Import create_client from blossom module
from blossom_ai.generators.blossom import create_client

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

__version__ = "0.4.0"

__all__ = [
    # Main client
    "Blossom",
    "create_client",

    # V1 Generators (Legacy)
    "ImageGenerator",
    "AsyncImageGenerator",
    "TextGenerator",
    "AsyncTextGenerator",
    "AudioGenerator",
    "AsyncAudioGenerator",
    "StreamChunk",

    # V2 Generators (New)
    "ImageGeneratorV2",
    "AsyncImageGeneratorV2",
    "TextGeneratorV2",
    "AsyncTextGeneratorV2",
    "V2_AVAILABLE",

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


# Helper function to check V2 availability
def check_v2_available():
    """Check if V2 API generators are available"""
    return V2_AVAILABLE


# Convenience aliases for backward compatibility
BlossomClient = Blossom