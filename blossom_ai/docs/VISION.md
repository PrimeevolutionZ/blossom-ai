# 👁️ Vision Support Guide

Complete guide to analyzing images with AI using Blossom AI V2 API.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [MessageBuilder Helper](#messagebuilder-helper)
- [Image Sources](#image-sources)
- [Image Detail Levels](#image-detail-levels)
- [Multiple Images](#multiple-images)
- [Vision with Chat](#vision-with-chat)
- [Common Use Cases](#common-use-cases)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)

---

## 🌟 Overview

**NEW in v0.5.0!** Blossom AI now supports vision capabilities, allowing you to analyze images with AI.

### What You Can Do

- 🖼️ **Analyze Images** - Describe, identify, and understand image content
- 🔗 **Multiple Sources** - Use URLs or local files
- 📊 **Control Detail** - Choose processing level (low/auto/high)
- 🎯 **Compare Images** - Analyze multiple images in one request
- 💬 **Contextual Chat** - Combine vision with conversation history

### Supported Models

Vision works with OpenAI-based models:
- `openai` (default) ✅
- `openai-fast` ✅
- `openai-large` ✅

Other models may not support vision features.

---

## 🚀 Quick Start

### Analyze Image from URL

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/photo.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Analyze Local Image File

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Describe this image in detail",
            image_path="photo.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 🔨 MessageBuilder Helper

The `MessageBuilder` class simplifies creating vision messages.

### Basic Usage

```python
from blossom_ai import MessageBuilder

# Image from URL
message = MessageBuilder.image_message(
    role="user",
    text="What do you see?",
    image_url="https://example.com/image.jpg"
)

# Image from local file
message = MessageBuilder.image_message(
    role="user",
    text="Analyze this photo",
    image_path="photo.jpg"
)

# Regular text message (for comparison)
message = MessageBuilder.text_message(
    role="user",
    content="Hello!"
)
```

### With Detail Level

```python
# Low detail (faster, cheaper)
message = MessageBuilder.image_message(
    role="user",
    text="Is this a cat or dog?",
    image_url="https://example.com/pet.jpg",
    detail="low"
)

# Auto detail (default - balanced)
message = MessageBuilder.image_message(
    role="user",
    text="What's happening here?",
    image_url="https://example.com/scene.jpg",
    detail="auto"
)

# High detail (slower, more accurate)
message = MessageBuilder.image_message(
    role="user",
    text="Extract all text from this document",
    image_url="https://example.com/document.jpg",
    detail="high"
)
```

---

## 🖼️ Image Sources

### From URL

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Describe this image",
            image_url="https://example.com/photo.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

**Requirements:**
- Must be publicly accessible URL
- Supported formats: JPEG, PNG, GIF, WebP
- Max size: ~20MB

### From Local File

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What's in this photo?",
            image_path="vacation.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

**Note:** Local files are automatically converted to base64.

### From Base64 (Manual)

```python
from blossom_ai import Blossom
import base64

# Encode image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

with Blossom(api_token="your-token") as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}",
                        "detail": "auto"
                    }
                }
            ]
        }
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 📊 Image Detail Levels

Control processing detail with the `detail` parameter.

### Available Levels

| Level  | Speed | Cost   | Accuracy | Best For                             |
|--------|-------|--------|----------|--------------------------------------|
| `low`  | ⚡⚡⚡   | 💰     | ⭐⭐⭐      | Quick checks, simple questions       |
| `auto` | ⚡⚡    | 💰💰   | ⭐⭐⭐⭐     | General use (default)                |
| `high` | ⚡     | 💰💰💰 | ⭐⭐⭐⭐⭐    | OCR, fine details, accuracy critical |

### Examples by Detail Level

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    # Low detail - simple classification
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Is this image blurry?",
            image_url="https://example.com/test.jpg",
            detail="low"
        )
    ]
    response = client.text.chat(messages, model="openai")
    
    # Auto detail - general analysis
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Describe what's happening",
            image_url="https://example.com/scene.jpg",
            detail="auto"
        )
    ]
    response = client.text.chat(messages, model="openai")
    
    # High detail - text extraction
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Extract all text visible in this image",
            image_url="https://example.com/document.jpg",
            detail="high"
        )
    ]
    response = client.text.chat(messages, model="openai")
```

---

## 🎯 Multiple Images

Analyze several images in one request.

### Compare Two Images

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two images"},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/before.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/after.jpg"}
                }
            ]
        }
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Multiple Images in Sequence

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Build content array
    content = [
        {"type": "text", "text": "Describe the progression in these images:"}
    ]
    
    # Add multiple images
    for i in range(1, 4):
        content.append({
            "type": "image_url",
            "image_url": {"url": f"https://example.com/step{i}.jpg"}
        })
    
    messages = [{"role": "user", "content": content}]
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 💬 Vision with Chat

Combine vision with conversation context.

### Multi-Turn Vision Chat

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    conversation = []
    
    # Turn 1: Show image
    conversation.append(
        MessageBuilder.image_message(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/photo.jpg"
        )
    )
    
    response = client.text.chat(conversation, model="openai")
    conversation.append({"role": "assistant", "content": response})
    print(f"AI: {response}\n")
    
    # Turn 2: Follow-up (no new image needed)
    conversation.append(
        MessageBuilder.text_message("user", "What colors are dominant?")
    )
    
    response = client.text.chat(conversation, model="openai")
    print(f"AI: {response}")
```

### Vision with System Message

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        {
            "role": "system",
            "content": "You are an expert art critic"
        },
        MessageBuilder.image_message(
            role="user",
            text="Analyze this artwork",
            image_url="https://example.com/painting.jpg",
            detail="high"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 🎨 Common Use Cases

### OCR (Text Extraction)

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Extract all text from this image",
            image_url="https://example.com/document.jpg",
            detail="high"  # High detail for OCR
        )
    ]
    
    text = client.text.chat(messages, model="openai")
    print(f"Extracted:\n{text}")
```

### Object Detection

```python
from blossom_ai import Blossom, MessageBuilder
import json

with Blossom(api_token="your-token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="List all objects visible in this image. Return as JSON array.",
            image_url="https://example.com/scene.jpg",
            detail="high"
        )
    ]
    
    response = client.text.chat(messages, model="openai", json_mode=True)
    objects = json.loads(response)
    
    for obj in objects:
        print(f"- {obj}")
```

### Image Classification

```python
from blossom_ai import Blossom, MessageBuilder

def classify_image(image_url, categories):
    with Blossom(api_token="your-token") as client:
        prompt = f"Classify into one of: {', '.join(categories)}. Reply with category name only."
        
        messages = [
            MessageBuilder.image_message(
                role="user",
                text=prompt,
                image_url=image_url,
                detail="low"
            )
        ]
        
        return client.text.chat(messages, model="openai").strip()

# Use it
categories = ["cat", "dog", "bird", "other"]
result = classify_image("https://example.com/pet.jpg", categories)
print(f"Category: {result}")
```

---

## ✅ Best Practices

### 1. Choose Right Detail Level

```python
# Simple check → low detail
detail="low"   # "Is this blurry?", "Cat or dog?"

# General analysis → auto detail
detail="auto"  # "Describe this scene"

# Text/fine details → high detail
detail="high"  # "Extract text", "Identify small objects"
```

### 2. Be Specific in Prompts

```python
# ❌ Vague
"What's here?"

# ✅ Specific
"List all people in the image with their approximate ages"

# ✅ Very specific
"Extract all text from this receipt: merchant name, date, total, and items"
```

### 3. Use System Messages for Context

```python
messages = [
    {
        "role": "system",
        "content": "You are a professional photo critic. Focus on composition and lighting."
    },
    MessageBuilder.image_message(
        role="user",
        text="Critique this photograph",
        image_url=url
    )
]
```

### 4. Handle Large Images

```python
from PIL import Image

def resize_if_needed(path, max_size=2048):
    img = Image.open(path)
    
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(d * ratio) for d in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        resized = f"resized_{path}"
        img.save(resized)
        return resized
    
    return path
```

### 5. Cache Results

```python
from blossom_ai.utils import cached

@cached(ttl=3600)
def analyze_image(url, question):
    with Blossom(api_token="your-token") as client:
        messages = [
            MessageBuilder.image_message("user", question, image_url=url)
        ]
        return client.text.chat(messages, model="openai")

# First call: hits API
result = analyze_image("https://example.com/photo.jpg", "What's this?")

# Second call: from cache (instant)
result = analyze_image("https://example.com/photo.jpg", "What's this?")
```

---

## 🛡️ Error Handling

### Model Not Supported

```python
from blossom_ai import Blossom, MessageBuilder, BlossomError

try:
    with Blossom(api_token="your-token") as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="Analyze",
                image_url="https://example.com/image.jpg"
            )
        ]
        
        # Some models don't support vision
        response = client.text.chat(messages, model="mistral")
        
except BlossomError as e:
    if "vision" in e.message.lower():
        print("❌ Model doesn't support vision")
        print("💡 Use 'openai' model instead")
```

### Image Not Found

```python
from blossom_ai import Blossom, MessageBuilder, ValidationError

try:
    with Blossom(api_token="your-token") as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="Analyze",
                image_path="nonexistent.jpg"
            )
        ]
        response = client.text.chat(messages, model="openai")
        
except ValidationError as e:
    print(f"❌ {e.message}")
    print("💡 Check file path")
```

### Complete Error Handler

```python
from blossom_ai import (
    Blossom,
    MessageBuilder,
    BlossomError,
    ValidationError,
    AuthenticationError,
    NetworkError
)

def safe_analyze(image_source, question):
    try:
        with Blossom(api_token="your-token") as client:
            # Determine source type
            if image_source.startswith("http"):
                messages = [
                    MessageBuilder.image_message(
                        role="user",
                        text=question,
                        image_url=image_source
                    )
                ]
            else:
                messages = [
                    MessageBuilder.image_message(
                        role="user",
                        text=question,
                        image_path=image_source
                    )
                ]
            
            return client.text.chat(messages, model="openai")
            
    except ValidationError as e:
        print(f"❌ Invalid: {e.message}")
        return None
        
    except AuthenticationError:
        print("❌ Auth failed. Check token.")
        return None
        
    except NetworkError as e:
        print(f"❌ Network: {e.message}")
        return None
        
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        return None
```

---

## 📚 Related Documentation

- **[Text Generation](TEXT_GENERATION.md)** - Generate text with AI
- **[Audio Support](AUDIO.md)** - Audio input/output
- **[Multimodal Guide](MULTIMODAL.md)** - Combine text, images, audio
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors gracefully

---

## 🆘 Need Help?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Quick Start](QUICKSTART.md) | [Index](INDEX.md) | [Next: Audio Support →](AUDIO.md)

</div>