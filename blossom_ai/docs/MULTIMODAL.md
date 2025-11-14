# 🎨 Multimodal Guide

> **Combine text, images, and audio in a single conversation with Blossom AI V2 API**

The V2 API supports true multimodal interactions, allowing you to mix text, images, and audio in your requests and responses.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Vision + Text](#vision--text)
- [Audio Output](#audio-output)
- [Multiple Images](#multiple-images)
- [Complex Workflows](#complex-workflows)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## 🌟 Overview

**Multimodal Capabilities:**
- 👁️ **Vision**: Analyze images (URLs or local files)
- 🔊 **Audio**: Generate audio responses
- 💬 **Text**: Standard text generation
- 🔄 **Mix & Match**: Combine modalities in one request

**Supported Models:**
- `openai` - Full multimodal support (vision + audio)
- Other models may have limited support

---

## 👁️ Vision + Text

### Basic Image Analysis

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    # Analyze image from URL
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What do you see in this image?",
            image_url="https://example.com/photo.jpg",
            detail="auto"  # auto, low, or high
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Local Image Analysis

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Describe this image in detail",
            image_path="/path/to/image.jpg",
            detail="high"  # Request detailed analysis
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Image Detail Levels

```python
# Low detail - faster, cheaper
detail="low"      # Quick overview, less tokens

# Auto detail - balanced (default)
detail="auto"     # API chooses optimal level

# High detail - more accurate
detail="high"     # Detailed analysis, more tokens
```

---

## 🔊 Audio Output

### Generate Audio Response

```python
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    messages = [
        {"role": "user", "content": "Tell me a short story"}
    ]
    
    # Request both text and audio
    response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={
            "voice": "alloy",  # Voice selection
            "format": "wav"    # Audio format
        }
    )
    
    print("Text response:", response)
    # Audio data would be in response metadata
```

### Available Voices

```python
voices = [
    "alloy",    # Neutral, balanced
    "echo",     # Deep, resonant
    "fable",    # British accent
    "onyx",     # Deep, authoritative
    "nova",     # Warm, friendly
    "shimmer"   # Soft, gentle
]

# Use in request
audio = {
    "voice": "nova",
    "format": "wav"  # or "mp3", "opus"
}
```

---

## 🖼️ Multiple Images

### Analyze Multiple Images

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these images"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image1.jpg",
                        "detail": "auto"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image2.jpg",
                        "detail": "auto"
                    }
                }
            ]
        }
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Mix Local and URL Images

```python
import base64
from pathlib import Path

def encode_image(image_path: str) -> str:
    """Encode local image to base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

with Blossom(api_token="your_token") as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two images"},
                # URL image
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image1.jpg"}
                },
                # Local image (base64)
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image('local.jpg')}"
                    }
                }
            ]
        }
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## 🔄 Complex Workflows

### Vision + Reasoning

```python
from blossom_ai import Blossom, MessageBuilder
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

with Blossom(api_token="your_token") as client:
    # First, analyze image
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/scene.jpg"
        )
    ]
    
    description = client.text.chat(messages, model="openai")
    
    # Then, reason about it
    enhanced_prompt = enhancer.enhance(
        f"Based on this image description: '{description}', "
        f"what safety concerns should I consider?",
        level="high",
        mode="native",
        api_version="v2",
        model="openai"
    )
    
    analysis = client.text.chat(
        messages=[{"role": "user", "content": enhanced_prompt["prompt"]}],
        thinking=enhanced_prompt.get("thinking")
    )
    
    print("Description:", description)
    print("\nSafety Analysis:", analysis)
```

### Image Generation + Analysis Loop

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    # Generate image
    prompt = "a futuristic city with flying cars"
    image_data = client.image.generate(
        prompt,
        model="flux",
        quality="high",
        width=1024,
        height=1024
    )
    
    # Save temporarily
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(image_data)
        temp_path = f.name
    
    # Analyze generated image
    messages = [
        MessageBuilder.image_message(
            role="user",
            text="Does this image match the prompt? Provide critique.",
            image_path=temp_path
        )
    ]
    
    critique = client.text.chat(messages, model="openai")
    print("Critique:", critique)
    
    # Clean up
    import os
    os.unlink(temp_path)
```

### Multi-Step Conversation with Images

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    conversation = [
        # User shows first image
        MessageBuilder.image_message(
            role="user",
            text="What color is the car?",
            image_url="https://example.com/car1.jpg"
        )
    ]
    
    response1 = client.text.chat(conversation, model="openai")
    print("AI:", response1)
    
    # Add AI response to conversation
    conversation.append({
        "role": "assistant",
        "content": response1
    })
    
    # User shows second image
    conversation.append(
        MessageBuilder.image_message(
            role="user",
            text="What about this one?",
            image_url="https://example.com/car2.jpg"
        )
    )
    
    response2 = client.text.chat(conversation, model="openai")
    print("AI:", response2)
```

---

## ✅ Best Practices

### 1. Image Optimization

```python
# ❌ Don't send huge images
messages = [
    MessageBuilder.image_message(
        role="user",
        text="Analyze this",
        image_url="https://example.com/huge_8k_image.jpg",  # Wasteful
        detail="high"  # Even more expensive
    )
]

# ✅ Use appropriate detail level
messages = [
    MessageBuilder.image_message(
        role="user",
        text="What's the main object?",
        image_url="https://example.com/image.jpg",
        detail="low"  # Sufficient for simple tasks
    )
]
```

### 2. Model Selection

```python
# ✅ Check model capabilities
with Blossom(api_token="your_token") as client:
    try:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="Analyze this",
                image_url="https://example.com/image.jpg"
            )
        ]
        
        response = client.text.chat(messages, model="openai")
    except Exception as e:
        if "vision" in str(e).lower():
            print("Model doesn't support vision")
            # Fallback to text-only
```

### 3. Error Handling

```python
from blossom_ai import Blossom, MessageBuilder, BlossomError

with Blossom(api_token="your_token") as client:
    try:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="What's in this image?",
                image_path="path/to/image.jpg"
            )
        ]
        
        response = client.text.chat(messages, model="openai")
        
    except FileNotFoundError:
        print("Image file not found")
    except BlossomError as e:
        print(f"API error: {e.message}")
        print(f"Suggestion: {e.suggestion}")
```

### 4. Caching with Multimodal

```python
from blossom_ai.utils import cached
import hashlib

def image_hash(url: str) -> str:
    """Create cache key for image URL"""
    return hashlib.md5(url.encode()).hexdigest()

@cached(ttl=3600)
def analyze_image_cached(image_url: str, question: str):
    """Cache image analysis results"""
    with Blossom(api_token="your_token") as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text=question,
                image_url=image_url
            )
        ]
        return client.text.chat(messages, model="openai")

# First call: API request
result = analyze_image_cached(
    "https://example.com/image.jpg",
    "What's in this image?"
)

# Second call: instant from cache
result = analyze_image_cached(
    "https://example.com/image.jpg",
    "What's in this image?"
)
```

---

## 📚 Examples

### Example 1: Product Analysis

```python
from blossom_ai import Blossom, MessageBuilder

def analyze_product(image_url: str) -> dict:
    """Analyze product from image"""
    with Blossom(api_token="your_token") as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="Analyze this product. Provide: category, color, condition, estimated price.",
                image_url=image_url,
                detail="high"
            )
        ]
        
        response = client.text.chat(
            messages,
            model="openai",
            json_mode=True  # Get structured output
        )
        
        import json
        return json.loads(response)

# Usage
product_info = analyze_product("https://example.com/product.jpg")
print(product_info)
```

### Example 2: Medical Image Assistant

```python
from blossom_ai import Blossom, MessageBuilder

def medical_image_analysis(image_path: str, symptoms: str) -> str:
    """Analyze medical image with patient symptoms"""
    with Blossom(api_token="your_token") as client:
        messages = [
            {
                "role": "system",
                "content": "You are a medical image analysis assistant. "
                          "Provide observations, not diagnoses."
            },
            MessageBuilder.image_message(
                role="user",
                text=f"Patient symptoms: {symptoms}\n\nObservations from image?",
                image_path=image_path,
                detail="high"
            )
        ]
        
        return client.text.chat(messages, model="openai")

# Usage
analysis = medical_image_analysis(
    "xray.jpg",
    "Patient reports chest pain and shortness of breath"
)
print(analysis)
```

### Example 3: Visual QA System

```python
from blossom_ai import Blossom, MessageBuilder

def visual_qa(image_url: str, questions: list[str]) -> dict:
    """Answer multiple questions about an image"""
    results = {}
    
    with Blossom(api_token="your_token") as client:
        for question in questions:
            messages = [
                MessageBuilder.image_message(
                    role="user",
                    text=question,
                    image_url=image_url,
                    detail="auto"
                )
            ]
            
            results[question] = client.text.chat(messages, model="openai")
    
    return results

# Usage
questions = [
    "What is the main object?",
    "What colors are present?",
    "Is this indoors or outdoors?",
    "How many people are visible?"
]

answers = visual_qa("https://example.com/scene.jpg", questions)
for q, a in answers.items():
    print(f"Q: {q}")
    print(f"A: {a}\n")
```

### Example 4: Image Comparison

```python
from blossom_ai import Blossom

def compare_images(image1_url: str, image2_url: str, aspect: str) -> str:
    """Compare two images on specific aspect"""
    with Blossom(api_token="your_token") as client:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Compare these images regarding: {aspect}"},
                    {
                        "type": "image_url",
                        "image_url": {"url": image1_url, "detail": "auto"}
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image2_url, "detail": "auto"}
                    }
                ]
            }
        ]
        
        return client.text.chat(messages, model="openai")

# Usage
comparison = compare_images(
    "https://example.com/before.jpg",
    "https://example.com/after.jpg",
    "lighting quality and composition"
)
print(comparison)
```

---

## ⚠️ Limitations

### Current Limitations

1. **Model Support**: Only `openai` model has full multimodal support
2. **Image Size**: Large images may be automatically resized
3. **Audio Input**: Audio input not yet supported (output only)
4. **Video**: Video analysis not supported

### Token Usage

Vision requests consume more tokens:
- Low detail: ~85 tokens per image
- Auto detail: varies based on image
- High detail: up to 1,360+ tokens per image

### File Formats

**Supported Image Formats:**
- PNG, JPEG, JPG, WEBP, GIF (non-animated)

**Supported Audio Formats:**
- WAV, MP3, OPUS (output only)

---

## 🔗 Related Documentation

- [Vision Support](VISION.md) - Detailed vision features
- [Audio Support](AUDIO.md) - Audio capabilities
- [Text Generation](TEXT_GENERATION.md) - Text-only features
- [MessageBuilder API](API_REFERENCE.md#messagebuilder) - Message construction helpers

---

## 💡 Tips

1. **Start Simple**: Begin with single-image, single-question requests
2. **Detail Matters**: Use `detail="low"` for simple tasks to save costs
3. **Cache Results**: Vision API calls are expensive - cache when possible
4. **Test Models**: Check if your model supports the features you need
5. **Error Handling**: Always handle vision-not-supported errors gracefully

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Vision Guide](VISION.md) | [Audio Guide](AUDIO.md) →

</div>