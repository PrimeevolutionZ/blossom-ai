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

## 🛠️ Utilities

Tools to enhance your workflows.

| Guide | Description |
|-------|-------------|
| **[File Content Reader](FILE_READER.md)** | Read text files and integrate them with AI prompts while respecting API limits |
| 📄 File Validation | Automatic size and encoding validation |
| ✂️ Auto-Truncation | Handle large files gracefully |
| 📦 Multiple Files | Combine and process multiple files |

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

## 🤝 Contributing & Security

Get involved and keep the project secure.

| Document | Description |
|----------|-------------|
| **[Contributing Guide](../../CONTRIBUTING.md)** | How to contribute code, docs, and ideas |
| **[Security Policy](../../SECURITY.md)** | Report vulnerabilities and security best practices |

> **Note:** These files are located in the project root (`blossom-ai/`), one level above the package directory.

---

## 🎯 Quick Links

### Common Tasks

- **Generate an image URL:** [Image Generation - URL Method](IMAGE_GENERATION.md#-image-url-generation)
- **Stream text in real-time:** [Text Generation - Streaming](TEXT_GENERATION.md#-streaming-text-generation)
- **Read files for prompts:** [File Reader - Quick Start](FILE_READER.md#-quick-start)
- **Handle errors properly:** [Error Handling Guide](ERROR_HANDLING.md)
- **Use in async code:** [Resource Management - Async](RESOURCE_MANAGEMENT.md#asynchronous-context-manager)
- **Contribute to project:** [Contributing Guide](../../CONTRIBUTING.md)
- **Report security issue:** [Security Policy](../../SECURITY.md)

### Examples by Use Case

| Use Case | Guide |
|----------|-------|
| **Web Application** | [Image Generation - Web Example](IMAGE_GENERATION.md#parallel-url-generation) |
| **Chat Bot (Discord)** | [Discord Bot Tutorial](DISCORD_BOT.md) |
| **Chat Bot (Telegram)** | [Telegram Bot Tutorial](TELEGRAM_BOT.md) |
| **CLI Tool** | [Resource Management - Sync Usage](RESOURCE_MANAGEMENT.md#synchronous-context-manager) |
| **Background Worker** | [Resource Management - Long-Running Apps](RESOURCE_MANAGEMENT.md#for-long-running-applications-eg-bots) |
| **Code Analysis** | [File Reader - Code Analysis](FILE_READER.md#1-code-analysis) |
| **Document Processing** | [File Reader - Document Summarization](FILE_READER.md#2-document-summarization) |

---

## 🆘 Need Help?

- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 🔒 **Security issue?** See [Security Policy](../../SECURITY.md) for responsible disclosure
- 💡 **Have a question?** Check the [Error Handling Guide](ERROR_HANDLING.md)
- 📚 **Want examples?** See individual feature guides above
- 🤝 **Want to contribute?** Read the [Contributing Guide](../../CONTRIBUTING.md)

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

### Read File for AI Analysis
```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

# Read file content
content = read_file_for_prompt("data.txt", max_length=5000)

# Analyze with AI
with Blossom() as ai:
    response = ai.text.generate(
        f"Analyze this data:\n\n{content}",
        model="deepseek"
    )
    print(response)
```

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[PyPI Package](https://pypi.org/project/eclips-blossom-ai/) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

[Contributing](../../CONTRIBUTING.md) • [Security](../../SECURITY.md) • [License](../../LICENSE)

</div>