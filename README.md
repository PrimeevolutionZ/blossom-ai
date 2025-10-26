# 🌸 Blossom AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.7-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)

**A beautiful Python SDK for Pollinations.AI - Generate images, text, and audio with AI.**

Blossom AI is a comprehensive, easy-to-use Python library that provides unified access to Pollinations.AI's powerful AI generation services. Create stunning images, generate text with various models, and convert text to speech with multiple voices - all through a beautifully designed, intuitive API.

## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 🔗 **Image URL Generation** - Get direct links without downloading (v0.2.5!)
- 📝 **Text Generation** - Generate text with various AI models
- 🌊 **Streaming** - Real-time text generation with timeout protection
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🚀 **Unified API** - Same code works in sync and async contexts
- 🧹 **Clean** - Proper resource management and automatic cleanup

## 🚀 Quick Start

### 📦 Installation

```bash
pip install eclips-blossom-ai
```

### ⚡ Basic Usage

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Generate image URL (Fast & Free!)
    url = ai.image.generate_url("a beautiful sunset")
    print(url)
     # Save image directly to a file
    ai.image.save("a serene lake at dawn", "lake.jpg")

    # Get raw image bytes for custom processing
    image_bytes = ai.image.generate("a robot painting a portrait")
    # Now you can upload, display, or manipulate image_bytes as needed

    # Generate text
    response = ai.text.generate("Explain quantum computing")
    print(response)

    # Stream text
    for chunk in ai.text.generate("Tell me a story", stream=True):
        print(chunk, end='', flush=True)
```

## 📚 Documentation

- **[Installation & Setup](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/INSTALLATION.md )**
- **[Image Generation Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/IMAGE_GENERATION.md )**
- **[Text Generation Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/TEXT_GENERATION.md )**
- **[Audio Generation Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/AUDIO_GENERATION.md )**
- **[Resource Management & Best Practices](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/RESOURCE_MANAGEMENT.md )**
- **[Discord Bot Tutorial](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/DISCORD_BOT.md )**
- **[Telegram Bot Tutorial](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/TELEGRAM_BOT.md )**
- **[Error Handling](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/ERROR_HANDLING.md )**
- **[API Reference](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/API_REFERENCE.md )**
- **[Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/docs/CHANGELOG.md )**


## 🤝 Contributing

Contributions welcome!

## 📄 License

MIT License - see [LICENSE](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/LICENSE)

---

Made with 🌸 by [Eclips Team](https://github.com/PrimeevolutionZ)
