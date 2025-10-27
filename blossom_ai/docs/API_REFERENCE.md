# API Reference

Complete API documentation for all classes and methods in Blossom AI.

---

## Blossom Class

The main entry point for the SDK.

### Initialization

```python
Blossom(
    timeout=30,           # Request timeout in seconds
    debug=False,          # Enable debug mode
    api_token=None        # Optional API token for auth
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `int` | `30` | Request timeout in seconds |
| `debug` | `bool` | `False` | Enable debug logging with request IDs |
| `api_token` | `str` | `None` | API token for authentication (required for audio) |

### Context Manager Support

```python
# Synchronous context manager (recommended)
with Blossom() as ai:
    result = ai.text.generate("Hello")
    # Resources automatically cleaned up

# Asynchronous context manager (recommended)
async with Blossom() as ai:
    result = await ai.text.generate("Hello")
    # Resources automatically cleaned up
```

### Manual Cleanup

```python
# Async manual cleanup
client = Blossom()
try:
    url = await client.image.generate_url("test")
finally:
    await client.close()  # Explicitly close async sessions

# Sync - no manual cleanup needed (auto-closes on exit)
client = Blossom()
url = client.image.generate_url("test")
# Sync sessions cleaned up automatically
```

---

## Image Generator (`ai.image`)

Methods for image generation.

### `generate_url()`

Generate image URL without downloading (fastest method).

```python
url = ai.image.generate_url(prompt, **options)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | - | Image description (required) |
| `model` | `str` | `"flux"` | Model to use |
| `width` | `int` | `1024` | Image width in pixels |
| `height` | `int` | `1024` | Image height in pixels |
| `seed` | `int` | `None` | Seed for reproducibility |
| `nologo` | `bool` | `False` | Remove watermark (requires token) |
| `private` | `bool` | `False` | Keep image private |
| `enhance` | `bool` | `False` | Enhance prompt with AI |
| `safe` | `bool` | `False` | Enable NSFW filtering |
| `referrer` | `str` | `None` | Optional referrer parameter |

**Returns:** `str` - Direct URL to the generated image

**Example:**
```python
url = ai.image.generate_url(
    "a beautiful sunset",
    model="flux",
    width=1920,
    height=1080,
    seed=42
)
```

### `generate()`

Generate image and return bytes.

```python
image_bytes = ai.image.generate(prompt, **options)
```

**Parameters:** Same as `generate_url()`

**Returns:** `bytes` - Raw image data

**Example:**
```python
image_bytes = ai.image.generate("a cute robot")
with open("robot.jpg", "wb") as f:
    f.write(image_bytes)
```

### `save()`

Generate image and save to file.

```python
filepath = ai.image.save(prompt, filename, **options)
```

**Parameters:**
- `prompt` (str): Image description (required)
- `filename` (str): Output file path (required)
- `**options`: Same parameters as `generate_url()`

**Returns:** `str` - Path to saved file

**Example:**
```python
ai.image.save(
    "a majestic dragon",
    "dragon.jpg",
    width=1024,
    height=1024
)
```

### `models()`

List available image generation models.

```python
models = ai.image.models()
```

**Returns:** `list[str]` - List of model names

**Example:**
```python
models = ai.image.models()
print(models)  # ['flux', 'kontext', 'turbo', 'gptimage', ...]
```

---

## Text Generator (`ai.text`)

Methods for text generation.

### `generate()`

Generate text from a prompt.

```python
text = ai.text.generate(prompt, **options)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | - | Text prompt (required) |
| `model` | `str` | `"openai"` | Model to use |
| `system` | `str` | `None` | System message |
| `seed` | `int` | `None` | Seed for reproducibility |
| `temperature` | `float` | `None` | ⚠️ Not supported in current API |
| `json_mode` | `bool` | `False` | Force JSON output |
| `private` | `bool` | `False` | Keep response private |
| `stream` | `bool` | `False` | Stream response in real-time |

**Returns:** 
- `str` if `stream=False`
- `Iterator[str]` if `stream=True` (sync)
- `AsyncIterator[str]` if `stream=True` (async)

**Example:**
```python
# Simple generation
response = ai.text.generate("Explain Python")

# With streaming
for chunk in ai.text.generate("Tell a story", stream=True):
    print(chunk, end='', flush=True)

# JSON mode
response = ai.text.generate(
    "List 3 colors in JSON",
    json_mode=True
)
```

### `chat()`

Generate text with message history.

```python
text = ai.text.chat(messages, **options)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `list` | - | Chat message history (required) |
| `model` | `str` | `"openai"` | Model to use |
| `temperature` | `float` | `1.0` | Fixed at 1.0 (API limitation) |
| `stream` | `bool` | `False` | Stream response in real-time |
| `json_mode` | `bool` | `False` | Force JSON output |
| `private` | `bool` | `False` | Keep response private |

**Message Format:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "Tell me about AI"}
]
```

**Returns:** Same as `generate()`

**Example:**
```python
messages = [
    {"role": "system", "content": "You are a Python expert"},
    {"role": "user", "content": "How do I read a file?"}
]

response = ai.text.chat(messages)

# With streaming
for chunk in ai.text.chat(messages, stream=True):
    print(chunk, end='', flush=True)
```

### `models()`

List available text generation models.

```python
models = ai.text.models()
```

**Returns:** `list[str]` - List of model names

**Example:**
```python
models = ai.text.models()
print(models)  # ['openai', 'deepseek', 'gemini', 'mistral', ...]
```

---

## Audio Generator (`ai.audio`)

Methods for audio generation (Text-to-Speech). **Requires API token.**

### `generate()`

Generate audio from text.

```python
audio_bytes = ai.audio.generate(text, voice="alloy", **options)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | - | Text to speak (required) |
| `voice` | `str` | `"alloy"` | Voice to use |
| `model` | `str` | `"openai-audio"` | TTS model |

**Returns:** `bytes` - Raw audio data (MP3 format)

**Example:**
```python
with Blossom(api_token="YOUR_TOKEN") as ai:
    audio_bytes = ai.audio.generate("Hello world", voice="nova")
    with open("hello.mp3", "wb") as f:
        f.write(audio_bytes)
```

### `save()`

Generate audio and save to file.

```python
filepath = ai.audio.save(text, filename, voice="alloy", **options)
```

**Parameters:**
- `text` (str): Text to speak (required)
- `filename` (str): Output file path (required)
- `voice` (str): Voice to use (default: "alloy")
- `**options`: Additional options

**Returns:** `str` - Path to saved file

**Example:**
```python
with Blossom(api_token="YOUR_TOKEN") as ai:
    ai.audio.save(
        "Welcome to Blossom AI!",
        "welcome.mp3",
        voice="nova"
    )
```

### `voices()`

List available voices.

```python
voices = ai.audio.voices()
```

**Returns:** `list[str]` - List of voice names

**Example:**
```python
voices = ai.audio.voices()
print(voices)  # ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', ...]
```

---

## Error Handling

All Blossom AI exceptions inherit from `BlossomError`.

### Exception Types

| Exception | Description |
|-----------|-------------|
| `BlossomError` | Base error class for all errors |
| `NetworkError` | Connection issues, timeouts |
| `APIError` | HTTP errors from API (4xx, 5xx) |
| `AuthenticationError` | Invalid or missing API token (401) |
| `ValidationError` | Invalid parameters |
| `RateLimitError` | Too many requests (429) |
| `StreamError` | Streaming-specific errors (timeouts, interruptions) |

### Error Attributes

All errors include:
- `message`: Human-readable error description
- `error_type`: Type of error (e.g., "authentication_error")
- `suggestion`: Actionable suggestion to fix the issue
- `context`: Additional context (status code, request ID, etc.)
- `original_error`: Original exception if wrapped

### Example

```python
from blossom_ai import (
    Blossom,
    BlossomError,
    AuthenticationError,
    APIError,
    NetworkError,
    RateLimitError,
    StreamError
)

try:
    with Blossom() as ai:
        response = ai.text.generate("Hello")
        
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    print(f"Context: {e.context}")
    
except NetworkError as e:
    print(f"Connection issue: {e.message}")
    
except RateLimitError as e:
    print(f"Too many requests: {e.message}")
    if e.retry_after:
        print(f"Retry after: {e.retry_after} seconds")
    
except StreamError as e:
    print(f"Stream error: {e.message}")
    
except APIError as e:
    print(f"API error: {e.message}")
    if e.context:
        print(f"Status: {e.context.status_code}")
        print(f"Request ID: {e.context.request_id}")
    
except BlossomError as e:
    print(f"Error: {e.message}")
    if e.context and e.context.request_id:
        print(f"Request ID: {e.context.request_id}")
```

---

## Async/Sync Unified API

All methods work in both synchronous and asynchronous contexts automatically.

### Synchronous Usage

```python
from blossom_ai import Blossom

with Blossom() as ai:
    url = ai.image.generate_url("sunset")
    image = ai.image.generate("sunset")
    text = ai.text.generate("Hello")
```

### Asynchronous Usage

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom() as ai:
        url = await ai.image.generate_url("sunset")
        image = await ai.image.generate("sunset")
        text = await ai.text.generate("Hello")
        
        # Streaming in async
        async for chunk in await ai.text.generate("Story", stream=True):
            print(chunk, end='')

asyncio.run(main())
```

---

## Notes

- **Token Security**: Tokens are never exposed in URLs generated by `generate_url()`
- **Streaming Timeout**: Default 30 seconds between chunks
- **Resource Management**: Always use context managers for proper cleanup
- **Request IDs**: Available in error contexts for debugging
- **Dynamic Models**: Model lists update from API at runtime with fallbacks