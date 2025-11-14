# 🔧 Resource Management Guide

> **Properly manage resources, connections, and memory in Blossom AI applications**

Learn best practices for managing client lifecycle, connections, memory, and resources to build reliable, production-ready applications.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Client Lifecycle](#client-lifecycle)
- [Connection Management](#connection-management)
- [Memory Management](#memory-management)
- [Best Practices](#best-practices)
- [Production Patterns](#production-patterns)

---

## 🌟 Overview

### Why Resource Management Matters

**Problems Without Proper Management:**
- 💥 Memory leaks
- 🔌 Unclosed connections
- 🐌 Performance degradation
- ❌ Resource exhaustion

**Benefits of Good Management:**
- ✅ Predictable memory usage
- ✅ Proper connection cleanup
- ✅ Stable long-running applications
- ✅ Efficient resource utilization

---

## 🔄 Client Lifecycle

### Context Manager (Recommended)

```python
from blossom_ai import Blossom

# ✅ BEST: Automatic cleanup
with Blossom(api_token="your_token") as client:
    response = client.text.generate("Hello")
    # Client automatically closed after block
```

### Manual Management

```python
from blossom_ai import Blossom

# Create client
client = Blossom(api_token="your_token")

try:
    response = client.text.generate("Hello")
finally:
    # Always clean up
    client.close_sync()
```

### Async Context Manager

```python
import asyncio
from blossom_ai import Blossom

async def main():
    # ✅ Automatic async cleanup
    async with Blossom(api_token="your_token") as client:
        response = await client.text.generate("Hello")
        # Client automatically closed

asyncio.run(main())
```

### Long-Lived Client

```python
from blossom_ai import Blossom

class Service:
    """Service with long-lived client"""
    
    def __init__(self, api_token: str):
        self.client = Blossom(api_token=api_token)
    
    def generate(self, prompt: str) -> str:
        """Use client"""
        return self.client.text.generate(prompt)
    
    def close(self):
        """Clean up resources"""
        self.client.close_sync()

# Usage
service = Service("your_token")
try:
    response = service.generate("Hello")
finally:
    service.close()
```

### With Dependency Injection

```python
from blossom_ai import Blossom
from contextlib import contextmanager

@contextmanager
def get_client(api_token: str):
    """Provide client with cleanup"""
    client = Blossom(api_token=api_token)
    try:
        yield client
    finally:
        client.close_sync()

# Usage
with get_client("your_token") as client:
    response = client.text.generate("Hello")
```

---

## 🔌 Connection Management

### Connection Pooling (Async)

```python
import asyncio
from blossom_ai import Blossom

class ConnectionPool:
    """Manage multiple async clients"""
    
    def __init__(self, api_token: str, pool_size: int = 5):
        self.api_token = api_token
        self.pool_size = pool_size
        self.semaphore = asyncio.Semaphore(pool_size)
    
    async def execute(self, task):
        """Execute task with connection limit"""
        async with self.semaphore:
            async with Blossom(api_token=self.api_token) as client:
                return await task(client)

# Usage
async def main():
    pool = ConnectionPool("your_token", pool_size=3)
    
    async def generate(client):
        return await client.text.generate("Hello")
    
    # Only 3 connections at a time
    tasks = [pool.execute(generate) for _ in range(10)]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Reusable Client Pattern

```python
from blossom_ai import Blossom
import threading

class ClientManager:
    """Thread-safe client manager"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self._client = None
        self._lock = threading.Lock()
    
    def get_client(self) -> Blossom:
        """Get or create client"""
        with self._lock:
            if self._client is None:
                self._client = Blossom(api_token=self.api_token)
            return self._client
    
    def close(self):
        """Close client"""
        with self._lock:
            if self._client is not None:
                self._client.close_sync()
                self._client = None

# Usage
manager = ClientManager("your_token")
try:
    client = manager.get_client()
    response = client.text.generate("Hello")
finally:
    manager.close()
```

### Connection Timeout Handling

```python
import asyncio
from blossom_ai import Blossom

async def with_timeout(api_token: str, timeout: int = 30):
    """Handle connection timeouts"""
    async with Blossom(api_token=api_token, timeout=timeout) as client:
        try:
            # Set operation timeout
            response = await asyncio.wait_for(
                client.text.generate("Hello"),
                timeout=timeout
            )
            return response
        except asyncio.TimeoutError:
            print(f"Operation timed out after {timeout}s")
            return None

asyncio.run(with_timeout("your_token"))
```

---

## 💾 Memory Management

### Image Data Management

```python
from blossom_ai import Blossom
import gc

def generate_and_save_image(prompt: str, filename: str):
    """Generate image with proper memory cleanup"""
    with Blossom(api_token="your_token") as client:
        # Generate image
        image_data = client.image.generate(
            prompt,
            width=1024,
            height=1024
        )
        
        # Save immediately
        with open(filename, "wb") as f:
            f.write(image_data)
        
        # Clear image data from memory
        del image_data
        gc.collect()
        
        print(f"Saved {filename}")

# Usage
generate_and_save_image("sunset", "sunset.png")
```

### Streaming for Large Responses

```python
from blossom_ai import Blossom

def stream_to_file(prompt: str, output_file: str):
    """Stream response directly to file"""
    with Blossom(api_token="your_token") as client:
        with open(output_file, "w") as f:
            for chunk in client.text.generate(prompt, stream=True):
                f.write(chunk)
                # Chunk is immediately written and can be GC'd

stream_to_file("Write a long story", "story.txt")
```

### Cache Memory Limits

```python
from blossom_ai.utils import CacheManager

# Limit memory cache size
cache = CacheManager(
    max_memory_items=100,  # Only 100 items in memory
    enable_disk_cache=True  # Rest goes to disk
)

# Monitor memory usage
stats = cache.get_stats()
print(f"Memory items: {stats.total_requests}")

# Clear old entries
cache.clear()
```

### Batch Processing with Memory Limits

```python
import asyncio
from blossom_ai import Blossom

async def process_in_batches(
    items: list,
    batch_size: int = 10
):
    """Process items in batches to limit memory"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}...")
        
        async with Blossom(api_token="your_token") as client:
            # Process batch
            batch_results = await asyncio.gather(*[
                client.text.generate(f"Process: {item}")
                for item in batch
            ])
            
            results.extend(batch_results)
        
        # Client closed, memory freed
        # Optional: explicit GC
        import gc
        gc.collect()
    
    return results

# Process 1000 items in batches of 10
items = [f"Item {i}" for i in range(1000)]
results = asyncio.run(process_in_batches(items, batch_size=10))
```

---

## ✅ Best Practices

### 1. Always Use Context Managers

```python
from blossom_ai import Blossom

# ✅ GOOD: Automatic cleanup
def good_practice():
    with Blossom(api_token="token") as client:
        return client.text.generate("Hello")

# ❌ BAD: Manual cleanup (error-prone)
def bad_practice():
    client = Blossom(api_token="token")
    response = client.text.generate("Hello")
    client.close_sync()  # What if error occurs before this?
    return response
```

### 2. Limit Concurrent Connections

```python
import asyncio
from blossom_ai import Blossom

async def with_semaphore(items: list, max_concurrent: int = 5):
    """Limit concurrent connections"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_item(item):
        async with semaphore:
            async with Blossom(api_token="token") as client:
                return await client.text.generate(f"Process: {item}")
    
    return await asyncio.gather(*[process_item(i) for i in items])
```

### 3. Handle Resource Cleanup in Errors

```python
from blossom_ai import Blossom

def safe_resource_usage():
    """Ensure cleanup even on errors"""
    client = None
    try:
        client = Blossom(api_token="token")
        response = client.text.generate("Hello")
        return response
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        if client is not None:
            client.close_sync()
```

### 4. Monitor Resource Usage

```python
import psutil
import os
from blossom_ai import Blossom

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process(os.getpid())
    
    # Before
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Execute
    with Blossom(api_token="token") as client:
        for i in range(100):
            response = client.text.generate("Hello")
    
    # After
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Memory before: {mem_before:.2f} MB")
    print(f"Memory after: {mem_after:.2f} MB")
    print(f"Memory increase: {mem_after - mem_before:.2f} MB")

monitor_memory()
```

### 5. Implement Health Checks

```python
from blossom_ai import Blossom

class HealthMonitor:
    """Monitor client health"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.client = None
        self.is_healthy = False
    
    def check_health(self) -> bool:
        """Check if client is healthy"""
        try:
            if self.client is None:
                self.client = Blossom(api_token=self.api_token)
            
            # Test connection
            self.client.text.models()
            self.is_healthy = True
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            self.is_healthy = False
            self.close()
            return False
    
    def close(self):
        """Close client"""
        if self.client is not None:
            try:
                self.client.close_sync()
            except:
                pass
            finally:
                self.client = None

# Usage
monitor = HealthMonitor("your_token")
if monitor.check_health():
    print("Client is healthy")
```

---

## 🏭 Production Patterns

### Pattern 1: Singleton Client

```python
from blossom_ai import Blossom
import threading

class SingletonClient:
    """Thread-safe singleton client"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, api_token: str):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.client = Blossom(api_token=api_token)
        return cls._instance
    
    def generate(self, prompt: str) -> str:
        return self.client.text.generate(prompt)
    
    @classmethod
    def close(cls):
        """Close singleton client"""
        if cls._instance is not None:
            with cls._lock:
                if cls._instance is not None:
                    cls._instance.client.close_sync()
                    cls._instance = None

# Usage
client = SingletonClient("your_token")
response = client.generate("Hello")

# Clean up at app shutdown
SingletonClient.close()
```

### Pattern 2: Factory Pattern

```python
from blossom_ai import Blossom
from typing import Protocol

class ClientFactory:
    """Create clients with consistent configuration"""
    
    def __init__(self, api_token: str, default_timeout: int = 30):
        self.api_token = api_token
        self.default_timeout = default_timeout
    
    def create_text_client(self) -> Blossom:
        """Create client for text operations"""
        return Blossom(
            api_token=self.api_token,
            timeout=self.default_timeout
        )
    
    def create_image_client(self) -> Blossom:
        """Create client for image operations"""
        return Blossom(
            api_token=self.api_token,
            timeout=120  # Longer timeout for images
        )

# Usage
factory = ClientFactory("your_token")

with factory.create_text_client() as client:
    text = client.text.generate("Hello")

with factory.create_image_client() as client:
    image = client.image.generate("sunset")
```

### Pattern 3: Service Layer

```python
from blossom_ai import Blossom
from contextlib import contextmanager

class AIService:
    """Service layer for AI operations"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
    
    @contextmanager
    def _get_client(self):
        """Internal client manager"""
        client = Blossom(api_token=self.api_token)
        try:
            yield client
        finally:
            client.close_sync()
    
    def generate_text(self, prompt: str) -> str:
        """Public text generation"""
        with self._get_client() as client:
            return client.text.generate(prompt)
    
    def generate_image(self, prompt: str) -> bytes:
        """Public image generation"""
        with self._get_client() as client:
            return client.image.generate(prompt)

# Usage
service = AIService("your_token")
text = service.generate_text("Hello")
image = service.generate_image("sunset")
```

### Pattern 4: Worker Pool

```python
import asyncio
from blossom_ai import Blossom
from asyncio import Queue

class WorkerPool:
    """Pool of workers for processing tasks"""
    
    def __init__(self, api_token: str, num_workers: int = 3):
        self.api_token = api_token
        self.num_workers = num_workers
        self.queue = Queue()
        self.results = []
    
    async def worker(self, worker_id: int):
        """Worker process"""
        async with Blossom(api_token=self.api_token) as client:
            while True:
                task = await self.queue.get()
                if task is None:  # Poison pill
                    break
                
                try:
                    result = await client.text.generate(task)
                    self.results.append((task, result))
                except Exception as e:
                    self.results.append((task, f"Error: {e}"))
                finally:
                    self.queue.task_done()
    
    async def process(self, tasks: list) -> list:
        """Process tasks with worker pool"""
        # Add tasks to queue
        for task in tasks:
            await self.queue.put(task)
        
        # Start workers
        workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]
        
        # Wait for all tasks
        await self.queue.join()
        
        # Stop workers
        for _ in range(self.num_workers):
            await self.queue.put(None)
        
        await asyncio.gather(*workers)
        
        return self.results

# Usage
async def main():
    pool = WorkerPool("your_token", num_workers=3)
    tasks = [f"Task {i}" for i in range(20)]
    results = await pool.process(tasks)
    print(f"Processed {len(results)} tasks")

asyncio.run(main())
```

### Pattern 5: Circuit Breaker

```python
from blossom_ai import Blossom
import time

class CircuitBreaker:
    """Prevent cascading failures"""
    
    def __init__(
        self,
        api_token: str,
        failure_threshold: int = 5,
        timeout: int = 60
    ):
        self.api_token = api_token
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        """Execute with circuit breaker"""
        if self.state == "OPEN":
            # Check if timeout passed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            with Blossom(api_token=self.api_token) as client:
                result = func(client, *args, **kwargs)
            
            # Success - reset
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            
            raise

# Usage
breaker = CircuitBreaker("your_token")

def generate(client, prompt):
    return client.text.generate(prompt)

try:
    result = breaker.call(generate, "Hello")
except Exception as e:
    print(f"Circuit breaker activated: {e}")
```

---

## 🔗 Related Documentation

- [Configuration](CONFIGURATION.md) - Configure client properly
- [Async Guide](ASYNC_GUIDE.md) - Async resource management
- [Error Handling](ERROR_HANDLING.md) - Handle resource errors
- [Performance](PERFORMANCE.md) - Optimize resource usage

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Configuration](CONFIGURATION.md) | [Async Guide](ASYNC_GUIDE.md) →

</div>