<div align="center">

# 🌸 Blossom AI
### <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=FF69B4&center=true&vCenter=true&width=600&lines=A+beautiful+Python+SDK+for+Pollinations.AI;Generate+Images%2C+Text+%26+Audio+with+AI;Beautifully+Simple+%E2%9C%A8" alt="Typing SVG" />

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.4.4-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)

[![Downloads](https://img.shields.io/pypi/dm/eclips-blossom-ai.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Stars](https://img.shields.io/github/stars/PrimeevolutionZ/blossom-ai?style=social)](https://github.com/PrimeevolutionZ/blossom-ai)

**Generate images, text, and audio with AI - beautifully simple.**

[🚀 Quick Start](#-quick-start) • [📚 Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md) • [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md) • [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md)

---

</div>

## ✨ Features

<table>
<tr>
<td>

🖼️ **Image Generation**
- Create stunning images from text
- Direct URL generation (no downloads!)
- Save to file or get raw bytes

</td>
<td>

📝 **Text Generation**
- Multiple AI models support
- Real-time streaming
- Timeout protection

</td>
<td>

🎙️ **Audio Generation**
- Text-to-speech conversion
- Multiple voice options
- High-quality output

</td>
</tr>
<tr>
<td>

🚀 **Unified API**
- Sync & async support
- Consistent interface
- Easy to learn

</td>
<td>

🧹 **Clean Code**
- Proper resource management
- Automatic cleanup
- Type hints included

</td>
<td>

⚡ **Fast & Reliable**
- Optimized performance
- Error handling
- Production-ready

</td>
</tr>
</table>

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

## 📊 Why Blossom AI?

```
┌─────────────────────────────────────────────────────────┐
│  ✓ Unified API for image, text, and audio generation   │
│  ✓ Both sync and async support out of the box          │
│  ✓ Clean, modern Python with type hints                │
│  ✓ Active development and community support            │
└─────────────────────────────────────────────────────────┘
```

## 📚 Documentation

<div align="center">

| Resource | Description |
|----------|-------------|
| [📖 Getting Started](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md) | Complete guide to using Blossom AI |
| [⚙️ Installation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INSTALLATION.md) | Setup and configuration instructions |
| [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md) | Practical code examples and use cases |
| [🆕 V2 API Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/V2_MIGRATION_GUIDE.md) | Migrate to V2 API with new features |
| [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md) | Version history and updates |

</div>

## 🌟 Showcase

<details>
<summary><b>🎨 Image Generation Examples</b></summary>

```python
# Generate artistic images
ai.image.save("a cyberpunk city at night", "cyberpunk.jpg")
ai.image.save("watercolor painting of mountains", "mountains.jpg")
```

</details>

<details>
<summary><b>💬 Text Generation Examples</b></summary>

```python
# Creative writing
story = ai.text.generate("Write a short sci-fi story")

# Code generation
code = ai.text.generate("Create a Python function to sort a list")
```

</details>

<details>
<summary><b>🔊 Audio Generation Examples</b></summary>

```python
# Text-to-speech
ai.audio.save("Hello, world!", "greeting.mp3")
```

</details>

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See [`LICENSE`](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/LICENSE) for more information.

## 💖 Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📢 Sharing with others

---

<div align="center">

**Made with 🌸 and ❤️ by [Eclips Team](https://github.com/PrimeevolutionZ)**

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Powered by Pollinations.AI](https://img.shields.io/badge/Powered%20by-Pollinations.AI-blueviolet.svg)](https://pollinations.ai/)

[⬆ Back to top](#-blossom-ai)

</div>