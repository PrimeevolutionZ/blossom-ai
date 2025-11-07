# 🎨 V2 Image Generation Guide

> **Advanced image generation with Pollinations V2 API**

The V2 API introduces powerful new features for image generation including quality control, guidance scaling, negative prompts, and transparency support.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [New V2 Features](#-new-v2-features)
- [Quality Levels](#-quality-levels)
- [Guidance Scale](#-guidance-scale)
- [Negative Prompts](#-negative-prompts)
- [Transparent Backgrounds](#-transparent-backgrounds)
- [Image-to-Image](#️-image-to-image)
- [Advanced Examples](#-advanced-examples)
- [Best Practices](#-best-practices)

---

## 🚀 Quick Start

```python
from blossom_ai import Blossom

# Initialize V2 client
client = Blossom(
    api_version="v2",
    api_token="your_token_here"
)

# Generate HD image with V2 features
image = client.image.generate(
    prompt="a majestic dragon flying over mountains",
    quality="hd",  # NEW: HD quality
    guidance_scale=7.5,  # NEW: Prompt adherence
    negative_prompt="blurry, distorted"  # NEW: What to avoid
)

# Save result
with open("dragon.png", "wb") as f:
    f.write(image)

client.close_sync()
```

---

## ✨ New V2 Features

| Feature             | Description                      | Example Value                         |
|---------------------|----------------------------------|---------------------------------------|
| **quality**         | Output quality level             | `"low"`, `"medium"`, `"high"`, `"hd"` |
| **guidance_scale**  | Prompt adherence strength        | `1.0` - `20.0` (default: `7.5`)       |
| **negative_prompt** | Elements to exclude              | `"blurry, low quality"`               |
| **transparent**     | PNG with alpha channel           | `True` / `False`                      |
| **image**           | Image-to-image transformation    | URL of source image                   |
| **nofeed**          | Keep private (don't add to feed) | `True` / `False`                      |

---

## 🎯 Quality Levels

Control the output quality vs generation time trade-off.

### Available Levels

```python
# Low quality - Fast generation, smaller files
image = client.image.generate(
    "sunset",
    quality="low"
)

# Medium quality - Balanced (DEFAULT)
image = client.image.generate(
    "sunset",
    quality="medium"
)

# High quality - Better details, larger files
image = client.image.generate(
    "sunset",
    quality="high"
)

# HD quality - Best quality, largest files, slower
image = client.image.generate(
    "sunset",
    quality="hd"
)
```

### Quality Comparison

| Level    | Speed       | File Size   | Use Case                         |
|----------|-------------|-------------|----------------------------------|
| `low`    | ⚡⚡⚡ Fast    | ~10-30 KB   | Previews, thumbnails, testing    |
| `medium` | ⚡⚡ Moderate | ~30-100 KB  | General use, web images          |
| `high`   | ⚡ Slower    | ~100-300 KB | Detailed artwork, prints         |
| `hd`     | 🐢 Slowest  | ~300-500 KB | Professional use, large displays |

### Example: Quality Progression

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

prompt = "a detailed portrait of a wise wizard"

# Generate at different quality levels
for quality in ["low", "medium", "high", "hd"]:
    image = client.image.generate(
        prompt=prompt,
        quality=quality,
        seed=42  # Same seed for comparison
    )
    
    filename = f"wizard_{quality}.png"
    with open(filename, "wb") as f:
        f.write(image)
    
    print(f"{quality}: {len(image)} bytes -> {filename}")

client.close_sync()

# Output:
# low: 24567 bytes -> wizard_low.png
# medium: 87234 bytes -> wizard_medium.png
# high: 234567 bytes -> wizard_high.png
# hd: 456789 bytes -> wizard_hd.png
```

---

## 🎚️ Guidance Scale

Controls how strictly the AI follows your prompt.

### Understanding Guidance Scale

- **Low (1.0-5.0)**: Creative freedom, may deviate from prompt
- **Medium (5.0-10.0)**: Balanced adherence
- **High (10.0-20.0)**: Strict prompt following

### Example: Guidance Scale Comparison

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

prompt = "a red apple on a blue table"

# Test different guidance scales
scales = [3.0, 7.5, 15.0]

for scale in scales:
    image = client.image.generate(
        prompt=prompt,
        guidance_scale=scale,
        seed=42
    )
    
    with open(f"apple_guidance_{scale}.png", "wb") as f:
        f.write(image)
    
    print(f"Guidance {scale}: Generated")

client.close_sync()

# Results:
# 3.0: More artistic, may have variations in color/position
# 7.5: Balanced, good adherence to "red apple on blue table"
# 15.0: Very strict, exactly red apple, exactly blue table
```

### When to Use Different Scales

**Low Guidance (1.0-5.0):**
- Abstract art
- Creative interpretations
- Artistic freedom desired
- Exploratory generation

```python
image = client.image.generate(
    "abstract cosmic energy",
    guidance_scale=3.0  # Let AI be creative
)
```

**Medium Guidance (5.0-10.0):**
- General purpose (DEFAULT: 7.5)
- Balanced results
- Most prompts work well

```python
image = client.image.generate(
    "a sunset over the ocean",
    guidance_scale=7.5  # Balanced
)
```

**High Guidance (10.0-20.0):**
- Precise requirements
- Technical drawings
- Specific compositions
- Logo/design work

```python
image = client.image.generate(
    "a minimalist logo with blue circle and white text saying 'AI'",
    guidance_scale=15.0  # Follow exactly
)
```

---

## 🚫 Negative Prompts

Specify what you DON'T want in the generated image.

### Basic Usage

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

image = client.image.generate(
    prompt="a beautiful portrait of a woman",
    negative_prompt="ugly, distorted, blurry, low quality, extra limbs"
)

client.close_sync()
```

### Common Negative Prompts

**For Quality:**
```python
negative_prompt="blurry, low quality, pixelated, jpeg artifacts, worst quality"
```

**For Portraits:**
```python
negative_prompt="distorted face, extra limbs, deformed, ugly, bad anatomy"
```

**For Realism:**
```python
negative_prompt="cartoon, anime, illustration, drawing, painting, unrealistic"
```

**For Professional Use:**
```python
negative_prompt="watermark, text, logo, signature, username, blurry"
```

### Combined Example

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Professional portrait with multiple exclusions
image = client.image.generate(
    prompt="professional headshot of a business person, studio lighting",
    negative_prompt=(
        "blurry, low quality, "
        "distorted face, extra limbs, "
        "watermark, text, logo, "
        "cartoon, illustration"
    ),
    quality="hd",
    guidance_scale=8.0
)

with open("professional_headshot.png", "wb") as f:
    f.write(image)

client.close_sync()
```

---

## 🌈 Transparent Backgrounds

Generate PNG images with alpha transparency.

### Basic Transparent Generation

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Generate with transparent background
image = client.image.generate(
    prompt="a red apple, isolated object",
    transparent=True  # Enable transparency
)

# Save as PNG (transparency preserved)
with open("apple_transparent.png", "wb") as f:
    f.write(image)

client.close_sync()
```

### Use Cases for Transparency

**1. Product Images:**
```python
image = client.image.generate(
    prompt="a sleek smartphone, product photo, isolated object",
    transparent=True,
    negative_prompt="background, table, surface",
    quality="hd"
)
```

**2. Logos and Icons:**
```python
image = client.image.generate(
    prompt="minimalist AI icon, geometric, simple",
    transparent=True,
    width=512,
    height=512
)
```

**3. Game Assets:**
```python
image = client.image.generate(
    prompt="fantasy sword, detailed, isolated weapon",
    transparent=True,
    quality="high"
)
```

**4. Stickers and Overlays:**
```python
image = client.image.generate(
    prompt="cute cartoon cat face, sticker style",
    transparent=True,
    negative_prompt="background, border"
)
```

### Tips for Better Transparency

```python
# ✅ DO: Be explicit about isolation
image = client.image.generate(
    prompt="a crown, isolated object, no background",
    transparent=True,
    negative_prompt="background, floor, wall, table, surface"
)

# ✅ DO: Use simple, clear subjects
image = client.image.generate(
    prompt="single red rose",
    transparent=True
)

# ❌ DON'T: Use complex scenes
# (Transparency works best with isolated objects)
```

---

## 🖼️ Image-to-Image

Transform existing images with text prompts.

### Basic Image-to-Image

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Transform an existing image
image = client.image.generate(
    prompt="turn this into a watercolor painting",
    image="https://example.com/photo.jpg",  # Source image URL
    guidance_scale=7.5
)

with open("watercolor_version.png", "wb") as f:
    f.write(image)

client.close_sync()
```

### Use Cases

**1. Style Transfer:**
```python
image = client.image.generate(
    prompt="convert to anime style, vibrant colors",
    image="https://example.com/portrait.jpg"
)
```

**2. Enhancement:**
```python
image = client.image.generate(
    prompt="enhance quality, professional photography, 4k",
    image="https://example.com/low_res.jpg",
    quality="hd"
)
```

**3. Variation Generation:**
```python
image = client.image.generate(
    prompt="same composition but at sunset",
    image="https://example.com/landscape.jpg"
)
```

**4. Object Replacement:**
```python
image = client.image.generate(
    prompt="replace the car with a bicycle",
    image="https://example.com/street_scene.jpg"
)
```

---

## 💡 Advanced Examples

### Example 1: Professional Product Photo

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

product_image = client.image.generate(
    prompt=(
        "professional product photography, "
        "luxury watch on white marble, "
        "studio lighting, 4k, ultra detailed"
    ),
    negative_prompt=(
        "blurry, low quality, amateur, "
        "bad lighting, shadows, "
        "text, watermark, logo"
    ),
    quality="hd",
    guidance_scale=10.0,
    width=1024,
    height=1024,
    seed=42
)

with open("product_watch.png", "wb") as f:
    f.write(product_image)

client.close_sync()
```

### Example 2: Character Concept Art

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

character = client.image.generate(
    prompt=(
        "fantasy warrior character, "
        "full body, detailed armor, "
        "heroic pose, concept art style, "
        "professional illustration"
    ),
    negative_prompt=(
        "blurry, low quality, realistic photo, "
        "distorted, extra limbs, deformed, "
        "ugly, bad anatomy"
    ),
    quality="high",
    guidance_scale=8.5,
    width=768,
    height=1024
)

with open("character_design.png", "wb") as f:
    f.write(character)

client.close_sync()
```

### Example 3: Logo with Transparency

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

logo = client.image.generate(
    prompt=(
        "minimalist tech startup logo, "
        "abstract geometric shape, "
        "blue and white colors, "
        "modern, clean, simple"
    ),
    negative_prompt=(
        "complex, detailed, realistic, "
        "text, letters, words, "
        "background"
    ),
    transparent=True,
    quality="hd",
    guidance_scale=12.0,
    width=512,
    height=512
)

with open("startup_logo.png", "wb") as f:
    f.write(logo)

client.close_sync()
```

### Example 4: Batch Generation with Variations

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

base_prompt = "a cozy coffee shop interior"
variations = [
    ("morning", "morning sunlight, bright, airy"),
    ("evening", "warm evening lighting, cozy atmosphere"),
    ("night", "moody night ambiance, dim lights")
]

for name, modifier in variations:
    image = client.image.generate(
        prompt=f"{base_prompt}, {modifier}",
        negative_prompt="blurry, low quality, people, faces",
        quality="high",
        guidance_scale=7.5,
        seed=42  # Same base seed for consistency
    )
    
    with open(f"coffee_shop_{name}.png", "wb") as f:
        f.write(image)
    
    print(f"Generated: coffee_shop_{name}.png")

client.close_sync()
```

---

## ✅ Best Practices

### 1. Prompt Engineering

**✅ DO:**
```python
# Be specific and descriptive
prompt = "professional headshot, studio lighting, neutral background, sharp focus"

# Use style keywords
prompt = "oil painting style, impressionism, Van Gogh inspired"

# Include quality markers
prompt = "4k, ultra detailed, high resolution, professional photography"
```

**❌ DON'T:**
```python
# Too vague
prompt = "a picture"

# Contradictory
prompt = "realistic photo in anime style"  # Pick one!
```

### 2. Quality Settings

**For Web/Social Media:**
```python
image = client.image.generate(
    prompt,
    quality="medium",  # Fast, good enough
    width=1024,
    height=1024
)
```

**For Print/Professional:**
```python
image = client.image.generate(
    prompt,
    quality="hd",  # Best quality
    width=2048,
    height=2048,
    guidance_scale=8.0
)
```

### 3. Negative Prompts

Always include quality exclusions:
```python
negative_prompt = "blurry, low quality, worst quality, jpeg artifacts"
```

### 4. Guidance Scale Guidelines

```python
# Creative/Artistic: 3.0-6.0
image = client.image.generate(prompt, guidance_scale=4.0)

# Balanced/General: 6.0-9.0
image = client.image.generate(prompt, guidance_scale=7.5)

# Precise/Technical: 9.0-15.0
image = client.image.generate(prompt, guidance_scale=12.0)
```

### 5. Seed for Consistency

```python
# Use same seed for similar results
FIXED_SEED = 42

image1 = client.image.generate("sunset", seed=FIXED_SEED)
image2 = client.image.generate("sunset", seed=FIXED_SEED)
# Similar but not identical
```

### 6. Error Handling

```python
from blossom_ai import Blossom, BlossomError, RateLimitError

client = Blossom(api_version="v2", api_token="token")

try:
    image = client.image.generate(
        prompt="test",
        quality="hd",
        timeout=60  # Increase for HD
    )
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except BlossomError as e:
    print(f"Error: {e.message}")
finally:
    client.close_sync()
```

---

## 🔗 Related Documentation

- **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)** - Migrate from V1 to V2
- **[V2 Text Generation](V2_TEXT_GENERATION.md)** - Advanced text features
- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API docs
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors properly

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>