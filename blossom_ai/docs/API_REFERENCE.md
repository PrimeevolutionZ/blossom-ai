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

## 🔧 Advanced Usage (v0.4.4+)

For advanced users who want more control or are building custom generators.

### Parameter Validation

Validate parameters before making API calls:

```python
from blossom_ai.generators import ParameterValidator
from blossom_ai.core.errors import BlossomError

try:
    # Validate prompt length
    ParameterValidator.validate_prompt_length(
        prompt="Your long prompt...",
        max_length=1000,
        param_name="prompt"
    )
    
    # Validate image dimensions
    ParameterValidator.validate_dimensions(
        width=1024,
        height=1024,
        min_size=64,
        max_size=2048
    )
    
    # Validate temperature
    ParameterValidator.validate_temperature(temperature=0.7)
    
    # If all valid, proceed with generation
    result = client.text.generate(prompt)
    
except BlossomError as e:
    print(f"Validation failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

### Type-Safe Parameters

Use dataclass builders for type safety and validation:

```python
from blossom_ai.generators import ImageParams, TextParams

# V1 Image parameters
params = ImageParams(
    model="flux",
    width=1024,
    height=1024,
    seed=42,
    nologo=True,
    enhance=True
)

# Convert to dict (only non-default values!)
request_params = params.to_dict()
print(request_params)
# Output: {'width': 1024, 'height': 1024, 'seed': 42, 'nologo': 'true', 'enhance': 'true'}
# Note: 'model' is not included (it's the default value)

# V1 Text parameters
text_params = TextParams(
    model="openai",
    system="You are a helpful assistant",
    temperature=0.7,
    json_mode=True
)

# Smart conversion (json_mode → json parameter)
request_params = text_params.to_dict()
print(request_params)
# Output: {'system': '...', 'temperature': 0.7, 'json': 'true'}
```

### Custom SSE Parsing

Parse Server-Sent Events streams manually:

```python
from blossom_ai.generators import SSEParser

parser = SSEParser()

# Parse individual lines
for line in your_stream_lines:
    parsed = parser.parse_line(line)
    
    if parsed is None:
        # Invalid or empty line
        continue
    
    if parsed.get('done'):
        # Stream finished
        break
    
    # Extract content (OpenAI format)
    content = parser.extract_content(parsed)
    if content:
        print(content, end='', flush=True)
```

**Example with requests:**
```python
import requests
from blossom_ai.generators import SSEParser

response = requests.get("https://api.example.com/stream", stream=True)
parser = SSEParser()

for line in response.iter_lines(decode_unicode=True):
    if line:
        parsed = parser.parse_line(line)
        if parsed:
            content = parser.extract_content(parsed)
            if content:
                yield content
```

### Custom Generator with Streaming

Extend base generators with your own logic:

```python
from blossom_ai.generators import SyncGenerator, SyncStreamingMixin
from blossom_ai.generators import SSEParser
from blossom_ai.core.config import ENDPOINTS

class MyCustomGenerator(SyncGenerator, SyncStreamingMixin):
    """Custom generator with specialized logic"""
    
    def __init__(self, timeout=30):
        super().__init__(ENDPOINTS.TEXT, timeout)
        self._sse_parser = SSEParser()
    
    def generate_with_metadata(self, prompt: str, stream: bool = False):
        """Generate text with custom metadata"""
        # Custom request building
        url = f"{self.base_url}/custom-endpoint"
        params = {
            "prompt": prompt,
            "custom_param": "value"
        }
        
        response = self._make_request("GET", url, params=params, stream=stream)
        
        if stream:
            # Use unified streaming from mixin
            return self._stream_sse_response(response, self._sse_parser)
        else:
            return response.text
    
    def _validate_prompt(self, prompt: str) -> None:
        """Custom validation"""
        from blossom_ai.generators import ParameterValidator
        ParameterValidator.validate_prompt_length(prompt, 2000, "prompt")

# Usage
gen = MyCustomGenerator()
result = gen.generate_with_metadata("Hello", stream=True)

for chunk in result:
    print(chunk, end='', flush=True)
```

### Async Custom Generator

Same pattern for async generators:

```python
from blossom_ai.generators import AsyncGenerator, AsyncStreamingMixin
from blossom_ai.generators import SSEParser

class MyAsyncGenerator(AsyncGenerator, AsyncStreamingMixin):
    """Async custom generator"""
    
    def __init__(self):
        super().__init__("https://api.example.com", timeout=30)
        self._sse_parser = SSEParser()
    
    async def custom_generate(self, prompt: str, stream: bool = False):
        url = f"{self.base_url}/endpoint"
        
        if stream:
            response = await self._make_request("GET", url, stream=True)
            # Use async streaming mixin
            return self._stream_sse_response(response, self._sse_parser)
        else:
            data = await self._make_request("GET", url)
            return data.decode('utf-8')

# Usage
import asyncio

async def main():
    gen = MyAsyncGenerator()
    
    # Streaming
    async for chunk in await gen.custom_generate("Hello", stream=True):
        print(chunk, end='', flush=True)
    
    await gen.close()

asyncio.run(main())
```

### Why Use These Utilities?

**Parameter Builders:**
- ✅ Type hints and IDE autocomplete
- ✅ Automatic validation
- ✅ Filter out None and default values
- ✅ Consistent parameter handling

**SSE Parser:**
- ✅ Reusable across projects
- ✅ Handles [DONE] markers
- ✅ Robust JSON parsing
- ✅ OpenAI format compatible

**Streaming Mixins:**
- ✅ Timeout handling built-in
- ✅ Proper resource cleanup
- ✅ Unicode error handling
- ✅ Works with both line-based and chunk-based streams

### Testing Components

These utilities are easy to unit test:

```python
import pytest
from blossom_ai.generators import SSEParser, ImageParams, ParameterValidator
from blossom_ai.core.errors import BlossomError

def test_sse_parser():
    parser = SSEParser()
    
    # Test valid line
    line = 'data: {"choices":[{"delta":{"content":"Hello"}}]}'
    parsed = parser.parse_line(line)
    assert parsed is not None
    assert parser.extract_content(parsed) == "Hello"
    
    # Test [DONE] marker
    done_line = 'data: [DONE]'
    parsed = parser.parse_line(done_line)
    assert parsed['done'] is True

def test_image_params():
    params = ImageParams(
        width=512,
        height=512,
        nologo=True
    )
    
    data = params.to_dict()
    
    # Default model not included
    assert 'model' not in data
    # Custom values included
    assert data['width'] == 512
    assert data['height'] == 512
    assert data['nologo'] == 'true'  # Boolean converted to string

def test_validator():
    # Valid prompt
    ParameterValidator.validate_prompt_length("Short", 1000, "prompt")
    
    # Too long prompt
    with pytest.raises(BlossomError) as exc:
        ParameterValidator.validate_prompt_length("x" * 2000, 1000, "prompt")
    
    assert "exceeds maximum length" in str(exc.value)
```

### When to Use Advanced Features

**Use parameter validation when:**
- Building user-facing applications
- Need early error detection
- Want clear error messages
- Implementing input forms

**Use parameter builders when:**
- Building SDKs or libraries
- Need type safety
- Want IDE autocomplete
- Have complex parameter logic

**Use SSE parser when:**
- Building custom streaming clients
- Integrating with other APIs
- Need standalone parsing logic
- Testing streaming implementations

**Use streaming mixins when:**
- Extending Blossom generators
- Building custom API clients
- Need reliable streaming with timeouts
- Want consistent error handling

---

## 📚 Related Documentation

- **[Refactoring Summary](REFACTORING.md)** - Architecture details
- **[V2 API Reference](V2_API_REFERENCE.md)** - V2-specific advanced usage
- **[Error Handling](ERROR_HANDLING.md)** - Error handling patterns
- **[Contributing Guide](../../CONTRIBUTING.md)** - How to contribute

---
---

## Notes

- **Token Security**: Tokens are never exposed in URLs generated by `generate_url()`
- **Streaming Timeout**: Default 30 seconds between chunks
- **Resource Management**: Always use context managers for proper cleanup
- **Request IDs**: Available in error contexts for debugging
- **Dynamic Models**: Model lists update from API at runtime with fallbacks