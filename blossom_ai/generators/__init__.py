"""
Blossom AI - Generators Module (v0.5.0)
V2 API Only (enter.pollinations.ai)
"""

# Main generators (V2 API)
from .generators import (
    ImageGenerator,
    AsyncImageGenerator,
    TextGenerator,
    AsyncTextGenerator,
)

# Main client
from .blossom import Blossom, create_client

# Helper modules (for advanced users)
try:
    from .streaming_mixin import SSEParser, SyncStreamingMixin, AsyncStreamingMixin
    from .parameter_builder import (
        ImageParamsV2,
        ChatParamsV2,
        AudioParamsV2,
        ParameterValidator,
        MessageBuilder
    )
    HELPERS_AVAILABLE = True
except ImportError:
    HELPERS_AVAILABLE = False

__all__ = [
    # Main generators
    "ImageGenerator",
    "AsyncImageGenerator",
    "TextGenerator",
    "AsyncTextGenerator",

    # Main client
    "Blossom",
    "create_client",
]

# Conditionally add helpers to __all__
if HELPERS_AVAILABLE:
    __all__.extend([
        "SSEParser",
        "SyncStreamingMixin",
        "AsyncStreamingMixin",
        "ImageParamsV2",
        "ChatParamsV2",
        "AudioParamsV2",
        "ParameterValidator",
        "MessageBuilder",
    ])