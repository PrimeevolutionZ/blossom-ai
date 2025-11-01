# 🚀 V2 API Migration Guide

> **Comprehensive guide to migrating from V1 to V2 API**

Blossom AI now supports the new Pollinations V2 API (`enter.pollinations.ai`), which offers significant improvements over the legacy V1 API. This guide will help you migrate smoothly.

---

## 📋 Table of Contents

- [What's New in V2](#-whats-new-in-v2)
- [Quick Start](#-quick-start)
- [Breaking Changes](#-breaking-changes)
- [Feature Comparison](#-feature-comparison)
- [Migration Steps](#-migration-steps)
- [Code Examples](#-code-examples)
- [FAQ](#-faq)

---

## ✨ What's New in V2

### 🎨 Image Generation Improvements

- ✅ **Quality Levels**: `low`, `medium`, `high`, `hd`
- ✅ **Guidance Scale Control**: Fine-tune generation strength (1.0-20.0)
- ✅ **Transparent Backgrounds**: Generate PNG images with transparency
- ✅ **Negative Prompts**: Specify what you don't want in the image
- ✅ **Image-to-Image**: Transform existing images with prompts
- ✅ **Feed Control**: `nofeed` parameter to keep generations private

### 💬 Text Generation Improvements

- ✅ **Full OpenAI Compatibility**: Drop-in replacement for OpenAI API
- ✅ **Function Calling**: Build agentic AI applications
- ✅ **Structured JSON Output**: Guaranteed JSON responses with `json_mode`
- ✅ **Advanced Parameters**: 
  - `max_tokens` - Control response length
  - `frequency_penalty` - Reduce repetition (0-2)
  - `presence_penalty` - Encourage topic diversity (0-2)
  - `top_p` - Nucleus sampling for more controlled randomness
- ✅ **Better Streaming**: More reliable real-time text generation
- ✅ **Model Aliases**: Multiple ways to access the same model

### 🔐 Authentication Improvements

- ✅ **Secret Keys**: Best rate limits, full feature access
- ✅ **Publishable Keys**: Client-side usage with IP-based limits
- ✅ **Better Rate Limits**: Higher quotas for authenticated users
- ✅ **Anonymous Access**: Still available for free models

---

## 🚀 Quick Start

### Installing V2 Support

V2 API support is included in Blossom AI v0.4.0+:

```bash
pip install --upgrade eclips-blossom-ai
```

### Basic V2 Usage

```python
from blossom_ai import Blossom

# Initialize with V2 API
client = Blossom(
    api_version="v2",  # ⬅️ NEW: specify V2
    api_token="your_token_here"  # Get from enter.pollinations.ai
)

# Use as normal - API is the same!
image = client.image.generate("a sunset", quality="hd")
text = client.text.generate("Hello world", max_tokens=50)

client.close_sync()
```

### Getting an API Token

1. Visit [enter.pollinations.ai](https://enter.pollinations.ai)
2. Create an account
3. Generate an API key (Secret or Publishable)
4. Use in your code

---

## ⚠️ Breaking Changes

### 1. Temperature Range

**V1 (Legacy):**
```python
client.text.generate(prompt, temperature=0.8)  # 0-1 range
```

**V2 (New):**
```python
client.text.generate(prompt, temperature=0.8)  # 0-2 range
```

**Impact:** Low - Values 0-1 still work, but you can now go higher.

---

### 2. Endpoint Structure

**V1 URLs:**
- `https://image.pollinations.ai`
- `https://text.pollinations.ai`

**V2 URLs:**
- `https://enter.pollinations.ai/api/generate/image`
- `https://enter.pollinations.ai/api/generate/openai`

**Impact:** None - Handled automatically by `api_version` parameter.

---

### 3. Model Names

Some models may have different names or aliases in V2.

**Check available models:**
```python
client = Blossom(api_version="v2", api_token="token")

# List all available models
image_models = client.image.models()
text_models = client.text.models()

print(f"Image: {image_models}")
print(f"Text: {text_models}")
```

**Impact:** Low - Most model names are the same or have aliases.

---

## 📊 Feature Comparison

### Image Generation

| Feature | V1 | V2 | Notes |
|---------|----|----|-------|
| Basic generation | ✅ | ✅ | Both work |
| Width/Height control | ✅ | ✅ | Both work |
| Seed control | ✅ | ✅ | Both work |
| Model selection | ✅ | ✅ | Both work |
| Quality levels | ❌ | ✅ | `low`, `medium`, `high`, `hd` |
| Guidance scale | ❌ | ✅ | 1.0-20.0 range |
| Negative prompts | ❌ | ✅ | Exclude unwanted elements |
| Transparent backgrounds | ❌ | ✅ | PNG with alpha channel |
| Image-to-image | ❌ | ✅ | Transform existing images |
| Feed control (nofeed) | ❌ | ✅ | Keep private |
| Logo removal (nologo) | ✅ | ✅ | Both work |
| Private generation | ✅ | ✅ | Both work |
| Safe mode | ✅ | ✅ | Both work |

### Text Generation

| Feature | V1 | V2 | Notes |
|---------|----|----|-------|
| Basic generation | ✅ | ✅ | Both work |
| Streaming | ✅ | ✅ | V2 more stable |
| Chat/Conversation | ✅ | ✅ | Both work |
| JSON mode | ✅ | ✅ | V2 more reliable |
| System messages | ✅ | ✅ | Both work |
| Function calling | ❌ | ✅ | **NEW in V2** |
| Max tokens control | ❌ | ✅ | Limit response length |
| Frequency penalty | ❌ | ✅ | Reduce repetition |
| Presence penalty | ❌ | ✅ | Topic diversity |
| Top-p sampling | ❌ | ✅ | Nucleus sampling |
| Temperature 0-2 | ❌ | ✅ | Extended range |
| Model aliases | ❌ | ✅ | Multiple names per model |

### Audio Generation

| Feature | V1 | V2 | Status |
|---------|----|----|--------|
| Text-to-speech | ✅ | 🚧 | Coming soon to V2 |
| Voice selection | ✅ | 🚧 | V1 still recommended |

---

## 🔄 Migration Steps

### Step 1: Update Blossom AI

```bash
pip install --upgrade eclips-blossom-ai
```

Verify version:
```python
import blossom_ai
print(blossom_ai.__version__)  # Should be 0.4.0+
```

---

### Step 2: Get API Token (Optional but Recommended)

1. Visit [enter.pollinations.ai](https://enter.pollinations.ai)
2. Create account
3. Generate API key
4. Save securely

---

### Step 3: Update Code

**Before (V1):**
```python
from blossom_ai import Blossom

client = Blossom()  # Defaults to V1
image = client.image.generate("sunset")
client.close_sync()
```

**After (V2):**
```python
from blossom_ai import Blossom

client = Blossom(
    api_version="v2",  # ⬅️ Add this
    api_token="your_token"  # ⬅️ Add this (optional)
)
image = client.image.generate("sunset")
client.close_sync()
```

---

### Step 4: Leverage New Features (Optional)

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Use V2-only features
image = client.image.generate(
    prompt="beautiful landscape",
    quality="hd",  # ⬅️ NEW
    guidance_scale=7.5,  # ⬅️ NEW
    negative_prompt="blurry, low quality"  # ⬅️ NEW
)

text = client.text.generate(
    prompt="Explain quantum computing",
    max_tokens=200,  # ⬅️ NEW
    frequency_penalty=0.5,  # ⬅️ NEW
    presence_penalty=0.3  # ⬅️ NEW
)

client.close_sync()
```

---

### Step 5: Test Thoroughly

Run your existing tests to ensure everything works:

```python
# Test basic functionality
def test_v2_migration():
    client = Blossom(api_version="v2", api_token="token")
    
    # Test image generation
    image = client.image.generate("test image", width=512, height=512)
    assert len(image) > 0
    
    # Test text generation
    text = client.text.generate("Say hello", max_tokens=10)
    assert len(text) > 0
    
    # Test models
    models = client.text.models()
    assert len(models) > 0
    
    client.close_sync()
    print("✅ Migration successful!")

test_v2_migration()
```

---

## 💡 Code Examples

### Example 1: High-Quality Image Generation

**V1:**
```python
client = Blossom(api_version="v1")
image = client.image.generate(
    "a majestic dragon",
    width=1024,
    height=1024,
    seed=42
)
client.close_sync()
```

**V2 (Enhanced):**
```python
client = Blossom(api_version="v2", api_token="token")
image = client.image.generate(
    "a majestic dragon",
    width=1024,
    height=1024,
    seed=42,
    quality="hd",  # ⬅️ Better quality
    guidance_scale=8.0,  # ⬅️ Stronger prompt adherence
    negative_prompt="blurry, distorted, low quality"  # ⬅️ Avoid bad results
)
client.close_sync()
```

---

### Example 2: Structured JSON Output

**V1:**
```python
client = Blossom(api_version="v1")
# JSON mode exists but less reliable
response = client.text.generate(
    "Generate a JSON with name and age",
    json_mode=True
)
# May need manual validation
client.close_sync()
```

**V2 (Improved):**
```python
client = Blossom(api_version="v2", api_token="token")
response = client.text.generate(
    "Generate a JSON with name, age, and city",
    json_mode=True,  # ⬅️ More reliable in V2
    max_tokens=100
)

import json
data = json.loads(response)  # ✅ Guaranteed to parse
print(data)
client.close_sync()
```

---

### Example 3: Function Calling (V2 Only)

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Chat with function calling
response = client.text.chat(
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ],
    tools=tools,
    tool_choice="auto"
)

print(response)
client.close_sync()
```

---

### Example 4: Advanced Text Control

**V1:**
```python
client = Blossom(api_version="v1")
response = client.text.generate(
    "Write a poem about AI",
    temperature=0.7
)
# Limited control over output
client.close_sync()
```

**V2 (Fine-tuned):**
```python
client = Blossom(api_version="v2", api_token="token")
response = client.text.generate(
    "Write a poem about AI",
    temperature=0.8,  # 0-2 range now
    max_tokens=150,  # ⬅️ Limit length
    frequency_penalty=0.6,  # ⬅️ Less repetition
    presence_penalty=0.4,  # ⬅️ More diverse vocabulary
    top_p=0.9  # ⬅️ Nucleus sampling
)
client.close_sync()
```

---

### Example 5: Gradual Migration (Run Both)

You can use V1 and V2 simultaneously during migration:

```python
from blossom_ai import Blossom

# Old code still works
client_v1 = Blossom(api_version="v1")
image_v1 = client_v1.image.generate("sunset")
client_v1.close_sync()

# New V2 features
client_v2 = Blossom(api_version="v2", api_token="token")
image_v2 = client_v2.image.generate(
    "sunset",
    quality="hd",
    guidance_scale=7.5
)
client_v2.close_sync()

# Compare results
print(f"V1: {len(image_v1)} bytes")
print(f"V2: {len(image_v2)} bytes")
```

---

## ❓ FAQ

### Q: Do I have to migrate to V2?

**A:** No. V1 API continues to work and is still supported. However, V2 offers significant improvements and is recommended for new projects.

---

### Q: Will V1 be deprecated?

**A:** Not immediately. Pollinations.AI maintains V1 for backward compatibility. However, new features are V2-only.

---

### Q: Do I need an API token?

**A:** Not required, but highly recommended:
- ✅ **With token**: Better rate limits, all models, all features
- ⚠️ **Without token**: Basic rate limits, free models only

---

### Q: Can I use V1 and V2 together?

**A:** Yes! You can run both in the same application:

```python
v1_client = Blossom(api_version="v1")
v2_client = Blossom(api_version="v2", api_token="token")
```

---

### Q: What if my code breaks?

**A:** V2 is designed to be backward compatible. Most V1 code works unchanged with V2. If you encounter issues:

1. Check [breaking changes](#-breaking-changes)
2. Verify model names: `client.text.models()`
3. Check [V2 API Reference](V2_API_REFERENCE.md)
4. [Report bugs](https://github.com/PrimeevolutionZ/blossom-ai/issues)

---

### Q: How do I get better image quality?

**V2 offers multiple quality levels:**

```python
# Low quality (fast, smaller files)
image = client.image.generate(prompt, quality="low")

# Medium quality (balanced) - default
image = client.image.generate(prompt, quality="medium")

# High quality (better, larger files)
image = client.image.generate(prompt, quality="high")

# HD quality (best quality, largest files)
image = client.image.generate(prompt, quality="hd")
```

---

### Q: What's guidance_scale?

**A:** Controls how closely the AI follows your prompt:

- **Low (1.0-5.0)**: More creative, may deviate from prompt
- **Medium (5.0-10.0)**: Balanced
- **High (10.0-20.0)**: Strict adherence to prompt

```python
# Creative interpretation
image = client.image.generate(prompt, guidance_scale=3.0)

# Strict adherence
image = client.image.generate(prompt, guidance_scale=15.0)
```

---

### Q: How do negative prompts work?

**A:** Specify what you DON'T want:

```python
image = client.image.generate(
    prompt="a beautiful portrait",
    negative_prompt="ugly, distorted, blurry, low quality, watermark"
)
```

---

### Q: Can I still use audio generation?

**A:** Yes, but V2 audio support is coming soon. Use V1 for now:

```python
# Audio still uses V1
client = Blossom(api_version="v1", api_token="token")
audio = client.audio.generate("Hello world", voice="nova")
```

---

### Q: What are Secret vs Publishable keys?

**Secret Keys (`sk_...`):**
- Best rate limits
- Server-side only
- Can spend Pollen credits
- Full feature access

**Publishable Keys (`pk_...`):**
- IP-based rate limits
- Can be used client-side (browsers)
- Free features only
- All models accessible

---

### Q: How do I debug V2 issues?

```python
from blossom_ai import Blossom

client = Blossom(
    api_version="v2",
    api_token="token",
    debug=True  # ⬅️ Enable debug logging
)

# Check available models
print("Image models:", client.image.models())
print("Text models:", client.text.models())

# Test basic functionality
try:
    image = client.image.generate("test")
    print(f"✅ Image: {len(image)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

client.close_sync()
```

---

## 🔗 Additional Resources

- **[V2 Image Generation Guide](V2_IMAGE_GENERATION.md)** - Detailed image features
- **[V2 Text Generation Guide](V2_TEXT_GENERATION.md)** - Advanced text features
- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API documentation
- **[Error Handling](ERROR_HANDLING.md)** - Handle V2 errors properly

---

## 🆘 Need Help?

- 🐛 **Found a bug?** [Report on GitHub](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 🔒 **Security issue?** See [Security Policy](../../SECURITY.md)
- 💬 **Questions?** Check [existing issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 📚 **More examples?** See feature-specific guides above

---

<div align="center">

**Ready to migrate?** Start with the [Quick Start](#-quick-start) section above!

**Made with 🌸 by the Blossom AI Team**

[Full Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>