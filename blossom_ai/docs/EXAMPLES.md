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