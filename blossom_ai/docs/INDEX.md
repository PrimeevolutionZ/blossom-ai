# 📚 Blossom AI Documentation

> **Complete guide to building AI-powered applications with Blossom AI**

Welcome to the Blossom AI documentation! This guide will help you get started with generating images, text, and audio using the Pollinations.AI platform.

---

## 🚀 Getting Started

Perfect for newcomers to Blossom AI.

| Guide                                      | Description |
|--------------------------------------------|-------------|
| **[Installation & Setup](INSTALLATION.md)** | Install the package and configure your environment |
---

## 🎨 Core Features

Learn how to use each generation type.

### Image Generation
| Guide | Description |
|-------|-------------|
| **[Image Generation Guide](IMAGE_GENERATION.md)** | Create stunning images from text prompts |
| 🔗 URL Generation | Get instant image URLs without downloading |
| 💾 Save to File | Generate and save images locally |
| 🎯 Advanced Parameters | Control dimensions, models, seeds, and more |

### Text Generation
| Guide | Description |
|-------|-------------|
| **[Text Generation Guide](TEXT_GENERATION.md)** | Generate text with various AI models |
| 🌊 Streaming | Real-time text generation with chunks |
| 💬 Chat Mode | Multi-turn conversations with context |
| 🎯 JSON Mode | Structured output for applications |

### Audio Generation
| Guide | Description |
|-------|-------------|
| **[Audio Generation Guide](AUDIO_GENERATION.md)** | Text-to-speech with multiple voices |
| 🎙️ Voice Selection | Choose from various voice models |
| 🔐 Authentication | Requires API token |

---

## 🛠️ Development Guides

Build real-world applications.

| Guide | Description |
|-------|-------------|
| **[Discord Bot Tutorial](DISCORD_BOT.md)** | Create an AI image generation bot for Discord |
| **[Telegram Bot Tutorial](TELEGRAM_BOT.md)** | Build a Telegram bot with image generation |
| **[Resource Management](RESOURCE_MANAGEMENT.md)** | Best practices for production applications |
| **[Error Handling](ERROR_HANDLING.md)** | Handle errors gracefully in your applications |

---

## 📖 Reference

Technical details and API specifications.

| Document | Description |
|----------|-------------|
| **[API Reference](API_REFERENCE.md)** | Complete API documentation for all methods |
| **[Changelog](CHANGELOG.md)** | Version history and updates |

---

## 🎯 Quick Links

### Common Tasks

- **Generate an image URL:** [Image Generation - URL Method](IMAGE_GENERATION.md#-image-url-generation)
- **Stream text in real-time:** [Text Generation - Streaming](TEXT_GENERATION.md#-streaming-text-generation)
- **Handle errors properly:** [Error Handling Guide](ERROR_HANDLING.md)
- **Use in async code:** [Resource Management - Async](RESOURCE_MANAGEMENT.md#asynchronous-context-manager)

### Examples by Use Case

| Use Case | Guide |
|----------|-------|
| **Web Application** | [Image Generation - Web Example](IMAGE_GENERATION.md#parallel-url-generation) |
| **Chat Bot (Discord)** | [Discord Bot Tutorial](DISCORD_BOT.md) |
| **Chat Bot (Telegram)** | [Telegram Bot Tutorial](TELEGRAM_BOT.md) |
| **CLI Tool** | [Resource Management - Sync Usage](RESOURCE_MANAGEMENT.md#synchronous-context-manager) |
| **Background Worker** | [Resource Management - Long-Running Apps](RESOURCE_MANAGEMENT.md#for-long-running-applications-eg-bots) |

---

## 🆘 Need Help?

- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💡 **Have a question?** Check the [Error Handling Guide](ERROR_HANDLING.md)
- 📚 **Want examples?** See individual feature guides above


---

## 🌟 Popular Recipes

Quick code snippets for common tasks:

### Generate and Save an Image
```python
from blossom_ai import Blossom

with Blossom() as ai:
    ai.image.save("a beautiful sunset", "sunset.jpg")
```

### Get Image URL (Fast!)
```python
from blossom_ai import Blossom

with Blossom() as ai:
    url = ai.image.generate_url("a cute robot")
    print(url)
```

### Stream Text Generation
```python
from blossom_ai import Blossom

with Blossom() as ai:
    for chunk in ai.text.generate("Tell me a story", stream=True):
        print(chunk, end='', flush=True)
```

### Generate Audio (Requires Token)
```python
from blossom_ai import Blossom

with Blossom(api_token="YOUR_TOKEN") as ai:
    ai.audio.save("Hello world", "hello.mp3", voice="nova")
```

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[PyPI Package](https://pypi.org/project/eclips-blossom-ai/) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

</div>