"""
🌸 Blossom AI - Beautiful Python SDK for Pollinations.AI
Generate images, text, and multimodal content with AI
"""

from blossom_ai.generators import (
    Blossom,
    create_client,
    ImageGenerator,
    AsyncImageGenerator,
    TextGenerator,
    AsyncTextGenerator,
    # NEW: Helpers for Vision & Audio
    MessageBuilder,
    AudioParamsV2,
    ImageParamsV2,
    ChatParamsV2,
    ParameterValidator,
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
    TimeoutError,
    ImageModel,
    TextModel,
    DEFAULT_IMAGE_MODELS,
    DEFAULT_TEXT_MODELS,
)

from blossom_ai.utils import (
    # File handling
    FileContentReader,
    FileContent,
    read_file_for_prompt,
    get_file_info,
    DEFAULT_MAX_FILE_LENGTH,
    DEFAULT_PROMPT_SPACE,
    API_MAX_TOTAL_LENGTH,
    SUPPORTED_TEXT_EXTENSIONS,
    # Reasoning
    ReasoningLevel,
    ReasoningConfig,
    ReasoningEnhancer,
    ReasoningChain,
    create_reasoning_enhancer,
    get_native_reasoning_models,
    ReasoningMode,
    # Caching
    CacheBackend,
    CacheConfig,
    CacheManager,
    get_cache,
    configure_cache,
    cached,
    # CLI
    BlossomCLI,
)

__version__ = "0.5.0"
__author__ = "Blossom AI Team"
__license__ = "MIT"

__all__ = [
    # Main client
    "Blossom",
    "create_client",

    # Generators (V2 API with Vision & Audio)
    "ImageGenerator",
    "AsyncImageGenerator",
    "TextGenerator",
    "AsyncTextGenerator",

    # NEW: Vision & Audio Helpers
    "MessageBuilder",
    "AudioParamsV2",
    "ImageParamsV2",
    "ChatParamsV2",
    "ParameterValidator",

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
    "TimeoutError",

    # Models
    "ImageModel",
    "TextModel",
    "DEFAULT_IMAGE_MODELS",
    "DEFAULT_TEXT_MODELS",

    # Utils - File handling
    "FileContentReader",
    "FileContent",
    "read_file_for_prompt",
    "get_file_info",
    "DEFAULT_MAX_FILE_LENGTH",
    "DEFAULT_PROMPT_SPACE",
    "API_MAX_TOTAL_LENGTH",
    "SUPPORTED_TEXT_EXTENSIONS",

    # Utils - Reasoning
    "ReasoningLevel",
    "ReasoningConfig",
    "ReasoningEnhancer",
    "ReasoningChain",
    "create_reasoning_enhancer",
    "get_native_reasoning_models",
    "ReasoningMode",

    # Utils - Caching
    "CacheBackend",
    "CacheConfig",
    "CacheManager",
    "get_cache",
    "configure_cache",
    "cached",

    # Utils - CLI
    "BlossomCLI",

    # Version
    "__version__",
]

# Convenience alias for backward compatibility
BlossomClient = Blossom