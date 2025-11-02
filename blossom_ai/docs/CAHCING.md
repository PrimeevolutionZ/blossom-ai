# 💾 Caching Guide

> **Intelligent caching for AI requests to reduce costs and improve performance**

The Caching Module provides automatic request caching with memory and disk storage, reducing API calls and improving response times.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Cache Backends](#-cache-backends)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Cache Statistics](#-cache-statistics)
- [Best Practices](#-best-practices)

---

## 🚀 Quick Start

### Basic Usage

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

# Cache function results automatically
@cached(ttl=3600)  # Cache for 1 hour
def generate_story(prompt):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(prompt)

# First call: generates and caches
result1 = generate_story("Tell me a story about AI")

# Second call: returns cached result (instant!)
result2 = generate_story("Tell me a story about AI")
```

### Manual Caching

```python
from blossom_ai.utils import CacheManager

# Create cache manager
cache = CacheManager()

# Set value
cache.set("my_key", "my_value", ttl=3600)

# Get value
value = cache.get("my_key")
print(value)  # "my_value"

# Check stats
print(cache.get_stats())
```

---

## 🗄️ Cache Backends

### MEMORY - Fast In-Memory Cache

Best for: Short-lived data, development, testing

```python
from blossom_ai.utils import CacheConfig, CacheBackend, CacheManager

config = CacheConfig(
    backend=CacheBackend.MEMORY,
    max_memory_size=100,  # Max 100 items
    ttl=3600
)

cache = CacheManager(config)
```

**Pros:**
- ⚡ Extremely fast
- 🎯 No disk I/O
- 🧹 Auto-cleanup on exit

**Cons:**
- ⏳ Lost on program restart
- 💾 Limited by RAM

---

### DISK - Persistent Disk Cache

Best for: Long-term storage, shared cache, large datasets

```python
from blossom_ai.utils import CacheConfig, CacheBackend, CacheManager
from pathlib import Path

config = CacheConfig(
    backend=CacheBackend.DISK,
    cache_dir=Path.home() / ".my_app_cache",
    max_disk_size=1000,  # Max 1000 items
    ttl=86400  # 24 hours
)

cache = CacheManager(config)
```

**Pros:**
- 💾 Persists across restarts
- 📦 Can store large amounts
- 🔄 Shareable between processes

**Cons:**
- 🐢 Slower than memory
- 💿 Requires disk space

---

### HYBRID - Memory + Disk (Recommended)

Best for: Production, balanced performance, large workloads

```python
from blossom_ai.utils import CacheConfig, CacheBackend, CacheManager

config = CacheConfig(
    backend=CacheBackend.HYBRID,  # Default
    max_memory_size=100,
    max_disk_size=1000,
    ttl=3600
)

cache = CacheManager(config)
```

**How it works:**
1. Check memory first (fast)
2. Check disk if not in memory
3. Promote disk → memory on access
4. Auto-evict old entries (LRU)

**Pros:**
- ⚡ Fast memory access
- 💾 Persistent storage
- 🔄 Auto-promotion
- 🎯 Best of both worlds

---

## ⚙️ Configuration

### Complete Configuration

```python
from blossom_ai.utils import CacheConfig, CacheBackend
from pathlib import Path

config = CacheConfig(
    # General
    enabled=True,  # Enable/disable caching
    backend=CacheBackend.HYBRID,  # Memory + Disk
    ttl=3600,  # Time to live (seconds)
    
    # Memory settings
    max_memory_size=100,  # Max items in memory
    
    # Disk settings
    max_disk_size=1000,  # Max items on disk
    cache_dir=Path.home() / ".blossom_cache",  # Cache directory
    
    # What to cache
    cache_text=True,  # Cache text responses
    cache_images=False,  # Don't cache images (large)
    cache_audio=False,  # Don't cache audio
    
    # Advanced
    compress=True,  # Compress disk cache
    serialize_format="pickle"  # pickle or json
)
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | `bool` | `True` | Enable/disable caching |
| `backend` | `CacheBackend` | `HYBRID` | Storage backend |
| `ttl` | `int` | `3600` | Time to live (seconds) |
| `max_memory_size` | `int` | `100` | Max items in memory |
| `max_disk_size` | `int` | `1000` | Max items on disk |
| `cache_dir` | `Optional[Path]` | `~/.blossom_cache` | Cache directory |
| `cache_text` | `bool` | `True` | Cache text responses |
| `cache_images` | `bool` | `False` | Cache images |
| `cache_audio` | `bool` | `False` | Cache audio |
| `compress` | `bool` | `True` | Compress disk cache |
| `serialize_format` | `str` | `"pickle"` | Serialization format |

---

## 💡 Usage Examples

### Example 1: Basic Decorator

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=1800)  # Cache 30 minutes
def analyze_code(code):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(
            f"Analyze this code:\n\n{code}",
            max_tokens=500
        )

# First call: generates response
result = analyze_code("def hello(): print('hi')")

# Second call: instant from cache
result = analyze_code("def hello(): print('hi')")
```

---

### Example 2: Manual Cache Control

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Generate key
key = "story_prompt_abc123"

# Check if cached
cached_result = cache.get(key)
if cached_result:
    print("Using cached result!")
    return cached_result

# Generate new
with Blossom(api_version="v2", api_token="token") as client:
    result = client.text.generate("Tell me a story")
    
    # Cache it
    cache.set(key, result, ttl=3600)
    
    return result
```

---

### Example 3: Global Cache

```python
from blossom_ai.utils import get_cache, configure_cache, CacheConfig

# Configure global cache once
configure_cache(CacheConfig(
    backend="hybrid",
    ttl=7200,  # 2 hours
    cache_text=True
))

# Use anywhere in your app
def function1():
    cache = get_cache()
    cache.set("key1", "value1")

def function2():
    cache = get_cache()  # Same cache instance
    value = cache.get("key1")
    print(value)  # "value1"
```

---

### Example 4: Custom Cache Keys

```python
from blossom_ai.utils import CacheManager
import hashlib

cache = CacheManager()

def generate_cache_key(prompt, model, temperature):
    """Generate deterministic cache key"""
    data = f"{prompt}:{model}:{temperature}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]

# Use custom key
prompt = "Explain AI"
model = "openai"
temp = 0.7

key = generate_cache_key(prompt, model, temp)

# Check cache
result = cache.get(key)
if not result:
    # Generate and cache
    with Blossom(api_version="v2", api_token="token") as client:
        result = client.text.generate(prompt, model=model, temperature=temp)
        cache.set(key, result, ttl=3600)
```

---

### Example 5: Selective Caching

```python
from blossom_ai.utils import CacheManager, CacheConfig

config = CacheConfig(
    cache_text=True,  # Cache text
    cache_images=False,  # Don't cache images (large files)
    cache_audio=False  # Don't cache audio
)

cache = CacheManager(config)

# Text will be cached
@cache.cached(ttl=3600)
def generate_text(prompt):
    # ...
    pass

# Images won't be cached (too large)
def generate_image(prompt):
    # Direct generation, no cache
    # ...
    pass
```

---

### Example 6: Cache with Metadata

```python
from blossom_ai.utils import CacheManager
import time

cache = CacheManager()

# Cache with metadata
cache.set(
    key="response_123",
    value="AI response here",
    ttl=3600,
    metadata={
        "model": "openai",
        "tokens": 150,
        "timestamp": time.time(),
        "user_id": "user_123"
    }
)

# Retrieve (metadata not returned in get, but stored)
value = cache.get("response_123")
```

---

### Example 7: Async Support

```python
import asyncio
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

cache = CacheManager()

@cache.cached(ttl=3600)
async def generate_async(prompt):
    async with Blossom(api_version="v2", api_token="token") as client:
        return await client.text.generate(prompt)

async def main():
    # First call: generates
    result1 = await generate_async("Hello")
    
    # Second call: cached
    result2 = await generate_async("Hello")
    
    print(f"Same result: {result1 == result2}")

asyncio.run(main())
```

---

### Example 8: Clear Cache

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Cache some data
cache.set("key1", "value1")
cache.set("key2", "value2")
cache.set("prefix_a", "value3")
cache.set("prefix_b", "value4")

# Clear all cache
cache.clear()

# Clear specific prefix
cache.clear(prefix="prefix_")  # Only clears prefix_a, prefix_b
```

---

## 📊 Cache Statistics

### Get Stats

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Perform operations
cache.set("key1", "value1")
cache.get("key1")  # Hit
cache.get("key2")  # Miss
cache.get("key1")  # Hit

# Get statistics
stats = cache.get_stats()

print(stats)
# CacheStats(hits=2, misses=1, hit_rate=66.7%, evictions=0)

print(f"Hit rate: {stats.hit_rate:.1f}%")
print(f"Hits: {stats.hits}")
print(f"Misses: {stats.misses}")
print(f"Memory usage: {stats.memory_usage} items")
print(f"Disk usage: {stats.disk_usage} items")
```

### Monitor Performance

```python
from blossom_ai.utils import CacheManager
import time

cache = CacheManager()

def generate_with_stats(prompt):
    key = f"prompt_{hash(prompt)}"
    
    start = time.time()
    result = cache.get(key)
    
    if result:
        elapsed = time.time() - start
        print(f"âœ… Cache hit! ({elapsed*1000:.1f}ms)")
        return result
    
    # Generate
    start = time.time()
    with Blossom(api_version="v2", api_token="token") as client:
        result = client.text.generate(prompt)
    elapsed = time.time() - start
    print(f"âš™ï¸ Generated ({elapsed*1000:.1f}ms)")
    
    # Cache it
    cache.set(key, result, ttl=3600)
    return result

# First call: slow
generate_with_stats("Tell me a story")
# âš™ï¸ Generated (2500.0ms)

# Second call: fast!
generate_with_stats("Tell me a story")
# âœ… Cache hit! (0.5ms)
```

---

## ✅ Best Practices

### 1. Choose Appropriate TTL

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Short TTL for dynamic content
cache.set("weather", data, ttl=300)  # 5 minutes

# Medium TTL for semi-static content
cache.set("news", data, ttl=1800)  # 30 minutes

# Long TTL for static content
cache.set("facts", data, ttl=86400)  # 24 hours

# Very long TTL for rarely changing content
cache.set("constants", data, ttl=604800)  # 1 week
```

---

### 2. Use Prefixes for Organization

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Organize with prefixes
cache.set("text:summary:doc1", summary1)
cache.set("text:summary:doc2", summary2)
cache.set("text:analysis:doc1", analysis1)
cache.set("image:thumbnail:img1", thumb1)

# Clear all summaries
cache.clear(prefix="text:summary:")

# Clear all text cache
cache.clear(prefix="text:")
```

---

### 3. Cache Expensive Operations Only

```python
from blossom_ai.utils import cached

# âœ… DO cache expensive AI calls
@cached(ttl=3600)
def analyze_document(doc):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(f"Analyze: {doc}", max_tokens=1000)

# âœ… DO cache large computations
@cached(ttl=7200)
def process_big_data(data):
    # Expensive processing...
    return result

# âŒ DON'T cache simple operations
def add_numbers(a, b):
    return a + b  # Too simple, overhead not worth it
```

---

### 4. Combine with Other Features

#### With Reasoning

```python
from blossom_ai.utils import cached, ReasoningEnhancer

enhancer = ReasoningEnhancer()

@cached(ttl=3600)
def analyze_with_reasoning(question):
    enhanced = enhancer.enhance(question, level="high")
    
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=1500)

# Cache + reasoning = efficient deep thinking
result = analyze_with_reasoning("Design a database schema")
```

#### With V2 API

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

cache = CacheManager()

def generate_with_v2(prompt):
    key = f"v2:{hash(prompt)}"
    
    result = cache.get(key)
    if result:
        return result
    
    with Blossom(api_version="v2", api_token="token") as client:
        result = client.text.generate(
            prompt,
            max_tokens=500,
            frequency_penalty=0.5
        )
        
        cache.set(key, result, ttl=3600)
        return result
```

---

### 5. Handle Cache Misses Gracefully

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

def get_or_generate(prompt):
    key = f"prompt_{hash(prompt)}"
    
    # Try cache first
    result = cache.get(key)
    if result:
        return result, True  # (result, from_cache)
    
    try:
        # Generate new
        with Blossom(api_version="v2", api_token="token") as client:
            result = client.text.generate(prompt)
            
            # Cache successful result
            cache.set(key, result, ttl=3600)
            return result, False
            
    except Exception as e:
        # If generation fails, return None
        print(f"Error: {e}")
        return None, False

# Use it
result, cached = get_or_generate("Hello")
if result:
    print(f"Result ({'cached' if cached else 'fresh'}): {result}")
```

---

### 6. Monitor and Tune

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Generate workload...
for i in range(1000):
    cache.set(f"key_{i}", f"value_{i}")
    cache.get(f"key_{i % 500}")  # 50% hit rate

# Check performance
stats = cache.get_stats()

if stats.hit_rate < 50:
    print("âš ï¸ Low hit rate! Consider:")
    print("  - Increasing TTL")
    print("  - Increasing cache size")
    print("  - Better key generation")
    
if stats.evictions > stats.hits:
    print("âš ï¸ Too many evictions! Consider:")
    print("  - Increasing max_memory_size")
    print("  - Using DISK or HYBRID backend")
```

---

### 7. Production Configuration

```python
from blossom_ai.utils import CacheConfig, CacheBackend, configure_cache
from pathlib import Path

# Production-ready config
config = CacheConfig(
    backend=CacheBackend.HYBRID,
    
    # Generous limits
    max_memory_size=500,  # 500 items in memory
    max_disk_size=5000,  # 5000 items on disk
    
    # Persistent storage
    cache_dir=Path("/var/cache/myapp"),
    
    # 2-hour TTL for most content
    ttl=7200,
    
    # Cache text only (images too large)
    cache_text=True,
    cache_images=False,
    cache_audio=False,
    
    # Optimize disk usage
    compress=True
)

# Set globally
configure_cache(config)
```

---

## 🎯 Use Cases

### 1. Chatbot with History Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

cache = CacheManager()

def chatbot(user_id, message, history):
    # Create cache key from user + history hash
    history_hash = hash(str(history))
    cache_key = f"chat:{user_id}:{history_hash}:{hash(message)}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Generate response
    with Blossom(api_version="v2", api_token="token") as client:
        messages = history + [{"role": "user", "content": message}]
        response = client.text.chat(messages=messages)
        
        # Cache for 30 minutes
        cache.set(cache_key, response, ttl=1800)
        return response
```

---

### 2. Document Analysis Pipeline

```python
from blossom_ai.utils import CacheManager, cached

cache = CacheManager()

@cached(ttl=86400)  # Cache 24 hours
def extract_text(doc_path):
    # Expensive OCR/extraction
    return text

@cached(ttl=86400)
def summarize(text):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(f"Summarize: {text}", max_tokens=200)

@cached(ttl=86400)
def extract_entities(text):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(f"Extract entities: {text}", json_mode=True)

def analyze_document(doc_path):
    # Each step cached independently
    text = extract_text(doc_path)
    summary = summarize(text)
    entities = extract_entities(text)
    
    return {
        "summary": summary,
        "entities": entities
    }
```

---

### 3. API Rate Limit Protection

```python
from blossom_ai import Blossom, RateLimitError
from blossom_ai.utils import CacheManager
import time

cache = CacheManager()

def generate_with_protection(prompt):
    key = f"prompt:{hash(prompt)}"
    
    # Always try cache first
    result = cache.get(key)
    if result:
        return result
    
    try:
        with Blossom(api_version="v2", api_token="token") as client:
            result = client.text.generate(prompt)
            
            # Cache successful result
            cache.set(key, result, ttl=3600)
            return result
            
    except RateLimitError as e:
        print(f"Rate limited! Using longer cache TTL")
        
        # Try to find any cached version (even expired)
        # Custom logic to check expired entries...
        
        print(f"Retry after {e.retry_after}s")
        time.sleep(e.retry_after)
        return generate_with_protection(prompt)
```

---

## 🔗 Related Documentation

- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API docs
- **[Reasoning Guide](REASONING.md)** - Structured thinking
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors properly

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>