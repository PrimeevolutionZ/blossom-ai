<div align="center">

# 🌸 Blossom AI
### <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=FF69B4&center=true&vCenter=true&width=600&lines=A+beautiful+Python+SDK+for+Pollinations.AI;Generate+Images%2C+Text+%26+Audio+with+AI;Beautifully+Simple+%E2%9C%A8" alt="Typing SVG" />

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.4.5-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/PrimeevolutionZ/blossom-ai)

[![Downloads](https://img.shields.io/pypi/dm/eclips-blossom-ai.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Stars](https://img.shields.io/github/stars/PrimeevolutionZ/blossom-ai?style=social)](https://github.com/PrimeevolutionZ/blossom-ai)


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

## 🆕 What's New in v0.4.5

<details>
<summary><b>🔧 Production Improvements</b></summary>

**Performance:**
- ⚡ 100x faster import time (5s → 50ms)
- 🧠 Smart model caching with 5-minute TTL
- 📉 19x less memory usage in long-running apps

**Reliability:**
- ✅ Integration tests with VCR.py
- 🔄 Intelligent retry with API-specified delays
- 🛡️ Better error handling and recovery

**Security:**
- 🔐 Tokens now only in headers (never in URLs)
- ✅ SSL certificate verification enforced
- 🔒 No token exposure in logs or browser history

**See [CHANGELOG](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md) for details**

</details>

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

### 🔐 Production-Ready Setup

```python
import os
from blossom_ai import Blossom

# ✅ Best practice: Use environment variables
api_token = os.getenv('POLLINATIONS_API_KEY')

# ✅ Always use context managers
with Blossom(api_version="v2", api_token=api_token) as ai:
    # Your code here
    image = ai.image.generate(
        "a sunset",
        quality="hd",
        nologo=True
    )
# Automatic cleanup - no resource leaks!
```

## 📊 Why Blossom AI?

```
┌─────────────────────────────────────────────────────────┐
│  ✓ Unified API for image, text, and audio generation   │
│  ✓ Both sync and async support out of the box          │
│  ✓ Clean, modern Python with type hints                │
│  ✓ Production-ready with comprehensive testing         │
│  ✓ Active development and community support            │
└─────────────────────────────────────────────────────────┘
```

## 📚 Documentation

<div align="center">

| Resource                                                                                                           | Description                           |
|--------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| [📖 Getting Started](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)           | Complete guide to using Blossom AI    |
| [⚙️ Installation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INSTALLATION.md)       | Setup and configuration instructions  |
| [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md)               | Practical code examples and use cases |
| [🆕 V2 API Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/V2_MIGRATION_GUIDE.md) | Migrate to V2 API with new features   |
| [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md)             | Version history and updates           |
| [🔒 Security](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/SECURITY.md)                               | Security best practices               |

</div>

## 🌟 Showcase

<details>
<summary><b>🎨 Image Generation Examples</b></summary>

```python
# Generate artistic images
ai.image.save("a cyberpunk city at night", "cyberpunk.jpg")
ai.image.save("watercolor painting of mountains", "mountains.jpg")

# V2 API: HD quality with advanced controls
with Blossom(api_version="v2", api_token="token") as ai:
    image = ai.image.generate(
        "majestic dragon",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality"
    )
```

</details>

<details>
<summary><b>💬 Text Generation Examples</b></summary>

```python
# Creative writing
story = ai.text.generate("Write a short sci-fi story")

# Code generation
code = ai.text.generate("Create a Python function to sort a list")

# V2 API: Advanced controls
with Blossom(api_version="v2", api_token="token") as ai:
    response = ai.text.generate(
        "Explain AI",
        max_tokens=200,
        frequency_penalty=0.5,
        temperature=0.8
    )
```

</details>

<details>
<summary><b>📊 Audio Generation Examples</b></summary>

```python
# Text-to-speech (requires API token)
with Blossom(api_token="your_token") as ai:
    ai.audio.save("Hello, world!", "greeting.mp3", voice="nova")
```

</details>

## 🛡️ super update

Blossom AI v0.4.5 best is  with:

✅ **Comprehensive Testing**: Integration tests with VCR.py  
✅ **Memory Safe**: No memory leaks in long-running applications  
✅ **Secure**: Tokens only in headers, SSL verification enforced  
✅ **Fast**: Optimized caching and connection pooling  
✅ **Reliable**: Smart retry logic with exponential backoff  

### Quick Health Check

```python
from blossom_ai import Blossom

# Verify everything works
def health_check():
    try:
        with Blossom(api_version="v2", api_token="token") as client:
            # Test image
            img = client.image.generate("test", width=256, height=256)
            assert len(img) > 1000
            
            # Test text
            txt = client.text.generate("Say hello", max_tokens=10)
            assert len(txt) > 0
            
            print("✅ Health check passed!")
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

health_check()
```

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/CONTRIBUTING.md) for detailed guidelines.

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

[⬆️ Back to top](#-blossom-ai)

</div>