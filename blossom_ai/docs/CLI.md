# 🖥️ CLI Interface Guide

> **Simple command-line interface for quick AI generation from terminal**

The Blossom AI CLI provides an intuitive text-based interface for terminal usage without writing Python code.

---

## 📦 Installation

The CLI is included with Blossom AI. No additional installation required:

```bash
pip install eclips-blossom-ai
```

---

## 🚀 Quick Start

### Launch Interactive Mode

From your terminal:

```bash
python -m blossom_ai.utils.cli
```

**Output:**
```
╔══════════════════════════════════════════╗
║                                          ║
║        🌸 BLOSSOM AI CLI 🌸             ║
║                                          ║
║  Simple interface for AI generation      ║
║                                          ║
╚══════════════════════════════════════════╝

🔑 API Token: ✓ Configured
📡 API Version: V2

┌─────────────────────────────────────┐
│  What would you like to do?         │
├─────────────────────────────────────┤
│  1. 🖼️  Generate Image              │
│  2. 💬 Generate Text                │
│  3. 🗣️  Generate Audio (TTS)        │
│  4. ℹ️  Show Available Models       │
│  5. 🚪 Exit                         │
└─────────────────────────────────────┘

Your choice [1-5]:
```

---

## 🎯 Usage Methods

### Method 1: Interactive Mode (Recommended)

Perfect for exploring and learning:

```bash
# Launch interactive menu
python -m blossom_ai.utils.cli

# With API token
python -m blossom_ai.utils.cli --token "your_token"

# Specify API version
python -m blossom_ai.utils.cli --version v2
```

Or from Python code:

```python
from blossom_ai.utils import BlossomCLI

cli = BlossomCLI()
cli.run()
```

### Method 2: Quick Commands

For scripting and automation:

```bash
# Quick image generation
python -m blossom_ai.utils.cli --image "a sunset" --output sunset.png

# Quick text generation
python -m blossom_ai.utils.cli --text "Write a haiku"

# Quick audio generation (V1 only)
python -m blossom_ai.utils.cli --audio "Hello world" --output hello.mp3

# With custom model
python -m blossom_ai.utils.cli --image "a cat" --model turbo --output cat.png
```

---

## 🖼️ Image Generation

### Interactive Mode

1. Launch CLI: `python -m blossom_ai.utils.cli`
2. Select option `1`
3. Enter your prompt
4. Configure parameters (optional):
   - Model (default: flux)
   - Width (default: 1024)
   - Height (default: 1024)
   - Filename (default: image.png)

**Example Session:**
```
🖼️  IMAGE GENERATION
──────────────────────────────────────────────────
📝 Image prompt: a beautiful sunset over mountains

⚙️  Optional settings (press Enter to skip):
   Model [flux]: turbo
   Width [1024]: 1920
   Height [1024]: 1080
   Save as [image.png]: sunset.png

🎨 Generating image...
✓ Image saved: sunset.png
🔗 URL: https://enter.pollinations.ai/api/generate/image/...
```

### Quick Command

```bash
# Basic
python -m blossom_ai.utils.cli --image "a sunset" --output sunset.png

# With model
python -m blossom_ai.utils.cli --image "a cat" --model flux --output cat.png
```

**For programmatic usage, use the main library:**
```python
from blossom_ai import Blossom

with Blossom(api_version="v2") as client:
    client.image.save("a sunset", "sunset.png", quality="hd")
```

---

## 💬 Text Generation

### Interactive Mode

1. Launch CLI
2. Select option `2`
3. Enter your prompt
4. Configure parameters (optional):
   - Model (default: openai)
   - System prompt
   - Streaming (y/N)

**Example Session:**
```
💬 TEXT GENERATION
──────────────────────────────────────────────────
📝 Text prompt: Write a haiku about AI

⚙️  Optional settings (press Enter to skip):
   Model [openai]: deepseek
   System prompt: You are a creative poet
   Stream output? [y/N]: y

🤖 Generating text...

──────────────────────────────────────────────────
Silicon minds think,
Learning patterns, data flows,
Future awakens.
──────────────────────────────────────────────────

✓ Generation complete
```

### Quick Command

```bash
# Basic
python -m blossom_ai.utils.cli --text "Write a poem"

# With model
python -m blossom_ai.utils.cli --text "Explain AI" --model deepseek
```

**For programmatic usage:**
```python
from blossom_ai import Blossom

with Blossom(api_version="v2") as client:
    result = client.text.generate("Write a haiku", model="openai")
    print(result)
```

---

## 🗣️ Audio Generation (TTS)

### Interactive Mode

1. Launch CLI
2. Select option `3`
3. Enter text to speak
4. Configure parameters (optional):
   - Voice (default: alloy)
   - Filename (default: audio.mp3)

**Example Session:**
```
🗣️  AUDIO GENERATION (TTS)
──────────────────────────────────────────────────
📝 Text to speak: Hello world, this is a test

⚙️  Optional settings (press Enter to skip):
   Voice [alloy]: nova
   Save as [audio.mp3]: test.mp3

🎵 Generating audio...
✓ Audio saved: test.mp3
```

**Note:** Audio generation requires V1 API (not yet available in V2).

### Quick Command

```bash
# Basic
python -m blossom_ai.utils.cli --version v1 --audio "Hello" --output hello.mp3

# With voice
python -m blossom_ai.utils.cli --version v1 --audio "Hello" --model nova --output hello.mp3
```

**For programmatic usage:**
```python
from blossom_ai import Blossom

with Blossom(api_version="v1", api_token="token") as client:
    client.audio.save("Hello world", "hello.mp3", voice="nova")
```

---

## ℹ️ Available Models

### Interactive Mode

Select option `4` to view all available models:

```
📋 AVAILABLE MODELS
──────────────────────────────────────────────────

🖼️  Image Models:
   1. flux
   2. turbo
   3. gptimage
   4. seedream
   5. kontext
   6. nanobanana

💬 Text Models:
   1. openai
   2. openai-fast
   3. openai-large
   4. deepseek
   5. gemini
   6. mistral
   7. claude
   ... and 6 more

🗣️  Audio Voices:
   1. alloy
   2. echo
   3. fable
   4. onyx
   5. nova
   6. shimmer
```

---

## ⚙️ Configuration

### API Token

Set your API token in several ways:

**1. Environment Variable (Recommended):**
```bash
export POLLINATIONS_API_KEY="your_token_here"
# or
export BLOSSOM_API_KEY="your_token_here"
```

**2. Command Line:**
```bash
python -m blossom_ai.utils.cli --token "your_token_here"
```

**3. In Python Code:**
```python
from blossom_ai.utils import BlossomCLI

cli = BlossomCLI(api_token="your_token_here")
cli.run()
```

### API Version

Choose between V1 (legacy) and V2 (new):

```bash
# V2 (default, recommended)
python -m blossom_ai.utils.cli --version v2

# V1 (legacy, includes audio)
python -m blossom_ai.utils.cli --version v1
```

---

## 📝 Command-Line Examples

### Automated Workflows

**Generate multiple images:**
```bash
#!/bin/bash

prompts=(
    "a sunset over mountains"
    "a futuristic city"
    "an abstract painting"
)

for i in "${!prompts[@]}"; do
    python -m blossom_ai.utils.cli \
        --image "${prompts[$i]}" \
        --output "image_$((i+1)).png"
    echo "✓ Generated image $((i+1))"
done
```

**Batch text processing:**
```bash
#!/bin/bash

questions=(
    "What is machine learning?"
    "Explain neural networks"
    "What is deep learning?"
)

for question in "${questions[@]}"; do
    echo "Q: $question"
    python -m blossom_ai.utils.cli --text "$question"
    echo "---"
done
```

**Generate and announce:**
```bash
#!/bin/bash

# Generate text
response=$(python -m blossom_ai.utils.cli --text "Write a motivational quote")

# Generate audio (V1 only)
python -m blossom_ai.utils.cli --version v1 \
    --audio "$response" \
    --output quote.mp3

echo "✓ Generated and saved as quote.mp3"
```

---

## 🎯 When to Use CLI vs Library

### Use CLI for:
- ✅ Quick terminal-based generation
- ✅ Testing and exploring features
- ✅ Simple automation scripts
- ✅ One-off generation tasks
- ✅ Learning the API

### Use Library for:
- ✅ Production applications
- ✅ Complex logic and workflows
- ✅ Integration with other code
- ✅ Advanced features (caching, reasoning)
- ✅ Error handling and retries

**Example: Library usage for production:**
```python
from blossom_ai import Blossom
from blossom_ai.utils import cached, ReasoningEnhancer

enhancer = ReasoningEnhancer()

@cached(ttl=3600)
def generate_with_reasoning(prompt):
    enhanced = enhancer.enhance(prompt, level="high")
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=1000)

# This is what the library is for!
result = generate_with_reasoning("Complex analysis task")
```

---

## ❓ FAQ

### Q: Can I use CLI in Python scripts?

**A:** Yes, but for production code, use the main library:

```python
# ❌ Don't do this
import subprocess
subprocess.run(["python", "-m", "blossom_ai.utils.cli", "--image", "sunset"])

# ✅ Do this instead
from blossom_ai import Blossom
with Blossom() as client:
    client.image.save("sunset", "sunset.png")
```

### Q: How do I automate CLI workflows?

**A:** Use shell scripts for simple automation, or the library for complex logic:

```bash
# Simple: Use CLI in bash
for i in {1..5}; do
    python -m blossom_ai.utils.cli --image "cat $i" --output "cat_$i.png"
done

# Complex: Use library in Python
```

### Q: Can I pipe CLI output?

**A:** Yes for text generation:

```bash
# Pipe text output
python -m blossom_ai.utils.cli --text "Write a poem" > poem.txt

# Use in scripts
response=$(python -m blossom_ai.utils.cli --text "Write a quote")
echo "Quote: $response"
```

### Q: Why no `quick_image()` functions?

**A:** The library already provides this functionality. CLI is for terminal use only:

```python
# The library IS the quick way
from blossom_ai import Blossom
with Blossom() as client:
    client.image.save("sunset", "sunset.png")  # Already simple!
```

---

## 🔗 Related Documentation

- **[Installation & Setup](INSTALLATION.md)** - Get started with Blossom AI
- **[V2 API Reference](V2_API_REFERENCE.md)** - Full API documentation
- **[Image Generation](V2_IMAGE_GENERATION.md)** - Image generation guide
- **[Text Generation](V2_TEXT_GENERATION.md)** - Text generation guide
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors properly

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[Back to Index](INDEX.md) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

</div>