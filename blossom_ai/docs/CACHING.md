# 💾 Caching Guide

> **Cache AI responses to reduce costs and improve performance**

The Caching module helps you store and reuse AI responses, dramatically reducing API calls and costs while improving response times.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Cache Manager](#cache-manager)
- [Decorator Usage](#decorator-usage)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Performance](#performance)

---

## 🌟 Overview

### Why Use Caching?

**Without Caching:**
- Every request hits the API (slow, expensive)
- Same questions = repeated costs
- High latency for common queries

**With Caching:**
- ⚡ **99%+ faster** for cached responses
- 💰 **Massive cost reduction** (no API calls for cached data)
- 🚀 **Instant responses** from cache
- 📊 **Performance metrics** built-in

### Key Features

| Feature | Description |
|---------|-------------|
| **Hybrid Storage** | Memory (fast) + Disk (persistent) |
| **TTL Support** | Automatic expiration |
| **Statistics** | Hit rate tracking |
| **Easy Decorator** | `@cached` for instant caching |
| **Custom Keys** | Flexible cache key generation |

---

## 🚀 Quick Start

### Basic Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

# Create cache manager
cache = CacheManager()

# Your prompt
prompt = "Explain quantum computing"

# Check cache first
cached_response = cache.get(f"text:{hash(prompt)}")

if cached_response:
    print("From cache:", cached_response)
else:
    # Generate and cache
    with Blossom(api_token="your_token") as client:
        response = client.text.generate(prompt)
        cache.set(f"text:{hash(prompt)}", response, ttl=3600)
        print("Fresh response:", response)
```

### Using Decorator (Easiest!)

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=3600)  # Cache for 1 hour
def generate_text(prompt: str) -> str:
    with Blossom(api_token="your_token") as client:
        return client.text.generate(prompt)

# First call - hits API
result1 = generate_text("Explain AI")  # ~2 seconds

# Second call - instant from cache
result2 = generate_text("Explain AI")  # ~0.001 seconds

# Same result, 1000x faster!
assert result1 == result2
```

---

## 🗄️ Cache Manager

### Creating Cache Manager

```python
from blossom_ai.utils import CacheManager

# Default configuration
cache = CacheManager()

# Custom configuration
cache = CacheManager(
    cache_dir="./my_cache",      # Custom cache directory
    max_memory_items=500,        # Memory cache size
    enable_disk_cache=True       # Enable disk persistence
)
```

### Basic Operations

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Set value (with TTL)
cache.set("key1", "value1", ttl=3600)  # 1 hour

# Get value
value = cache.get("key1")
print(value)  # "value1"

# Check if exists
exists = cache.exists("key1")
print(exists)  # True

# Delete value
cache.delete("key1")

# Clear all cache
cache.clear()
```

### TTL (Time To Live)

```python
import time
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Cache for 5 seconds
cache.set("temp", "data", ttl=5)

# Immediately available
print(cache.get("temp"))  # "data"

# After 6 seconds - expired
time.sleep(6)
print(cache.get("temp"))  # None
```

### Cache Statistics

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Make some requests
for i in range(10):
    key = f"key_{i % 3}"  # Only 3 unique keys
    
    cached = cache.get(key)
    if not cached:
        cache.set(key, f"value_{i}")

# Get statistics
stats = cache.get_stats()

print(f"Hits: {stats.hits}")           # Cache hits
print(f"Misses: {stats.misses}")       # Cache misses
print(f"Hit rate: {stats.hit_rate}%")  # Success rate
print(f"Total: {stats.total_requests}")

# Example output:
# Hits: 7
# Misses: 3
# Hit rate: 70.0%
# Total: 10
```

---

## 🎨 Decorator Usage

### Basic Decorator

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=3600)
def ask_ai(question: str) -> str:
    """Cached AI generation"""
    with Blossom(api_token="your_token") as client:
        return client.text.generate(question)

# Usage
answer = ask_ai("What is Python?")
```

### With Multiple Parameters

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=7200)  # 2 hours
def generate_with_params(
    prompt: str,
    max_tokens: int,
    temperature: float
) -> str:
    with Blossom(api_token="your_token") as client:
        return client.text.generate(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

# Each unique combination is cached separately
result1 = generate_with_params("Hello", 100, 0.7)
result2 = generate_with_params("Hello", 200, 0.7)  # Different cache key
result3 = generate_with_params("Hello", 100, 0.7)  # Same as result1 - cached!
```

### Custom Cache Keys

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached
import hashlib

def make_cache_key(prompt: str, model: str) -> str:
    """Custom cache key generator"""
    combined = f"{model}:{prompt}"
    return hashlib.md5(combined.encode()).hexdigest()

@cached(ttl=3600)
def generate_cached(prompt: str, model: str = "openai") -> str:
    # Cache key automatically includes all parameters
    with Blossom(api_token="your_token") as client:
        return client.text.generate(prompt, model=model)

# Different models = different cache entries
response1 = generate_cached("Hello", "openai")
response2 = generate_cached("Hello", "gemini")
```

### Async Decorator

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=3600)
async def async_generate(prompt: str) -> str:
    """Cached async generation"""
    async with Blossom(api_token="your_token") as client:
        return await client.text.generate(prompt)

# Usage
import asyncio

async def main():
    result = await async_generate("Explain async/await")
    print(result)

asyncio.run(main())
```

---

## 🔧 Advanced Features

### Hybrid Storage (Memory + Disk)

```python
from blossom_ai.utils import CacheManager

# Memory-only (faster, not persistent)
cache_memory = CacheManager(
    enable_disk_cache=False,
    max_memory_items=1000
)

# Memory + Disk (persistent)
cache_hybrid = CacheManager(
    enable_disk_cache=True,
    cache_dir="./persistent_cache",
    max_memory_items=500
)

# First in memory, then disk
cache_hybrid.set("key", "value", ttl=86400)  # 24 hours

# Survives restart
value = cache_hybrid.get("key")  # Loaded from disk if not in memory
```

### Cache Warming

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

def warm_cache(common_questions: list[str]):
    """Pre-populate cache with common questions"""
    cache = CacheManager()
    
    with Blossom(api_token="your_token") as client:
        for question in common_questions:
            cache_key = f"faq:{hash(question)}"
            
            if not cache.exists(cache_key):
                print(f"Warming cache: {question}")
                response = client.text.generate(question)
                cache.set(cache_key, response, ttl=86400)

# Usage
common_questions = [
    "What is Python?",
    "How to install packages?",
    "What is pip?",
    "How to create virtual environment?"
]

warm_cache(common_questions)
```

### Cache Namespacing

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Different namespaces for different purposes
cache.set("text:user123:q1", "answer1")
cache.set("image:user123:i1", "image_data")
cache.set("text:user456:q1", "answer2")

# Organize by type and user
def get_user_cache_key(user_id: str, query_type: str, query: str) -> str:
    return f"{query_type}:{user_id}:{hash(query)}"

# Usage
key = get_user_cache_key("user123", "text", "What is AI?")
cache.set(key, "AI is...", ttl=3600)
```

### Conditional Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

cache = CacheManager()

def should_cache(prompt: str, response: str) -> bool:
    """Decide whether to cache this response"""
    # Don't cache errors
    if "error" in response.lower():
        return False
    
    # Don't cache very short responses
    if len(response) < 50:
        return False
    
    # Don't cache time-sensitive queries
    time_keywords = ["today", "now", "current", "latest"]
    if any(kw in prompt.lower() for kw in time_keywords):
        return False
    
    return True

# Usage
with Blossom(api_token="your_token") as client:
    prompt = "Explain caching"
    response = client.text.generate(prompt)
    
    if should_cache(prompt, response):
        cache.set(f"text:{hash(prompt)}", response, ttl=3600)
```

### Batch Operations

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

def batch_generate_with_cache(prompts: list[str]) -> dict[str, str]:
    """Generate responses for multiple prompts with caching"""
    cache = CacheManager()
    results = {}
    to_generate = []
    
    # Check cache first
    for prompt in prompts:
        cache_key = f"batch:{hash(prompt)}"
        cached = cache.get(cache_key)
        
        if cached:
            results[prompt] = cached
        else:
            to_generate.append(prompt)
    
    # Generate only uncached
    if to_generate:
        with Blossom(api_token="your_token") as client:
            for prompt in to_generate:
                response = client.text.generate(prompt)
                cache_key = f"batch:{hash(prompt)}"
                cache.set(cache_key, response, ttl=3600)
                results[prompt] = response
    
    return results

# Usage
prompts = [
    "What is Python?",
    "What is JavaScript?",
    "What is Python?",  # Duplicate - cached
]

results = batch_generate_with_cache(prompts)
# Only 2 API calls instead of 3!
```

---

## ✅ Best Practices

### 1. Use Appropriate TTL

```python
from blossom_ai.utils import cached

# ❌ Don't cache everything forever
@cached(ttl=None)  # Never expires - can cause stale data

# ✅ Set reasonable TTL based on data type
@cached(ttl=86400)  # 24 hours for general knowledge
def generate_fact(topic: str) -> str:
    ...

@cached(ttl=300)  # 5 minutes for time-sensitive data
def generate_news_summary(topic: str) -> str:
    ...

@cached(ttl=3600)  # 1 hour for user queries
def generate_answer(question: str) -> str:
    ...
```

### 2. Clear Cache Key Strategy

```python
from blossom_ai.utils import CacheManager
import hashlib

def make_cache_key(
    operation: str,
    model: str,
    params: dict
) -> str:
    """Consistent cache key generation"""
    # Sort dict for consistency
    sorted_params = sorted(params.items())
    key_parts = [operation, model] + [f"{k}={v}" for k, v in sorted_params]
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

# Usage
cache = CacheManager()
key = make_cache_key(
    "text_gen",
    "openai",
    {"prompt": "Hello", "max_tokens": 100, "temperature": 0.7}
)
```

### 3. Monitor Cache Performance

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Periodically check stats
def monitor_cache():
    stats = cache.get_stats()
    
    print(f"Cache Hit Rate: {stats.hit_rate:.1f}%")
    
    if stats.hit_rate < 30:
        print("⚠️ Low hit rate - consider adjusting cache strategy")
    elif stats.hit_rate > 80:
        print("✅ Excellent hit rate!")
    
    return stats

# Monitor after every N requests
if cache.get_stats().total_requests % 100 == 0:
    monitor_cache()
```

### 4. Handle Cache Misses Gracefully

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

cache = CacheManager()

def get_with_fallback(cache_key: str, generator_func, ttl: int = 3600):
    """Get from cache or generate with fallback"""
    try:
        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Generate fresh
        result = generator_func()
        
        # Cache for next time
        try:
            cache.set(cache_key, result, ttl=ttl)
        except Exception as e:
            print(f"Cache set failed: {e}")
            # Continue anyway - we have the result
        
        return result
        
    except Exception as e:
        print(f"Cache error: {e}")
        # Fallback to direct generation
        return generator_func()
```

### 5. Clean Up Old Cache

```python
from blossom_ai.utils import CacheManager
import time

cache = CacheManager()

# Periodic cleanup
def cleanup_expired():
    """Clean up expired cache entries"""
    stats_before = cache.get_stats()
    
    # Clear will remove expired items
    cache.clear()
    
    stats_after = cache.get_stats()
    print(f"Cleaned up {stats_before.total_requests - stats_after.total_requests} expired entries")

# Run cleanup periodically
import threading

def periodic_cleanup(interval: int = 3600):
    """Run cleanup every hour"""
    while True:
        time.sleep(interval)
        cleanup_expired()

# Start cleanup thread
cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()
```

---

## 📊 Performance

### Performance Comparison

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached
import time

# Without caching
def without_cache(prompt: str) -> str:
    with Blossom(api_token="your_token") as client:
        return client.text.generate(prompt)

# With caching
@cached(ttl=3600)
def with_cache(prompt: str) -> str:
    with Blossom(api_token="your_token") as client:
        return client.text.generate(prompt)

# Test
prompt = "Explain quantum computing"

# First call (both hit API)
start = time.time()
result1 = without_cache(prompt)
time_no_cache = time.time() - start

start = time.time()
result2 = with_cache(prompt)
time_first_cached = time.time() - start

# Second call (cached version instant)
start = time.time()
result3 = without_cache(prompt)
time_no_cache_2 = time.time() - start

start = time.time()
result4 = with_cache(prompt)
time_from_cache = time.time() - start

print(f"Without cache: {time_no_cache:.3f}s")
print(f"With cache (first): {time_first_cached:.3f}s")
print(f"With cache (cached): {time_from_cache:.6f}s")
print(f"Speed improvement: {time_no_cache/time_from_cache:.0f}x faster!")

# Typical output:
# Without cache: 2.145s
# With cache (first): 2.156s
# With cache (cached): 0.001s
# Speed improvement: 2145x faster!
```

### Cost Reduction Example

```python
from blossom_ai.utils import CacheManager

cache = CacheManager()

# Simulate 1000 requests
# With 70% cache hit rate
total_requests = 1000
hit_rate = 0.70
cost_per_request = 0.002  # $0.002 per API call

# Without caching
cost_no_cache = total_requests * cost_per_request
print(f"Cost without cache: ${cost_no_cache:.2f}")

# With caching
cache_hits = int(total_requests * hit_rate)
cache_misses = total_requests - cache_hits
cost_with_cache = cache_misses * cost_per_request
savings = cost_no_cache - cost_with_cache

print(f"Cost with cache: ${cost_with_cache:.2f}")
print(f"Savings: ${savings:.2f} ({savings/cost_no_cache*100:.0f}%)")

# Typical output:
# Cost without cache: $2.00
# Cost with cache: $0.60
# Savings: $1.40 (70%)
```

### Real-World Example: Chatbot

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached
import time

class Chatbot:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.request_count = 0
        self.cache_hits = 0
    
    @cached(ttl=3600)
    def get_response(self, question: str) -> str:
        """Get cached response"""
        self.request_count += 1
        
        with Blossom(api_token=self.api_token) as client:
            return client.text.generate(question)
    
    def chat(self, question: str) -> str:
        """Chat with caching"""
        start = time.time()
        response = self.get_response(question)
        elapsed = time.time() - start
        
        if elapsed < 0.01:  # Instant = from cache
            self.cache_hits += 1
            print(f"⚡ From cache ({elapsed*1000:.1f}ms)")
        else:
            print(f"🌐 From API ({elapsed:.2f}s)")
        
        return response
    
    def stats(self):
        """Show performance stats"""
        hit_rate = (self.cache_hits / self.request_count * 100) if self.request_count > 0 else 0
        print(f"\n📊 Chatbot Stats:")
        print(f"Total requests: {self.request_count}")
        print(f"Cache hits: {self.cache_hits}")
        print(f"Hit rate: {hit_rate:.1f}%")

# Usage
bot = Chatbot("your_token")

# Simulate conversation with repeated questions
questions = [
    "What is Python?",
    "What is JavaScript?",
    "What is Python?",  # Cached!
    "How to learn programming?",
    "What is Python?",  # Cached!
    "What is JavaScript?",  # Cached!
]

for q in questions:
    print(f"\nQ: {q}")
    response = bot.chat(q)
    print(f"A: {response[:100]}...")

bot.stats()
```

---

## 🔗 Related Documentation

- [Text Generation](TEXT_GENERATION.md) - Generate text to cache
- [Image Generation](IMAGE_GENERATION.md) - Cache image URLs
- [Reasoning Guide](REASONING.md) - Cache reasoning results
- [Performance Guide](PERFORMANCE.md) - Overall performance tips

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Reasoning Guide](REASONING.md) | [File Reader](FILE_READER.md) →

</div>