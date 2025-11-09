<div align="center">

# 🌸 Blossom AI
### <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=FF69B4&center=true&vCenter=true&width=700&lines=Beautiful+Python+SDK+for+Pollinations.AI;Generate+Images%2C+Text+%26+Audio+with+AI;CLI+Interface+%2B+Python+Library;Beautifully+Simple+%E2%9C%A8" alt="Typing SVG" />

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.4.7-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/PrimeevolutionZ/blossom-ai)

[![Downloads](https://img.shields.io/pypi/dm/eclips-blossom-ai.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Stars](https://img.shields.io/github/stars/PrimeevolutionZ/blossom-ai?style=social)](https://github.com/PrimeevolutionZ/blossom-ai)


[🚀 Quick Start](#-quick-start) • [📚 Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md) • [🖥️ CLI Interface](#%EF%B8%8F-cli-interface-new) • [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md) • [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md)

---

</div>

## ✨ Features

<table>
<tr>
<td>

🖼️ **Image Generation**
- Create stunning images from text
- Direct URL generation (no downloads!)
- HD quality with V2 API

</td>
<td>

📝 **Text Generation**
- Multiple AI models support
- Real-time streaming
- Function calling & tools

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

🖥️ **CLI Interface** 🆕
- Interactive terminal menu
- Quick command-line access
- No code required

</td>
<td>

🚀 **Unified API**
- Sync & async support
- Consistent interface
- Easy to learn

</td>
<td>

⚡ **Fast & Reliable**
- Optimized performance
- Smart caching
- Production-ready

</td>
</tr>
</table>

## 🆕 What's New in v0.4.7

<details open>
<summary><b>🖥️ CLI Interface (NEW!)</b></summary>

**Quick Terminal Access:**
- 🌸 Beautiful interactive menu
- ⚡ Quick commands for automation
- 🎯 Perfect for testing and learning
- 🔧 Shell script integration

```bash
# Interactive mode
python -m blossom_ai.utils.cli

# Quick generation
python -m blossom_ai.utils.cli --image "sunset" --output sunset.png
python -m blossom_ai.utils.cli --text "Write a poem"
```

**[View CLI Documentation →](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md)**

</details>

<details>
<summary><b>🔧 Production Improvements (v0.4.5-v0.4.6)</b></summary>

**Performance:**
- ⚡ 100x faster import time (5s → 50ms)
- 🧠 Smart model caching with 5-minute TTL
- 📉 19x less memory usage in long-running apps

**Reliability:**
- ✅ Integration tests with VCR.py
- 🔄 Intelligent retry with API-specified delays
- 🛡️ Better error handling and recovery

**Security:**
- 🔒 Tokens now only in headers (never in URLs)
- ✅ SSL certificate verification enforced
- 🔑 No token exposure in logs or browser history

**See [CHANGELOG](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md) for details**

</details>

## 🚀 Quick Start

### 📦 Installation

```bash
pip install eclips-blossom-ai
```

### 🖥️ CLI Interface (NEW!)

Perfect for quick testing and learning:

```bash
# Launch interactive menu
python -m blossom_ai.utils.cli

# Quick commands
python -m blossom_ai.utils.cli --image "a beautiful sunset" --output sunset.png
python -m blossom_ai.utils.cli --text "Explain quantum computing"

# Set API token
export POLLINATIONS_API_KEY="your_token"
python -m blossom_ai.utils.cli
```

**Interactive Menu:**
```
╔══════════════════════════════════════════╗
║        🌸 BLOSSOM AI CLI 🌸             ║
║  Simple interface for AI generation      ║
╚══════════════════════════════════════════╝

1. 🖼️  Generate Image
2. 💬 Generate Text
3. 🗣️  Generate Audio (TTS)
4. ℹ️  Show Available Models
5. 🚪 Exit
```

**[📚 Full CLI Documentation →](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md)**

### ⚡ Python Library

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

### 🎯 V2 API with Advanced Features

```python
import os
from blossom_ai import Blossom

# ✅ Best practice: Use environment variables
api_token = os.getenv('POLLINATIONS_API_KEY')

# ✅ V2 API with advanced features
with Blossom(api_version="v2", api_token=api_token) as ai:
    # HD image with advanced controls
    image = ai.image.generate(
        "majestic dragon",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality"
    )
    
    # Text with advanced parameters
    response = ai.text.generate(
        "Explain AI",
        max_tokens=200,
        frequency_penalty=0.5,
        temperature=0.8
    )
# Automatic cleanup - no resource leaks!
```

## 📊 Why Blossom AI?

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ CLI Interface for quick terminal access 🆕              │
│  ✓ Unified API for image, text, and audio generation       │
│  ✓ Both sync and async support out of the box              │
│  ✓ V2 API with HD quality and advanced features            │
│  ✓ Clean, modern Python with type hints                    │
│  ✓ Production-ready with comprehensive testing             │
│  ✓ Smart caching and optimization utilities                │
│  ✓ Active development and community support                │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Choose Your Style

<table>
<tr>
<td width="50%">

### 🖥️ CLI (Terminal)

Perfect for:
- ✅ Quick testing
- ✅ Learning the API
- ✅ Shell automation
- ✅ No code required

```bash
python -m blossom_ai.utils.cli \
  --image "sunset" \
  --output sunset.png
```

</td>
<td width="50%">

### 🐍 Library (Python)

Perfect for:
- ✅ Production apps
- ✅ Complex workflows
- ✅ Integration
- ✅ Advanced features

```python
from blossom_ai import Blossom

with Blossom() as ai:
    ai.image.save("sunset", "sunset.png")
```

</td>
</tr>
</table>

## 📚 Documentation

<div align="center">

| Resource                                                                                                           | Description                           |
|--------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| [📖 Getting Started](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)           | Complete guide to using Blossom AI    |
| [🖥️ CLI Interface](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md) 🆕            | Terminal interface documentation      |
| [⚙️ Installation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INSTALLATION.md)       | Setup and configuration instructions  |
| [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md)               | Practical code examples and use cases |
| [🆕 V2 API Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/V2_MIGRATION_GUIDE.md) | Migrate to V2 API with new features   |
| [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md)             | Version history and updates           |
| [🔒 Security](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/SECURITY.md)                               | Security best practices               |

</div>

## 🌟 Showcase

<details>
<summary><b>🎨 Image Generation Examples</b></summary>

**CLI:**
```bash
# Quick generation
python -m blossom_ai.utils.cli --image "cyberpunk city" --output city.png

# Interactive mode with custom settings
python -m blossom_ai.utils.cli
# Then select: 1. Generate Image
```

**Python:**
```python
# V1 API - Simple and fast
ai.image.save("a cyberpunk city at night", "cyberpunk.jpg")
ai.image.save("watercolor painting of mountains", "mountains.jpg")

# V2 API - HD quality with advanced controls
with Blossom(api_version="v2", api_token="token") as ai:
    image = ai.image.generate(
        "majestic dragon",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality",
        width=1920,
        height=1080
    )
```

</details>

<details>
<summary><b>💬 Text Generation Examples</b></summary>

**CLI:**
```bash
# Quick text generation
python -m blossom_ai.utils.cli --text "Write a haiku about AI"

# Streaming mode
python -m blossom_ai.utils.cli
# Select: 2. Generate Text
# Then enable streaming for real-time output
```

**Python:**
```python
# Creative writing
story = ai.text.generate("Write a short sci-fi story")

# Code generation
code = ai.text.generate("Create a Python function to sort a list")

# V2 API - Advanced controls
with Blossom(api_version="v2", api_token="token") as ai:
    response = ai.text.generate(
        "Explain quantum computing",
        max_tokens=200,
        frequency_penalty=0.5,
        temperature=0.8,
        stream=True
    )
```

</details>

<details>
<summary><b>🎙️ Audio Generation Examples</b></summary>

**CLI:**
```bash
# Text-to-speech (requires API token)
export POLLINATIONS_API_KEY="your_token"
python -m blossom_ai.utils.cli --version v1 --audio "Hello world" --output hello.mp3
```

**Python:**
```python
# Text-to-speech (requires API token)
with Blossom(api_version="v1", api_token="your_token") as ai:
    ai.audio.save("Hello, world!", "greeting.mp3", voice="nova")
    ai.audio.save("Welcome to Blossom AI", "welcome.mp3", voice="alloy")
```

</details>

<details>
<summary><b>🔧 Shell Automation Examples</b></summary>

```bash
#!/bin/bash

# Generate multiple images
for i in {1..5}; do
    python -m blossom_ai.utils.cli \
        --image "abstract art $i" \
        --output "art_$i.png"
done

# Batch text processing
questions=(
    "What is AI?"
    "Explain machine learning"
    "What is deep learning?"
)

for q in "${questions[@]}"; do
    echo "Q: $q"
    python -m blossom_ai.utils.cli --text "$q"
    echo "---"
done
```

</details>

## 🛡️ Production Ready

Blossom AI v0.4.7 is battle-tested with:

✅ **CLI Interface**: Quick terminal access for testing and automation  
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

## 🎨 Advanced Features

<table>
<tr>
<td>

### 🧠 Reasoning Module
Enhance prompts with structured thinking:

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()
enhanced = enhancer.enhance(
    "Design a microservices architecture",
    level="high"
)
```

</td>
<td>

### ⚡ Caching Module
Cache responses for better performance:

```python
from blossom_ai.utils import cached

@cached(ttl=3600)
def generate_text(prompt):
    with Blossom() as ai:
        return ai.text.generate(prompt)
```

</td>
</tr>
</table>

**[📚 View Full Documentation →](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)**

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
[![CLI Available](https://img.shields.io/badge/CLI-Available-success.svg)](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md)

[⬆️ Back to top](#-blossom-ai)

</div>