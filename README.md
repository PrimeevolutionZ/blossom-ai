# 🌸 Blossom AI

A beautiful Python SDK for [Pollinations.AI](https://pollinations.ai) - Generate images, text, and audio with AI.



---
>Warning!!
> 
>image generation and text generation are working properly in the current version of the library. Unfortunately, audio generation is temporarily unavailable. I'm already working on it.
---
## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 📝 **Text Generation** - Generate text with various models
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🚀 **Simple API** - Easy to use, beautifully designed
- 🎨 **Beautiful Errors** - Helpful error messages with suggestions
- 🔄 **Reproducible** - Use seeds for consistent results

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

# Generate audio
ai.audio.save("Hello, welcome to Blossom AI!", "welcome.mp3")
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
```

### Audio Generation

```python
from blossom_ai import Blossom

ai = Blossom()

# Generate and save audio
ai.audio.save(
    text="Welcome to the future of AI",
    filename="welcome.mp3",
    voice="nova"
)

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
| `temperature` | float | Randomness control | ❌ Not supported in GET API |

**Note:** The current Pollinations.AI GET endpoint doesn't support the `temperature` parameter. For temperature control, you would need to use their POST endpoint, which is currently experiencing issues.

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

## 🛠️ API Methods

### Blossom Class

```python
ai = Blossom(timeout=30)  # Main client

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

Blossom AI provides beautiful, helpful error messages:

```python
from blossom_ai import Blossom, BlossomError

ai = Blossom()

try:
    response = ai.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

## 📚 More Examples

Check out the `tests/` directory for more detailed examples:

- `01_audio_generation.py` - audio generation examples
- `02_image_generation.py` - Image generation examples
- `03_text_generation.py` - Text generation examples

## 🔑 Authentication (Optional)

For higher rate limits and additional features:

1. Visit [auth.pollinations.ai](https://auth.pollinations.ai)
2. Register your application
3. Use tokens or referrers for authentication

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- **Temperature parameter**: The GET text endpoint doesn't support `temperature`. This is a limitation of the Pollinations.AI API
- **POST endpoint**: Currently experiencing connectivity issues

## 🔗 Links

- [Pollinations.AI](https://pollinations.ai)
- [API Documentation](https://github.com/pollinations/pollinations)
- [Auth Portal](https://auth.pollinations.ai)

## ❤️ Credits

Built with love using the [Pollinations.AI](https://pollinations.ai) platform.

---

Made with 🌸 by the eclips team