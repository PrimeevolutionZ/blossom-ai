# Examples

Practical examples from the original documentation.

---

## Image Generation Examples

### Generate and Save Image

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Generate and save an image
    ai.image.save(
        prompt="a majestic dragon in a mystical forest",
        filename="dragon.jpg",
        width=1024,
        height=1024,
        model="flux"
    )

    # Get image data as bytes
    image_data = ai.image.generate("a cute robot")

    # Use different models
    image_data = ai.image.generate("futuristic city", model="turbo")

    # Reproducible results with seed
    image_data = ai.image.generate("random art", seed=42)

    # List available models (dynamically fetched from API)
    models = ai.image.models()
    print(models)  # ['flux', 'kontext', 'turbo', 'gptimage', ...]
```

### Image URL Generation

```python
from blossom_ai import Blossom

client = Blossom()

# Get image URL instantly
url = client.image.generate_url("a beautiful sunset")
print(url)
# Output: https://image.pollinations.ai/prompt/a%20beautiful%20sunset?model=flux&width=1024&height=1024
```

### With Custom Parameters

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
            client.image.generate_url(prompt, seed=i)
            for i, prompt in enumerate(prompts)
        ])
    
    return dict(zip(prompts, urls))

# Run it
results = asyncio.run(generate_gallery())
for prompt, url in results.items():
    print(f"{prompt}: {url}")
```

### HTML Gallery Generator

```python
from blossom_ai import Blossom

def create_gallery(prompts):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Image Gallery</title>
        <style>
            .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            img { width: 100%; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>AI Generated Gallery</h1>
        <div class="gallery">
    """
    
    # Use context manager
    with Blossom() as client:
        for prompt in prompts:
            url = client.image.generate_url(prompt, nologo=True)
            html += f"""
                <div>
                    <img src="{url}" alt="{prompt}">
                    <p>{prompt}</p>
                </div>
            """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    with open('gallery.html', 'w') as f:
        f.write(html)

# Create gallery
prompts = ["sunset", "mountains", "ocean", "forest", "city", "space"]
create_gallery(prompts)
```

### Comparing URL vs Download

```python
import time
from blossom_ai import Blossom

with Blossom() as client:
    # Method 1: URL generation (instant)
    start = time.time()
    url = client.image.generate_url("a cat", seed=42)
    url_time = time.time() - start
    print(f"URL generation: {url_time:.3f}s")

    # Method 2: Download bytes (slower)
    start = time.time()
    image_bytes = client.image.generate("a cat", seed=42)
    download_time = time.time() - start
    print(f"Download: {download_time:.3f}s ({len(image_bytes)} bytes)")

    print(f"Speed improvement: {download_time / url_time:.1f}x faster!")
    # Typical output: 20-50x faster!
```

---

## Text Generation Examples

### Simple Text Generation

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Simple text generation
    response = ai.text.generate("What is Python?")

    # With system message
    response = ai.text.generate(
        prompt="Write a haiku about coding",
        system="You are a creative poet"
    )

    # Reproducible results with seed
    response = ai.text.generate(
        prompt="Generate a random idea",
        seed=42  # Same seed = same result
    )

    # JSON mode
    response = ai.text.generate(
        prompt="List 3 colors in JSON format",
        json_mode=True
    )

    # List available models (dynamically updated)
    models = ai.text.models()
    print(models)  # ['deepseek', 'gemini', 'mistral', 'openai', 'qwen-coder', ...]
```

### Streaming

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Streaming (with automatic timeout protection)
    for chunk in ai.text.generate("Tell a story", stream=True):
        print(chunk, end='', flush=True)
```

### Chat with Message History

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Chat with message history
    response = ai.text.chat([
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What's the weather like?"}
    ])

    # Chat with streaming
    messages = [{"role": "user", "content": "Explain AI"}]
    for chunk in ai.text.chat(messages, stream=True):
        print(chunk, end='', flush=True)
```

### Asynchronous Streaming

```python
import asyncio
from blossom_ai import Blossom

async def stream_example():
    # Use async context manager
    async with Blossom() as ai:
        # Async streaming with timeout protection
        async for chunk in await ai.text.generate("Tell me a story", stream=True):
            print(chunk, end='', flush=True)
        
        # Async chat streaming
        messages = [{"role": "user", "content": "Hello!"}]
        async for chunk in await ai.text.chat(messages, stream=True):
            print(chunk, end='', flush=True)

asyncio.run(stream_example())
```

---

## Audio Generation Examples

### Generate and Save Audio

```python
from blossom_ai import Blossom

# Audio generation requires an API token
with Blossom(api_token="YOUR_API_TOKEN") as ai:
    # Generate and save audio
    ai.audio.save(
        text="Welcome to the future of AI",
        filename="welcome.mp3",
        voice="nova"
    )

    # Try different voices
    ai.audio.save("Hello", "hello_alloy.mp3", voice="alloy")
    ai.audio.save("Hello", "hello_echo.mp3", voice="echo")

    # Get audio data as bytes
    audio_data = ai.audio.generate("Hello world", voice="shimmer")

    # List available voices (dynamically updated)
    voices = ai.audio.voices()
    print(voices)  # ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', ...]
```

---

## Discord Bot Example

```python
import discord
from blossom_ai import Blossom

bot = discord.Client()

@bot.event
async def on_message(message):
    if message.content.startswith('!imagine'):
        prompt = message.content[8:].strip()
        
        # Use context manager for proper cleanup
        async with Blossom() as client:
            # Generate URL instantly - no download needed!
            url = await client.image.generate_url(
                prompt,
                nologo=True,
                private=True
            )
        
        # Discord will automatically show image preview
        await message.channel.send(url)

bot.run('YOUR_DISCORD_TOKEN')
```

---

## Telegram Bot Example

```python
from telegram import Update
from telegram.ext import Application, CommandHandler
from blossom_ai import Blossom

async def imagine(update: Update, context):
    prompt = ' '.join(context.args)
    
    # Use context manager for proper resource handling
    async with Blossom() as client:
        # Generate URL - fast and efficient
        url = await client.image.generate_url(prompt, nologo=True)
    
    # Send image directly from URL
    await update.message.reply_photo(photo=url)

app = Application.builder().token("YOUR_TELEGRAM_TOKEN").build()
app.add_handler(CommandHandler("imagine", imagine))
app.run_polling()
```

---

## Web Application Example

```python
from flask import Flask, render_template, request
from blossom_ai import Blossom

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    
    # Sync context manager for Flask
    with Blossom() as client:
        # Generate URL for web embedding
        url = client.image.generate_url(
            prompt,
            width=512,
            height=512,
            nologo=True
        )
    
    return render_template('result.html', image_url=url)

# In result.html:
# <img src="{{ image_url }}" alt="Generated Image">
```

---

## Unified Sync/Async API

```python
from blossom_ai import Blossom

# Synchronous usage
with Blossom() as ai:
    url = ai.image.generate_url("a cute robot")
    image_data = ai.image.generate("a cute robot")
    text = ai.text.generate("Hello world")

# Asynchronous usage - same methods!
import asyncio

async def main():
    async with Blossom() as ai:
        url = await ai.image.generate_url("a cute robot")
        image_data = await ai.image.generate("a cute robot")
        text = await ai.text.generate("Hello world")
    
asyncio.run(main())
```

---

## Error Handling Example

```python
from blossom_ai import (
    Blossom, 
    BlossomError,
    NetworkError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    StreamError
)

try:
    with Blossom() as ai:
        response = ai.text.generate("Hello")
        
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    # Output: Visit https://auth.pollinations.ai to get an API token
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    print(f"Context: {e.context}")
    
except NetworkError as e:
    print(f"Connection issue: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except RateLimitError as e:
    print(f"Too many requests: {e.message}")
    if e.retry_after:
        print(f"Retry after: {e.retry_after} seconds")
    
except StreamError as e:
    print(f"Stream error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    # Example: "Stream timeout: no data for 30s"
    
except APIError as e:
    print(f"API error: {e.message}")
    if e.context:
        print(f"Status: {e.context.status_code}")
        print(f"Request ID: {e.context.request_id}")
    
except BlossomError as e:
    # Catch-all for any Blossom error
    print(f"Error type: {e.error_type}")
    print(f"Message: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    if e.context and e.context.request_id:
        print(f"Request ID: {e.context.request_id}")
    if e.original_error:
        print(f"Original error: {e.original_error}")
```

---

## Custom Timeout

```python
# Set custom timeout for slow connections
with Blossom(timeout=60) as ai:  # 60 seconds
    response = ai.text.generate("Long query...")
```

---

## Debug Mode

```python
# Enable debug mode for detailed logging (includes request IDs)
with Blossom(debug=True) as ai:
    response = ai.text.generate("Hello")
```

---

## Handling Rate Limits

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom() as ai:
    try:
        response = ai.text.generate("Hello")
    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
        if e.retry_after:
            print(f"Waiting {e.retry_after} seconds...")
            time.sleep(e.retry_after)
            # Retry request
            response = ai.text.generate("Hello")
```