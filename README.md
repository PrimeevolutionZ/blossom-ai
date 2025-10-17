# 🌸 Blossom AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

**A beautiful Python SDK for Pollinations.AI - Generate images, text, and audio with AI.**

Blossom AI is a comprehensive, easy-to-use Python library that provides unified access to Pollinations.AI's powerful AI generation services. Create stunning images, generate text with various models, and convert text to speech with multiple voices - all through a beautifully designed, intuitive API.

## ⚠️ Important Notes

- **Audio Generation**: Requires authentication (API token)
- **Robust Error Handling**: Graceful fallbacks when API endpoints are unavailable
- **Async Support**: Full asynchronous API for high-performance applications

## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 📝 **Text Generation** - Generate text with various AI models
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🚀 **Simple API** - Easy to use, beautifully designed interface
- 🎨 **Beautiful Errors** - Helpful error messages with suggestions
- 🔄 **Reproducible** - Use seeds for consistent results
- ⚡ **Async Support** - Full asynchronous API for better performance
- 🛡️ **Robust** - Graceful error handling and fallbacks

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

# Generate audio (requires API token)
ai.audio.save("Hello, welcome to Blossom AI!", "welcome.mp3", voice="nova")
```

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

# List available models
models = ai.image.models()
print(models)  # ['flux', 'kontext', 'turbo', 'gptimage']
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

# List available models
models = ai.text.models()
print(models)  # ['deepseek', 'gemini', 'mistral', 'openai', 'qwen-coder', ...]
```

### Audio Generation

```python
from blossom_ai import Blossom

# For audio generation, you need an API token
ai = Blossom(api_token="YOUR_API_TOKEN")

# Generate and save audio
ai.audio.save(
    text="Welcome to the future of AI",
    filename="welcome.mp3",
    voice="nova"
)

# Get available voices
voices = ai.audio.voices()
print(voices)  # ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', ...]

# Generate audio data as bytes
audio_data = ai.audio.generate("Hello world", voice="alloy")
```

## 🎯 Supported Parameters

### Text Generation

| Parameter | Type | Description | Supported |
|-----------|------|-------------|-----------|
| prompt | str | Your text prompt | ✅ |
| model | str | Model to use (default: "openai") | ✅ |
| system | str | System message to guide behavior | ✅ |
| seed | int | For reproducible results | ✅ |
| json_mode | bool | Return JSON response | ✅ |
| private | bool | Keep response private | ✅ |
| temperature | float | Randomness control | ❌ Not supported in GET API |

**Note**: The current Pollinations.AI GET endpoint doesn't support the temperature parameter. For temperature control, you would need to use their POST endpoint, which is currently experiencing issues.

### Image Generation

| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | str | Image description |
| model | str | Model (default: "flux") |
| width | int | Width in pixels |
| height | int | Height in pixels |
| seed | int | Reproducibility |
| nologo | bool | Remove watermark (requires auth) |
| enhance | bool | Enhance prompt with AI |
| safe | bool | NSFW filtering |

### Audio Generation

| Parameter | Type | Description |
|-----------|------|-------------|
| text | str | Text to convert to speech |
| voice | str | Voice to use (default: "alloy") |
| model | str | Model (default: "openai-audio") |

## 🛠️ API Methods

### Blossom Class

```python
ai = Blossom(timeout=30, api_token=None)  # Main client

ai.image  # ImageGenerator instance
ai.text   # TextGenerator instance  
ai.audio  # AudioGenerator instance
```

### ImageGenerator

```python
# Generate image (returns bytes)
image_data = ai.image.generate(prompt, **options)

# Save image to file
filepath = ai.image.save(prompt, filename, **options)

# List available models
models = ai.image.models()
```

### TextGenerator

```python
# Generate text (simple)
text = ai.text.generate(prompt, **options)

# Chat with message history
text = ai.text.chat(messages, **options)

# List available models
models = ai.text.models()
```

### AudioGenerator

```python
# Generate audio (returns bytes)
audio_data = ai.audio.generate(text, voice="alloy")

# Save audio to file
filepath = ai.audio.save(text, filename, voice="nova")

# List available voices
voices = ai.audio.voices()
```

## 🎨 Error Handling

Blossom AI provides beautiful, helpful error messages with suggestions for resolution:

```python
from blossom_ai import Blossom, BlossomError

ai = Blossom()

try:
    response = ai.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

## 🔄 Async Support

Blossom AI supports full asynchronous operations for better performance:

```python
import asyncio
from blossom_ai import Blossom

async def main():
    ai = Blossom()
    
    # Async image generation
    image_data = await ai.image.generate("a beautiful landscape")
    
    # Async text generation
    text = await ai.text.generate("Tell me a story")
    
    # Run async function
    await main()
```

## 🔑 Authentication (Optional)

For higher rate limits, access to advanced features (like `nologo` for image generation), and to avoid Payment Required errors, you can provide an API token.

Visit [auth.pollinations.ai](https://auth.pollinations.ai) to register your application and obtain an API token.

```python
from blossom_ai import Blossom

# Initialize with your API token
ai = Blossom(api_token="YOUR_API_TOKEN_HERE")

# Now you can use features that require authentication, e.g., nologo
ai.image.save("a beautiful sunset", "sunset_no_logo.jpg", nologo=True)
```

If no `api_token` is provided, the library will operate in anonymous mode with default rate limits and feature restrictions.

## 🧪 Testing

The project includes comprehensive tests to ensure reliability:

```bash
# Run all tests
python test_examples.py

# Run only sync tests
python test_examples.py --sync

# Run only async tests
python test_examples.py --async
```

## 📚 More Examples

Check out the `tests/` directory for more detailed examples:

- `test_examples.py` - Complete test suite with all features
- Individual test files for specific functionality

## 🛡️ Robustness Features

Blossom AI includes several robustness features:

- **Graceful Fallbacks**: When API endpoints return invalid data, the library provides sensible defaults
- **Connection Retry Logic**: Automatic retry with exponential backoff for failed requests
- **Resource Management**: Proper cleanup of network resources to prevent memory leaks
- **Error Recovery**: Continues operation even when some API endpoints are unavailable

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- **Temperature parameter**: The GET text endpoint doesn't support temperature. This is a limitation of the Pollinations.AI API
- **POST endpoint**: Currently experiencing connectivity issues
- **Server Response Variability**: Some API endpoints may occasionally return empty responses - the library handles this gracefully with fallbacks

## 🔗 Links

- [Pollinations.AI](https://pollinations.ai)
- [API Documentation](https://pollinations.ai/api)
- [Auth Portal](https://auth.pollinations.ai)

## ❤️ Credits

Built with love using the Pollinations.AI platform.

Made with 🌸 by the eclips team

---

*This README reflects the current state of the Blossom AI SDK with all recent improvements and fixes.*