# Image Generation Guide

Blossom AI provides powerful and fast image generation capabilities, including a unique `generate_url()` method for instant access to image URLs without downloading the bytes.

## 🖼️ Image Generation

### Generating and Saving an Image

Use the `save()` method to generate an image based on a prompt and save it directly to a file.

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Generate and save an image
    ai.image.save("a beautiful sunset over mountains", "sunset.jpg")
```

### Generating Image Bytes

Use the `generate()` method to get the raw image data (bytes) directly.

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Generate image bytes
    image_bytes = ai.image.generate("a beautiful sunset over mountains")
    # Process image_bytes (e.g., upload to a server, display in memory)
```

## 🔗 Image URL Generation

The `generate_url()` method provides instant access to image URLs without downloading, which is ideal for web applications and bots.

### Basic Usage

```python
from blossom_ai import Blossom

client = Blossom()

# Get image URL instantly
url = client.image.generate_url("a beautiful sunset")
print(url)
# Output: https://image.pollinations.ai/prompt/a%20beautiful%20sunset?model=flux&width=1024&height=1024
```

### With Custom Parameters

You can pass various parameters to control the generation process, such as model, dimensions, and seed.

```python
# Full control over generation
url = client.image.generate_url(
    prompt="cyberpunk city at night",
    model="flux",
    width=1920,
    height=1080,
    seed=42,           # Reproducible results
    nologo=True,       # Remove watermark
    private=True,      # Private generation
    enhance=True,      # AI prompt enhancement
    safe=True          # NSFW filter
)

# URLs are always safe to share - no tokens included!
print(url)  # https://image.pollinations.ai/prompt/...
```

### Parallel URL Generation

The `generate_url()` method is extremely fast and can be used in parallel for gallery generation.

```python
import asyncio
from blossom_ai import Blossom

async def generate_gallery():
    prompts = [
        "a red sunset",
        "a blue ocean",
        "a green forest",
        "a purple galaxy"
    ]

    # Use context manager
    async with Blossom() as client:
        # Generate all URLs in parallel - super fast!
        urls = await asyncio.gather(*[
            client.image.generate_url(p)
            for p in prompts
        ])
        
    for url in urls:
        print(url)

# asyncio.run(generate_gallery())
```
