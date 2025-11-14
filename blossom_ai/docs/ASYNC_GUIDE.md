# ⚡ Async/Await Guide

> **Build high-performance async applications with Blossom AI**

Learn how to use async/await for concurrent operations, parallel requests, and building scalable applications.

---

## 📋 Table of Contents

- [Why Async?](#why-async)
- [Quick Start](#quick-start)
- [Basic Async Operations](#basic-async-operations)
- [Parallel Requests](#parallel-requests)
- [Async Streaming](#async-streaming)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)

---

## 🌟 Why Async?

### Sync vs Async Performance

**Synchronous (Sequential):**
```python
# Takes 6 seconds (3 × 2s)
for i in range(3):
    response = client.text.generate("Question")  # 2s each
    # Total: 2s + 2s + 2s = 6s
```

**Asynchronous (Concurrent):**
```python
# Takes ~2 seconds (all run concurrently)
responses = await asyncio.gather(
    client.text.generate("Question 1"),  # 2s
    client.text.generate("Question 2"),  # 2s
    client.text.generate("Question 3"),  # 2s
)
# Total: max(2s, 2s, 2s) = 2s (3x faster!)
```

### When to Use Async

**✅ Use Async When:**
- Making multiple API calls
- Building web servers (FastAPI, aiohttp)
- Processing many items concurrently
- I/O-bound operations
- Need high throughput

**❌ Stick with Sync When:**
- Simple scripts
- Single requests
- Learning/prototyping
- CPU-bound operations

---

## 🚀 Quick Start

### Basic Async Usage

```python
import asyncio
from blossom_ai import Blossom

async def main():
    """Basic async example"""
    async with Blossom(api_token="your_token") as client:
        response = await client.text.generate("Hello, async world!")
        print(response)

# Run
asyncio.run(main())
```

### Converting Sync to Async

```python
# Sync version
from blossom_ai import Blossom

with Blossom(api_token="token") as client:
    response = client.text.generate("Hello")

# Async version
import asyncio
from blossom_ai import Blossom

async def main():
    async with Blossom(api_token="token") as client:
        response = await client.text.generate("Hello")

asyncio.run(main())
```

---

## 🔧 Basic Async Operations

### Text Generation

```python
import asyncio
from blossom_ai import Blossom

async def generate_text():
    """Async text generation"""
    async with Blossom(api_token="your_token") as client:
        # Simple generation
        response = await client.text.generate(
            "Explain async programming",
            max_tokens=200
        )
        print(response)

asyncio.run(generate_text())
```

### Image Generation

```python
import asyncio
from blossom_ai import Blossom

async def generate_image():
    """Async image generation"""
    async with Blossom(api_token="your_token") as client:
        # Generate image
        image_data = await client.image.generate(
            "a beautiful sunset",
            model="flux",
            width=1024,
            height=1024
        )
        
        # Save
        with open("sunset.png", "wb") as f:
            f.write(image_data)
        
        print(f"Saved image: {len(image_data)} bytes")

asyncio.run(generate_image())
```

### Chat Completion

```python
import asyncio
from blossom_ai import Blossom

async def chat():
    """Async chat completion"""
    async with Blossom(api_token="your_token") as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is async/await?"}
        ]
        
        response = await client.text.chat(messages, model="openai")
        print(response)

asyncio.run(chat())
```

---

## 🚀 Parallel Requests

### Multiple Text Generations

```python
import asyncio
from blossom_ai import Blossom

async def parallel_text_generation():
    """Generate multiple texts in parallel"""
    async with Blossom(api_token="your_token") as client:
        # Define tasks
        tasks = [
            client.text.generate("What is Python?"),
            client.text.generate("What is JavaScript?"),
            client.text.generate("What is Rust?"),
            client.text.generate("What is Go?"),
        ]
        
        # Run in parallel
        responses = await asyncio.gather(*tasks)
        
        # Process results
        for i, response in enumerate(responses, 1):
            print(f"\n{i}. {response[:100]}...")

asyncio.run(parallel_text_generation())
```

### Multiple Image Generations

```python
import asyncio
from blossom_ai import Blossom

async def parallel_image_generation():
    """Generate multiple images in parallel"""
    async with Blossom(api_token="your_token") as client:
        prompts = [
            "a red apple",
            "a blue ocean",
            "a green forest",
            "a yellow sun"
        ]
        
        # Create tasks
        tasks = [
            client.image.generate(prompt, model="flux", width=512, height=512)
            for prompt in prompts
        ]
        
        # Run in parallel
        images = await asyncio.gather(*tasks)
        
        # Save all images
        for i, (prompt, image_data) in enumerate(zip(prompts, images)):
            filename = f"image_{i}.png"
            with open(filename, "wb") as f:
                f.write(image_data)
            print(f"Saved {filename}: {len(image_data)} bytes")

asyncio.run(parallel_image_generation())
```

### Mixed Operations

```python
import asyncio
from blossom_ai import Blossom

async def mixed_operations():
    """Mix text and image generation"""
    async with Blossom(api_token="your_token") as client:
        # Different types of operations
        text_task = client.text.generate("Describe a sunset")
        image_task = client.image.generate("beautiful sunset", width=512, height=512)
        chat_task = client.text.chat([
            {"role": "user", "content": "Hello"}
        ])
        
        # Run all in parallel
        text, image, chat = await asyncio.gather(
            text_task,
            image_task,
            chat_task
        )
        
        print(f"Text: {text[:100]}...")
        print(f"Image: {len(image)} bytes")
        print(f"Chat: {chat[:100]}...")

asyncio.run(mixed_operations())
```

### Batch Processing

```python
import asyncio
from blossom_ai import Blossom

async def batch_process(items: list[str], batch_size: int = 5):
    """Process items in batches"""
    async with Blossom(api_token="your_token") as client:
        results = []
        
        # Process in batches
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}...")
            
            # Create tasks for batch
            tasks = [
                client.text.generate(f"Summarize: {item}")
                for item in batch
            ]
            
            # Run batch in parallel
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Optional: small delay between batches
            if i + batch_size < len(items):
                await asyncio.sleep(0.5)
        
        return results

# Usage
items = [f"Article {i}" for i in range(20)]
results = asyncio.run(batch_process(items, batch_size=5))
```

---

## 🌊 Async Streaming

### Basic Streaming

```python
import asyncio
from blossom_ai import Blossom

async def stream_text():
    """Stream text generation"""
    async with Blossom(api_token="your_token") as client:
        print("Streaming response: ", end="", flush=True)
        
        async for chunk in await client.text.generate(
            "Tell me a short story",
            stream=True
        ):
            print(chunk, end="", flush=True)
        
        print()  # New line

asyncio.run(stream_text())
```

### Stream with Processing

```python
import asyncio
from blossom_ai import Blossom

async def stream_with_processing():
    """Stream and process chunks"""
    async with Blossom(api_token="your_token") as client:
        chunks = []
        word_count = 0
        
        async for chunk in await client.text.generate(
            "Explain quantum computing",
            stream=True
        ):
            chunks.append(chunk)
            word_count += len(chunk.split())
            
            # Print progress
            print(f"\rWords: {word_count}", end="", flush=True)
        
        print()  # New line
        full_response = "".join(chunks)
        print(f"\nTotal words: {word_count}")
        print(f"Total chars: {len(full_response)}")

asyncio.run(stream_with_processing())
```

### Multiple Concurrent Streams

```python
import asyncio
from blossom_ai import Blossom

async def stream_multiple():
    """Handle multiple streams concurrently"""
    
    async def stream_one(client, prompt: str, label: str):
        """Single stream handler"""
        print(f"\n[{label}] Starting...")
        chunks = []
        
        async for chunk in await client.text.generate(prompt, stream=True):
            chunks.append(chunk)
        
        result = "".join(chunks)
        print(f"\n[{label}] Done: {len(result)} chars")
        return result
    
    async with Blossom(api_token="your_token") as client:
        # Start multiple streams
        results = await asyncio.gather(
            stream_one(client, "Count to 5", "Stream 1"),
            stream_one(client, "List 3 colors", "Stream 2"),
            stream_one(client, "Name 3 animals", "Stream 3")
        )
        
        return results

results = asyncio.run(stream_multiple())
```

---

## ⚠️ Error Handling

### Basic Error Handling

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def safe_generation():
    """Handle errors in async operations"""
    async with Blossom(api_token="your_token") as client:
        try:
            response = await client.text.generate("Hello")
            return response
        except BlossomError as e:
            print(f"API Error: {e.message}")
            print(f"Suggestion: {e.suggestion}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

asyncio.run(safe_generation())
```

### Handle Multiple Errors

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def process_with_errors():
    """Handle errors in parallel operations"""
    async with Blossom(api_token="your_token") as client:
        async def safe_generate(prompt: str):
            try:
                return await client.text.generate(prompt)
            except BlossomError as e:
                return f"Error: {e.message}"
        
        # Some may fail, others succeed
        tasks = [
            safe_generate("Valid prompt"),
            safe_generate("x" * 500),  # Too long - will fail
            safe_generate("Another valid prompt"),
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Process results
        for i, result in enumerate(results):
            if result.startswith("Error:"):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} succeeded: {result[:50]}...")

asyncio.run(process_with_errors())
```

### Retry Logic

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def generate_with_retry(
    client: Blossom,
    prompt: str,
    max_retries: int = 3
) -> str:
    """Retry failed requests with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await client.text.generate(prompt)
        except BlossomError as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                print(f"Attempt {attempt + 1} failed, retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                print(f"All {max_retries} attempts failed")
                raise

# Usage
async def main():
    async with Blossom(api_token="your_token") as client:
        response = await generate_with_retry(client, "Hello")
        print(response)

asyncio.run(main())
```

### Timeout Handling

```python
import asyncio
from blossom_ai import Blossom

async def with_timeout():
    """Handle operation timeouts"""
    async with Blossom(api_token="your_token") as client:
        try:
            # Set timeout (5 seconds)
            response = await asyncio.wait_for(
                client.text.generate("Long response..."),
                timeout=5.0
            )
            print(response)
        except asyncio.TimeoutError:
            print("Request timed out after 5 seconds")

asyncio.run(with_timeout())
```

---

## ✅ Best Practices

### 1. Always Use Context Managers

```python
import asyncio
from blossom_ai import Blossom

# ✅ GOOD: Automatic cleanup
async def good_practice():
    async with Blossom(api_token="token") as client:
        return await client.text.generate("Hello")

# ❌ BAD: Manual cleanup
async def bad_practice():
    client = Blossom(api_token="token")
    response = await client.text.generate("Hello")
    await client.close()  # Easy to forget!
    return response
```

### 2. Limit Concurrency

```python
import asyncio
from blossom_ai import Blossom

async def limited_concurrency(items: list, max_concurrent: int = 5):
    """Limit number of concurrent operations"""
    async with Blossom(api_token="token") as client:
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_limit(item):
            async with semaphore:
                return await client.text.generate(f"Process: {item}")
        
        # Only max_concurrent tasks run at once
        tasks = [process_with_limit(item) for item in items]
        return await asyncio.gather(*tasks)

# Process 100 items, max 5 at a time
items = [f"Item {i}" for i in range(100)]
results = asyncio.run(limited_concurrency(items, max_concurrent=5))
```

### 3. Handle Partial Failures

```python
import asyncio
from blossom_ai import Blossom

async def handle_partial_failures():
    """Continue even if some tasks fail"""
    async with Blossom(api_token="token") as client:
        tasks = [
            client.text.generate("Valid 1"),
            client.text.generate("x" * 500),  # May fail
            client.text.generate("Valid 2"),
        ]
        
        # return_exceptions=True prevents gather from failing
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successes = []
        failures = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failures.append((i, str(result)))
            else:
                successes.append((i, result))
        
        print(f"Successes: {len(successes)}")
        print(f"Failures: {len(failures)}")
        
        return successes, failures

asyncio.run(handle_partial_failures())
```

### 4. Use Task Groups (Python 3.11+)

```python
import asyncio
from blossom_ai import Blossom

async def use_task_groups():
    """Modern task management with TaskGroup"""
    async with Blossom(api_token="token") as client:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(client.text.generate("Question 1"))
            task2 = tg.create_task(client.text.generate("Question 2"))
            task3 = tg.create_task(client.text.generate("Question 3"))
        
        # All tasks completed here
        return [task1.result(), task2.result(), task3.result()]

# Python 3.11+
results = asyncio.run(use_task_groups())
```

### 5. Progress Tracking

```python
import asyncio
from blossom_ai import Blossom
from tqdm.asyncio import tqdm

async def with_progress(items: list):
    """Show progress bar"""
    async with Blossom(api_token="token") as client:
        async def process_item(item):
            result = await client.text.generate(f"Process: {item}")
            return result
        
        # Process with progress bar
        tasks = [process_item(item) for item in items]
        results = await tqdm.gather(*tasks, desc="Processing")
        
        return results

items = [f"Item {i}" for i in range(20)]
asyncio.run(with_progress(items))
```

---

## 🏗️ Real-World Examples

### Example 1: Async Web Server (FastAPI)

```python
from fastapi import FastAPI, BackgroundTasks
from blossom_ai import Blossom
import asyncio

app = FastAPI()

@app.get("/generate")
async def generate_text(prompt: str):
    """Async endpoint"""
    async with Blossom(api_token="your_token") as client:
        response = await client.text.generate(prompt)
        return {"response": response}

@app.post("/batch")
async def batch_generate(prompts: list[str]):
    """Process multiple prompts"""
    async with Blossom(api_token="your_token") as client:
        tasks = [client.text.generate(p) for p in prompts]
        responses = await asyncio.gather(*tasks)
        return {"responses": responses}
```

### Example 2: Data Processing Pipeline

```python
import asyncio
from blossom_ai import Blossom

async def process_pipeline(data_items: list):
    """Multi-stage async pipeline"""
    async with Blossom(api_token="your_token") as client:
        # Stage 1: Analyze
        print("Stage 1: Analyzing...")
        analyze_tasks = [
            client.text.generate(f"Analyze: {item}")
            for item in data_items
        ]
        analyses = await asyncio.gather(*analyze_tasks)
        
        # Stage 2: Summarize
        print("Stage 2: Summarizing...")
        summarize_tasks = [
            client.text.generate(f"Summarize: {analysis}")
            for analysis in analyses
        ]
        summaries = await asyncio.gather(*summarize_tasks)
        
        # Stage 3: Generate report
        print("Stage 3: Generating report...")
        combined = "\n\n".join(summaries)
        report = await client.text.generate(
            f"Create final report from:\n{combined}"
        )
        
        return report

# Usage
data = ["Data 1", "Data 2", "Data 3"]
report = asyncio.run(process_pipeline(data))
```

### Example 3: Real-time Chat Application

```python
import asyncio
from blossom_ai import Blossom

class AsyncChatBot:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.conversation_history = []
    
    async def chat(self, message: str) -> str:
        """Async chat with history"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        async with Blossom(api_token=self.api_token) as client:
            response = await client.text.chat(
                self.conversation_history,
                model="openai"
            )
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    async def chat_stream(self, message: str):
        """Streaming chat"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        async with Blossom(api_token=self.api_token) as client:
            chunks = []
            async for chunk in await client.text.chat(
                self.conversation_history,
                stream=True
            ):
                chunks.append(chunk)
                yield chunk
            
            full_response = "".join(chunks)
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })

# Usage
async def main():
    bot = AsyncChatBot("your_token")
    
    # Regular chat
    response = await bot.chat("Hello!")
    print(f"Bot: {response}")
    
    # Streaming chat
    print("Bot (streaming): ", end="", flush=True)
    async for chunk in bot.chat_stream("Tell me a joke"):
        print(chunk, end="", flush=True)
    print()

asyncio.run(main())
```

---

## 🔗 Related Documentation

- [Configuration](CONFIGURATION.md) - Configure async client
- [Error Handling](ERROR_HANDLING.md) - Handle async errors
- [Resource Management](RESOURCE_MANAGEMENT.md) - Manage async resources
- [Performance](PERFORMANCE.md) - Optimize async performance

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Configuration](CONFIGURATION.md) | [Resource Management](RESOURCE_MANAGEMENT.md) →

</div>