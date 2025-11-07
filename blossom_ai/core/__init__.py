"""
Blossom AI - Core Module
Refactored version with improved exports and organization
"""

# ==============================================================================
# ERROR HANDLING
# ==============================================================================

from .errors import (
    # Base error
    BlossomError,
    ErrorType,
    ErrorContext,

    # Specific errors
    NetworkError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    StreamError,
    FileTooLargeError,
    TimeoutError,

    # Error handlers
    handle_request_error,
    handle_validation_error,

    # Logging utilities
    print_info,
    print_warning,
    print_error,
    print_debug,
    print_success,
)


# ==============================================================================
# MODELS
# ==============================================================================

from .models import (
    # Base classes
    DynamicModel,
    ModelInfo,

    # Model enums
    ImageModel,
    TextModel,
    Voice,

    # Backward compatibility
    DEFAULT_IMAGE_MODELS,
    DEFAULT_TEXT_MODELS,
    DEFAULT_VOICES,
)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

from .config import (
    # Enums
    APIVersion,

    # Configuration classes
    APIEndpoints,
    Limits,
    Defaults,
    Config,

    # Singletons (backward compatibility)
    ENDPOINTS,
    LIMITS,
    DEFAULTS,
    AUTH_URL,

    # Global config management
    get_config,
    set_config,
    reset_config,
)


# ==============================================================================
# SESSION MANAGEMENT
# ==============================================================================

from .session_manager import (
    # Managers
    SyncSessionManager,
    AsyncSessionManager,
    SessionConfig,

    # Convenience functions
    get_sync_session,
    get_async_session,
)


# ==============================================================================
# PUBLIC API
# ==============================================================================

__all__ = [
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
    "handle_request_error",
    "handle_validation_error",
    "print_info",
    "print_warning",
    "print_error",
    "print_debug",
    "print_success",

    # Models
    "DynamicModel",
    "ModelInfo",
    "ImageModel",
    "TextModel",
    "Voice",
    "DEFAULT_IMAGE_MODELS",
    "DEFAULT_TEXT_MODELS",
    "DEFAULT_VOICES",

    # Configuration
    "APIVersion",
    "APIEndpoints",
    "Limits",
    "Defaults",
    "Config",
    "ENDPOINTS",
    "LIMITS",
    "DEFAULTS",
    "AUTH_URL",
    "get_config",
    "set_config",
    "reset_config",

    # Session Management
    "SyncSessionManager",
    "AsyncSessionManager",
    "SessionConfig",
    "get_sync_session",
    "get_async_session",
]
