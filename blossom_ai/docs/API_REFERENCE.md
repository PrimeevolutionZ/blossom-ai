# 📖 API Reference

Complete API reference for Blossom AI v0.5.0 (V2 API).

---

## 📋 Table of Contents

- [Client](#client)
- [Image Generator](#image-generator)
- [Text Generator](#text-generator)
- [Message Builder](#message-builder)
- [Models](#models)
- [Errors](#errors)
- [Utilities](#utilities)

---

## 🌸 Client

### Blossom

Main client class for interacting with the API.

#### Initialization

```python
from blossom_ai import Blossom

client = Blossom(
    api_token: str = None,
    timeout: int = 30,
    debug: bool = False
)
```

**Parameters:**
- `api_token` (str, optional): API token from [enter.pollinations.ai](https://enter.pollinations.ai). If not provided, reads from `POLLINATIONS_API_KEY` or `BLOSSOM_API_KEY` env var.
- `timeout` (int): Request timeout in seconds. Default: 30
- `debug` (bool): Enable debug logging. Default: False

**Example:**
```python
# With explicit token
client = Blossom(api_token="your-token")

# From environment variable
client = Blossom()

# With custom timeout
client = Blossom(api_token="your-token", timeout=60)
```

#### Context Manager (Recommended)

```python
with Blossom(api_token="your-token") as client:
    # Use client
    response = client.text.generate("Hello")
# Automatically closes connection
```

#### Manual Cleanup

```python
client = Blossom(api_token="your-token")
try:
    response = client.text.generate("Hello")
finally:
    client.close_sync()  # Must call manually
```

#### Async Context Manager

```python
async with Blossom(api_token="your-token") as client:
    response = await client.text.generate("Hello")
```

#### Properties

- `client.image` - ImageGenerator instance
- `client.text` - TextGenerator instance

---

## 🖼️ Image Generator

Generate images with the V2 API.

### Methods

#### generate()

Generate image and return bytes.

```python
image_bytes = client.image.generate(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    model: str = "flux",
    seed: int = 42,
    quality: str = "medium",
    guidance_scale: float = None,
    negative_prompt: str = "worst quality, blurry",
    enhance: bool = False,
    transparent: bool = False,
    image: str = None,
    private: bool = False,
    nologo: bool = False,
    nofeed: bool = False,
    safe: bool = False,
    timeout: int = None
) -> bytes
```

**Parameters:**
- `prompt` (str, required): Image description
- `width` (int): Image width, 64-2048. Default: 1024
- `height` (int): Image height, 64-2048. Default: 1024
- `model` (str): Model name. Default: "flux"
- `seed` (int): Random seed for reproducibility. Default: 42
- `quality` (str): "low", "medium", "high", "hd". Default: "medium"
- `guidance_scale` (float): Prompt adherence, 1.0-20.0. Default: None
- `negative_prompt` (str): What to avoid. Default: "worst quality, blurry"
- `enhance` (bool): Auto-enhance prompt. Default: False
- `transparent` (bool): Transparent background. Default: False
- `image` (str): Input image URL for img2img. Default: None
- `private` (bool): Private generation. Default: False
- `nologo` (bool): Remove watermark. Default: False
- `nofeed` (bool): Don't add to public feed. Default: False
- `safe` (bool): Enable safety filter. Default: False
- `timeout` (int): Override default timeout. Default: None

**Returns:** bytes - Image data

**Example:**
```python
with Blossom(api_token="your-token") as client:
    image_data = client.image.generate(
        "a beautiful sunset",
        width=1920,
        height=1080,
        quality="hd"
    )
    
    with open("sunset.jpg", "wb") as f:
        f.write(image_data)
```

#### save()

Generate and save image to file.

```python
filepath = client.image.save(
    prompt: str,
    filename: str | Path,
    width: int = 1024,
    height: int = 1024,
    # ... same parameters as generate()
) -> str
```

**Returns:** str - Path to saved file

**Example:**
```python
with Blossom(api_token="your-token") as client:
    path = client.image.save(
        "a cute cat",
        "cat.jpg",
        width=512,
        height=512
    )
    print(f"Saved to: {path}")
```

#### generate_url()

Generate image URL without downloading.

```python
url = client.image.generate_url(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    # ... same parameters as generate()
) -> str
```

**Returns:** str - Image URL

**Example:**
```python
with Blossom(api_token="your-token") as client:
    url = client.image.generate_url(
        "a robot",
        width=256,
        height=256
    )
    print(f"URL: {url}")
```

**⚠️ Security Note:** API token is NEVER included in URL. It's sent in Authorization header.

#### models()

List available image models.

```python
models = client.image.models() -> list[str]
```

**Returns:** list[str] - Model names

**Example:**
```python
with Blossom(api_token="your-token") as client:
    models = client.image.models()
    print(f"Available: {models}")
```

---

## 💬 Text Generator

Generate text with the V2 API.

### Methods

#### generate()

Generate text response.

```python
response = client.text.generate(
    prompt: str,
    system: str = None,
    model: str = "openai",
    temperature: float = 1.0,
    max_tokens: int = None,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    top_p: float = 1.0,
    stream: bool = False,
    json_mode: bool = False,
    tools: list = None,
    tool_choice: str | dict = None,
    thinking: dict = None,
    modalities: list[str] = None,
    audio: dict = None,
    timeout: int = None
) -> str | Iterator[str]
```

**Parameters:**
- `prompt` (str, required): User message
- `system` (str): System message for instructions. Default: None
- `model` (str): Model name. Default: "openai"
- `temperature` (float): Creativity, 0.0-2.0. Default: 1.0
- `max_tokens` (int): Max response length. Default: None (model default)
- `frequency_penalty` (float): Reduce repetition, -2.0 to 2.0. Default: 0.0
- `presence_penalty` (float): Encourage new topics, -2.0 to 2.0. Default: 0.0
- `top_p` (float): Nucleus sampling, 0.0-1.0. Default: 1.0
- `stream` (bool): Enable streaming. Default: False
- `json_mode` (bool): Force JSON output. Default: False
- `tools` (list): Function calling tools. Default: None
- `tool_choice` (str | dict): Tool selection. Default: None
- `thinking` (dict): Native reasoning config (V2). Default: None
- `modalities` (list[str]): Output modalities ["text", "audio"]. Default: None
- `audio` (dict): Audio config. Default: None
- `timeout` (int): Override default timeout. Default: None

**Returns:**
- If `stream=False`: str - Full response
- If `stream=True`: Iterator[str] - Chunks

**Example - Simple:**
```python
with Blossom(api_token="your-token") as client:
    response = client.text.generate("What is Python?")
    print(response)
```

**Example - With Parameters:**
```python
with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a creative story",
        system="You are a creative writer",
        temperature=1.5,
        max_tokens=500
    )
    print(response)
```

**Example - Streaming:**
```python
with Blossom(api_token="your-token") as client:
    for chunk in client.text.generate("Count to 5", stream=True):
        print(chunk, end="", flush=True)
```

**Example - JSON Mode:**
```python
import json

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        "List 3 colors in JSON",
        json_mode=True
    )
    data = json.loads(response)
    print(data)
```

#### chat()

Chat completion with message history.

```python
response = client.text.chat(
    messages: list[dict],
    model: str = "openai",
    temperature: float = 1.0,
    max_tokens: int = None,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    top_p: float = 1.0,
    stream: bool = False,
    json_mode: bool = False,
    tools: list = None,
    tool_choice: str | dict = None,
    thinking: dict = None,
    modalities: list[str] = None,
    audio: dict = None,
    timeout: int = None
) -> str | Iterator[str]
```

**Parameters:**
- `messages` (list[dict], required): Conversation messages
- Other parameters same as `generate()`

**Message Format:**
```python
messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
]
```

**Returns:** Same as `generate()`

**Example - Basic Chat:**
```python
with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What is 2+2?"}
    ]
    
    response = client.text.chat(messages)
    print(response)
```

**Example - Multi-Turn:**
```python
with Blossom(api_token="your-token") as client:
    conversation = [
        {"role": "system", "content": "You are helpful"}
    ]
    
    # Turn 1
    conversation.append({"role": "user", "content": "Hi"})
    response = client.text.chat(conversation)
    conversation.append({"role": "assistant", "content": response})
    
    # Turn 2
    conversation.append({"role": "user", "content": "Tell me a joke"})
    response = client.text.chat(conversation)
    print(response)
```

**Example - Vision (NEW in v0.5.0):**
```python
from blossom_ai import MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/photo.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

#### models()

List available text models.

```python
models = client.text.models() -> list[str]
```

**Returns:** list[str] - Model names

**Example:**
```python
with Blossom(api_token="your-token") as client:
    models = client.text.models()
    print(f"Available: {models}")
```

---

## 🔨 Message Builder

Helper for creating vision messages (NEW in v0.5.0).

### MessageBuilder.text_message()

Create regular text message.

```python
from blossom_ai import MessageBuilder

message = MessageBuilder.text_message(
    role: str,
    content: str
) -> dict
```

**Parameters:**
- `role` (str): "system", "user", or "assistant"
- `content` (str): Message text

**Returns:** dict - Message object

**Example:**
```python
msg = MessageBuilder.text_message("user", "Hello!")
# Returns: {"role": "user", "content": "Hello!"}
```

### MessageBuilder.image_message()

Create vision message with image.

```python
from blossom_ai import MessageBuilder

message = MessageBuilder.image_message(
    role: str,
    text: str,
    image_url: str = None,
    image_path: str = None,
    detail: str = "auto"
) -> dict
```

**Parameters:**
- `role` (str): "user" (typically)
- `text` (str): Question/instruction about the image
- `image_url` (str): URL to image. Default: None
- `image_path` (str): Path to local image. Default: None
- `detail` (str): "low", "auto", or "high". Default: "auto"

**Note:** Provide either `image_url` OR `image_path`, not both.

**Returns:** dict - Message object with image

**Example - From URL:**
```python
msg = MessageBuilder.image_message(
    role="user",
    text="What's this?",
    image_url="https://example.com/photo.jpg",
    detail="auto"
)
```

**Example - From File:**
```python
msg = MessageBuilder.image_message(
    role="user",
    text="Describe this",
    image_path="photo.jpg",
    detail="high"
)
```

---

## 🎭 Models

### ImageModel

Image model information.

```python
from blossom_ai import ImageModel

# Get default models
defaults = ImageModel.get_defaults() -> list[str]

# Get all models from API
all_models = ImageModel.list_all(api_token="your-token") -> list[str]

# Reset cache
ImageModel.reset()
```

**Default Models:**
```python
["flux", "turbo"]
```

### TextModel

Text model information.

```python
from blossom_ai import TextModel

# Get default models
defaults = TextModel.get_defaults() -> list[str]

# Get all models from API
all_models = TextModel.list_all(api_token="your-token") -> list[str]

# Reset cache
TextModel.reset()
```

**Default Models:**
```python
["openai", "openai-fast", "openai-large", "openai-reasoning"]
```

---

## 🛡️ Errors

### Error Hierarchy

```
BlossomError (base)
├── NetworkError
├── APIError
│   ├── AuthenticationError
│   ├── RateLimitError
│   └── ValidationError
├── StreamError
├── TimeoutError
└── FileTooLargeError
```

### BlossomError

Base exception class.

```python
from blossom_ai import BlossomError

try:
    # API call
    pass
except BlossomError as e:
    print(e.error_type)    # ErrorType enum
    print(e.message)       # Human-readable message
    print(e.suggestion)    # How to fix (if available)
    print(e.status_code)   # HTTP status (if applicable)
```

**Attributes:**
- `error_type` (ErrorType): Error type enum
- `message` (str): Error description
- `suggestion` (str | None): How to fix
- `status_code` (int | None): HTTP status code
- `retry_after` (int | None): Retry delay for rate limits

### ErrorType (Enum)

```python
from blossom_ai import ErrorType

ErrorType.NETWORK           # Network/connection error
ErrorType.TIMEOUT           # Request timeout
ErrorType.AUTH              # Authentication failed
ErrorType.RATE_LIMIT        # Rate limit exceeded
ErrorType.INVALID_PARAM     # Invalid parameter
ErrorType.API_ERROR         # General API error
ErrorType.STREAM_ERROR      # Streaming error
ErrorType.FILE_TOO_LARGE    # File exceeds limit
```

### Specific Exceptions

#### AuthenticationError

```python
from blossom_ai import AuthenticationError

try:
    client = Blossom(api_token="invalid")
    client.text.generate("test")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Fix: {e.suggestion}")
```

#### RateLimitError

```python
from blossom_ai import RateLimitError
import time

try:
    client.text.generate("test")
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    if e.retry_after:
        print(f"Retry after: {e.retry_after}s")
        time.sleep(e.retry_after)
```

#### ValidationError

```python
from blossom_ai import ValidationError

try:
    client.image.generate("x" * 300)  # Too long
except ValidationError as e:
    print(f"Invalid: {e.message}")
```

#### StreamError

```python
from blossom_ai import StreamError

try:
    for chunk in client.text.generate("test", stream=True):
        print(chunk)
except StreamError as e:
    print(f"Stream failed: {e.message}")
```

#### TimeoutError

```python
from blossom_ai import TimeoutError

try:
    client = Blossom(timeout=5)
    client.text.generate("long task")
except TimeoutError as e:
    print(f"Timeout: {e.message}")
```

#### FileTooLargeError

```python
from blossom_ai import FileTooLargeError

try:
    from blossom_ai.utils import read_file_for_prompt
    content = read_file_for_prompt("huge_file.txt")
except FileTooLargeError as e:
    print(f"File too large: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

---

## 🛠️ Utilities

### File Reader

Read files for prompts with size limits.

```python
from blossom_ai.utils import read_file_for_prompt, get_file_info

# Read file (respects API limits)
content = read_file_for_prompt(
    filepath: str | Path,
    max_length: int = 8000,
    truncate_if_needed: bool = False
) -> str

# Get file information
info = get_file_info(filepath: str | Path) -> dict
```

**Example:**
```python
from blossom_ai.utils import read_file_for_prompt

# Read file for prompt
content = read_file_for_prompt("code.py", max_length=5000)

# Build prompt
prompt = f"Review this code:\n\n{content}"
```

### Reasoning Enhancer

Add structured thinking to prompts.

```python
from blossom_ai.utils import ReasoningEnhancer, create_reasoning_enhancer

# Create enhancer
enhancer = ReasoningEnhancer()

# Enhance prompt
enhanced = enhancer.enhance(
    prompt: str,
    level: str = "medium",
    mode: str = "auto",
    api_version: str = "v2",
    model: str = "openai"
) -> str | dict
```

**Levels:** "low", "medium", "high", "adaptive"

**Modes:**
- "prompt" - Prompt engineering (works with all models)
- "native" - Native reasoning (OpenAI models only in V2)
- "auto" - Auto-detect best mode

**Example:**
```python
from blossom_ai import Blossom
from blossom_ai.utils import create_reasoning_enhancer

enhancer = create_reasoning_enhancer(level="high", mode="auto")

with Blossom(api_token="your-token") as client:
    enhanced = enhancer.enhance(
        "Design a microservices architecture",
        api_version="v2",
        model="openai"
    )
    
    if isinstance(enhanced, dict):
        # Native reasoning
        response = client.text.chat(
            messages=[{"role": "user", "content": enhanced["prompt"]}],
            thinking=enhanced.get("thinking")
        )
    else:
        # Prompt reasoning
        response = client.text.generate(enhanced)
    
    print(response)
```

### Cache Manager

Cache API responses to reduce costs.

```python
from blossom_ai.utils import cached, get_cache, configure_cache

# Decorator
@cached(ttl=3600)
def expensive_call(prompt):
    with Blossom(api_token="your-token") as client:
        return client.text.generate(prompt)

# Manual cache
cache = get_cache()
cache.set("key", "value", ttl=3600)
value = cache.get("key")

# Configure
configure_cache(
    backend="hybrid",  # memory, disk, hybrid
    max_memory_items=1000,
    disk_path="./cache"
)
```

**Example:**
```python
from blossom_ai.utils import cached

@cached(ttl=3600)
def generate_cached(prompt):
    with Blossom(api_token="your-token") as client:
        return client.text.generate(prompt)

# First call: hits API
result = generate_cached("Hello")

# Second call: from cache (instant)
result = generate_cached("Hello")
```

### CLI Interface

Command-line interface for quick tasks.

```bash
# Interactive mode
python -m blossom_ai.utils.cli

# Quick commands
python -m blossom_ai.utils.cli --image "sunset" --output sunset.png
python -m blossom_ai.utils.cli --text "Write a poem"
```

---

## 📚 Type Hints

### Common Types

```python
from typing import Iterator, Union
from pathlib import Path

# Image methods
def generate(prompt: str, **kwargs) -> bytes: ...
def save(prompt: str, filename: Union[str, Path], **kwargs) -> str: ...
def generate_url(prompt: str, **kwargs) -> str: ...

# Text methods
def generate(prompt: str, stream: bool = False, **kwargs) -> Union[str, Iterator[str]]: ...
def chat(messages: list[dict], stream: bool = False, **kwargs) -> Union[str, Iterator[str]]: ...

# Message types
Message = dict[str, Union[str, list]]
MessageContent = Union[str, list[dict]]
```

---

## 🔗 Related Documentation

- **[Quick Start](QUICKSTART.md)** - Get started quickly
- **[Image Generation](IMAGE_GENERATION.md)** - Image generation guide
- **[Text Generation](TEXT_GENERATION.md)** - Text generation guide
- **[Vision Support](VISION.md)** - Vision features guide
- **[Error Handling](ERROR_HANDLING.md)** - Error handling guide

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md)

</div>