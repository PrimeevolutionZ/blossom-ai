"""
Blossom AI - Generators Module (Refactored)
"""

# V1 Generators
from .generators import (
    ImageGenerator,
    AsyncImageGenerator,
    TextGenerator,
    AsyncTextGenerator,
    AudioGenerator,
    AsyncAudioGenerator,
    StreamChunk,
)

# Main client
from .blossom import Blossom, create_client

# Try to import V2 generators
try:
    from .generators_v2 import (
        ImageGeneratorV2,
        AsyncImageGeneratorV2,
        TextGeneratorV2,
        AsyncTextGeneratorV2,
    )
    V2_AVAILABLE = True
except ImportError:
    # V2 not available, set to None
    ImageGeneratorV2 = None
    AsyncImageGeneratorV2 = None
    TextGeneratorV2 = None
    AsyncTextGeneratorV2 = None
    V2_AVAILABLE = False

# Export helper modules (optional, for advanced users)
try:
    from .streaming_mixin import SSEParser, SyncStreamingMixin, AsyncStreamingMixin
    from .parameter_builder import (
        ImageParams, ImageParamsV2,
        TextParams, ChatParams, ChatParamsV2,
        AudioParams, ParameterValidator
    )
    HELPERS_AVAILABLE = True
except ImportError:
    HELPERS_AVAILABLE = False

__all__ = [
    # V1 Generators
    "ImageGenerator",
    "AsyncImageGenerator",
    "TextGenerator",
    "AsyncTextGenerator",
    "AudioGenerator",
    "AsyncAudioGenerator",
    "StreamChunk",

    # Main client
    "Blossom",
    "create_client",

    # V2 Generators
    "ImageGeneratorV2",
    "AsyncImageGeneratorV2",
    "TextGeneratorV2",
    "AsyncTextGeneratorV2",
    "V2_AVAILABLE",
]

# Conditionally add helpers to __all__ if available
if HELPERS_AVAILABLE:
    __all__.extend([
        "SSEParser",
        "SyncStreamingMixin",
        "AsyncStreamingMixin",
        "ImageParams",
        "ImageParamsV2",
        "TextParams",
        "ChatParams",
        "ChatParamsV2",
        "AudioParams",
        "ParameterValidator",
    ])