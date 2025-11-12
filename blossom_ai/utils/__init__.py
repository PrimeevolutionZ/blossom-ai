"""
Blossom AI - Utilities Module
Enhanced with Reasoning capabilities and CLI
"""

from .file_uploader import (
    FileContentReader,
    FileContent,
    read_file_for_prompt,
    get_file_info,
    DEFAULT_MAX_FILE_LENGTH,
    DEFAULT_PROMPT_SPACE,
    API_MAX_TOTAL_LENGTH,
    SUPPORTED_TEXT_EXTENSIONS,
)

from .reasoning import (
    ReasoningLevel,
    ReasoningMode,
    ReasoningConfig,
    ReasoningEnhancer,
    ReasoningChain,
    create_reasoning_enhancer,
    REASONING_PROMPTS,
    get_native_reasoning_models,
)

from .cache import (
    CacheBackend,
    CacheConfig,
    CacheEntry,
    CacheStats,
    CacheManager,
    get_cache,
    configure_cache,
    cached,
)

from .cli import (
    BlossomCLI,
)

__all__ = [
    # File handling
    "FileContentReader",
    "FileContent",
    "read_file_for_prompt",
    "get_file_info",
    "DEFAULT_MAX_FILE_LENGTH",
    "DEFAULT_PROMPT_SPACE",
    "API_MAX_TOTAL_LENGTH",
    "SUPPORTED_TEXT_EXTENSIONS",

    # Reasoning capabilities
    "ReasoningLevel",
    "ReasoningMode",
    "ReasoningConfig",
    "ReasoningEnhancer",
    "ReasoningChain",
    "create_reasoning_enhancer",
    "REASONING_PROMPTS",
    "get_native_reasoning_models",

    # Caching
    "CacheBackend",
    "CacheConfig",
    "CacheEntry",
    "CacheStats",
    "CacheManager",
    "get_cache",
    "configure_cache",
    "cached",

    # CLI
    "BlossomCLI",
]