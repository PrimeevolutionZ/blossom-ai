# 🌸 Blossom AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.6-blue.svg)](https://pypi.org/project/eclips-blossom-ai/)

**A beautiful Python SDK for Pollinations.AI - Generate images, text, and audio with AI.**

Blossom AI is a comprehensive, easy-to-use Python library that provides unified access to Pollinations.AI's powerful AI generation services. Create stunning images, generate text with various models, and convert text to speech with multiple voices - all through a beautifully designed, intuitive API.

## ✨ What's New in v0.2.6

### 🧹 Enhanced Resource Management

- **🔧 Fixed Session Cleanup**: No more `ResourceWarning` about unclosed sessions
- **♻️ Automatic Cleanup**: Sessions properly closed at program exit via `atexit`
- **🎯 Better Context Managers**: Improved `async with` support for proper resource handling
- **🔒 Thread-Safe**: Safe cleanup even in complex async scenarios
- **📊 Global Session Registry**: Centralized tracking of all active sessions

### 🔗 URL Generation Support (v0.2.5)

- **🌐 `generate_url()` Method**: Get direct image URLs without downloading bytes
- **⚡ Lightning Fast**: No network overhead - instant URL generation
- **🤖 Bot-Friendly**: Perfect for Discord, Telegram, and web integrations
- **💾 Traffic Efficient**: Save bandwidth by sharing URLs instead of bytes
- **🔒 Secure**: Tokens are never included in URLs - always safe to share

## 📦 Installation

```bash
pip install eclips-blossom-ai
```

## 🚀 Quick Start

```python
from blossom_ai import Blossom

# Initialize
ai = Blossom()

# Generate an image URL (Fast & Free!)
url = ai.image.generate_url("a beautiful sunset over mountains")
print(url)  # https://image.pollinations.ai/prompt/...

# Generate and save an image
ai.image.save("a beautiful sunset over mountains", "sunset.jpg")

# Generate text
response = ai.text.generate("Explain quantum computing in simple terms")
print(response)

# Stream text in real-time (with automatic timeout protection)
for chunk in ai.text.generate("Tell me a story", stream=True):
    print(chunk, end='', flush=True)

# Generate audio (requires API token)
ai = Blossom(api_token="YOUR_TOKEN")
ai.audio.save("Hello, welcome to Blossom AI!", "welcome.mp3", voice="nova")
```

## 🧹 Resource Management

Blossom AI automatically manages resources, but for best practices use context managers:

### ✅ Recommended: Use Context Managers

```python
# Synchronous - automatic cleanup
with Blossom() as ai:
    url = ai.image.generate_url("sunset")
    image = ai.image.generate("sunset")
    # Resources automatically cleaned up on exit

# Asynchronous - automatic cleanup
async with Blossom() as ai:
    url = await ai.image.generate_url("sunset")
    image = await ai.image.generate("sunset")
    # Async resources properly closed
```

### Manual Cleanup (if needed)

```python
# Async manual cleanup
client = Blossom()
try:
    url = await client.image.generate_url("test")
finally:
    await client.close()  # Explicitly close async sessions

# Sync - no manual cleanup needed (auto-closes on exit)
client = Blossom()
url = client.image.generate_url("test")
# Sync sessions cleaned up automatically
```

### For Long-Running Applications

```python
import asyncio
from blossom_ai import Blossom

async def bot_command(prompt: str):
    """Single command handler - use context manager"""
    async with Blossom() as ai:
        return await ai.image.generate_url(prompt)

# ✅ Good: One event loop for all operations
async def main():
    results = []
    for prompt in ["cat", "dog", "bird"]:
        result = await bot_command(prompt)
        results.append(result)

asyncio.run(main())  # Single event loop

# ❌ Avoid: Multiple asyncio.run() calls
# This creates/destroys event loops repeatedly, leaving resources
def bad_example():
    asyncio.run(bot_command("cat"))   # Creates loop #1
    asyncio.run(bot_command("dog"))   # Creates loop #2 - may leave resources
    asyncio.run(bot_command("bird"))  # Creates loop #3 - may leave resources
```

### Testing Best Practices

```python
import asyncio
from blossom_ai import Blossom

# ✅ Recommended: Single async main function
async def test_all():
    """Run all async tests in one event loop"""
    
    # Test 1
    async with Blossom() as ai:
        url1 = await ai.image.generate_url("test1")
        print(f"Test 1: {url1}")
    
    # Test 2
    async with Blossom() as ai:
        url2 = await ai.image.generate_url("test2")
        print(f"Test 2: {url2}")
    
    # Test 3 - parallel generation
    async with Blossom() as ai:
        urls = await asyncio.gather(*[
            ai.image.generate_url(f"test{i}")
            for i in range(5)
        ])
        print(f"Parallel: {len(urls)} URLs generated")

# Run all tests in one go
if __name__ == "__main__":
    print("=== Sync Tests ===")
    with Blossom() as ai:
        url = ai.image.generate_url("sync test")
        print(f"Sync: {url}")
    
    print("\n=== Async Tests ===")
    asyncio.run(test_all())  # One asyncio.run() for all async tests
```

## ⚠️ Important Notes

- **Resource Management**: Always use context managers (`with`/`async with`) for proper cleanup
- **Event Loops**: Avoid multiple `asyncio.run()` calls - use one event loop per application run
- **Audio Generation**: Requires authentication (API token)
- **Hybrid API**: Automatically detects sync/async context - no need for separate imports
- **Streaming**: Works in both sync and async contexts with iterators
- **Stream Timeout**: Default 30 seconds between chunks - automatically raises error if no data
- **Robust Error Handling**: Graceful fallbacks when API endpoints are unavailable

## ✨ Features

- 🖼️ **Image Generation** - Create stunning images from text descriptions
- 🔗 **Image URL Generation** - Get direct links without downloading (v0.2.5!)
- 📝 **Text Generation** - Generate text with various AI models
- 🌊 **Streaming** - Real-time text generation with timeout protection
- 🎙️ **Audio Generation** - Text-to-speech with multiple voices
- 🚀 **Unified API** - Same code works in sync and async contexts
- 🎨 **Beautiful Errors** - Helpful error messages with actionable suggestions
- 🔄 **Reproducible** - Use seeds for consistent results
- ⚡ **Smart Async** - Automatically switches between sync/async modes
- 🛡️ **Robust** - Graceful error handling with fallbacks and timeout protection
- 🧹 **Clean** - Proper resource management and automatic cleanup
- 🔍 **Traceable** - Request IDs for debugging

## 🔗 Image URL Generation

The `generate_url()` method provides instant access to image URLs without downloading:

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

### Discord Bot Example

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

### Telegram Bot Example

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

### Web Application Example

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

### When to Use URL vs Download

**Use `generate_url()` when:**
- ✅ Sharing images in chat apps (Discord, Telegram, Slack)
- ✅ Embedding in web pages
- ✅ Creating image galleries
- ✅ Mobile apps (reduce data usage)
- ✅ You need instant results
- ✅ Generating many images quickly

**Use `generate()` when:**
- ✅ You need the actual image file
- ✅ Processing/editing the image locally
- ✅ Storing images in your own system
- ✅ Working offline after generation
- ✅ Need pixel-level access

## 🌊 Streaming Support

Get responses in real-time as they're generated, with built-in timeout protection:

### Synchronous Streaming

```python
from blossom_ai import Blossom

# Use context manager
with Blossom() as ai:
    # Simple streaming with automatic timeout protection
    for chunk in ai.text.generate("Write a poem about AI", stream=True):
        print(chunk, end='', flush=True)

    # Chat streaming
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain Python"}
    ]
    for chunk in ai.text.chat(messages, stream=True):
        print(chunk, end='', flush=True)

    # Collect full response from stream
    chunks = []
    for chunk in ai.text.generate("Hello", stream=True):
        chunks.append(chunk)
    full_response = ''.join(chunks)
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

## 🔄 Unified Sync/Async API

The same API works seamlessly in both synchronous and asynchronous contexts:

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

**No need for separate imports or different APIs** - Blossom automatically detects your context and does the right thing!

## 📖 Examples

### Image Generation

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # NEW: Get URL without downloading
    url = ai.image.generate_url(
        prompt="a majestic dragon in a mystical forest",
        width=1024,
        height=1024,
        model="flux",
        seed=42
    )
    print(f"Image URL: {url}")

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

### Text Generation

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

    # Streaming (with automatic timeout protection)
    for chunk in ai.text.generate("Tell a story", stream=True):
        print(chunk, end='', flush=True)

    # Chat with message history
    response = ai.text.chat([
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What's the weather like?"}
    ])

    # Chat with streaming
    messages = [{"role": "user", "content": "Explain AI"}]
    for chunk in ai.text.chat(messages, stream=True):
        print(chunk, end='', flush=True)

    # List available models (dynamically updated)
    models = ai.text.models()
    print(models)  # ['deepseek', 'gemini', 'mistral', 'openai', 'qwen-coder', ...]
```

### Audio Generation

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

## 🎯 Supported Parameters

### Image Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | str | - | Image description (required) |
| model | str | "flux" | Model to use |
| width | int | 1024 | Image width in pixels |
| height | int | 1024 | Image height in pixels |
| seed | int | None | Seed for reproducibility |
| nologo | bool | False | Remove watermark (requires token) |
| private | bool | False | Keep image private |
| enhance | bool | False | Enhance prompt with AI |
| safe | bool | False | Enable NSFW filtering |
| referrer | str | None | Optional referrer parameter |

### Image URL Generation

Same parameters as Image Generation, but returns URL string instead of bytes.

```python
url = ai.image.generate_url(
    prompt="your prompt",
    model="flux",
    width=1024,
    height=1024,
    seed=42,
    nologo=True,
    private=True,
    enhance=False,
    safe=False,
    referrer="my-app"  # Optional
)
```

### Text Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | str | - | Text prompt (required) |
| model | str | "openai" | Model to use |
| system | str | None | System message |
| seed | int | None | Seed for reproducibility |
| temperature | float | None | ⚠️ Not supported in current API |
| json_mode | bool | False | Force JSON output |
| private | bool | False | Keep response private |
| stream | bool | False | Stream response in real-time |

### Text Chat

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| messages | list | - | Chat message history (required) |
| model | str | "openai" | Model to use |
| temperature | float | 1.0 | Fixed at 1.0 (API limitation) |
| stream | bool | False | Stream response in real-time |
| json_mode | bool | False | Force JSON output |
| private | bool | False | Keep response private |

### Audio Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| text | str | - | Text to speak (required) |
| voice | str | "alloy" | Voice to use |
| model | str | "openai-audio" | TTS model |

## 🛠️ API Reference

### Blossom Class

```python
ai = Blossom(
    timeout=30,           # Request timeout in seconds
    debug=False,          # Enable debug mode
    api_token=None        # Optional API token for auth
)

# Generators (work in sync and async)
ai.image   # Image generation
ai.text    # Text generation (with streaming!)
ai.audio   # Audio generation (requires token)
```

### Context Manager Support

```python
# Synchronous context manager (recommended)
with Blossom() as ai:
    result = ai.text.generate("Hello")
    # Resources automatically cleaned up

# Asynchronous context manager (recommended)
async with Blossom() as ai:
    result = await ai.text.generate("Hello")
    # Resources automatically cleaned up
```

### Image Generator Methods

```python
# Generate image URL (returns str)
url = ai.image.generate_url(prompt, **options)

# Generate image (returns bytes)
image_data = ai.image.generate(prompt, **options)

# Save image to file (returns filepath)
filepath = ai.image.save(prompt, filename, **options)

# List available models
models = ai.image.models()  # Returns list of model names
```

### Text Generator Methods

```python
# Generate text (returns str or Iterator[str] if stream=True)
text = ai.text.generate(prompt, **options)

# Generate with streaming (automatic timeout protection)
for chunk in ai.text.generate(prompt, stream=True):
    print(chunk, end='')

# Chat with message history (returns str or Iterator[str] if stream=True)
text = ai.text.chat(messages, **options)

# Chat with streaming
for chunk in ai.text.chat(messages, stream=True):
    print(chunk, end='')

# List available models
models = ai.text.models()  # Returns list of model names
```

### Audio Generator Methods

```python
# Generate audio (returns bytes)
audio_data = ai.audio.generate(text, voice="alloy")

# Save audio to file (returns filepath)
filepath = ai.audio.save(text, filename, voice="nova")

# List available voices
voices = ai.audio.voices()  # Returns list of voice names
```

## 🎨 Error Handling

Blossom AI provides structured, informative errors with actionable suggestions:

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

### Error Types

- **NetworkError** - Connection issues, timeouts
- **APIError** - HTTP errors from API (4xx, 5xx)
- **AuthenticationError** - Invalid or missing API token (401)
- **ValidationError** - Invalid parameters
- **RateLimitError** - Too many requests (429) with `retry_after` info
- **StreamError** - Streaming-specific errors (timeouts, interruptions)
- **BlossomError** - Base error class for all errors

## 🔐 Authentication

For higher rate limits and advanced features, get an API token:

```python
from blossom_ai import Blossom

# With authentication
with Blossom(api_token="YOUR_API_TOKEN") as ai:
    # Use token for downloading images with premium features
    image_bytes = ai.image.generate("sunset", nologo=True)  # Token used here
    ai.image.save("sunset", "sunset.jpg", nologo=True)      # Token used here
    ai.audio.save("Hello", "hello.mp3")                     # Token required

    # Generate URLs (always safe - no token in URL)
    url = ai.image.generate_url("sunset", nologo=True)
    print(url)  # https://image.pollinations.ai/...&nologo=true
    # ✅ Safe to share - no token exposed!
```

**When to use token:**
- ✅ `generate()` - Download images with authentication
- ✅ `save()` - Save images with authentication
- ✅ `audio.generate()` - Audio requires token
- ❌ `generate_url()` - URLs never include tokens (always safe)

Get your API token at [auth.pollinations.ai](https://auth.pollinations.ai)

## 🔒 Security Considerations

### URL Generation Security

`generate_url()` is designed to be **always secure**:

```python
with Blossom(api_token="YOUR_SECRET_TOKEN") as ai:
    # ✅ URLs NEVER contain your token
    url = ai.image.generate_url("landscape")
    # Safe to share publicly - token not exposed

    # The URL works for everyone, no authentication needed
    print(url)  # https://image.pollinations.ai/prompt/landscape?model=flux&...
```

### When You Need Authentication

Use `generate()` or `save()` for authenticated features:

```python
with Blossom(api_token="YOUR_TOKEN") as ai:
    # ✅ Token used securely (not exposed in URLs)
    image_bytes = ai.image.generate("cat", nologo=True)
    # Token sent in request headers, never in public URLs

    # Save to file with authentication
    ai.image.save("cat", "cat.jpg", nologo=True)
    # Token used internally, file saved locally
```

### Best Practices

**For Public Bots (Discord, Telegram):**
```python
# Option 1: Share URL (fast, no token exposure)
async with Blossom() as ai:
    url = await ai.image.generate_url(prompt)
    await ctx.send(url)

# Option 2: Download and upload (with auth features)
async with Blossom(api_token="TOKEN") as ai:
    image = await ai.image.generate(prompt, nologo=True)
    await ctx.send(file=discord.File(io.BytesIO(image), 'image.png'))
```

**For Web Applications:**
```python
# ✅ Safe: URL in HTML (no token)
with Blossom() as ai:
    url = ai.image.generate_url(prompt)
    return f'<img src="{url}">'

# ✅ Safe: Download server-side (token not exposed)
with Blossom(api_token="TOKEN") as ai:
    image = ai.image.generate(prompt, nologo=True)
    # Process/store image server-side
```

## 🔄 Async Usage

The same API works in async contexts automatically:

```python
import asyncio
from blossom_ai import Blossom

async def generate_content():
    # Use async context manager for proper cleanup
    async with Blossom() as ai:
        # All methods work with await
        url = await ai.image.generate_url("landscape")
        image = await ai.image.generate("landscape")
        text = await ai.text.generate("story")
        audio = await ai.audio.generate("speech")
        
        # Streaming with async (with timeout protection)
        async for chunk in await ai.text.generate("poem", stream=True):
            print(chunk, end='')
        
        return url, image, text, audio

# Run async function
asyncio.run(generate_content())
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_examples.py

# Run only sync tests
python test_examples.py --sync

# Run only async tests
python test_examples.py --async

# Run only streaming tests
python test_examples.py --streaming

# With API token
python test_examples.py --token YOUR_TOKEN
```

## 🛡️ Robustness Features

Blossom AI includes several robustness features:

### Retry Logic
- Automatic retry with exponential backoff for failed requests
- Configurable retry attempts (default: 3)
- Smart retry only for retryable errors (502, timeouts)
- Respects `Retry-After` header for rate limits

### Streaming Protection 
- Automatic timeout detection: 30 seconds between chunks by default
- Graceful error handling: Clear messages when streams timeout
- Resource cleanup: Guaranteed cleanup even if stream is interrupted
- Request tracing: Every stream has a unique request ID

### Resource Management
- Centralized session management with `SessionManager`
- Proper cleanup with context managers (`with`/`async with`)
- Global session registry for tracking all active sessions
- `atexit` cleanup to ensure no resources are left open
- Thread-safe async session handling across event loops
- Optimized connection pool settings

### Error Recovery
- Graceful fallbacks when API endpoints are unavailable
- Dynamic model discovery with fallback to defaults
- Continues operation even when some endpoints fail
- Enhanced error messages with request IDs and retry information

### Dynamic Models
- Models automatically update from API responses
- Fallback to sensible defaults if API unavailable
- Type-safe model validation with helpful error messages

## 📚 Advanced Usage

### Custom Timeout

```python
# Set custom timeout for slow connections
with Blossom(timeout=60) as ai:  # 60 seconds
    response = ai.text.generate("Long query...")
```

### Debug Mode

```python
# Enable debug mode for detailed logging (includes request IDs)
with Blossom(debug=True) as ai:
    response = ai.text.generate("Hello")
```

### Handling Rate Limits

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

## 🗝️ Architecture

### Key Components:
- **Base Generators** - `SyncGenerator` and `AsyncGenerator` base classes with timeout protection
- **Session Managers** - Centralized session lifecycle management with connection pooling
- **Global Session Registry** - Class-level tracking of all sessions for proper cleanup
- **atexit Cleanup** - Automatic cleanup at program exit to prevent resource warnings
- **Dynamic Models** - Models that update from API at runtime
- **Hybrid Generators** - Automatic sync/async detection
- **URL Generation** - Instant URL creation without network requests
- **Streaming Support** - SSE parsing with Iterator/AsyncIterator and timeout protection
- **Structured Errors** - Rich error context with suggestions and request IDs
- **Request Tracing** - Unique IDs for debugging and error correlation

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- **Temperature parameter**: The GET text endpoint doesn't support temperature parameter
- **Chat temperature**: Fixed at 1.0 in OpenAI-compatible endpoint
- **API Variability**: Some endpoints may occasionally return unexpected formats - handled gracefully with fallbacks

## 📋 Changelog

### v0.2.6 (Current)
- 🧹 **Fixed Session Cleanup**: Resolved `ResourceWarning` about unclosed aiohttp sessions
- ♻️ **Automatic Resource Management**: Sessions now properly closed at program exit via `atexit`
- 🔒 **Thread-Safe Cleanup**: Improved cleanup in complex async scenarios
- 📊 **Global Session Registry**: Centralized tracking of all active sessions
- 🎯 **Better Context Managers**: Enhanced `async with` support for proper resource handling
- 📖 **Documentation**: Added comprehensive resource management guide and best practices

### v0.2.5
- 🔗 **URL Generation**: New `generate_url()` method for instant image URLs without downloading
- ⚡ **Performance**: URL generation is 20-50x faster than downloading bytes
- 🤖 **Bot-Friendly**: Perfect for Discord, Telegram, and web integrations
- 💾 **Bandwidth Efficient**: Share URLs instead of transferring bytes
- 🔒 **Always Secure**: Tokens never included in URLs - completely safe to share publicly
- 📚 **Documentation**: Comprehensive examples for bots and web apps

## 🔗 Links

- [Pollinations.AI](https://pollinations.ai)
- [API Documentation](https://pollinations.ai/api)
- [Auth Portal](https://auth.pollinations.ai)
- [PyPI Package](https://pypi.org/project/eclips-blossom-ai/)

## ❤️ Credits

Built with love using the Pollinations.AI platform.

Made with 🌸 by the eclips team

---

*This README reflects v0.2.6 with enhanced resource management and session cleanup.*