# 🎨 Image Generation Guide

Complete guide to generating images with Blossom AI V2 API.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [Generation Methods](#generation-methods)
- [Quality Levels](#quality-levels)
- [Advanced Parameters](#advanced-parameters)
- [Guidance Scale](#guidance-scale)
- [Negative Prompts](#negative-prompts)
- [Image-to-Image](#image-to-image)
- [Transparency](#transparency)
- [Models](#models)
- [Dimensions & Aspect Ratios](#dimensions--aspect-ratios)
- [Reproducibility](#reproducibility)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## 🌟 Overview

Blossom AI v0.5.0 uses the Pollinations V2 API for image generation, offering:

- ✨ **HD Quality** - Generate high-definition images up to 2048x2048
- 🎯 **Guidance Scale** - Fine control over prompt adherence (1.0-20.0)
- 🚫 **Negative Prompts** - Specify what to avoid in generation
- 🌈 **Transparency** - Generate images with transparent backgrounds
- 🖼️ **Image-to-Image** - Transform existing images
- 🎲 **Reproducibility** - Use seeds for consistent results
- ⚡ **Fast URLs** - Get instant image URLs without downloading

### Supported Models

Default models in V2 API:
- `flux` (default) - High quality, versatile
- `turbo` - Fast generation
- `gptimage` - GPT-based generation
- And more (fetch dynamically)

---

## 🚀 Basic Usage

### Simplest Example

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate and save image
    filepath = client.image.save(
        prompt="a beautiful sunset over mountains",
        filename="sunset.jpg"
    )
    print(f"✅ Saved to: {filepath}")
```

### Quick URL Generation

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Get URL without downloading (fastest)
    url = client.image.generate_url(
        prompt="a cute robot"
    )
    print(f"🔗 {url}")
    # Share this URL directly!
```

### Get Raw Bytes

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Get image as bytes
    image_data = client.image.generate(
        prompt="a colorful pattern"
    )
    
    # Process or save manually
    with open("pattern.png", "wb") as f:
        f.write(image_data)
```

---

## 📦 Generation Methods

The image generator provides three methods:

### 1. `generate()` - Get Bytes

Returns raw image data as bytes.

```python
image_data = client.image.generate(
    prompt="a landscape",
    width=1024,
    height=1024,
    model="flux"
)

# Returns: bytes object
print(f"Size: {len(image_data)} bytes")
```

**Use when:**
- You need to process image data
- Sending to another API
- Custom storage handling
- Working with image libraries (PIL, OpenCV)

### 2. `save()` - Generate and Save

Generates and saves image to file in one step.

```python
filepath = client.image.save(
    prompt="a sunset",
    filename="sunset.jpg",
    width=1920,
    height=1080
)

# Returns: str (file path)
print(f"Saved to: {filepath}")
```

**Use when:**
- You want to save directly to disk
- Building a CLI tool
- Batch generation to files
- Simplest workflow

### 3. `generate_url()` - Get URL Only

Returns image URL without downloading.

```python
url = client.image.generate_url(
    prompt="a robot",
    width=512,
    height=512
)

# Returns: str (URL)
print(f"URL: {url}")
```

**Use when:**
- Fastest method (no download)
- Sharing URLs directly
- Using in web applications
- Preview before downloading
- Embedding in HTML/Markdown

---

## ✨ Quality Levels

**NEW in V2!** Control image quality with the `quality` parameter.

### Available Quality Levels

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Low quality - fastest, smallest
    client.image.save(
        "a test image",
        "test_low.jpg",
        quality="low"
    )
    
    # Medium quality - balanced (default)
    client.image.save(
        "a test image",
        "test_medium.jpg",
        quality="medium"
    )
    
    # High quality - detailed
    client.image.save(
        "a test image",
        "test_high.jpg",
        quality="high"
    )
    
    # HD quality - maximum detail
    client.image.save(
        "a test image",
        "test_hd.jpg",
        quality="hd"
    )
```

### Quality Comparison

| Quality  | Speed | Detail | File Size | Use Case                      |
|----------|-------|--------|-----------|-------------------------------|
| `low`    | ⚡⚡⚡⚡  | ⭐      | ~100KB    | Previews, thumbnails, testing |
| `medium` | ⚡⚡⚡   | ⭐⭐⭐    | ~500KB    | General use, social media     |
| `high`   | ⚡⚡    | ⭐⭐⭐⭐   | ~2MB      | Print, professional use       |
| `hd`     | ⚡     | ⭐⭐⭐⭐⭐  | ~5MB      | Maximum quality, large prints |

### Progressive Quality Example

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a detailed mountain landscape"
    
    # Step 1: Quick preview
    preview = client.image.generate_url(
        prompt,
        width=256,
        height=256,
        quality="low"
    )
    print(f"Preview: {preview}")
    
    # Step 2: Show user preview, then generate HD
    hd_path = client.image.save(
        prompt,
        "landscape_hd.jpg",
        width=1920,
        height=1080,
        quality="hd"
    )
    print(f"HD saved: {hd_path}")
```

---

## ⚙️ Advanced Parameters

### Complete Parameter List

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    filepath = client.image.save(
        # Required
        prompt="a futuristic city at night",
        filename="city.jpg",
        
        # Dimensions
        width=1920,              # Image width (default: 1024)
        height=1080,             # Image height (default: 1024)
        
        # Quality & Model
        quality="hd",            # low, medium, high, hd (default: medium)
        model="flux",            # Model name (default: flux)
        
        # Control
        seed=42,                 # Random seed (default: 42)
        guidance_scale=7.5,      # Prompt adherence 1-20 (default: None)
        negative_prompt="blurry, low quality",  # What to avoid
        
        # Enhancement
        enhance=True,            # Auto-enhance prompt (default: False)
        
        # Special Features
        transparent=False,       # Transparent background (default: False)
        image=None,              # Input image URL for img2img
        
        # Privacy
        private=False,           # Private generation (default: False)
        nologo=False,            # Remove watermark (default: False)
        nofeed=False,            # Don't add to public feed (default: False)
        safe=False               # Enable safety filter (default: False)
    )
```

### Parameter Details

#### `width` & `height`
- **Type:** `int`
- **Range:** 64-2048 pixels
- **Default:** 1024x1024
- **Notes:** Larger sizes = slower generation

#### `quality`
- **Type:** `str`
- **Values:** `"low"`, `"medium"`, `"high"`, `"hd"`
- **Default:** `"medium"`
- **NEW in V2!**

#### `model`
- **Type:** `str`
- **Default:** `"flux"`
- **Examples:** `"flux"`, `"turbo"`, `"gptimage"`

#### `seed`
- **Type:** `int`
- **Default:** `42`
- **Notes:** Same seed = reproducible results

#### `guidance_scale`
- **Type:** `float`
- **Range:** 1.0-20.0
- **Default:** `None` (model default)
- **NEW in V2!** See [Guidance Scale](#guidance-scale)

#### `negative_prompt`
- **Type:** `str`
- **Default:** `"worst quality, blurry"`
- **NEW in V2!** See [Negative Prompts](#negative-prompts)

#### `enhance`
- **Type:** `bool`
- **Default:** `False`
- **Notes:** Automatically improves your prompt

#### `transparent`
- **Type:** `bool`
- **Default:** `False`
- **NEW in V2!** See [Transparency](#transparency)

#### `image`
- **Type:** `str` (URL)
- **Default:** `None`
- **NEW in V2!** See [Image-to-Image](#image-to-image)

#### Privacy Options

- `private`: Make generation private
- `nologo`: Remove Pollinations watermark
- `nofeed`: Don't add to public feed
- `safe`: Enable content safety filter

---

## 🎯 Guidance Scale

**NEW in V2!** Control how closely the AI follows your prompt.

### What is Guidance Scale?

Guidance scale controls the balance between:
- **Creativity** (low values)
- **Prompt adherence** (high values)

### Scale Range

- **1.0-3.0** - Very creative, loose interpretation
- **4.0-7.0** - Balanced (recommended)
- **7.5-12.0** - Strong adherence to prompt
- **12.0-20.0** - Maximum adherence, less creativity

### Examples

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a surreal dreamscape"
    
    # Low guidance - more creative
    client.image.save(
        prompt,
        "creative.jpg",
        guidance_scale=2.0
    )
    
    # Balanced - recommended
    client.image.save(
        prompt,
        "balanced.jpg",
        guidance_scale=7.5
    )
    
    # High guidance - strict adherence
    client.image.save(
        prompt,
        "strict.jpg",
        guidance_scale=15.0
    )
```

### When to Use Different Values

**Low (1.0-3.0):**
- Abstract art
- Artistic interpretation
- Experimental generations

**Medium (4.0-8.0):**
- General use
- Photorealistic images
- Most prompts (recommended)

**High (8.0-15.0):**
- Precise compositions
- Specific details required
- Product images
- Technical illustrations

**Very High (15.0-20.0):**
- Exact prompt matching
- Professional requirements
- May reduce creativity

---

## 🚫 Negative Prompts

**NEW in V2!** Specify what you DON'T want in the image.

### Basic Usage

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    filepath = client.image.save(
        prompt="a beautiful portrait",
        filename="portrait.jpg",
        negative_prompt="blurry, low quality, distorted, ugly"
    )
```

### Common Negative Prompts

#### For Quality

```python
negative_prompt = "blurry, low quality, pixelated, jpeg artifacts, worst quality"
```

#### For Portraits

```python
negative_prompt = "distorted face, extra limbs, deformed, ugly, bad anatomy"
```

#### For Landscapes

```python
negative_prompt = "blurry, low quality, oversaturated, unrealistic colors"
```

#### For Product Photos

```python
negative_prompt = "blurry, shadows, reflections, watermark, text, logo"
```

### Best Practices

1. **Be specific** - "distorted hands" better than "bad"
2. **Comma-separated** - Multiple issues: "blur, noise, grain"
3. **Common issues** - Include typical problems
4. **Don't overdo** - 3-7 terms usually sufficient
5. **Test combinations** - Find what works for your use case

### Examples

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Portrait with quality control
    client.image.save(
        prompt="professional headshot, studio lighting",
        filename="headshot.jpg",
        negative_prompt="blurry, low quality, bad lighting, distorted face",
        guidance_scale=7.5,
        quality="hd"
    )
    
    # Landscape without common issues
    client.image.save(
        prompt="mountain landscape at sunset",
        filename="landscape.jpg",
        negative_prompt="blurry, oversaturated, unrealistic, low quality",
        quality="high"
    )
    
    # Product photo
    client.image.save(
        prompt="product photography, white background, professional",
        filename="product.jpg",
        negative_prompt="shadows, reflections, text, watermark, low quality",
        guidance_scale=10.0,
        quality="hd"
    )
```

---

## 🖼️ Image-to-Image

**NEW in V2!** Transform existing images with prompts.

### Basic Image-to-Image

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Transform existing image
    result = client.image.save(
        prompt="transform into oil painting style",
        filename="oil_painting.jpg",
        image="https://example.com/photo.jpg",  # Input image URL
        guidance_scale=7.5
    )
```

### Use Cases

#### 1. Style Transfer

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Convert photo to different art styles
    styles = [
        "oil painting",
        "watercolor",
        "pencil sketch",
        "digital art"
    ]
    
    input_image = "https://example.com/photo.jpg"
    
    for style in styles:
        client.image.save(
            prompt=f"transform into {style} style",
            filename=f"photo_{style.replace(' ', '_')}.jpg",
            image=input_image,
            guidance_scale=8.0
        )
```

#### 2. Image Enhancement

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Enhance and upscale
    client.image.save(
        prompt="enhance quality, increase detail, professional photography",
        filename="enhanced.jpg",
        image="https://example.com/low_res.jpg",
        width=1920,
        height=1080,
        quality="hd",
        guidance_scale=6.0
    )
```

#### 3. Creative Variations

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Create variations
    base_image = "https://example.com/concept.jpg"
    
    variations = [
        "same scene at sunset",
        "same scene in winter",
        "same scene with neon lights"
    ]
    
    for i, variation in enumerate(variations):
        client.image.save(
            prompt=variation,
            filename=f"variation_{i}.jpg",
            image=base_image,
            guidance_scale=7.0
        )
```

#### 4. Background Modification

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Change background
    client.image.save(
        prompt="same subject, tropical beach background",
        filename="new_background.jpg",
        image="https://example.com/portrait.jpg",
        guidance_scale=8.0
    )
```

---

## 🌈 Transparency

**NEW in V2!** Generate images with transparent backgrounds.

### Basic Transparency

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate with transparent background
    client.image.save(
        prompt="a red apple",
        filename="apple.png",  # Use PNG format
        transparent=True
    )
```

### Use Cases

#### 1. Logos and Icons

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    client.image.save(
        prompt="modern tech company logo, simple, minimalist",
        filename="logo.png",
        transparent=True,
        width=512,
        height=512
    )
```

#### 2. Product Images

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    client.image.save(
        prompt="product photo, single object, no background",
        filename="product.png",
        transparent=True,
        quality="hd"
    )
```

#### 3. Stickers and Graphics

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    stickers = ["cute cat", "happy dog", "cool robot"]
    
    for sticker in stickers:
        client.image.save(
            prompt=f"{sticker} sticker, cartoon style",
            filename=f"{sticker.replace(' ', '_')}.png",
            transparent=True,
            width=512,
            height=512
        )
```

### Best Practices

1. **Use PNG format** - Required for transparency
2. **Clear prompts** - Mention "no background" or "isolated object"
3. **Simple subjects** - Works best with single objects
4. **Higher quality** - Use `quality="high"` or `"hd"` for clean edges
5. **Test guidance** - Try `guidance_scale=8-12` for better separation

---

## 🎭 Models

### Available Models

Fetch available models dynamically:

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    models = client.image.models()
    print(f"Available models: {models}")
```

### Common Models

- **flux** (default) - High quality, versatile
- **turbo** - Fast generation
- **gptimage** - GPT-based generation
- **seedream** - Experimental
- **kontext** - Context-aware

### Choosing a Model

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # High quality (default)
    client.image.save(
        "a landscape",
        "landscape_flux.jpg",
        model="flux"
    )
    
    # Fast generation
    client.image.save(
        "a portrait",
        "portrait_turbo.jpg",
        model="turbo"
    )
```

### Model Comparison

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a mountain landscape"
    models = ["flux", "turbo", "gptimage"]
    
    for model in models:
        try:
            client.image.save(
                prompt,
                f"test_{model}.jpg",
                model=model,
                width=512,
                height=512
            )
            print(f"✅ {model} completed")
        except Exception as e:
            print(f"❌ {model} failed: {e}")
```

---

## 📐 Dimensions & Aspect Ratios

### Standard Sizes

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Square (1:1)
    client.image.save("square image", "square.jpg", width=1024, height=1024)
    
    # Landscape (16:9)
    client.image.save("landscape", "landscape.jpg", width=1920, height=1080)
    
    # Portrait (9:16)
    client.image.save("portrait", "portrait.jpg", width=1080, height=1920)
    
    # Ultrawide (21:9)
    client.image.save("ultrawide", "ultrawide.jpg", width=2560, height=1080)
```

### Common Aspect Ratios

| Ratio | Use Case                | Example Sizes        |
|-------|-------------------------|----------------------|
| 1:1   | Social media, icons     | 512x512, 1024x1024   |
| 4:3   | Traditional photos      | 1024x768, 1600x1200  |
| 16:9  | Widescreen, video       | 1920x1080, 2560x1440 |
| 9:16  | Vertical video, stories | 1080x1920            |
| 21:9  | Ultrawide               | 2560x1080            |
| 3:2   | Photography             | 1620x1080            |

### Social Media Sizes

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Instagram Post (1:1)
    client.image.save(
        "instagram post",
        "instagram.jpg",
        width=1080,
        height=1080
    )
    
    # Instagram Story (9:16)
    client.image.save(
        "instagram story",
        "story.jpg",
        width=1080,
        height=1920
    )
    
    # Twitter Header (3:1)
    client.image.save(
        "twitter header",
        "twitter_header.jpg",
        width=1500,
        height=500
    )
    
    # Facebook Cover (205:78)
    client.image.save(
        "facebook cover",
        "fb_cover.jpg",
        width=820,
        height=312
    )
```

### Best Practices

1. **Stay within limits** - 64-2048 pixels
2. **Consider file size** - Larger = slower generation
3. **Match use case** - Choose appropriate ratio
4. **Test first** - Use smaller sizes for testing
5. **Upscale if needed** - Start smaller, upscale later

---

## 🎲 Reproducibility

### Using Seeds

Seeds ensure reproducible results:

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate with specific seed
    SEED = 42
    
    # These will be identical
    client.image.save(
        "a mountain",
        "mountain_1.jpg",
        seed=SEED
    )
    
    client.image.save(
        "a mountain",
        "mountain_2.jpg",
        seed=SEED  # Same seed = same result
    )
```

### Testing Variations

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a futuristic city"
    
    # Test different seeds
    for seed in [42, 123, 456, 789]:
        client.image.save(
            prompt,
            f"city_seed_{seed}.jpg",
            seed=seed,
            width=512,
            height=512
        )
```

### Parameter Exploration

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    SEED = 42  # Fixed seed for fair comparison
    prompt = "a portrait"
    
    # Test different guidance scales
    for guidance in [3.0, 7.5, 12.0]:
        client.image.save(
            prompt,
            f"portrait_guidance_{guidance}.jpg",
            seed=SEED,
            guidance_scale=guidance
        )
    
    # Test different qualities
    for quality in ["low", "medium", "high", "hd"]:
        client.image.save(
            prompt,
            f"portrait_{quality}.jpg",
            seed=SEED,
            quality=quality
        )
```

---

## ✅ Best Practices

### 1. Writing Effective Prompts

```python
# ❌ Bad: Vague, unclear
prompt = "nice picture"

# ✅ Good: Specific, detailed
prompt = "professional portrait photograph, soft lighting, shallow depth of field"

# ✅ Better: Very detailed
prompt = "professional headshot, studio lighting, blurred background, sharp focus on face, neutral expression, business attire"
```

### 2. Start Small, Then Upscale

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a detailed landscape"
    
    # Step 1: Test with low quality/size (fast)
    test_url = client.image.generate_url(
        prompt,
        width=256,
        height=256,
        quality="low"
    )
    print(f"Preview: {test_url}")
    
    # Step 2: If satisfied, generate HD
    final = client.image.save(
        prompt,
        "final.jpg",
        width=1920,
        height=1080,
        quality="hd"
    )
```

### 3. Use Appropriate Quality

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Testing/Preview - use low
    client.image.generate_url("test", quality="low")
    
    # Social media - use medium
    client.image.save("post", "post.jpg", quality="medium")
    
    # Print/Professional - use hd
    client.image.save("print", "print.jpg", quality="hd")
```

### 4. Combine Features

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Maximum quality control
    client.image.save(
        prompt="professional product photo",
        filename="product.jpg",
        width=1920,
        height=1080,
        quality="hd",
        guidance_scale=10.0,
        negative_prompt="blurry, shadows, reflections, low quality",
        seed=42  # Reproducible
    )
```

### 5. Error Handling

```python
from blossom_ai import Blossom, BlossomError

with Blossom(api_token="your-token") as client:
    try:
        filepath = client.image.save(
            "a test image",
            "test.jpg",
            width=2048,
            height=2048,
            quality="hd"
        )
        print(f"✅ Success: {filepath}")
        
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        if e.suggestion:
            print(f"💡 Suggestion: {e.suggestion}")
```

---

## 🛡️ Error Handling

### Common Errors

#### ValidationError

```python
from blossom_ai import Blossom, ValidationError

with Blossom(api_token="your-token") as client:
    try:
        # Prompt too long
        client.image.generate("a" * 300)
    except ValidationError as e:
        print(f"Invalid parameter: {e.message}")
```

#### AuthenticationError

```python
from blossom_ai import Blossom, AuthenticationError

try:
    client = Blossom(api_token="invalid-token")
    client.image.generate("test")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

#### RateLimitError

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom(api_token="your-token") as client:
    try:
        client.image.generate("test")
    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
        if e.retry_after:
            print(f"Wait {e.retry_after}s")
            time.sleep(e.retry_after)
```

### Complete Error Handling

```python
from blossom_ai import (
    Blossom,
    BlossomError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
    TimeoutError
)

with Blossom(api_token="your-token") as client:
    try:
        filepath = client.image.save("test", "test.jpg")
        print(f"✅ {filepath}")
        
    except ValidationError as e:
        print(f"❌ Invalid: {e.message}")
        
    except AuthenticationError as e:
        print(f"❌ Auth: {e.message}")
        print(f"💡 {e.suggestion}")
        
    except RateLimitError as e:
        print(f"❌ Rate limit: {e.message}")
        if e.retry_after:
            print(f"⏳ Wait {e.retry_after}s")
            
    except TimeoutError as e:
        print(f"❌ Timeout: {e.message}")
        
    except NetworkError as e:
        print(f"❌ Network: {e.message}")
        
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
```

---

## 📚 Examples

### Example 1: Batch Generation

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompts = [
        "a sunset",
        "a forest",
        "a mountain",
        "an ocean",
        "a desert"
    ]
    
    for i, prompt in enumerate(prompts):
        filepath = client.image.save(
            prompt,
            f"scene_{i}.jpg",
            width=1024,
            height=1024,
            quality="high"
        )
        print(f"✅ Generated: {filepath}")
```

### Example 2: A/B Testing

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a product photo"
    
    # Version A: Standard
    client.image.save(
        prompt,
        "version_a.jpg",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality"
    )
    
    # Version B: Enhanced
    client.image.save(
        prompt,
        "version_b.jpg",
        guidance_scale=10.0,
        negative_prompt="blurry, low quality, shadows, reflections",
        quality="hd"
    )
```

### Example 3: Progressive Enhancement

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "a cityscape"
    seed = 42
    
    # Low res preview
    preview_url = client.image.generate_url(
        prompt,
        width=256,
        height=256,
        quality="low",
        seed=seed
    )
    print(f"Preview: {preview_url}")
    
    # Medium quality
    medium = client.image.save(
        prompt,
        "city_medium.jpg",
        width=1024,
        height=1024,
        quality="medium",
        seed=seed
    )
    
    # High quality final
    final = client.image.save(
        prompt,
        "city_final.jpg",
        width=1920,
        height=1080,
        quality="hd",
        seed=seed,
        guidance_scale=8.0
    )
```

### Example 4: Style Exploration

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    subject = "a portrait of a woman"
    styles = [
        "oil painting",
        "watercolor",
        "digital art",
        "pencil sketch",
        "photorealistic"
    ]
    
    for style in styles:
        prompt = f"{subject}, {style} style"
        client.image.save(
            prompt,
            f"portrait_{style.replace(' ', '_')}.jpg",
            width=768,
            height=1024,
            quality="high",
            guidance_scale=7.5
        )
```

### Example 5: Thumbnail Grid

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    base_prompt = "a nature scene"
    variations = [
        "forest", "mountain", "ocean", "desert",
        "river", "waterfall", "canyon", "valley"
    ]
    
    # Generate thumbnail grid
    for i, variation in enumerate(variations):
        client.image.save(
            f"{base_prompt}, {variation}",
            f"thumb_{i:02d}_{variation}.jpg",
            width=256,
            height=256,
            quality="medium"
        )
```

### Example 6: Template System

```python
from blossom_ai import Blossom

class ImageTemplate:
    def __init__(self, client):
        self.client = client
    
    def social_media_post(self, content):
        return self.client.image.save(
            content,
            "social_post.jpg",
            width=1080,
            height=1080,
            quality="high",
            guidance_scale=8.0
        )
    
    def banner(self, content):
        return self.client.image.save(
            content,
            "banner.jpg",
            width=1920,
            height=400,
            quality="high"
        )
    
    def thumbnail(self, content):
        return self.client.image.save(
            content,
            "thumbnail.jpg",
            width=256,
            height=256,
            quality="medium"
        )

with Blossom(api_token="your-token") as client:
    templates = ImageTemplate(client)
    
    templates.social_media_post("summer sale announcement")
    templates.banner("welcome banner")
    templates.thumbnail("product preview")
```

### Example 7: Quality Comparison

```python
from blossom_ai import Blossom
import os

with Blossom(api_token="your-token") as client:
    prompt = "a detailed landscape"
    qualities = ["low", "medium", "high", "hd"]
    
    print("Generating quality comparison...")
    for quality in qualities:
        filepath = client.image.save(
            prompt,
            f"quality_{quality}.jpg",
            width=1024,
            height=1024,
            quality=quality,
            seed=42  # Same seed for fair comparison
        )
        
        # Check file size
        size = os.path.getsize(filepath) / 1024  # KB
        print(f"{quality:8s}: {size:8.1f} KB - {filepath}")
```

### Example 8: Async Batch Generation

```python
import asyncio
from blossom_ai import Blossom

async def generate_images():
    async with Blossom(api_token="your-token") as client:
        prompts = [f"scene {i}" for i in range(10)]
        
        # Generate all in parallel
        tasks = [
            client.image.save(prompt, f"scene_{i}.jpg", width=512, height=512)
            for i, prompt in enumerate(prompts)
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"✅ Generated {len(results)} images")

asyncio.run(generate_images())
```

---

## 🔗 Related Documentation

- **[Text Generation](TEXT_GENERATION.md)** - Generate text with AI
- **[Vision Support](VISION.md)** - Analyze images with AI
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors gracefully
- **[Quick Start](QUICKSTART.md)** - Get started quickly

---

## 💡 Tips & Tricks

### Prompt Engineering

1. **Be specific** - "professional headshot, studio lighting" > "nice photo"
2. **Add style** - "oil painting style", "photorealistic", "digital art"
3. **Mention quality** - "high quality", "detailed", "sharp focus"
4. **Describe lighting** - "soft lighting", "golden hour", "dramatic shadows"
5. **Set mood** - "peaceful", "energetic", "mysterious"

### Performance Optimization

1. **Use `generate_url()` for previews** - Fastest method
2. **Start with lower quality** - Test before HD generation
3. **Cache results** - Use [Caching Module](CACHING.md)
4. **Batch similar requests** - Reuse same parameters
5. **Use async for parallel** - Generate multiple images at once

### Quality Control

1. **Use negative prompts** - Avoid common issues
2. **Set guidance scale** - Control prompt adherence
3. **Test different seeds** - Find best results
4. **Compare qualities** - Find balance of speed/quality
5. **Enhance prompts** - Use `enhance=True` for auto-improvement

### Cost Optimization

1. **Use lower quality for testing** - Save tokens
2. **Cache frequently used images** - Avoid regeneration
3. **Start small, upscale later** - Test before final generation
4. **Reuse URLs when possible** - Share instead of regenerating
5. **Batch operations** - Fewer API calls

---

## 🆘 Troubleshooting

### Issue: Blurry Images

**Solution:**
```python
# Use higher quality + negative prompt
client.image.save(
    prompt,
    "sharp.jpg",
    quality="hd",
    negative_prompt="blurry, low quality, out of focus",
    guidance_scale=8.0
)
```

### Issue: Wrong Colors

**Solution:**
```python
# Increase guidance scale + specific color mentions
client.image.save(
    "portrait with natural skin tones",
    "portrait.jpg",
    guidance_scale=10.0,
    negative_prompt="oversaturated, wrong colors"
)
```

### Issue: Distorted Objects

**Solution:**
```python
# Higher guidance + negative prompt
client.image.save(
    prompt,
    "clean.jpg",
    guidance_scale=12.0,
    negative_prompt="distorted, deformed, malformed, bad anatomy"
)
```

### Issue: Generation Too Slow

**Solution:**
```python
# Use lower quality or smaller size
client.image.save(
    prompt,
    "fast.jpg",
    width=512,
    height=512,
    quality="medium"
)

# Or use turbo model
client.image.save(
    prompt,
    "turbo.jpg",
    model="turbo"
)
```

### Issue: Inconsistent Results

**Solution:**
```python
# Use fixed seed for reproducibility
client.image.save(
    prompt,
    "consistent.jpg",
    seed=42  # Same seed = same result
)
```

---

## 📝 Summary

### Key Features

- ✨ **Quality Levels** - low, medium, high, hd
- 🎯 **Guidance Scale** - Control prompt adherence (1-20)
- 🚫 **Negative Prompts** - Specify what to avoid
- 🖼️ **Image-to-Image** - Transform existing images
- 🌈 **Transparency** - Generate transparent backgrounds
- 🎲 **Reproducibility** - Use seeds for consistent results
- ⚡ **Fast URLs** - Get URLs without downloading

### Best Practices

1. Start with previews, then generate HD
2. Use negative prompts for quality control
3. Test different guidance scales
4. Use appropriate quality for use case
5. Handle errors gracefully
6. Cache results when possible
7. Use async for batch generation

### Next Steps

1. 💬 **[Text Generation](TEXT_GENERATION.md)** - Generate text with AI
2. 👁️ **[Vision Support](VISION.md)** - Analyze images
3. 🧠 **[Reasoning Module](REASONING.md)** - Enhanced prompts
4. ⚡ **[Caching Module](CACHING.md)** - Reduce costs
5. 📖 **[API Reference](API_REFERENCE.md)** - Complete documentation

---

## 🆘 Need Help?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Quick Start](QUICKSTART.md) | [Index](INDEX.md) | [Next: Text Generation →](TEXT_GENERATION.md)

</div>