# 📝 Changelog

> **Beautiful Python SDK for Pollinations.AI**  
> Track the evolution of Blossom AI across versions

---

## 🌸 v0.5.2 — *Audio & Stability* (November 2024)

> **New TTS Support & Critical Fixes**  
> This release adds proper text-to-speech generation and resolves major audio/modalities parameter issues.

### 🎯 What's New

**🔊 Text-to-Speech (TTS) Support**
- NEW: Dedicated `AudioGenerator` and `AsyncAudioGenerator` classes
- Generate MP3 audio from text using Pollinations TTS endpoint
- 6 premium voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`
- Simple API: `client.audio.generate(text, voice="alloy")`
- No authentication required for TTS endpoint
- Save directly to file: `client.audio.save(text, "output.mp3", voice="nova")`

**Example:**
```python
from blossom_ai import Blossom

with Blossom() as client:
    # Generate audio
    audio_data = client.audio.generate(
        "Hello, world! This is text-to-speech.",
        voice="nova"
    )
    
    # Or save directly
    client.audio.save(
        "Welcome to Blossom AI!",
        "welcome.mp3",
        voice="alloy"
    )
```

---

### 🐛 Critical Fixes

**Audio/Modalities Parameters Removed from Chat**
- ⚠️ **BREAKING FIX**: Removed unsupported `audio` and `modalities` parameters from text chat
- These parameters were causing API errors as Pollinations doesn't support audio input in chat messages
- Added clear warning messages when users try to use these parameters
- Updated `MessageBuilder.audio()` to raise `NotImplementedError` with helpful guidance

**Before (❌ Would fail):**
```python
# This would silently fail or cause errors
response = client.text.chat(
    messages=[...],
    audio={"voice": "alloy"},  # NOT SUPPORTED
    modalities=["text", "audio"]  # NOT SUPPORTED
)
```

**After (✅ Correct usage):**
```python
# For TTS, use the audio endpoint:
audio = client.audio.generate("Hello!", voice="alloy")

# For chat, use standard text/vision:
response = client.text.chat(
    messages=[MessageBuilder.text("user", "Hello!")],
    model="openai"
)
```

**Image Generation 520 Error Handling**
- Added automatic retry logic for HTTP 520 errors (server timeout)
- Exponential backoff: 1s, 2s, 4s between retries
- Up to 3 attempts before failing
- Applies to both sync and async image generators

---

### 🔧 API Improvements

**Parameter Validation**
- Enhanced validation for audio voices and formats
- Better error messages with actionable suggestions
- Reasoning effort validation (`low`, `medium`, `high`)
- Updated `AudioParamsV2` with proper voice/format validation

**Model Updates**
- Added new models: `mistral-fast`, `claude-large`, `grok`
- Updated default model lists for better coverage
- Improved model fetching and caching

**Code Quality**
- Removed unused debug print statements
- Cleaner parameter building in generators
- Better type hints and documentation
- Fixed import organization

---

### 📚 Documentation Updates

**Updated Examples**
```python
# TTS Generation
client.audio.generate("Text to speak", voice="nova")

# Image with retry on 520
image = client.image.generate("A sunset", model="flux")

# Chat without unsupported params
response = client.text.chat(
    messages=[MessageBuilder.text("user", "Hello")],
    model="openai",
    temperature=0.7
)
```

---

### ⚠️ Breaking Changes

**Removed from Text Chat:**
- `audio` parameter (use `client.audio.generate()` instead)
- `modalities` parameter (not supported by Pollinations API)
- `MessageBuilder.audio()` now raises `NotImplementedError`

**Migration Guide:**
```python
# OLD (v0.5.0-0.5.1) - Would fail
response = client.text.chat(
    messages=[...],
    audio={"voice": "alloy"},
    modalities=["text", "audio"]
)

# NEW (v0.5.2) - Correct approach
# For audio generation:
audio = client.audio.generate("Hello!", voice="alloy")

# For chat (text/vision only):
response = client.text.chat(
    messages=[MessageBuilder.text("user", "Hello!")]
)
```

---

### 🎨 New Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| TTS Support | ✅ NEW | Generate speech from text |
| Audio Voices | ✅ NEW | 6 premium voice options |
| 520 Retry Logic | ✅ NEW | Auto-retry on server timeout |
| Parameter Cleanup | ✅ FIXED | Removed unsupported params |
| Voice Validation | ✅ NEW | Validate audio parameters |
| Error Messages | ✅ IMPROVED | Better user guidance |

---

### 🔗 Links

- [PyPI Package](https://pypi.org/project/eclips-blossom-ai/)
- [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)
- [Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)
- [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

---

## 🌸 v0.5.0 — *The Grand Rewrite* (December 2024)

> **A Complete Transformation**  
> No words are enough to describe all the changes that happened between v0.4.7 and v0.5.0.  
> The entire core has been rewritten from the ground up, with new architecture, new capabilities, and a completely new internal structure.

### 🎯 What's New

This release represents a **fundamental reimagining** of Blossom AI. Here's what changed:

---

### ⚡ Core Architecture

**Complete Rewrite**
- 🔄 Entirely new core architecture built from scratch
- 🗃️ Modular design with clear separation of concerns
- 🧩 Clean abstractions for sync and async operations
- 🎭 Unified client that works seamlessly in both modes

**Session Management**
- 🔌 Smart connection pooling with automatic cleanup
- 💾 Memory-safe session handling (no leaks!)
- 🔄 Automatic retry with intelligent backoff
- 🎯 Per-event-loop async session management

**Error Handling**
- 📊 Rich error context with detailed information
- 💡 Actionable suggestions for every error type
- 🔍 Request tracing with unique IDs
- 🛡️ Graceful degradation on failures

---

### 🆕 Major Features

**👁️ Vision Support (NEW!)**
- Analyze images with AI models
- Support for URLs and local files
- Multiple images in single request
- Adjustable detail levels (low/auto/high)

**🎨 Enhanced Image Generation**
- Quality levels: `low`, `medium`, `high`, `hd`
- Guidance scale control (1.0-20.0)
- Negative prompts for better control
- Transparent background support
- Image-to-image transformation
- URL generation (no download needed)

**💬 Advanced Text Features**
- Function calling / Tool use
- Structured JSON output
- Native reasoning support (V2 OpenAI models)
- Extended temperature range (0-2)
- Advanced parameters: `max_tokens`, `frequency_penalty`, `presence_penalty`, `top_p`
- Improved streaming with Server-Sent Events

**🧠 Reasoning Module Enhancement**
- Native reasoning mode for V2 API
- Auto-detection of best reasoning mode
- Token budget control for reasoning
- Support for multiple reasoning levels

**📄 File Processing**
- **9x capacity increase**: 10,000 → 90,000 characters
- File content reader with smart truncation
- Multiple file handling
- Automatic encoding detection
- API limit validation

---

### 🔧 Developer Experience

**Better APIs**
- Type-safe parameter builders
- Immutable configuration objects
- Clean message builders for vision/audio
- Consistent error types across all modules

**Documentation**
- Complete rewrite of all documentation
- New guides for vision and multimodal
- Production-ready examples
- Security best practices guide

**CLI Interface**
- Beautiful interactive menu
- Quick command-line access
- Shell script integration
- Perfect for testing and learning

---

### 🛡️ Security & Stability

**Enhanced Security**
- Tokens **only** in Authorization headers (never in URLs)
- SSL verification enforced by default
- No token exposure in logs or browser history
- Safe URL sharing - no credentials leaked

**Production Ready**
- Zero memory leaks in long-running applications
- Smart retry with API-specified delays
- Connection pooling with limits
- Comprehensive error recovery

**Validation**
- Input validation for all parameters
- Prompt length checking (90K limit)
- File size validation
- Model name validation

---

### 📊 API Changes

**V2 API Only**
- Migrated exclusively to Pollinations V2 API
- New endpoint structure
- Enhanced model support
- Better error responses

**Breaking Changes from v0.4.x**
- Removed V1 API support
- New client initialization
- Updated parameter names for consistency
- Changed error types for clarity

**Migration Path**
```python
# OLD (v0.4.x - V1 API)
from blossom_ai import Blossom
client = Blossom(api_version="v1")

# NEW (v0.5.0 - V2 API only)
from blossom_ai import Blossom
client = Blossom(api_token="your_token")
```

---

### 🎨 New Utilities

**MessageBuilder**
```python
from blossom_ai import MessageBuilder

# Vision message
msg = MessageBuilder.image(
    role="user",
    text="What's in this image?",
    image_url="https://example.com/photo.jpg"
)
```

**Enhanced Caching**
```python
from blossom_ai.utils import cached

@cached(ttl=3600)
def expensive_operation(prompt):
    return client.text.generate(prompt)
```

**File Reader**
```python
from blossom_ai.utils import read_file_for_prompt

content = read_file_for_prompt("data.txt", max_length=70000)
```

---

### 📈 Performance

**Speed Improvements**
- Smart caching reduces API calls by 99%+
- Connection pooling for faster requests
- Lazy model initialization (5s → 50ms import time)
- Optimized memory usage

**Scalability**
- Handle 100+ concurrent requests
- Memory-safe for 24/7 operation
- Automatic cleanup and resource management
- No connection leaks

---
### 📚 Documentation

**New Guides**
- [Vision Support](VISION.md) - Image analysis with AI
- [Web Applications](WEB_APP.md) - FastAPI/Flask integration
- [Multimodal Guide](MULTIMODAL.md) - Text, images, audio
- [Security Policy](../../SECURITY.md) - Updated for v0.5.0


---
### 🎉 Highlights
```python
# Before v0.5.0: Simple but limited
client.text.generate("Hello")

# After v0.5.0: Powerful and flexible
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="token") as client:
    # Vision analysis
    messages = [
        MessageBuilder.image(
            role="user",
            text="Describe this image",
            image_url="https://example.com/photo.jpg",
            detail="high"
        )
    ]
    
    # With advanced controls
    response = client.text.chat(
        messages,
        model="openai",
        max_tokens=500,
        temperature=0.8,
        thinking={"type": "enabled", "budget_tokens": 2000}
    )
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### How to Help
- 🐛 Report bugs
- 💡 Suggest features  
- 📝 Improve documentation
- 🧪 Write tests
- 🌍 Translate guides

---

## 📜 License

MIT License - See [LICENSE](../../LICENSE) for details.

---

## 🔗 Links

- [PyPI Package](https://pypi.org/project/eclips-blossom-ai/)
- [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)
- [Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)
- [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 and ❤️ by [Eclips Team](https://github.com/PrimeevolutionZ)**

*Empowering developers to build amazing AI applications*

[⬆️ Back to top](#-changelog)

</div>