# 🚀 Quick Start Guide

Get started with Blossom AI in 5 minutes! This guide covers the basics of image generation, text generation, and new vision features.

---

## 📋 Prerequisites

Before you start, make sure you have:

1. ✅ **Python 3.8+** installed
2. ✅ **Blossom AI** installed: `pip install eclips-blossom-ai`
3. ✅ **API Token** from [enter.pollinations.ai](https://enter.pollinations.ai)

If you haven't installed Blossom AI yet, see [Installation Guide](INSTALLATION.md).

---

## 🎯 Your First Generation in 30 Seconds

### Minimal Example

```python
from blossom_ai import Blossom

# Initialize client with your API token
client = Blossom(api_token="your-api-token-here")

# Generate text
response = client.text.generate("Write a haiku about coding")
print(response)

# Generate image URL (fast!)
url = client.image.generate_url("a cute robot painting")
print(url)

# Don't forget to close
client.close_sync()
```

**Output:**
```
Code flows like a stream,
Functions dance in memory,
Bugs flee from my screen.

https://image.pollinations.ai/prompt/a%20cute%20robot%20painting?width=1024&height=1024&model=flux
```

---

## 📚 Table of Contents

- [Basic Image Generation](#basic-image-generation)
- [Basic Text Generation](#basic-text-generation)
- [Streaming Text](#streaming-text)
- [Vision: Analyze Images](#vision-analyze-images)
- [Using Context Managers](#using-context-managers)
- [Async/Await Support](#asyncawait-support)
- [CLI Interface](#cli-interface)
- [Common Patterns](#common-patterns)
- [Next Steps](#next-steps)

---

## 🖼️ Basic Image Generation

### Generate and Save Image

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate and save to file
    filepath = client.image.save(
        prompt="a beautiful sunset over mountains",
        filename="sunset.jpg"
    )
    print(f"✅ Image saved to: {filepath}")
```

### Generate Image with Parameters

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    filepath = client.image.save(
        prompt="a futuristic city at night",
        filename="city.png",
        width=1920,           # Image width
        height=1080,          # Image height
        quality="hd",         # Quality: low, medium, high, hd
        model="flux",         # Model to use
        seed=42,              # Reproducible results
        guidance_scale=7.5,   # Control adherence to prompt (1-20)
        negative_prompt="blurry, low quality"  # What to avoid
    )
    print(f"✅ HD image saved: {filepath}")
```

### Get Image URL (Fast!)

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Get URL without downloading
    url = client.image.generate_url(
        prompt="a cute robot",
        width=512,
        height=512,
        quality="medium"
    )
    
    print(f"🔗 Image URL: {url}")
    # You can share this URL directly!
```

### Generate Image as Bytes

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Get raw image data
    image_bytes = client.image.generate(
        prompt="a colorful abstract pattern",
        width=256,
        height=256
    )
    
    print(f"📦 Received {len(image_bytes)} bytes")
    
    # Save manually if needed
    with open("pattern.png", "wb") as f:
        f.write(image_bytes)
```

---

## 💬 Basic Text Generation

### Simple Text Generation

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate text
    response = client.text.generate(
        prompt="Explain quantum computing in simple terms"
    )
    print(response)
```

### Text with System Message

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a function to reverse a string",
        system="You are an expert Python programmer",
        model="openai"
    )
    print(response)
```

### Text with Parameters

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a short story about AI",
        model="openai",
        temperature=0.8,        # Creativity (0-2)
        max_tokens=200,         # Limit response length
        frequency_penalty=0.5,  # Reduce repetition
        presence_penalty=0.3    # Encourage new topics
    )
    print(response)
```

### Chat Completion

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Multi-turn conversation
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant"},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a high-level programming language..."},
        {"role": "user", "content": "What makes it popular?"}
    ]
    
    response = client.text.chat(messages)
    print(response)
```

### JSON Mode (Structured Output)

```python
from blossom_ai import Blossom
import json

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="List 3 programming languages with their primary use cases in JSON format",
        json_mode=True
    )
    
    # Parse JSON response
    data = json.loads(response)
    print(json.dumps(data, indent=2))
```

---

## 🌊 Streaming Text

Stream responses in real-time for better UX:

### Basic Streaming

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    print("AI: ", end="", flush=True)
    
    for chunk in client.text.generate(
        prompt="Tell me a short story about a robot",
        stream=True
    ):
        print(chunk, end="", flush=True)
    
    print()  # New line at end
```

### Streaming with System Message

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    for chunk in client.text.generate(
        prompt="Explain machine learning",
        system="You are a teacher explaining concepts to beginners",
        stream=True,
        max_tokens=300
    ):
        print(chunk, end="", flush=True)
```

### Streaming Chat

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What are the benefits of streaming?"}
    ]
    
    for chunk in client.text.chat(messages, stream=True):
        print(chunk, end="", flush=True)
```

---

## 👁️ Vision: Analyze Images

**NEW in v0.5.0!** Analyze images with AI.

### Analyze Image from URL

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    # Create message with image
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What's in this image? Describe it in detail.",
            image_url="https://example.com/photo.jpg",
            detail="auto"  # auto, low, or high
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Analyze Local Image

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    # Use local image file
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What colors are in this image?",
            image_path="photo.jpg",
            detail="low"  # Use 'low' for faster processing
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Multiple Images

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two images"},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image1.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image2.jpg"}
                }
            ]
        }
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 🔄 Using Context Managers

**Best practice:** Use context managers for automatic cleanup.

### Synchronous Context Manager

```python
from blossom_ai import Blossom

# Automatically closes connection when done
with Blossom(api_token="your-token") as client:
    # Generate image
    url = client.image.generate_url("a test image")
    
    # Generate text
    text = client.text.generate("Hello AI!")
    
# Connection automatically closed here ✅
```

### Multiple Operations

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Multiple operations in one session
    for i in range(5):
        url = client.image.generate_url(f"scene {i}")
        print(f"Image {i}: {url}")
    
    # Text generation
    response = client.text.generate("Summarize our session")
    print(response)
```

---

## ⚡ Async/Await Support

Use async for better performance in async applications:

### Basic Async Example

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom(api_token="your-token") as client:
        # Async image generation
        image_bytes = await client.image.generate(
            "a beautiful landscape",
            width=512,
            height=512
        )
        print(f"✅ Generated {len(image_bytes)} bytes")
        
        # Async text generation
        response = await client.text.generate(
            "Explain async programming"
        )
        print(f"✅ Response: {response[:100]}...")

# Run async function
asyncio.run(main())
```

### Parallel Generation

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom(api_token="your-token") as client:
        # Generate multiple images in parallel
        tasks = [
            client.image.generate_url(f"scene {i}", width=256, height=256)
            for i in range(5)
        ]
        
        urls = await asyncio.gather(*tasks)
        
        for i, url in enumerate(urls):
            print(f"Image {i}: {url}")

asyncio.run(main())
```

### Async Streaming

```python
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom(api_token="your-token") as client:
        print("AI: ", end="", flush=True)
        
        # Async streaming
        stream = await client.text.generate(
            "Tell me about async programming",
            stream=True
        )
        
        async for chunk in stream:
            print(chunk, end="", flush=True)
        
        print()

asyncio.run(main())
```

---

## 🖥️ CLI Interface

Use Blossom AI from the terminal without writing code!

### Interactive Mode

```bash
# Launch interactive menu
python -m blossom_ai.utils.cli

# Or with token
python -m blossom_ai.utils.cli --token your-token
```

**Interactive menu:**
```
┌───────────────────────────────────┐
│  What would you like to do?       │
├───────────────────────────────────┤
│  1. 🖼️  Generate Image            │
│  2. 💬 Generate Text              │
│  3. ℹ️  Show Available Models     │
│  4. 🚪 Exit                       │
└───────────────────────────────────┘
```

### Quick Commands

```bash
# Generate image
python -m blossom_ai.utils.cli --image "a sunset" --output sunset.png

# Generate text
python -m blossom_ai.utils.cli --text "Write a poem"

# With custom model
python -m blossom_ai.utils.cli --image "a robot" --model flux --output robot.png

# Show help
python -m blossom_ai.utils.cli --help
```

### Shell Scripting

```bash
#!/bin/bash

# Batch generate images
for animal in cat dog bird; do
    python -m blossom_ai.utils.cli \
        --image "a cute $animal" \
        --output "${animal}.png" \
        --token "$POLLINATIONS_API_KEY"
done
```

---

## 🎯 Common Patterns

### Pattern 1: Error Handling

```python
from blossom_ai import Blossom, BlossomError

with Blossom(api_token="your-token") as client:
    try:
        response = client.text.generate("Hello AI!")
        print(response)
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        if e.suggestion:
            print(f"💡 Suggestion: {e.suggestion}")
```

### Pattern 2: Reproducible Images

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Use same seed for reproducible results
    SEED = 42
    
    # Generate same image multiple times
    for i in range(3):
        filepath = client.image.save(
            "a mountain landscape",
            f"mountain_{i}.jpg",
            seed=SEED  # Same seed = same result
        )
        print(f"Generated: {filepath}")
```

### Pattern 3: Progressive Image Quality

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a beautiful sunset"
    
    # Generate preview (fast)
    preview = client.image.generate_url(
        prompt,
        width=256,
        height=256,
        quality="low"
    )
    print(f"Preview (low): {preview}")
    
    # Generate HD version (slower)
    hd_version = client.image.save(
        prompt,
        "sunset_hd.jpg",
        width=1920,
        height=1080,
        quality="hd"
    )
    print(f"HD saved: {hd_version}")
```

### Pattern 4: Chat with Context

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Build conversation
    conversation = [{"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "What is Python?"}]
    
    # First turn
    response = client.text.chat(conversation)
    conversation.append({"role": "assistant", "content": response})
    print(f"AI: {response}")
    
    # Second turn with context
    conversation.append({"role": "user", "content": "What are its benefits?"})
    response = client.text.chat(conversation)
    print(f"AI: {response}")
```

### Pattern 5: Retry on Failure

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom(api_token="your-token") as client:
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = client.text.generate("Hello!")
            print(response)
            break
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = e.retry_after or 60
                print(f"⏳ Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries reached")
                raise
```

---

## 📚 Next Steps

Now that you know the basics, explore more features:

### Core Features
- 🎨 **[Image Generation Guide](IMAGE_GENERATION.md)** - Advanced image features
- 💬 **[Text Generation Guide](TEXT_GENERATION.md)** - Advanced text features
- 👁️ **[Vision Guide](VISION.md)** - Complete vision documentation
- 🔊 **[Audio Guide](AUDIO.md)** - Audio input/output

### Utilities
- 📁 **[File Reader](FILE_READER.md)** - Read files for prompts
- 🧠 **[Reasoning Module](REASONING.md)** - Structured thinking
- ⚡ **[Caching Module](CACHING.md)** - Reduce costs with caching
- 🖥️ **[CLI Guide](CLI.md)** - Complete CLI documentation

### Advanced Topics
- 📖 **[API Reference](API_REFERENCE.md)** - Complete API docs
- 🛡️ **[Error Handling](ERROR_HANDLING.md)** - Comprehensive error handling
- ⚙️ **[Configuration](CONFIGURATION.md)** - Advanced configuration
- 🚀 **[Performance Guide](PERFORMANCE.md)** - Optimization tips

### Tutorials
- 🤖 **[Discord Bot](DISCORD_BOT.md)** - Build a Discord bot
- 📱 **[Telegram Bot](TELEGRAM_BOT.md)** - Build a Telegram bot
- 🌐 **[Web App](WEB_APP.md)** - Build a web application

---

## 💡 Tips for Beginners

1. **Always use context managers** (`with` statement) for automatic cleanup
2. **Start with simple prompts** before adding parameters
3. **Use `generate_url()` for quick testing** (no download needed)
4. **Enable debug mode** when troubleshooting: `Blossom(debug=True)`
5. **Check error suggestions** - they often contain solutions
6. **Use environment variables** for API tokens (never hardcode them)
7. **Try streaming** for better user experience in chat applications
8. **Use `seed` parameter** for reproducible image generation
9. **Start with lower quality** (`medium`) for faster iterations
10. **Read error messages carefully** - they're designed to be helpful!

---

## 🆘 Need Help?

- 📖 **Full Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Installation](INSTALLATION.md) | [Index](INDEX.md) | [Next: Image Generation →](IMAGE_GENERATION.md)

</div>