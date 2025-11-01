"""
Blossom AI - Generators Module
"""

from .generators import (
    ImageGenerator,
    AsyncImageGenerator,
    TextGenerator,
    AsyncTextGenerator,
    AudioGenerator,
    AsyncAudioGenerator,
    StreamChunk,
)

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

    # V2 Generators (may be None if not available)
    "ImageGeneratorV2",
    "AsyncImageGeneratorV2",
    "TextGeneratorV2",
    "AsyncTextGeneratorV2",
    "V2_AVAILABLE",
]