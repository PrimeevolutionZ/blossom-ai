# 📖 V2 API Reference

> **Complete reference for Blossom AI V2 API**

This document provides detailed reference information for all V2 API methods, parameters, and return values.

---

## 📋 Table of Contents

- [Client Initialization](#-client-initialization)
- [Image Generation](#-image-generation)
- [Text Generation](#-text-generation)
- [Chat Methods](#-chat-methods)
- [Streaming](#-streaming)
- [Model Information](#-model-information)
- [Error Handling](#-error-handling)

---

## 🎯 Client Initialization

### Blossom()

Initialize the Blossom AI client with V2 API support.

```python
from blossom_ai import Blossom

client = Blossom(
    api_version="v2",
    api_token="your_token_here",
    timeout=30,
    debug=False
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_version` | `str` | `"v1"` | API version: `"v1"` (legacy) or `"v2"` (new) |
| `api_token` | `Optional[str]` | `None` | API token from enter.pollinations.ai |
| `timeout` | `int` | `30` | Request timeout in seconds |
| `debug` | `bool` | `False` | Enable debug logging |

#### Returns

`Blossom` instance with `.image`, `.text`, and `.audio` generators.

#### Example

```python
# V2 with authentication
client = Blossom(
    api_version="v2",
    api_token="sk_your_secret_key",
    timeout=60
)

# V2 without token (free tier)
client = Blossom(api_version="v2")

# Context manager (recommended)
with Blossom(api_version="v2", api_token="token") as client:
    image = client.image.generate("sunset")
```

---

## 🎨 Image Generation

### client.image.generate()

Generate an image from a text prompt using V2 API.

```python
image_bytes = client.image.generate(
    prompt="a beautiful sunset over mountains",
    model="flux",
    width=1024,
    height=1024,
    seed=42,
    enhance=False,
    negative_prompt="blurry, low quality",
    private=False,
    nologo=True,
    nofeed=False,
    safe=False,
    quality="medium",
    image=None,
    transparent=False,
    guidance_scale=7.5
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | **Required** | Text description of desired image (max 200 chars) |
| `model` | `str` | `"flux"` | Model to use: `"flux"`, `"turbo"`, etc. |
| `width` | `int` | `1024` | Image width in pixels |
| `height` | `int` | `1024` | Image height in pixels |
| `seed` | `int` | `42` | Random seed for reproducibility |
| `enhance` | `bool` | `False` | Enhance prompt automatically |
| `negative_prompt` | `str` | `"worst quality, blurry"` | Elements to exclude |
| `private` | `bool` | `False` | Make generation private |
| `nologo` | `bool` | `False` | Remove Pollinations watermark |
| `nofeed` | `bool` | `False` | Don't add to public feed (**V2 only**) |
| `safe` | `bool` | `False` | Enable safety filter |
| `quality` | `str` | `"medium"` | Quality: `"low"`, `"medium"`, `"high"`, `"hd"` (**V2 only**) |
| `image` | `Optional[str]` | `None` | Source image URL for img2img (**V2 only**) |
| `transparent` | `bool` | `False` | Generate with transparency (**V2 only**) |
| `guidance_scale` | `Optional[float]` | `None` | Prompt adherence (1.0-20.0) (**V2 only**) |

#### Returns

`bytes` - Raw image data (PNG format)

#### Example

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Basic generation
    image = client.image.generate("a sunset")
    
    # Advanced V2 features
    image = client.image.generate(
        prompt="professional portrait, studio lighting",
        quality="hd",
        guidance_scale=8.0,
        negative_prompt="blurry, distorted, low quality",
        nologo=True,
        nofeed=True
    )
    
    # Save to file
    with open("portrait.png", "wb") as f:
        f.write(image)
```

---

### client.image.save()

Generate and save image to file in one call.

```python
filepath = client.image.save(
    prompt="a sunset",
    filename="sunset.png",
    quality="hd",
    guidance_scale=7.5
)
```

#### Parameters

Same as `generate()`, plus:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | **Required** | Path where to save the image |

#### Returns

`str` - Path to saved file

---

### client.image.models()

Get list of available image models from V2 API.

```python
models = client.image.models()
```

#### Parameters

None

#### Returns

`List[str]` - List of available model names

#### Example

```python
with Blossom(api_version="v2", api_token="token") as client:
    models = client.image.models()
    print(f"Available models: {models}")
    # ['flux', 'turbo', 'gptimage', 'kontext', ...]
    
    # Use discovered model
    image = client.image.generate("sunset", model=models[0])
```

---

## 💬 Text Generation

### client.text.generate()

Generate text from a prompt using V2 API.

```python
response = client.text.generate(
    prompt="Explain quantum computing in simple terms",
    model="openai",
    system=None,
    temperature=1.0,
    max_tokens=None,
    stream=False,
    json_mode=False,
    tools=None
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | **Required** | Input text prompt (max 10,000 chars) |
| `model` | `str` | `"openai"` | Model: `"openai"`, `"deepseek"`, `"qwen-coder"`, etc. |
| `system` | `Optional[str]` | `None` | System message for behavior |
| `temperature` | `float` | `1.0` | Randomness (0.0-2.0, V2 extended range) |
| `max_tokens` | `Optional[int]` | `None` | Maximum response length (**V2 only**) |
| `stream` | `bool` | `False` | Enable streaming |
| `json_mode` | `bool` | `False` | Force JSON output |
| `tools` | `Optional[List[Dict]]` | `None` | Function definitions (**V2 only**) |

#### Additional V2 Parameters (via **kwargs)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frequency_penalty` | `float` | `0.0` | Reduce word repetition (0.0-2.0) |
| `presence_penalty` | `float` | `0.0` | Encourage topic diversity (0.0-2.0) |
| `top_p` | `float` | `1.0` | Nucleus sampling (0.1-1.0) |
| `n` | `int` | `1` | Number of completions |
| `tool_choice` | `Union[str, Dict]` | `None` | Tool selection: `"auto"`, `"none"`, or specific tool |

#### Returns

- `str` if `stream=False`
- `Iterator[str]` if `stream=True`

#### Example

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Basic generation
    response = client.text.generate(
        "Explain AI in one sentence",
        max_tokens=50
    )
    print(response)
    
    # Advanced V2 features
    response = client.text.generate(
        prompt="Write a creative story about robots",
        model="openai",
        temperature=1.2,
        max_tokens=300,
        frequency_penalty=0.8,
        presence_penalty=0.6,
        top_p=0.95
    )
    print(response)
    
    # JSON mode
    response = client.text.generate(
        "Generate a user profile with name, age, city",
        json_mode=True,
        max_tokens=100
    )
    
    import json
    data = json.loads(response)
    print(data)
```

---

## 💭 Chat Methods

### client.text.chat()

Multi-turn conversation with message history.

```python
response = client.text.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help?"},
        {"role": "user", "content": "Tell me about AI"}
    ],
    model="openai",
    temperature=1.0,
    max_tokens=None,
    stream=False,
    json_mode=False,
    tools=None,
    tool_choice=None,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    top_p=1.0,
    n=1
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `List[Dict[str, Any]]` | **Required** | Conversation history |
| `model` | `str` | `"openai"` | Model to use |
| `temperature` | `float` | `1.0` | Randomness (0.0-2.0) |
| `max_tokens` | `Optional[int]` | `None` | Maximum response length (**V2 only**) |
| `stream` | `bool` | `False` | Enable streaming |
| `json_mode` | `bool` | `False` | Force JSON output |
| `tools` | `Optional[List[Dict]]` | `None` | Function calling definitions (**V2 only**) |
| `tool_choice` | `Optional[Union[str, Dict]]` | `None` | Tool selection (**V2 only**) |
| `frequency_penalty` | `float` | `0.0` | Reduce repetition (**V2 only**) |
| `presence_penalty` | `float` | `0.0` | Topic diversity (**V2 only**) |
| `top_p` | `float` | `1.0` | Nucleus sampling (**V2 only**) |
| `n` | `int` | `1` | Number of completions (**V2 only**) |

#### Message Format

```python
{
    "role": "user" | "assistant" | "system",
    "content": "Message text"
}
```

#### Returns

- `str` if `stream=False`
- `Iterator[str]` if `stream=True`

#### Example

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    messages = [
        {"role": "system", "content": "You are a math tutor"},
        {"role": "user", "content": "What is 15% of 200?"}
    ]
    
    response = client.text.chat(
        messages=messages,
        model="openai",
        max_tokens=100
    )
    
    print(response)
    
    # Add to history
    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": "Show me the calculation"})
    
    response2 = client.text.chat(messages=messages)
    print(response2)
```

---

### Function Calling Example

```python
from blossom_ai import Blossom

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. London"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.chat(
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"}
        ],
        tools=tools,
        tool_choice="auto"  # Let AI decide when to call
    )
    
    print(response)
    # AI will indicate it wants to call get_weather function
```

---

## 🌊 Streaming

### Synchronous Streaming

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Stream text generation
    for chunk in client.text.generate(
        "Tell me a story",
        stream=True,
        max_tokens=200
    ):
        print(chunk, end="", flush=True)
    
    print()  # Newline
    
    # Stream chat
    for chunk in client.text.chat(
        messages=[{"role": "user", "content": "Explain AI"}],
        stream=True
    ):
        print(chunk, end="", flush=True)
```

### Asynchronous Streaming

```python
import asyncio
from blossom_ai import Blossom

async def stream_text():
    async with Blossom(api_version="v2", api_token="token") as client:
        async for chunk in await client.text.generate(
            "Write a poem",
            stream=True,
            max_tokens=150
        ):
            print(chunk, end="", flush=True)

asyncio.run(stream_text())
```

### Streaming Parameters

All streaming methods support the same parameters as their non-streaming counterparts, plus:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `stream` | `bool` | `False` | Enable streaming mode |

---

## 📊 Model Information

### client.text.models()

Get list of available text models from V2 API.

```python
models = client.text.models()
```

#### Parameters

None

#### Returns

`List[str]` - List of available model names (including aliases)

#### Example

```python
with Blossom(api_version="v2", api_token="token") as client:
    models = client.text.models()
    print(f"Available models: {models}")
    # ['openai', 'gpt-4', 'deepseek', 'qwen-coder', 'mistral', ...]
    
    # Check if specific model available
    if "qwen-coder" in models:
        response = client.text.generate(
            "Write Python code to sort a list",
            model="qwen-coder"
        )
```

---

### client.image.models()

Get list of available image models from V2 API.

```python
models = client.image.models()
```

#### Parameters

None

#### Returns

`List[str]` - List of available model names

#### Example

```python
with Blossom(api_version="v2", api_token="token") as client:
    models = client.image.models()
    print(f"Available models: {models}")
    # ['flux', 'turbo', 'gptimage', 'kontext', ...]
```

---

## 🛡️ Error Handling

All methods can raise the following errors:

### Error Types

| Error Class | When Raised | Attributes |
|-------------|-------------|------------|
| `NetworkError` | Connection issues | `.message`, `.suggestion`, `.context` |
| `APIError` | API errors (4xx, 5xx) | `.message`, `.context.status_code` |
| `AuthenticationError` | Invalid/missing token | `.message`, `.suggestion` |
| `ValidationError` | Invalid parameters | `.message`, `.suggestion` |
| `RateLimitError` | Too many requests | `.message`, `.retry_after` |
| `StreamError` | Streaming failures | `.message`, `.original_error` |

### Error Example

```python
from blossom_ai import (
    Blossom,
    NetworkError,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

try:
    with Blossom(api_version="v2", api_token="token") as client:
        response = client.text.generate("test", max_tokens=100)
        
except NetworkError as e:
    print(f"Network issue: {e.message}")
    
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Get token at: https://enter.pollinations.ai")
    
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    print(f"Retry after: {e.retry_after}s")
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except APIError as e:
    print(f"API error: {e.message}")
    if e.context:
        print(f"Status: {e.context.status_code}")
        print(f"URL: {e.context.url}")
```

### HTTP Status Codes

| Status | Error Type | Description |
|--------|-----------|-------------|
| 400 | `APIError` | Bad request (invalid parameters) |
| 401 | `AuthenticationError` | Unauthorized (invalid token) |
| 402 | `APIError` | Payment required (upgrade needed) |
| 429 | `RateLimitError` | Too many requests |
| 500 | `APIError` | Server error |
| 502 | `APIError` | Bad gateway (retry with backoff) |
| 503 | `APIError` | Service unavailable |

---

## 🔄 Context Managers

### Synchronous Context Manager

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Resources automatically cleaned up on exit
    image = client.image.generate("sunset")
    text = client.text.generate("hello")
# client.close_sync() called automatically
```

### Asynchronous Context Manager

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom(api_version="v2", api_token="token") as client:
        # Async resources automatically cleaned up
        image = await client.image.generate("sunset")
        text = await client.text.generate("hello")
    # await client.close() called automatically

asyncio.run(main())
```

### Manual Resource Management

```python
from blossom_ai import Blossom

# Sync
client = Blossom(api_version="v2", api_token="token")
try:
    image = client.image.generate("sunset")
finally:
    client.close_sync()

# Async
async def example():
    client = Blossom(api_version="v2", api_token="token")
    try:
        image = await client.image.generate("sunset")
    finally:
        await client.close()
```

---

## 📝 Complete Example

```python
from blossom_ai import Blossom, BlossomError, RateLimitError
import json

def generate_content():
    """Complete example using V2 API"""
    
    with Blossom(api_version="v2", api_token="your_token") as client:
        
        # 1. Check available models
        print("=== Available Models ===")
        print(f"Image: {client.image.models()}")
        print(f"Text: {client.text.models()}")
        
        # 2. Generate HD image
        print("\n=== Generating Image ===")
        try:
            image = client.image.generate(
                prompt="professional portrait, studio lighting",
                quality="hd",
                guidance_scale=8.0,
                negative_prompt="blurry, distorted",
                nologo=True,
                nofeed=True
            )
            
            with open("portrait.png", "wb") as f:
                f.write(image)
            print(f"✅ Image saved: {len(image)} bytes")
            
        except RateLimitError as e:
            print(f"⚠️ Rate limited: wait {e.retry_after}s")
            
        # 3. Generate structured JSON
        print("\n=== Generating JSON ===")
        response = client.text.generate(
            prompt="Generate a user profile with name, age, email, interests",
            json_mode=True,
            max_tokens=150
        )
        
        data = json.loads(response)
        print(f"✅ JSON: {json.dumps(data, indent=2)}")
        
        # 4. Stream response
        print("\n=== Streaming Response ===")
        print("AI: ", end="", flush=True)
        
        for chunk in client.text.generate(
            "Explain quantum computing in 2 sentences",
            stream=True,
            max_tokens=100
        ):
            print(chunk, end="", flush=True)
        
        print()
        
        # 5. Chat with history
        print("\n=== Chat Conversation ===")
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What's 15% of 200?"}
        ]
        
        response = client.text.chat(
            messages=messages,
            max_tokens=50,
            frequency_penalty=0.3
        )
        print(f"Assistant: {response}")

if __name__ == "__main__":
    try:
        generate_content()
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        if e.suggestion:
            print(f"💡 Suggestion: {e.suggestion}")
```

---

## 🔗 Related Documentation

- **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)** - Migrate from V1 to V2
- **[V2 Image Generation](V2_IMAGE_GENERATION.md)** - Detailed image guide
- **[V2 Text Generation](V2_TEXT_GENERATION.md)** - Detailed text guide
- **[Error Handling](ERROR_HANDLING.md)** - Error handling best practices
- **[Resource Management](RESOURCE_MANAGEMENT.md)** - Context managers and cleanup

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>