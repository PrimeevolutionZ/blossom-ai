# Text Generation Guide

Blossom AI provides simple and unified methods for generating text and streaming the response in real-time.

## 📝 Basic Text Generation

Use the `generate()` method to get a complete text response from the AI.

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Generate text
    response = ai.text.generate("Explain quantum computing in simple terms")
    print(response)
```

## 🌊 Streaming Text Generation

For long responses or real-time user interfaces, use `stream=True` to receive the response in chunks as it is generated.

```python
from blossom_ai import Blossom

with Blossom() as ai:
    print("AI is telling a story...")
    # Stream text in real-time (with automatic timeout protection)
    for chunk in ai.text.generate("Tell me a story about a friendly robot who loves to paint", stream=True):
        print(chunk, end='', flush=True)

    print("\n--- End of Story ---")
```

### Streaming in Asynchronous Context

The streaming feature works seamlessly in asynchronous environments.

```python
import asyncio
from blossom_ai import Blossom

async def async_stream_example():
    async with Blossom() as ai:
        print("AI is streaming a poem...")
        # Stream text in async context
        async for chunk in ai.text.generate("Write a short poem about the ocean", stream=True):
            print(chunk, end='', flush=True)

asyncio.run(async_stream_example())
```
