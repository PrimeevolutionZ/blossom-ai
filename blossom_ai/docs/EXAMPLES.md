# Examples

Practical examples including V2 API, Reasoning, and Caching features.

---

## 🆕 New Features Examples (v0.4.1)

### Reasoning + Caching Combined

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)  # Cache for 1 hour
def deep_analysis(question):
    """Cached deep reasoning - best of both worlds!"""
    enhanced = enhancer.enhance(question, level="high")
    
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=1500)

# First call: deep reasoning + caches result (takes 3-5 seconds)
result = deep_analysis("Design a scalable microservices architecture")

# Second call: instant from cache (0.5ms instead of 3000ms!)
result = deep_analysis("Design a scalable microservices architecture")
```

### Cache Statistics Monitoring

```python
from blossom_ai import Blossom
from blossom_ai.utils import get_cache, cached

@cached(ttl=1800)
def generate_summary(text):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(f"Summarize: {text}", max_tokens=200)

# Generate some requests
for i in range(100):
    generate_summary(f"Text {i % 20}")  # 20 unique, 80 cached

# Check performance
cache = get_cache()
stats = cache.get_stats()

print(f"✅ Hit rate: {stats.hit_rate:.1f}%")  # Should be ~80%
print(f"📊 Hits: {stats.hits}, Misses: {stats.misses}")
print(f"⚡ Speed improvement: {stats.hits / max(stats.misses, 1):.1f}x faster!")
```

### Reasoning Levels Comparison

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, ReasoningLevel

enhancer = ReasoningEnhancer()
question = "How do I optimize database queries?"

with Blossom(api_version="v2", api_token="token") as client:
    # Quick answer (LOW)
    low = enhancer.enhance(question, level=ReasoningLevel.LOW)
    result_low = client.text.generate(low, max_tokens=300)
    
    # Systematic analysis (MEDIUM)
    medium = enhancer.enhance(question, level=ReasoningLevel.MEDIUM)
    result_medium = client.text.generate(medium, max_tokens=800)
    
    # Deep reasoning (HIGH)
    high = enhancer.enhance(question, level=ReasoningLevel.HIGH)
    result_high = client.text.generate(high, max_tokens=2000)
    
    print("=== LOW (Quick) ===")
    print(result_low[:200] + "...\n")
    
    print("=== MEDIUM (Systematic) ===")
    print(result_medium[:200] + "...\n")
    
    print("=== HIGH (Deep) ===")
    print(result_high[:200] + "...")
```

### Extract Reasoning from Response

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Design a caching system for a web application",
    level="high"
)

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced, max_tokens=1500)
    
    # Parse structured output
    parsed = enhancer.extract_reasoning(response)
    
    print("=== REASONING PROCESS ===")
    print(parsed['reasoning'])
    
    print("\n=== FINAL ANSWER ===")
    print(parsed['answer'])
    
    if parsed['confidence']:
        print(f"\n=== CONFIDENCE: {parsed['confidence']} ===")
```

### Production-Ready Chatbot with Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager, ReasoningEnhancer

cache = CacheManager()
enhancer = ReasoningEnhancer()

def chatbot_with_cache(user_id, message, history):
    """Intelligent chatbot with caching and reasoning"""
    
    # Generate cache key
    history_hash = hash(str(history))
    cache_key = f"chat:{user_id}:{history_hash}:{hash(message)}"
    
    # Try cache first
    cached_response = cache.get(cache_key)
    if cached_response:
        print("✅ Cache hit!")
        return cached_response
    
    print("⚙️ Generating response...")
    
    # Enhance complex questions with reasoning
    if any(word in message.lower() for word in ['how', 'why', 'explain', 'design']):
        message = enhancer.enhance(message, level="medium")
    
    # Generate response
    with Blossom(api_version="v2", api_token="token") as client:
        messages = history + [{"role": "user", "content": message}]
        response = client.text.chat(
            messages=messages,
            max_tokens=500,
            frequency_penalty=0.3
        )
        
        # Cache for 30 minutes
        cache.set(cache_key, response, ttl=1800)
        return response

# Example usage
history = [
    {"role": "system", "content": "You are a helpful assistant"}
]

response1 = chatbot_with_cache("user123", "What is Python?", history)
# ⚙️ Generating response... (takes 2-3 seconds)

response2 = chatbot_with_cache("user123", "What is Python?", history)
# ✅ Cache hit! (instant!)
```

---

## V2 API Examples

### HD Image with Advanced Features

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Professional HD image
    image = client.image.generate(
        prompt="professional portrait, studio lighting, 4k",
        quality="hd",  # Best quality
        guidance_scale=8.0,  # Strong prompt adherence
        negative_prompt="blurry, distorted, low quality, amateur",
        width=1024,
        height=1024,
        nologo=True,
        nofeed=True  # Keep private
    )
    
    with open("portrait_hd.png", "wb") as f:
        f.write(image)
    
    print(f"✅ Generated HD image: {len(image)} bytes")
```

### Text Generation with Advanced Parameters

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(
        prompt="Write a creative story about AI",
        model="openai",
        max_tokens=500,  # Limit length
        temperature=1.2,  # More creative (0-2 range)
        frequency_penalty=0.8,  # Reduce repetition
        presence_penalty=0.6,  # Diverse topics
        top_p=0.95  # Nucleus sampling
    )
    
    print(response)
```

### Function Calling (AI Agents)

```python
from blossom_ai import Blossom

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
                        "description": "City name, e.g. London"
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

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.chat(
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"}
        ],
        tools=tools,
        tool_choice="auto"
    )
    
    print(response)
    # AI will indicate it wants to call get_weather function
```

### Transparent Images

```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as client:
    # Logo with transparency
    logo = client.image.generate(
        prompt="minimalist tech logo, geometric, modern",
        transparent=True,  # PNG with alpha channel
        negative_prompt="background, text, complex",
        quality="hd",
        width=512,
        height=512
    )
    
    with open("logo_transparent.png", "wb") as f:
        f.write(logo)
```

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

## Web Application Example (with Caching)

```python
from flask import Flask, render_template, request
from blossom_ai import Blossom
from blossom_ai.utils import cached

app = Flask(__name__)

@cached(ttl=3600)  # Cache images for 1 hour
def generate_cached_image(prompt):
    """Generate image with caching"""
    with Blossom() as client:
        return client.image.generate_url(
            prompt,
            width=512,
            height=512,
            nologo=True
        )

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    
    # Use cached generator
    url = generate_cached_image(prompt)
    
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

## Handling Rate Limits with Caching

```python
from blossom_ai import Blossom, RateLimitError
from blossom_ai.utils import CacheManager
import time

cache = CacheManager()

def generate_with_protection(prompt):
    """Generate with rate limit protection via caching"""
    key = f"prompt:{hash(prompt)}"
    
    # Always try cache first
    cached = cache.get(key)
    if cached:
        print("✅ Using cached result (avoiding rate limit)")
        return cached
    
    try:
        with Blossom() as ai:
            response = ai.text.generate(prompt)
            cache.set(key, response, ttl=3600)
            return response
    except RateLimitError as e:
        print(f"⚠️ Rate limited: {e.message}")
        if e.retry_after:
            print(f"⏳ Waiting {e.retry_after} seconds...")
            time.sleep(e.retry_after)
            return generate_with_protection(prompt)  # Retry
```

---

## Document Analysis Pipeline (with Caching)

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached, ReasoningEnhancer

enhancer = ReasoningEnhancer()

@cached(ttl=86400)  # Cache 24 hours
def extract_text(doc_path):
    # Expensive OCR/extraction
    with open(doc_path) as f:
        return f.read()

@cached(ttl=86400)
def summarize_with_reasoning(text):
    """Summarize with structured thinking"""
    enhanced = enhancer.enhance(
        f"Summarize this document:\n\n{text}",
        level="medium"
    )
    
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=300)

@cached(ttl=86400)
def extract_entities(text):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(
            f"Extract entities as JSON: {text}",
            json_mode=True,
            max_tokens=200
        )

def analyze_document(doc_path):
    """Cached pipeline - each step cached independently"""
    text = extract_text(doc_path)
    summary = summarize_with_reasoning(text)
    entities = extract_entities(text)
    
    return {
        "summary": summary,
        "entities": entities
    }

# First run: all steps execute
result = analyze_document("document.txt")

# Second run: instant from cache!
result = analyze_document("document.txt")
```
# 🧠 Reasoning V2: Native Support Examples

## Overview

Reasoning now supports **two modes**:
- **PROMPT mode** (universal): Works with all models, adds reasoning to prompt
- **NATIVE mode** (V2 only): Uses built-in `thinking` parameter (OpenAI models)
- **AUTO mode** (recommended): Automatically chooses best approach

---

## 🎯 Quick Start - Auto Mode (Recommended)

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

# AUTO mode - automatically chooses best approach
with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    result = enhancer.enhance(
        "Design a scalable microservices architecture",
        level="high",
        mode="auto",  # ✅ Automatically uses native for OpenAI
        api_version="v2",
        model="openai"
    )
    
    # Check which mode was used
    if isinstance(result, dict) and "thinking" in result:
        # Native mode - use thinking parameter
        response = client.text.chat(
            messages=[{"role": "user", "content": result["prompt"]}],
            thinking=result["thinking"]
        )
        print("✨ Used NATIVE reasoning")
    else:
        # Prompt mode - enhanced prompt
        response = client.text.generate(result)
        print("✨ Used PROMPT reasoning")
    
    print(response)
```

---

## 📊 Mode Comparison

### When AUTO mode chooses NATIVE:
- ✅ API version = "v2"
- ✅ Model in ["openai", "openai-large", "openai-fast"]
- ✅ More token-efficient
- ✅ Better reasoning quality

### When AUTO mode chooses PROMPT:
- ✅ API version = "v1" (only option)
- ✅ Model not supporting native reasoning
- ✅ Works with ANY model
- ✅ Full control over reasoning format

---

## 💡 Usage Examples

### Example 1: Auto Mode with V2 (Recommended)

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import create_reasoning_enhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

# Create enhancer with auto mode
enhancer = create_reasoning_enhancer(level="high", mode="auto")

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    # Enhance prompt
    result = enhancer.enhance(
        "Optimize this database query for 1M rows",
        api_version="v2",
        model="openai"
    )
    
    # Generate with native reasoning
    response = client.text.chat(
        messages=[{"role": "user", "content": result["prompt"]}],
        thinking=result.get("thinking"),  # Safe - None if PROMPT mode
        max_tokens=1500
    )
    
    print(response)
```

---

### Example 2: Force PROMPT Mode (Universal)

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

# Works with ANY model (even non-OpenAI)
with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    enhanced = enhancer.enhance(
        "How to implement caching?",
        level="medium",
        mode="prompt"  # ✅ Force prompt mode
    )
    
    # Use with any model
    response = client.text.generate(
        enhanced,
        model="mistral"  # Works with non-OpenAI models!
    )
    
    print(response)
```

---

### Example 3: Force NATIVE Mode (V2 OpenAI Only)

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, ReasoningConfig, ReasoningMode

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

# Configure for native reasoning
config = ReasoningConfig(
    level="high",
    mode=ReasoningMode.NATIVE,
    budget_tokens=3000  # Token budget for reasoning
)

enhancer = ReasoningEnhancer(default_config=config)

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    result = enhancer.enhance(
        "Design a distributed system",
        api_version="v2",
        model="openai"  # Must be OpenAI model
    )
    
    # Use native reasoning
    response = client.text.chat(
        messages=[{"role": "user", "content": result["prompt"]}],
        thinking={
            "type": "enabled",
            "budget_tokens": 3000
        }
    )
    
    print(response)
```

---

### Example 4: Check Model Support

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# Check if model supports native reasoning
models = ["openai", "mistral", "gemini", "openai-large"]

for model in models:
    supports = enhancer.supports_native_reasoning(model)
    print(f"{model}: {'✅ Native' if supports else '❌ Prompt only'}")

# Output:
# openai: ✅ Native
# mistral: ❌ Prompt only
# gemini: ❌ Prompt only
# openai-large: ✅ Native
```

---

### Example 5: V1 API (Auto Falls Back to PROMPT)

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

# V1 API - always uses PROMPT mode
with Blossom(api_version="v1") as client:
    enhanced = enhancer.enhance(
        "How does HTTP caching work?",
        level="medium",
        mode="auto",  # AUTO detects V1 → uses PROMPT
        api_version="v1"
    )
    
    # Returns string (not dict)
    response = client.text.generate(enhanced)
    print(response)
```

---

### Example 6: Adaptive Level + Auto Mode

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import create_reasoning_enhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

# Both level and mode are adaptive
enhancer = create_reasoning_enhancer(level="adaptive", mode="auto")

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    # Simple question → LOW level, NATIVE mode (if OpenAI)
    result1 = enhancer.enhance(
        "What is Python?",
        api_version="v2",
        model="openai"
    )
    
    # Complex question → HIGH level, NATIVE mode
    result2 = enhancer.enhance(
        "Design a fault-tolerant distributed consensus algorithm",
        api_version="v2",
        model="openai"
    )
    
    # Both use optimal settings automatically!
```

---

### Example 7: With Context and Examples

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    result = enhancer.enhance(
        prompt="How to fix this performance issue?",
        level="high",
        mode="auto",
        api_version="v2",
        model="openai",
        context="Python API with 10k req/s, database queries taking 2s each",
        examples=[
            "Check for N+1 queries",
            "Consider connection pooling",
            "Review index usage"
        ]
    )
    
    response = client.text.chat(
        messages=[{"role": "user", "content": result["prompt"]}],
        thinking=result.get("thinking")
    )
    
    print(response)
```

---

### Example 8: Multi-Step Reasoning Chain (Auto)

```python
import os
import asyncio
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningChain

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

async def solve_complex():
    async with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        chain = ReasoningChain(client.text)
        
        # Automatically uses native reasoning for V2
        result = await chain.solve(
            problem="Design a scalable e-commerce platform",
            steps=["analyze", "design", "validate", "optimize"],
            level="high",
            api_version="v2",
            model="openai"
        )
        
        print("=== PROBLEM ===")
        print(result['problem'])
        
        for step in result['steps']:
            print(f"\n=== {step['step'].upper()} ===")
            print(step['output'])
        
        print("\n=== FINAL ANSWER ===")
        print(result['final_answer'])

asyncio.run(solve_complex())
```

---

### Example 9: Error Handling

```python
import os
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    try:
        # Try to use native mode with non-OpenAI model
        result = enhancer.enhance(
            "Design a system",
            level="high",
            mode="native",  # Force native
            api_version="v2",
            model="mistral"  # ❌ Doesn't support native
        )
    except ValueError as e:
        print(f"Error: {e}")
        # Output: Model 'mistral' doesn't support native reasoning
        
        # Fallback to prompt mode
        result = enhancer.enhance(
            "Design a system",
            level="high",
            mode="prompt",  # Use prompt mode instead
            api_version="v2",
            model="mistral"
        )
        
        response = client.text.generate(result, model="mistral")
        print(response)
```

---

### Example 10: Compare Modes

```python
import os
import time
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
enhancer = ReasoningEnhancer()

prompt = "Explain quantum computing"

with Blossom(api_version="v2", api_token=API_TOKEN) as client:
    # PROMPT mode
    start = time.time()
    result_prompt = enhancer.enhance(prompt, level="high", mode="prompt")
    response_prompt = client.text.generate(result_prompt, model="openai")
    time_prompt = time.time() - start
    
    # NATIVE mode
    start = time.time()
    result_native = enhancer.enhance(
        prompt, level="high", mode="native",
        api_version="v2", model="openai"
    )
    response_native = client.text.chat(
        messages=[{"role": "user", "content": result_native["prompt"]}],
        thinking=result_native["thinking"]
    )
    time_native = time.time() - start
    
    print(f"PROMPT mode: {time_prompt:.2f}s, {len(response_prompt)} chars")
    print(f"NATIVE mode: {time_native:.2f}s, {len(response_native)} chars")
```

---

## 🔧 Configuration

### Global Configuration

```python
from blossom_ai.utils import ReasoningConfig, ReasoningMode, ReasoningLevel

# Configure once
config = ReasoningConfig(
    level=ReasoningLevel.HIGH,
    mode=ReasoningMode.AUTO,  # Recommended
    budget_tokens=2000,  # For native mode
    include_confidence=True,
    self_critique=True
)

enhancer = ReasoningEnhancer(default_config=config)

# Use everywhere
result1 = enhancer.enhance("Question 1", api_version="v2", model="openai")
result2 = enhancer.enhance("Question 2", api_version="v2", model="openai")
```

### Per-Request Override

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()  # Default config

# Override for specific request
result = enhancer.enhance(
    "Special question",
    level="low",  # Override level
    mode="prompt",  # Override mode
    api_version="v2"
)
```

---

## 📋 Supported Models

### Native Reasoning Support (V2 Only)

```python
from blossom_ai.utils.reasoning import get_native_reasoning_models

models = get_native_reasoning_models()
print(models)
# ['openai', 'openai-large', 'openai-fast']
```

### All Models (PROMPT Mode)

PROMPT mode works with **ALL** models:
- openai, mistral, gemini, qwen-coder, deepseek
- Any custom or community models
- Works on both V1 and V2 APIs

---

## ✅ Best Practices

### 1. Use AUTO Mode by Default

```python
# ✅ Good - let system choose
enhancer.enhance(prompt, mode="auto", api_version="v2", model="openai")

# ❌ Avoid unless you have specific reason
enhancer.enhance(prompt, mode="native")  # Too restrictive
```

### 2. Provide API Version and Model

```python
# ✅ Good - allows auto-detection
result = enhancer.enhance(
    prompt,
    mode="auto",
    api_version="v2",  # ✅ Provide version
    model="openai"     # ✅ Provide model
)

# ⚠️ Works but can't auto-detect
result = enhancer.enhance(prompt, mode="auto")  # Falls back to PROMPT
```

### 3. Handle Both Return Types

```python
result = enhancer.enhance(prompt, mode="auto", api_version="v2", model="openai")

# ✅ Good - handles both modes
if isinstance(result, dict) and "thinking" in result:
    response = client.text.chat(
        messages=[{"role": "user", "content": result["prompt"]}],
        thinking=result.get("thinking")
    )
else:
    response = client.text.generate(result)

# ❌ Bad - assumes one mode
response = client.text.generate(result)  # Fails if NATIVE mode
```

### 4. Use Native for High-Quality Reasoning

```python
# For complex problems with OpenAI models
result = enhancer.enhance(
    "Design distributed system",
    level="high",
    mode="auto",  # Will use native for OpenAI
    api_version="v2",
    model="openai"
)
```

### 5. Use Prompt for Universal Compatibility

```python
# For any model, any API version
enhanced = enhancer.enhance(
    "Explain caching",
    level="medium",
    mode="prompt"  # Works everywhere
)
```

---

## 🎓 When to Use Each Mode

| Scenario | Recommended Mode | Reason |
|----------|------------------|---------|
| V2 + OpenAI model | `auto` or `native` | Best quality, token-efficient |
| V2 + Other models | `prompt` | Only option |
| V1 API | `prompt` | Only option |
| Need full control | `prompt` | See reasoning in output |
| Production (mixed models) | `auto` | Adapts to each case |
| Development/Testing | `prompt` | Easier debugging |

---

## 📚 Related Documentation

- **[REASONING.md](REASONING.md)** - Full reasoning guide
- **[V2_API_REFERENCE.md](V2_API_REFERENCE.md)** - V2 API details
- **[CACHING.md](CACHING.md)** - Cache reasoning results

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

</div>