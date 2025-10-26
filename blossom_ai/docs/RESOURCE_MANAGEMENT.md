# Resource Management & Best Practices

Blossom AI automatically manages resources, but for best practices use context managers to ensure proper cleanup, especially in long-running or asynchronous applications.

## ✅ Recommended: Use Context Managers

Using `with` (for synchronous code) or `async with` (for asynchronous code) ensures that the underlying HTTP sessions are closed correctly, preventing resource leaks.

### Synchronous Context Manager

```python
from blossom_ai import Blossom

# Synchronous - automatic cleanup
with Blossom() as ai:
    url = ai.image.generate_url("sunset")
    image = ai.image.generate("sunset")
    # Resources automatically cleaned up on exit
```

### Asynchronous Context Manager

```python
import asyncio
from blossom_ai import Blossom

async def run_async_example():
    # Asynchronous - automatic cleanup
    async with Blossom() as ai:
        url = await ai.image.generate_url("sunset")
        image = await ai.image.generate("sunset")
        # Async resources properly closed

asyncio.run(run_async_example())
```

## Manual Cleanup (if needed)

While context managers are recommended, you can manually close the client if necessary.

### Asynchronous Manual Cleanup

```python
from blossom_ai import Blossom

client = Blossom()
try:
    # Perform async operations
    # url = await client.image.generate_url("test")
    pass
finally:
    # Explicitly close async sessions
    await client.close()
```

### Synchronous Manual Cleanup

Sync sessions are generally cleaned up automatically at program exit, but the context manager is still the most explicit and reliable method.

```python
from blossom_ai import Blossom

client = Blossom()
url = client.image.generate_url("test")
# Sync sessions cleaned up automatically via atexit hook
```

## For Long-Running Applications (e.g., Bots)

In asynchronous applications, be mindful of how you manage the event loop and client lifecycle.

```python
import asyncio
from blossom_ai import Blossom

# ✅ Good: Single command handler using a context manager
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
    print(results)

# asyncio.run(main()) # Run the main function once per application start

# ❌ Avoid: Multiple asyncio.run() calls
# This creates/destroys event loops repeatedly, leaving resources
def bad_example():
    asyncio.run(bot_command("cat"))   # Creates loop #1
    asyncio.run(bot_command("dog"))   # Creates loop #2 - may leave resources
    asyncio.run(bot_command("bird"))  # Creates loop #3 - may leave resources
```

## ⚠️ Important Notes

- **Resource Management**: Always use context managers (`with`/`async with`) for proper cleanup.
- **Event Loops**: Avoid multiple `asyncio.run()` calls - use one event loop per application run.
- **Audio Generation**: Requires authentication (API token).
- **Hybrid API**: Automatically detects sync/async context - no need for separate imports.
- **Streaming**: Works in both sync and async contexts with iterators.
- **Stream Timeout**: Default 30 seconds between chunks - automatically raises an error if no data is received.
- **Robust Error Handling**: Graceful fallbacks when API endpoints are unavailable.
