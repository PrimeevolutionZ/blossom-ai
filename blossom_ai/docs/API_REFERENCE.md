# API Reference

This section provides a high-level overview of the main classes and methods in the Blossom AI SDK.

## `Blossom` Class

The main entry point for the SDK. It manages the connection to the Pollinations.AI services.

### Initialization

```python
Blossom(api_token: str = None, **kwargs)
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_token` | `str` | Your Pollinations.AI API token. Required for some features (e.g., Audio Generation). |
| `**kwargs` | `dict` | Additional keyword arguments for configuration. |

### Context Management

The `Blossom` class supports synchronous and asynchronous context management.

| Method | Description |
| :--- | :--- |
| `with Blossom() as ai:` | Synchronous context manager for automatic resource cleanup. |
| `async with Blossom() as ai:` | Asynchronous context manager for automatic resource cleanup. |
| `ai.close()` | Manually closes the client's session (use primarily in async code outside a context manager). |

## `ai.image` Module

Methods for image generation.

| Method | Signature | Description |
| :--- | :--- | :--- |
| `generate_url` | `generate_url(prompt: str, **kwargs) -> str` | Instantly generates a direct image URL without downloading the image bytes. |
| `generate` | `generate(prompt: str, **kwargs) -> bytes` | Generates the image and returns the raw image bytes. |
| `save` | `save(prompt: str, output_path: str, **kwargs) -> None` | Generates the image and saves it to the specified file path. |

**Common `**kwargs` for Image Generation:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `model` | `str` | The image generation model to use (e.g., `"flux"`). |
| `width` | `int` | The width of the generated image. |
| `height` | `int` | The height of the generated image. |
| `seed` | `int` | A seed for reproducible results. |
| `nologo` | `bool` | If `True`, removes the watermark. |
| `private` | `bool` | If `True`, generates a private image. |

## `ai.text` Module

Methods for text generation.

| Method | Signature | Description |
| :--- | :--- | :--- |
| `generate` | `generate(prompt: str, stream: bool = False, **kwargs) -> str \| Iterator[str]` | Generates text. If `stream=True`, returns an iterator of text chunks. |

## `ai.audio` Module

Methods for audio generation (Text-to-Speech). **Requires `api_token`**.

| Method | Signature | Description |
| :--- | :--- | :--- |
| `generate` | `generate(text: str, voice: str = "nova", **kwargs) -> bytes` | Generates audio and returns the raw audio bytes. |
| `save` | `save(text: str, output_path: str, voice: str = "nova", **kwargs) -> None` | Generates audio and saves it to the specified file path. |
| `voices` | `voices() -> list[str]` | Returns a list of available voices for audio generation. |
