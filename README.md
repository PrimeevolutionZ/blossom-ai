# 🌸 Blossom AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.1-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)

**A beautiful Python SDK for Pollinations.AI - Generate images, text, and audio with AI.**

Blossom AI is a comprehensive, easy-to-use Python library that provides unified access to Pollinations.AI's powerful AI generation services. Create stunning images, generate text with various models, and convert text to speech with multiple voices - all through a beautifully designed, intuitive API.

## ✨ What's New in v0.2.2
- 🌊 **Streaming Support** - Real-time text generation with streaming responses

## ⚠️ Important Notes

- **Audio Generation**: Requires authentication (API token)
- **Hybrid API**: Automatically detects sync/async context - no need for separate imports
- **Streaming**: Works in both sync and async contexts with iterators
- **Robust Error Handling**: Graceful fallbacks when API endpoints are unavailable
- **Resource Management**: Use context managers for proper cleanup

## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 📝 **Text Generation** - Generate text with various AI models
- 🌊 **Streaming** - Real-time text generation with streaming responses (NEW!)
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🚀 **Unified API** - Same code works in sync and async contexts
- 🎨 **Beautiful Errors** - Helpful error messages with actionable suggestions
- 🔄 **Reproducible** - Use seeds for consistent results
- ⚡ **Smart Async** - Automatically switches between sync/async modes
- 🛡️ **Robust** - Graceful error handling with fallbacks
- 🧹 **Clean** - Proper resource management and cleanup

## 📦 Installation

```bash
pip install eclips-blossom-ai
```

## 🚀 Quick Start

```python
from blossom_ai import Blossom

# Initialize
ai = Blossom()

# Generate an image
ai.image.save("a beautiful sunset over mountains", "sunset.jpg")

# Generate text
response = ai.text.generate("Explain quantum computing in simple terms")
print(response)

# Stream text in real-time (NEW!)
for chunk in ai.text.generate("Tell me a story", stream=True):
    print(chunk, end='', flush=True)

# Generate audio (requires API token)
ai = Blossom(api_token="YOUR_TOKEN")
ai.audio.save("Hello, welcome to Blossom AI!", "welcome.mp3", voice="nova")
```

## 🌊 Streaming Support (NEW!)

Get responses in real-time as they're generated:

### Synchronous Streaming

```python
from blossom_ai import Blossom

ai = Blossom()

# Simple streaming
for chunk in ai.text.generate("Write a poem about AI", stream=True):
    print(chunk, end='', flush=True)

# Chat streaming
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Explain Python"}
]
for chunk in ai.text.chat(messages, stream=True):
    print(chunk, end='', flush=True)

# Collect full response from stream
chunks = []
for chunk in ai.text.generate("Hello", stream=True):
    chunks.append(chunk)
full_response = ''.join(chunks)
```

### Asynchronous Streaming

```python
import asyncio
from blossom_ai import Blossom

async def stream_example():
    ai = Blossom()
    
    # Async streaming
    async for chunk in await ai.text.generate("Tell me a story", stream=True):
        print(chunk, end='', flush=True)
    
    # Async chat streaming
    messages = [{"role": "user", "content": "Hello!"}]
    async for chunk in await ai.text.chat(messages, stream=True):
        print(chunk, end='', flush=True)

asyncio.run(stream_example())
```

### Parallel Async Streaming

```python
import asyncio
from blossom_ai import Blossom

async def collect_stream(ai, prompt):
    """Collect all chunks from a stream"""
    chunks = []
    async for chunk in await ai.text.generate(prompt, stream=True):
        chunks.append(chunk)
    return ''.join(chunks)

async def parallel_streams():
    ai = Blossom()
    
    # Run multiple streams in parallel
    results = await asyncio.gather(
        collect_stream(ai, "What is Python?"),
        collect_stream(ai, "What is JavaScript?"),
        collect_stream(ai, "What is Rust?")
    )
    
    for i, result in enumerate(results, 1):
        print(f"Stream {i}: {result}\n")

asyncio.run(parallel_streams())
```

### Streaming to File

```python
from blossom_ai import Blossom

ai = Blossom()

# Write stream directly to file
with open('output.txt', 'w', encoding='utf-8') as f:
    for chunk in ai.text.generate("Write an article", stream=True):
        f.write(chunk)
        f.flush()  # Ensure real-time writing
```

### Streaming with Processing

```python
from blossom_ai import Blossom

ai = Blossom()

# Process chunks on-the-fly
word_count = 0
for chunk in ai.text.generate("Write a paragraph", stream=True):
    print(chunk, end='', flush=True)
    word_count += len(chunk.split())

print(f"\nTotal words: {word_count}")
```

## 🔄 Unified Sync/Async API

The same API works seamlessly in both synchronous and asynchronous contexts:

```python
from blossom_ai import Blossom

ai = Blossom()

# Synchronous usage
image_data = ai.image.generate("a cute robot")
text = ai.text.generate("Hello world")

# Asynchronous usage - same methods!
import asyncio

async def main():
    ai = Blossom()
    image_data = await ai.image.generate("a cute robot")
    text = await ai.text.generate("Hello world")
    
asyncio.run(main())
```

**No need for separate imports or different APIs** - Blossom automatically detects your context and does the right thing!

## 📖 Examples

### Image Generation

```python
from blossom_ai import Blossom

ai = Blossom()

# Generate and save an image
ai.image.save(
    prompt="a majestic dragon in a mystical forest",
    filename="dragon.jpg",
    width=1024,
    height=1024,
    model="flux"
)

# Get image data as bytes
image_data = ai.image.generate("a cute robot")

# Use different models
image_data = ai.image.generate("futuristic city", model="turbo")

# Reproducible results with seed
image_data = ai.image.generate("random art", seed=42)

# List available models (dynamically fetched from API)
models = ai.image.models()
print(models)  # ['flux', 'kontext', 'turbo', 'gptimage', ...]
```

### Text Generation

```python
from blossom_ai import Blossom

ai = Blossom()

# Simple text generation
response = ai.text.generate("What is Python?")

# With system message
response = ai.text.generate(
    prompt="Write a haiku about coding",
    system="You are a creative poet"
)

# Reproducible results with seed
response = ai.text.generate(
    prompt="Generate a random idea",
    seed=42  # Same seed = same result
)

# JSON mode
response = ai.text.generate(
    prompt="List 3 colors in JSON format",
    json_mode=True
)

# Streaming (NEW!)
for chunk in ai.text.generate("Tell a story", stream=True):
    print(chunk, end='', flush=True)

# Chat with message history
response = ai.text.chat([
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's the weather like?"}
])

# Chat with streaming (NEW!)
messages = [{"role": "user", "content": "Explain AI"}]
for chunk in ai.text.chat(messages, stream=True):
    print(chunk, end='', flush=True)

# List available models (dynamically updated)
models = ai.text.models()
print(models)  # ['deepseek', 'gemini', 'mistral', 'openai', 'qwen-coder', ...]
```

### Audio Generation

```python
from blossom_ai import Blossom

# Audio generation requires an API token
ai = Blossom(api_token="YOUR_API_TOKEN")

# Generate and save audio
ai.audio.save(
    text="Welcome to the future of AI",
    filename="welcome.mp3",
    voice="nova"
)

# Try different voices
ai.audio.save("Hello", "hello_alloy.mp3", voice="alloy")
ai.audio.save("Hello", "hello_echo.mp3", voice="echo")

# Get audio data as bytes
audio_data = ai.audio.generate("Hello world", voice="shimmer")

# List available voices (dynamically updated)
voices = ai.audio.voices()
print(voices)  # ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', ...]
```

## 🎯 Supported Parameters

### Image Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | str | - | Image description (required) |
| model | str | "flux" | Model to use |
| width | int | 1024 | Image width in pixels |
| height | int | 1024 | Image height in pixels |
| seed | int | None | Seed for reproducibility |
| nologo | bool | False | Remove watermark (requires token) |
| private | bool | False | Keep image private |
| enhance | bool | False | Enhance prompt with AI |
| safe | bool | False | Enable NSFW filtering |

### Text Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | str | - | Text prompt (required) |
| model | str | "openai" | Model to use |
| system | str | None | System message |
| seed | int | None | Seed for reproducibility |
| temperature | float | None | ⚠️ Not supported in current API |
| json_mode | bool | False | Force JSON output |
| private | bool | False | Keep response private |
| **stream** | **bool** | **False** | **Stream response in real-time (NEW!)** |

### Text Chat

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| messages | list | - | Chat message history (required) |
| model | str | "openai" | Model to use |
| temperature | float | 1.0 | Fixed at 1.0 (API limitation) |
| **stream** | **bool** | **False** | **Stream response in real-time (NEW!)** |
| json_mode | bool | False | Force JSON output |
| private | bool | False | Keep response private |

### Audio Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| text | str | - | Text to speak (required) |
| voice | str | "alloy" | Voice to use |
| model | str | "openai-audio" | TTS model |

## 🛠️ API Reference

### Blossom Class

```python
ai = Blossom(
    timeout=30,           # Request timeout in seconds
    debug=False,          # Enable debug mode
    api_token=None        # Optional API token for auth
)

# Generators (work in sync and async)
ai.image   # Image generation
ai.text    # Text generation (with streaming!)
ai.audio   # Audio generation (requires token)
```

### Context Manager Support

```python
# Synchronous context manager
with Blossom() as ai:
    result = ai.text.generate("Hello")
    # Resources automatically cleaned up

# Asynchronous context manager
async with Blossom() as ai:
    result = await ai.text.generate("Hello")
    # Resources automatically cleaned up
```

### Image Generator Methods

```python
# Generate image (returns bytes)
image_data = ai.image.generate(prompt, **options)

# Save image to file (returns filepath)
filepath = ai.image.save(prompt, filename, **options)

# List available models
models = ai.image.models()  # Returns list of model names
```

### Text Generator Methods

```python
# Generate text (returns str or Iterator[str] if stream=True)
text = ai.text.generate(prompt, **options)

# Generate with streaming
for chunk in ai.text.generate(prompt, stream=True):
    print(chunk, end='')

# Chat with message history (returns str or Iterator[str] if stream=True)
text = ai.text.chat(messages, **options)

# Chat with streaming
for chunk in ai.text.chat(messages, stream=True):
    print(chunk, end='')

# List available models
models = ai.text.models()  # Returns list of model names
```

### Audio Generator Methods

```python
# Generate audio (returns bytes)
audio_data = ai.audio.generate(text, voice="alloy")

# Save audio to file (returns filepath)
filepath = ai.audio.save(text, filename, voice="nova")

# List available voices
voices = ai.audio.voices()  # Returns list of voice names
```

## 🎨 Error Handling

Blossom AI provides structured, informative errors with actionable suggestions:

```python
from blossom_ai import (
    Blossom, 
    BlossomError,
    NetworkError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError
)

ai = Blossom()

try:
    response = ai.text.generate("Hello")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    # Output: Visit https://auth.pollinations.ai to get an API token
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    print(f"Context: {e.context}")
    
except NetworkError as e:
    print(f"Connection issue: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except RateLimitError as e:
    print(f"Too many requests: {e.message}")
    
except APIError as e:
    print(f"API error: {e.message}")
    print(f"Status: {e.context.status_code if e.context else 'unknown'}")
    
except BlossomError as e:
    # Catch-all for any Blossom error
    print(f"Error type: {e.error_type}")
    print(f"Message: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    if e.original_error:
        print(f"Original error: {e.original_error}")
```

### Error Types

- **NetworkError** - Connection issues, timeouts
- **APIError** - HTTP errors from API (4xx, 5xx)
- **AuthenticationError** - Invalid or missing API token (401)
- **ValidationError** - Invalid parameters
- **RateLimitError** - Too many requests (429)
- **BlossomError** - Base error class for all errors

## 🔑 Authentication

For higher rate limits and advanced features, get an API token:

```python
from blossom_ai import Blossom

# With authentication
ai = Blossom(api_token="YOUR_API_TOKEN")

# Now you can use features requiring auth
ai.image.save("sunset", "sunset.jpg", nologo=True)  # Remove watermark
ai.audio.save("Hello", "hello.mp3")  # Audio requires token
```

Get your API token at [auth.pollinations.ai](https://auth.pollinations.ai)

## 🔄 Async Usage

The same API works in async contexts automatically:

```python
import asyncio
from blossom_ai import Blossom

async def generate_content():
    ai = Blossom()
    
    # All methods work with await
    image = await ai.image.generate("landscape")
    text = await ai.text.generate("story")
    audio = await ai.audio.generate("speech")
    
    # Streaming with async
    async for chunk in await ai.text.generate("poem", stream=True):
        print(chunk, end='')
    
    # Context manager support
    async with Blossom() as ai:
        result = await ai.text.generate("Hello")
    
    return image, text, audio

# Run async function
asyncio.run(generate_content())
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_examples.py

# Run only sync tests
python test_examples.py --sync

# Run only async tests
python test_examples.py --async

# Run only streaming tests (NEW!)
python test_examples.py --streaming

# With API token
python test_examples.py --token YOUR_TOKEN
```

## 🛡️ Robustness Features

Blossom AI includes several robustness features:

### Retry Logic
- Automatic retry with exponential backoff for failed requests
- Configurable retry attempts (default: 3)
- Smart retry only for retryable errors (502, timeouts)

### Resource Management
- Centralized session management with `SessionManager`
- Proper cleanup with context managers
- Weakref-based cleanup to prevent memory leaks
- Thread-safe async session handling across event loops

### Streaming Support
- Server-Sent Events (SSE) parsing
- Works in both sync and async contexts
- Proper error handling during streaming
- Resource cleanup even if stream is interrupted

### Error Recovery
- Graceful fallbacks when API endpoints are unavailable
- Dynamic model discovery with fallback to defaults
- Continues operation even when some endpoints fail

### Dynamic Models
- Models automatically update from API responses
- Fallback to sensible defaults if API unavailable
- Type-safe model validation with helpful error messages

## 📚 Advanced Usage

### Custom Timeout

```python
# Set custom timeout for slow connections
ai = Blossom(timeout=60)  # 60 seconds
```

### Debug Mode

```python
# Enable debug mode for detailed logging
ai = Blossom(debug=True)
```

### Streaming with Timeout

```python
import asyncio
from blossom_ai import Blossom

async def stream_with_timeout():
    ai = Blossom()
    
    try:
        async with asyncio.timeout(5):  # 5 second timeout
            async for chunk in await ai.text.generate("Long story", stream=True):
                print(chunk, end='')
    except asyncio.TimeoutError:
        print("\n⚠️ Stream timed out")

asyncio.run(stream_with_timeout())
```

### Resource Cleanup

```python
# Manual cleanup (usually not needed)
ai = Blossom()
# ... use ai ...
ai._cleanup_sync()  # For sync generators

# Async cleanup
async with Blossom() as ai:
    # Resources auto-cleaned
    pass
```

## 🗂️ Architecture

Blossom AI uses a clean, modular architecture:

- **Base Generators** - `SyncGenerator` and `AsyncGenerator` base classes
- **Session Managers** - Centralized session lifecycle management
- **Dynamic Models** - Models that update from API at runtime
- **Hybrid Generators** - Automatic sync/async detection
- **Streaming Support** - SSE parsing with Iterator/AsyncIterator
- **Structured Errors** - Rich error context with suggestions

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- **Temperature parameter**: The GET text endpoint doesn't support temperature parameter
- **Chat temperature**: Fixed at 1.0 in OpenAI-compatible endpoint
- **API Variability**: Some endpoints may occasionally return unexpected formats - handled gracefully with fallbacks

## 📋 Changelog

### v0.2.2 (Current)
- 🌊 **NEW**: Streaming support for text generation (sync & async)


### v0.2.1
- ✨ Unified sync/async API with hybrid generators
- 🗂️ Refactored architecture with base classes
- 🛡️ Enhanced error handling with structured errors
- 📦 Centralized session management
- 🎯 Dynamic model discovery from API
- ⚡ Improved retry logic with tenacity
- 🧹 Better resource cleanup with weakref

## 🔗 Links

- [Pollinations.AI](https://pollinations.ai)
- [API Documentation](https://pollinations.ai/api)
- [Auth Portal](https://auth.pollinations.ai)
- [PyPI Package](https://pypi.org/project/eclips-blossom-ai/)

## ❤️ Credits

Built with love using the Pollinations.AI platform.

Made with 🌸 by the eclips team

---

*This README reflects v0.2.2 with streaming support and the latest refactored architecture.*