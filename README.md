# 🌸 Blossom AI

A beautiful Python SDK for [Pollinations.AI](https://pollinations.ai) - Generate images, text, and audio with AI.

**✨ Now with Hybrid Sync/Async Support!** - Use the same code in both synchronous and asynchronous contexts.

---

> **Warning!!**
> 
> To generate audio, you need authentication!

---

## 🎯 What's New in V0.2.0

- **🔄 Hybrid Sync/Async Support** - Write once, run anywhere! The same `Blossom` client works in both sync and async contexts
- **⚡ Automatic Context Detection** - No need to choose between sync/async - Blossom detects your context automatically
- **🛡️ Improved Error Handling** - Better retry logic with exponential backoff for 502 errors
- **🔒 Proper Resource Management** - Async sessions are properly managed and cleaned up

---

## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 📝 **Text Generation** - Generate text with various models
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🔄 **Hybrid Sync/Async** - Same API works in both synchronous and asynchronous code
- 🚀 **Simple API** - Easy to use, beautifully designed
- 🎨 **Beautiful Errors** - Helpful error messages with suggestions
- 🔁 **Reproducible** - Use seeds for consistent results
- 🛡️ **Robust** - Automatic retries with exponential backoff

## 📦 Installation

```bash
pip install eclips-blossom-ai
```

## 🚀 Quick Start

### Synchronous Usage (No `await` needed)

```python
from blossom_ai import Blossom

# Initialize
ai = Blossom()

# Generate an image
ai.image.save("a beautiful sunset over mountains", "sunset.jpg")

# Generate text
response = ai.text.generate("Explain quantum computing in simple terms")
print(response)

# Generate audio (requires authentication)
ai.audio.save("Hello, welcome to Blossom AI!", "welcome.mp3")
```

### Asynchronous Usage (With `await`)

```python
import asyncio
from blossom_ai import Blossom

async def main():
    # Same Blossom client!
    ai = Blossom()
    
    # Just add await
    await ai.image.save("a beautiful sunset", "sunset.jpg")
    
    response = await ai.text.generate("Explain quantum computing")
    print(response)
    
    await ai.audio.save("Hello, world!", "hello.mp3")
    
    # Clean up (optional but recommended)
    await ai.close()

asyncio.run(main())
```

### Async Context Manager (Recommended for Async)

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom() as ai:
        # Automatic cleanup when done!
        await ai.image.save("a majestic dragon", "dragon.jpg")
        text = await ai.text.generate("Write a haiku")
        print(text)

asyncio.run(main())
```

## 📖 Detailed Examples

### Image Generation

```python
from blossom_ai import Blossom

ai = Blossom()

# Synchronous - no await needed
ai.image.save(
    prompt="a majestic dragon in a mystical forest",
    filename="dragon.jpg",
    width=1024,
    height=1024,
    model="flux",
    seed=42  # For reproducible results
)

# Get image data as bytes
image_data = ai.image.generate("a cute robot")

# List available models
models = ai.image.models()
print(models)
```

### Async Image Generation

```python
import asyncio
from blossom_ai import Blossom

async def generate_images():
    ai = Blossom()
    
    # Parallel image generation!
    tasks = [
        ai.image.save("a sunset", "sunset.jpg"),
        ai.image.save("a forest", "forest.jpg"),
        ai.image.save("mountains", "mountains.jpg")
    ]
    
    await asyncio.gather(*tasks)
    await ai.close()

asyncio.run(generate_images())
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

# Chat with message history
response = ai.text.chat([
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's the weather like?"}
])

# JSON mode
response = ai.text.generate(
    prompt="List 3 programming languages",
    json_mode=True
)
```

### Async Text Generation

```python
import asyncio
from blossom_ai import Blossom

async def chat_example():
    async with Blossom() as ai:
        # Multiple requests in parallel
        responses = await asyncio.gather(
            ai.text.generate("Explain AI in one sentence"),
            ai.text.generate("What is machine learning?"),
            ai.text.generate("Define neural networks")
        )
        
        for response in responses:
            print(response)

asyncio.run(chat_example())
```

### Audio Generation

**⚠️ Authentication Required!** Audio generation requires an API token from [auth.pollinations.ai](https://auth.pollinations.ai).

```python
from blossom_ai import Blossom

# Initialize with API token
ai = Blossom(api_token="YOUR_API_TOKEN")

# Generate and save audio
ai.audio.save(
    text="Welcome to the future of AI",
    filename="welcome.mp3",
    voice="nova"
)

# Get audio data as bytes
audio_data = ai.audio.generate("Hello world!", voice="alloy")

# Available voices
voices = ai.audio.voices()
print(voices)  # ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
```

## 🎯 Supported Parameters

### Text Generation

| Parameter | Type | Description | Supported |
|-----------|------|-------------|-----------|
| `prompt` | str | Your text prompt | ✅ |
| `model` | str | Model to use (default: "openai") | ✅ |
| `system` | str | System message to guide behavior | ✅ |
| `seed` | int | For reproducible results | ✅ |
| `json_mode` | bool | Return JSON response | ✅ |
| `private` | bool | Keep response private | ✅ |
| `stream` | bool | Stream response | ✅ |

**Note:** Temperature parameter support depends on the endpoint used (GET vs POST).

### Image Generation

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | Image description |
| `model` | str | Model (default: "flux") |
| `width` | int | Width in pixels |
| `height` | int | Height in pixels |
| `seed` | int | Reproducibility |
| `nologo` | bool | Remove watermark (requires auth) |
| `enhance` | bool | Enhance prompt with AI |
| `safe` | bool | NSFW filtering |
| `private` | bool | Keep image private |

### Audio Generation

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | str | Text to convert to speech |
| `voice` | str | Voice (default: "alloy") |
| `model` | str | Model (default: "openai-audio") |

## 🛠️ API Reference

### Blossom Class

```python
ai = Blossom(
    timeout=30,           # Request timeout in seconds
    debug=False,          # Enable debug mode
    api_token=None        # Your API token (optional)
)

# Access generators
ai.image   # HybridImageGenerator
ai.text    # HybridTextGenerator
ai.audio   # HybridAudioGenerator

# Async cleanup (only needed in async context)
await ai.close()
```

### HybridImageGenerator

Works in both sync and async contexts!

```python
# Sync usage
image_data = ai.image.generate(prompt, **options)
filepath = ai.image.save(prompt, filename, **options)
models = ai.image.models()

# Async usage (same methods, just add await)
image_data = await ai.image.generate(prompt, **options)
filepath = await ai.image.save(prompt, filename, **options)
models = await ai.image.models()
```

### HybridTextGenerator

```python
# Sync usage
text = ai.text.generate(prompt, **options)
text = ai.text.chat(messages, **options)
models = ai.text.models()

# Async usage
text = await ai.text.generate(prompt, **options)
text = await ai.text.chat(messages, **options)
models = await ai.text.models()
```

### HybridAudioGenerator

```python
# Sync usage
audio_data = ai.audio.generate(text, voice="alloy")
filepath = ai.audio.save(text, filename, voice="nova")
voices = ai.audio.voices()

# Async usage
audio_data = await ai.audio.generate(text, voice="alloy")
filepath = await ai.audio.save(text, filename, voice="nova")
voices = await ai.audio.voices()
```

## 🎨 Error Handling

Blossom AI provides beautiful, helpful error messages:

```python
from blossom_ai import Blossom, BlossomError

ai = Blossom()

try:
    response = ai.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")
    print(f"Type: {e.error_type}")
    print(f"Suggestion: {e.suggestion}")
```

### Error Types

- `ErrorType.NETWORK` - Connection issues
- `ErrorType.API` - API errors (including 402 Payment Required)
- `ErrorType.INVALID_PARAM` - Invalid parameters
- `ErrorType.UNKNOWN` - Unexpected errors

### Automatic Retries

Blossom automatically retries failed requests with exponential backoff for:
- HTTP 502 errors (up to 3 attempts)
- Connection errors
- Chunked encoding errors

## 🔒 Authentication

For higher rate limits and access to advanced features (like audio generation and `nologo` for images):

1. Visit [auth.pollinations.ai](https://auth.pollinations.ai) to register and obtain an API token
2. Initialize Blossom with your token:

```python
from blossom_ai import Blossom

ai = Blossom(api_token="YOUR_API_TOKEN_HERE")

# Now you can use authenticated features
ai.image.save("sunset", "sunset.jpg", nologo=True)
ai.audio.save("Hello!", "hello.mp3")
```

## 📝 Best Practices

### For Synchronous Code

```python
from blossom_ai import Blossom

ai = Blossom()

# No special cleanup needed - sessions are managed automatically
image = ai.image.generate("a sunset")
text = ai.text.generate("Hello")
```

### For Asynchronous Code

```python
import asyncio
from blossom_ai import Blossom

# Recommended: Use context manager
async def main():
    async with Blossom() as ai:
        image = await ai.image.generate("a sunset")
        text = await ai.text.generate("Hello")
    # Automatic cleanup here

# Or manually call close()
async def main():
    ai = Blossom()
    try:
        image = await ai.image.generate("a sunset")
    finally:
        await ai.close()

asyncio.run(main())
```

## 🛡️ Known Limitations

- **Audio Generation**: Requires authentication (Seed tier or higher)
- **Prompt Length**: Image prompts are limited to 200 characters
- **Temperature Parameter**: Not supported in GET text endpoint
- **502 Errors**: May occur during high load - automatic retries are in place

## 📚 More Examples

Check out the `tests/` directory for more detailed examples:
- `test_examples.py` -  generation examples

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- [Pollinations.AI](https://pollinations.ai)
- [API Documentation](https://github.com/pollinations/pollinations)
- [Auth Portal](https://auth.pollinations.ai)

## ❤️ Credits

Built with love using the [Pollinations.AI](https://pollinations.ai) platform.

---

Made with 🌸 by the eclips team