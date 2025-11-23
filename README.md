<div align="center">

# 🌸 Blossom AI
### <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=FF69B4&center=true&vCenter=true&width=700&lines=Beautiful+Python+SDK+for+Pollinations.AI;Generate+Images%2C+Text+%26+Vision+with+AI;CLI+Interface+%2B+Python+Library;Beautifully+Simple+%E2%9C%A8" alt="Typing SVG" />

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.5.3-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/PrimeevolutionZ/blossom-ai)

[![Downloads](https://img.shields.io/pypi/dm/eclips-blossom-ai.svg)](https://pypi.org/project/eclips-blossom-ai/)
[![Stars](https://img.shields.io/github/stars/PrimeevolutionZ/blossom-ai?style=social)](https://github.com/PrimeevolutionZ/blossom-ai)

[🚀 Quick Start](#-quick-start) • [📚 Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md) • [🖥️ CLI Interface](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md) • [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md) • [📝 Changelog](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md)

---

</div>

## ✨ Features

<table>
<tr>
<td>

🖼️ **HD Image Generation**
- Create stunning images from text
- HD quality up to 2048x2048
- Advanced controls (guidance, quality)
- Direct URL generation

</td>
<td>

💬 **Advanced Text Generation**
- Multiple AI models (OpenAI, Gemini, etc.)
- Real-time streaming
- Function calling & tools
- JSON mode

</td>
<td>

👁️ **Vision & Multimodal**
- Analyze images with AI
- Multiple image support
- Local & URL images
- High-quality analysis

</td>
</tr>
<tr>
<td>

🖥️ **CLI Interface**
- Interactive terminal menu
- Quick command-line access
- No code required
- Shell automation

</td>
<td>

🚀 **Production Ready**
- Sync & async support
- Connection pooling
- Smart caching
- Comprehensive tests

</td>
<td>

⚡ **Fast & Secure**
- Token in headers only
- SSL verification enforced
- Optimized performance
- No memory leaks

</td>
</tr>
</table>

## 🆕 What's New in v0.5.0

<details open>
<summary><b>👁️ Vision Support (NEW!)</b></summary>

**Analyze images with AI:**
- 🔍 Image analysis from URLs or local files
- 🎨 Multiple images in one request
- 📊 Adjustable detail levels (low/auto/high)
- 🤖 Works with vision-capable models

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="token") as client:
    messages = [
        MessageBuilder.image(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/image.jpg",
            detail="high"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

**[📚 Full Vision Documentation →](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/VISION.md)**

</details>

<details>
<summary><b>🎨 Enhanced Image Generation</b></summary>

**Advanced image controls:**
- 🎯 Quality levels: `low`, `medium`, `high`, `hd`
- 🎨 Guidance scale control (1.0-20.0)
- 🚫 Negative prompts for better control
- 🌈 Transparent background support
- 🖼️ Image-to-image transformation
- ⚡ Fast URL generation (no download needed)

```python
with Blossom(api_token="token") as client:
    # HD quality with advanced controls
    image = client.image.generate(
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
<summary><b>📝 Advanced Text Features</b></summary>

**Powerful text generation:**
- 🛠️ Function calling / Tool use
- 📋 Structured JSON output
- ⚙️ Advanced parameters: `max_tokens`, `frequency_penalty`, `presence_penalty`, `top_p`
- 🌊 Improved streaming with SSE
- 🌡️ Extended temperature range (0-2)
- 💬 Multi-turn conversations

```python
with Blossom(api_token="token") as client:
    response = client.text.generate(
        "Explain quantum computing",
        max_tokens=500,
        temperature=0.8,
        frequency_penalty=0.5,
        json_mode=True
    )
```

</details>

## 🚀 Quick Start

### 📦 Installation

```bash
pip install eclips-blossom-ai
```

### 🖥️ CLI Interface

Perfect for quick testing and learning:

```bash
# Launch interactive menu
python -m blossom_ai.utils.cli

# Quick commands
python -m blossom_ai.utils.cli --image "a beautiful sunset" --output sunset.png
python -m blossom_ai.utils.cli --text "Explain quantum computing"

# Set API token (optional for some features)
export POLLINATIONS_API_KEY="your_token"
python -m blossom_ai.utils.cli
```

**Interactive Menu:**
```
╔════════════════════════════════════════╗
║        🌸 BLOSSOM AI CLI 🌸            ║
║  Simple interface for AI generation    ║
╚════════════════════════════════════════╝

1. 🖼️  Generate Image
2. 💬 Generate Text
3. 👁️  Analyze Image (Vision)
4. ℹ️  Show Available Models
5. 🚪 Exit
```

**[📚 Full CLI Documentation →](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md)**

### ⚡ Python Library

```python
from blossom_ai import Blossom
import os
api_token = os.getenv('POLLINATIONS_API_KEY')
# Simple usage
with Blossom(api_token=api_token) as ai:
    # Generate image URL 
    url = ai.image.generate_url("a beautiful sunset")
    print(url)
    
    # Save image directly
    ai.image.save("a serene lake at dawn", "lake.jpg")
    
    # Generate text
    response = ai.text.generate("Explain quantum computing")
    print(response)
    
    # Stream text in real-time
    for chunk in ai.text.generate("Tell me a story", stream=True):
        print(chunk, end='', flush=True)
```

### 🎯 With API Token (Advanced Features)

```python
import os
from blossom_ai import Blossom

# ✅ Best practice: Use environment variables
api_token = os.getenv('POLLINATIONS_API_KEY')

with Blossom(api_token=api_token) as client:
    # HD image with advanced controls
    image = client.image.generate(
        "majestic dragon",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality",
        width=1920,
        height=1080
    )
    
    # Advanced text generation
    response = client.text.generate(
        "Explain AI",
        max_tokens=200,
        frequency_penalty=0.5,
        temperature=0.8
    )
    
    # Vision analysis (requires token)
    from blossom_ai import MessageBuilder
    
    messages = [
        MessageBuilder.image(
            role="user",
            text="Describe this image",
            image_url="https://example.com/photo.jpg"
        )
    ]
    
    analysis = client.text.chat(messages, model="openai")
    print(analysis)

# Automatic cleanup - no resource leaks!
```

## 📊 Why Blossom AI?

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ CLI Interface for quick terminal access                 │
│  ✓ Vision & multimodal support (images + text)             │
│  ✓ HD image generation with advanced controls              │
│  ✓ Function calling and structured outputs                 │
│  ✓ Both sync and async support out of the box              │
│  ✓ Clean, modern Python with type hints                    │
│  ✓ Production-ready with comprehensive testing             │
│  ✓ Smart caching and optimization utilities                │
│  ✓ Secure: tokens in headers only, SSL enforced            │
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

### 📚 Library (Python)

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
| [🖥️ CLI Interface](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CLI.md)              | Terminal interface documentation      |
| [👁️ Vision Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/VISION.md)            | Vision and multimodal features        |
| [🎨 Image Generation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/IMAGE_GENERATION.md) | HD images with advanced controls   |
| [💬 Text Generation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/TEXT_GENERATION.md) | Advanced text generation features     |
| [⚙️ Installation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INSTALLATION.md)       | Setup and configuration               |
| [💡 Examples](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/EXAMPLES.md)               | Practical code examples               |
| [🌐 Web Apps](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/WEB_APP.md)               | Build FastAPI/Flask applications      |
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

# HD quality with custom size
python -m blossom_ai.utils.cli \
  --image "mountain landscape" \
  --width 1920 \
  --height 1080 \
  --quality hd \
  --output landscape.png
```

**Python:**
```python
# Simple and fast
with Blossom() as ai:
    ai.image.save("a cyberpunk city at night", "cyberpunk.jpg")
    ai.image.save("watercolor painting of mountains", "mountains.jpg")

# HD quality with advanced controls
with Blossom(api_token="token") as ai:
    image = ai.image.generate(
        "majestic dragon breathing fire",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality, distorted",
        width=1920,
        height=1080,
        seed=42  # Reproducible results
    )
```

</details>

<details>
<summary><b>💬 Text Generation Examples</b></summary>

**CLI:**
```bash
# Quick text generation
python -m blossom_ai.utils.cli --text "Write a haiku about AI"

# With streaming for real-time output
python -m blossom_ai.utils.cli --text "Tell me a story" --stream
```

**Python:**
```python
# Creative writing
story = ai.text.generate("Write a short sci-fi story about time travel")

# Code generation
code = ai.text.generate("Create a Python function to sort a list")

# Advanced controls
response = ai.text.generate(
    "Explain quantum computing for beginners",
    max_tokens=500,
    temperature=0.8,
    frequency_penalty=0.5,
    stream=True  # Real-time streaming
)

# Structured JSON output
json_data = ai.text.generate(
    "List 5 programming languages with their use cases",
    json_mode=True
)
```

</details>

<details>
<summary><b>👁️ Vision Analysis Examples (NEW!)</b></summary>

**Python:**
```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="token") as ai:
    # Analyze image from URL
    messages = [
        MessageBuilder.image(
            role="user",
            text="What's in this image? Describe in detail.",
            image_url="https://example.com/photo.jpg",
            detail="high"
        )
    ]
    
    analysis = ai.text.chat(messages, model="openai")
    print(analysis)
    
    # Analyze local image
    messages = [
        MessageBuilder.image(
            role="user",
            text="Identify the objects in this image",
            image_path="/path/to/image.jpg",
            detail="auto"
        )
    ]
    
    result = ai.text.chat(messages, model="openai")
    
    # Compare multiple images
    messages = [
        MessageBuilder.image(
            role="user",
            text="Compare these two images",
            image_url="https://example.com/image1.jpg"
        ),
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "And this second image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image2.jpg",
                        "detail": "high"
                    }
                }
            ]
        }
    ]
    
    comparison = ai.text.chat(messages, model="openai")
```

</details>

<details>
<summary><b>🔧 Shell Automation Examples</b></summary>

```bash
#!/bin/bash

# Generate multiple images in parallel
for i in {1..5}; do
    python -m blossom_ai.utils.cli \
        --image "abstract art style $i" \
        --output "art_$i.png" &
done
wait

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

# Vision analysis pipeline
for img in *.jpg; do
    echo "Analyzing: $img"
    python -c "
from blossom_ai import Blossom, MessageBuilder
with Blossom(api_token='token') as ai:
    messages = [MessageBuilder.image('user', 'Describe', image_path='$img')]
    print(ai.text.chat(messages, model='openai'))
"
done
```

</details>

## 🛡️ Production Ready

Blossom AI v0.5.0 is battle-tested with:

✅ **Vision Support**: Analyze images with AI models  
✅ **HD Image Generation**: Up to 2048x2048 with quality controls  
✅ **Advanced Text Features**: Function calling, JSON mode, streaming  
✅ **CLI Interface**: Quick terminal access for testing and automation  
✅ **Comprehensive Testing**: Integration tests with VCR.py  
✅ **Memory Safe**: No memory leaks in long-running applications  
✅ **Secure**: Tokens only in headers, SSL verification enforced  
✅ **Fast**: Optimized caching and connection pooling  
✅ **Reliable**: Smart retry logic with exponential backoff  

### Quick Health Check

```python
from blossom_ai import Blossom

def health_check():
    """Verify everything works"""
    try:
        with Blossom(api_token="token") as client:
            # Test image
            img = client.image.generate("test", width=256, height=256)
            assert len(img) > 1000
            
            # Test text
            txt = client.text.generate("Say hello", max_tokens=10)
            assert len(txt) > 0
            
            # Test vision
            from blossom_ai import MessageBuilder
            messages = [
                MessageBuilder.image(
                    "user",
                    "What's this?",
                    image_url="https://pollinations.ai/p/test"
                )
            ]
            vision = client.text.chat(messages, model="openai")
            assert len(vision) > 0
            
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
    level="high",
    mode="auto"
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
<tr>
<td>

### 📁 File Reader
Process files for AI prompts:

```python
from blossom_ai.utils import read_file_for_prompt

content = read_file_for_prompt(
    "code.py",
    max_length=8000,
    truncate_if_needed=True
)
```

</td>
<td>

### 🌐 Web Applications
Build REST APIs with FastAPI/Flask:

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/generate")
async def generate(prompt: str):
    async with Blossom() as ai:
        return await ai.text.generate(prompt)
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
[![Version 0.5.0](https://img.shields.io/badge/version-0.5.0-success.svg)](https://pypi.org/project/eclips-blossom-ai/)

[⬆️ Back to top](#-blossom-ai)

</div>