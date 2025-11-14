# 🚀 Performance Guide

> **Optimize your Blossom AI applications for maximum speed and efficiency**

Learn techniques to improve response times, reduce costs, and build high-performance AI applications.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Wins](#quick-wins)
- [Caching Strategies](#caching-strategies)
- [Parallel Processing](#parallel-processing)
- [Request Optimization](#request-optimization)
- [Cost Optimization](#cost-optimization)
- [Benchmarking](#benchmarking)

---

## 🌟 Overview

### Performance Metrics

| Metric | Without Optimization | With Optimization | Improvement |
|--------|---------------------|-------------------|-------------|
| **Cache Hit** | 2000ms | 1ms | 2000x faster |
| **Parallel Requests** | 6000ms (3×2s) | 2000ms | 3x faster |
| **Streaming** | Wait for full response | Real-time chunks | Perceived instant |
| **Batch Processing** | Sequential | Concurrent | Up to Nx faster |
| **Cost** | Full API calls | Cached + optimized | 50-90% reduction |

### Key Principles

1. **Cache aggressively** - Avoid redundant API calls
2. **Parallelize** - Run independent operations concurrently
3. **Stream when possible** - Improve perceived performance
4. **Batch intelligently** - Balance concurrency and resources
5. **Optimize requests** - Minimize token usage

---

## ⚡ Quick Wins

### 1. Use Caching (99%+ faster)

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

# Without cache: ~2s per call
def slow():
    with Blossom(api_token="token") as client:
        return client.text.generate("What is Python?")

# With cache: ~0.001s after first call
@cached(ttl=3600)
def fast():
    with Blossom(api_token="token") as client:
        return client.text.generate("What is Python?")

# First call: 2s
result1 = fast()

# Second call: 0.001s (2000x faster!)
result2 = fast()
```

### 2. Use Async for Multiple Requests

```python
import asyncio
from blossom_ai import Blossom

# Sync: 6 seconds (3 × 2s)
def sync_version():
    with Blossom(api_token="token") as client:
        r1 = client.text.generate("Question 1")  # 2s
        r2 = client.text.generate("Question 2")  # 2s
        r3 = client.text.generate("Question 3")  # 2s
        return [r1, r2, r3]

# Async: 2 seconds (all concurrent)
async def async_version():
    async with Blossom(api_token="token") as client:
        results = await asyncio.gather(
            client.text.generate("Question 1"),  # 2s
            client.text.generate("Question 2"),  # 2s
            client.text.generate("Question 3"),  # 2s
        )
        return results

# 3x faster!
results = asyncio.run(async_version())
```

### 3. Stream for Perceived Speed

```python
from blossom_ai import Blossom

# Without streaming: Wait 5s, then show all
def without_streaming():
    with Blossom(api_token="token") as client:
        response = client.text.generate("Write a story")
        print(response)  # Wait... wait... BOOM! All at once

# With streaming: Show immediately as generated
def with_streaming():
    with Blossom(api_token="token") as client:
        for chunk in client.text.generate("Write a story", stream=True):
            print(chunk, end="", flush=True)  # Instant feedback!
```

### 4. Optimize Token Usage

```python
from blossom_ai import Blossom

# Inefficient: Wastes tokens
def inefficient():
    with Blossom(api_token="token") as client:
        return client.text.generate(
            "Explain quantum computing in extreme detail with examples",
            max_tokens=2000  # May not need all
        )

# Efficient: Request only what you need
def efficient():
    with Blossom(api_token="token") as client:
        return client.text.generate(
            "Explain quantum computing briefly",
            max_tokens=200  # Faster & cheaper
        )
```

### 5. Batch Similar Requests

```python
import asyncio
from blossom_ai import Blossom

# Inefficient: Multiple client instances
async def inefficient():
    for i in range(10):
        async with Blossom(api_token="token") as client:
            await client.text.generate(f"Question {i}")

# Efficient: Reuse client
async def efficient():
    async with Blossom(api_token="token") as client:
        tasks = [
            client.text.generate(f"Question {i}")
            for i in range(10)
        ]
        await asyncio.gather(*tasks)
```

---

## 💾 Caching Strategies

### Basic Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import cached

@cached(ttl=3600)  # Cache for 1 hour
def cached_generation(prompt: str) -> str:
    with Blossom(api_token="token") as client:
        return client.text.generate(prompt)

# First call: API request
result = cached_generation("What is AI?")  # ~2s

# Subsequent calls: instant from cache
result = cached_generation("What is AI?")  # ~0.001s
```

### Smart Cache Keys

```python
from blossom_ai.utils import cached
import hashlib

def make_cache_key(prompt: str, model: str, max_tokens: int) -> str:
    """Create unique cache key"""
    key = f"{model}:{max_tokens}:{prompt}"
    return hashlib.md5(key.encode()).hexdigest()

@cached(ttl=7200)
def smart_cached_generate(
    prompt: str,
    model: str = "openai",
    max_tokens: int = 500
) -> str:
    with Blossom(api_token="token") as client:
        return client.text.generate(
            prompt,
            model=model,
            max_tokens=max_tokens
        )

# Different parameters = different cache entries
r1 = smart_cached_generate("Hello", model="openai", max_tokens=100)
r2 = smart_cached_generate("Hello", model="openai", max_tokens=200)
r3 = smart_cached_generate("Hello", model="openai", max_tokens=100)  # Cached!
```

### Cache Warming

```python
from blossom_ai import Blossom
from blossom_ai.utils import CacheManager

def warm_cache(common_questions: list[str]):
    """Pre-populate cache with common questions"""
    cache = CacheManager()
    
    with Blossom(api_token="token") as client:
        for question in common_questions:
            cache_key = f"faq:{hash(question)}"
            
            if not cache.exists(cache_key):
                print(f"Warming: {question}")
                response = client.text.generate(question)
                cache.set(cache_key, response, ttl=86400)

# Warm cache at startup
common_questions = [
    "What is your return policy?",
    "How do I reset my password?",
    "What are your business hours?",
]
warm_cache(common_questions)

# Users get instant responses
```

### Tiered Caching

```python
from blossom_ai.utils import CacheManager

# Fast memory cache + persistent disk cache
cache = CacheManager(
    max_memory_items=1000,     # 1000 items in memory
    enable_disk_cache=True,    # Rest on disk
    cache_dir="./cache"
)

# First access: From API
response = cache.get("key1") or generate_and_cache("key1")

# Second access: From memory (fastest)
response = cache.get("key1")

# After restart: From disk (still fast)
response = cache.get("key1")
```

---

## 🔄 Parallel Processing

### Async Parallel Requests

```python
import asyncio
from blossom_ai import Blossom

async def parallel_generation(prompts: list[str]):
    """Generate responses in parallel"""
    async with Blossom(api_token="token") as client:
        tasks = [
            client.text.generate(prompt)
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)

# 10 requests in ~2 seconds instead of 20 seconds
prompts = [f"Question {i}" for i in range(10)]
results = asyncio.run(parallel_generation(prompts))
```

### Controlled Concurrency

```python
import asyncio
from blossom_ai import Blossom

async def controlled_parallel(
    prompts: list[str],
    max_concurrent: int = 5
):
    """Limit concurrent requests"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def generate_with_limit(prompt: str):
        async with semaphore:
            async with Blossom(api_token="token") as client:
                return await client.text.generate(prompt)
    
    tasks = [generate_with_limit(p) for p in prompts]
    return await asyncio.gather(*tasks)

# Process 100 prompts, max 5 at a time
prompts = [f"Prompt {i}" for i in range(100)]
results = asyncio.run(controlled_parallel(prompts, max_concurrent=5))
```

### Batch with Progress

```python
import asyncio
from blossom_ai import Blossom
from tqdm.asyncio import tqdm

async def batch_with_progress(items: list, batch_size: int = 10):
    """Process in batches with progress bar"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        async with Blossom(api_token="token") as client:
            tasks = [
                client.text.generate(f"Process: {item}")
                for item in batch
            ]
            batch_results = await tqdm.gather(
                *tasks,
                desc=f"Batch {i//batch_size + 1}"
            )
            results.extend(batch_results)
    
    return results

items = [f"Item {i}" for i in range(100)]
results = asyncio.run(batch_with_progress(items))
```

---

## 🎯 Request Optimization

### Minimize Token Usage

```python
from blossom_ai import Blossom

# ❌ Inefficient: Long prompt, unnecessary details
def inefficient():
    with Blossom(api_token="token") as client:
        prompt = """
        Please explain to me in great detail, with many examples,
        and comprehensive coverage of all aspects, what exactly
        is the concept of variables in programming languages.
        """
        return client.text.generate(prompt, max_tokens=2000)

# ✅ Efficient: Concise prompt
def efficient():
    with Blossom(api_token="token") as client:
        return client.text.generate(
            "Explain variables in programming briefly",
            max_tokens=200
        )
```

### Reuse System Messages

```python
from blossom_ai import Blossom

# ❌ Inefficient: Repeat system message
def inefficient_chat():
    with Blossom(api_token="token") as client:
        for question in ["Q1", "Q2", "Q3"]:
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question}
            ]
            client.text.chat(messages)

# ✅ Efficient: Maintain conversation
def efficient_chat():
    with Blossom(api_token="token") as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]
        
        for question in ["Q1", "Q2", "Q3"]:
            messages.append({"role": "user", "content": question})
            response = client.text.chat(messages)
            messages.append({"role": "assistant", "content": response})
```

### Use Lower Temperature for Deterministic Tasks

```python
from blossom_ai import Blossom

with Blossom(api_token="token") as client:
    # High temperature (creative, slower to converge)
    creative = client.text.generate(
        "Write a poem",
        temperature=0.9  # More exploration
    )
    
    # Low temperature (deterministic, faster)
    factual = client.text.generate(
        "What is 2+2?",
        temperature=0.1  # Quick, consistent answer
    )
```

### Optimize Image Generation

```python
from blossom_ai import Blossom

with Blossom(api_token="token") as client:
    # ❌ Slow: Huge image
    slow = client.image.generate(
        "a cat",
        width=2048,
        height=2048,
        quality="hd"
    )
    
    # ✅ Fast: Appropriate size
    fast = client.image.generate(
        "a cat",
        width=512,
        height=512,
        quality="medium"
    )
```

---

## 💰 Cost Optimization

### Monitor Token Usage

```python
from blossom_ai import Blossom

def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars)"""
    return len(text) // 4

# Before calling API
prompt = "Your long prompt here..."
estimated = estimate_tokens(prompt)
print(f"Estimated tokens: {estimated}")

if estimated > 1000:
    print("⚠️ Warning: High token usage")
```

### Use Smaller Models When Possible

```python
from blossom_ai import Blossom

with Blossom(api_token="token") as client:
    # Simple task: Use efficient model
    simple = client.text.generate(
        "What is 2+2?",
        model="openai"  # Fast, cheap
    )
    
    # Complex task: Use powerful model if needed
    complex = client.text.generate(
        "Design a distributed system",
        model="openai"  # More capable
    )
```

### Cache Expensive Operations

```python
from blossom_ai.utils import cached, CacheManager

# Track cache savings
cache = CacheManager()

@cached(ttl=3600)
def expensive_operation(prompt: str) -> str:
    with Blossom(api_token="token") as client:
        return client.text.generate(prompt, max_tokens=1000)

# Make many calls
for i in range(100):
    result = expensive_operation("Same question")  # Only 1 API call!

# Check savings
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate}%")
print(f"API calls saved: {stats.hits}")
```

### Batch Processing Savings

```python
import asyncio
from blossom_ai import Blossom

async def batch_savings_demo():
    """Demonstrate cost savings from batching"""
    
    # Without batching: 10 separate client instances
    # More overhead, slower
    async def without_batching():
        results = []
        for i in range(10):
            async with Blossom(api_token="token") as client:
                result = await client.text.generate(f"Q{i}")
                results.append(result)
        return results
    
    # With batching: 1 client instance
    # Less overhead, faster, cheaper
    async def with_batching():
        async with Blossom(api_token="token") as client:
            tasks = [
                client.text.generate(f"Q{i}")
                for i in range(10)
            ]
            return await asyncio.gather(*tasks)
    
    return await with_batching()

asyncio.run(batch_savings_demo())
```

---

## 📊 Benchmarking

### Basic Benchmarking

```python
import time
from blossom_ai import Blossom

def benchmark_generation():
    """Benchmark text generation"""
    with Blossom(api_token="token") as client:
        # Warm up
        client.text.generate("test")
        
        # Benchmark
        times = []
        for _ in range(10):
            start = time.time()
            client.text.generate("Explain AI")
            elapsed = time.time() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min: {min(times):.3f}s")
        print(f"Max: {max(times):.3f}s")

benchmark_generation()
```

### Compare Strategies

```python
import time
import asyncio
from blossom_ai import Blossom

def benchmark_strategies():
    """Compare sync vs async performance"""
    
    # Sync version
    start = time.time()
    with Blossom(api_token="token") as client:
        for i in range(5):
            client.text.generate(f"Question {i}")
    sync_time = time.time() - start
    
    # Async version
    async def async_version():
        async with Blossom(api_token="token") as client:
            tasks = [
                client.text.generate(f"Question {i}")
                for i in range(5)
            ]
            await asyncio.gather(*tasks)
    
    start = time.time()
    asyncio.run(async_version())
    async_time = time.time() - start
    
    print(f"Sync: {sync_time:.3f}s")
    print(f"Async: {async_time:.3f}s")
    print(f"Speed improvement: {sync_time/async_time:.1f}x")

benchmark_strategies()
```

### Cache Performance

```python
import time
from blossom_ai import Blossom
from blossom_ai.utils import cached, CacheManager

def benchmark_cache():
    """Benchmark cache performance"""
    
    @cached(ttl=3600)
    def cached_gen(prompt: str):
        with Blossom(api_token="token") as client:
            return client.text.generate(prompt)
    
    # First call (no cache)
    start = time.time()
    result = cached_gen("Test prompt")
    first_time = time.time() - start
    
    # Second call (cached)
    times = []
    for _ in range(100):
        start = time.time()
        result = cached_gen("Test prompt")
        elapsed = time.time() - start
        times.append(elapsed)
    
    avg_cached = sum(times) / len(times)
    
    print(f"First call (API): {first_time:.3f}s")
    print(f"Cached calls (avg): {avg_cached:.6f}s")
    print(f"Speed improvement: {first_time/avg_cached:.0f}x")

benchmark_cache()
```

### Memory Profiling

```python
import psutil
import os
from blossom_ai import Blossom

def profile_memory():
    """Profile memory usage"""
    process = psutil.Process(os.getpid())
    
    # Baseline
    mem_before = process.memory_info().rss / 1024 / 1024
    
    # Generate many images
    with Blossom(api_token="token") as client:
        for i in range(10):
            image = client.image.generate(
                f"Test {i}",
                width=512,
                height=512
            )
            # Save and clear
            with open(f"temp_{i}.png", "wb") as f:
                f.write(image)
            del image
    
    # After
    mem_after = process.memory_info().rss / 1024 / 1024
    
    print(f"Memory before: {mem_before:.2f} MB")
    print(f"Memory after: {mem_after:.2f} MB")
    print(f"Memory increase: {mem_after - mem_before:.2f} MB")

profile_memory()
```

---

## 🎯 Performance Checklist

### Before Production

- [ ] Implement caching for repeated queries
- [ ] Use async for parallel operations
- [ ] Enable streaming where appropriate
- [ ] Optimize token usage
- [ ] Set appropriate timeouts
- [ ] Limit concurrent connections
- [ ] Monitor memory usage
- [ ] Implement retry logic
- [ ] Track cache hit rates
- [ ] Benchmark critical paths

### Optimization Priorities

1. **Cache First** - Biggest impact (2000x faster)
2. **Parallelize** - Next biggest (3-10x faster)
3. **Stream** - Improve UX (perceived instant)
4. **Optimize Requests** - Reduce costs (20-50%)
5. **Monitor & Iterate** - Continuous improvement

---

## 🔗 Related Documentation

- [Caching Guide](CACHING.md) - Deep dive into caching
- [Async Guide](ASYNC_GUIDE.md) - Async best practices
- [Resource Management](RESOURCE_MANAGEMENT.md) - Manage resources efficiently
- [Configuration](CONFIGURATION.md) - Optimize configuration

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Caching](CACHING.md) | [Async Guide](ASYNC_GUIDE.md) →

</div>