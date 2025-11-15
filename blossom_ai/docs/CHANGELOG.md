# 📝 Changelog

> **Beautiful Python SDK for Pollinations.AI**  
> Track the evolution of Blossom AI across versions

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
- 🏗️ Modular design with clear separation of concerns
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

**📁 File Processing**
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

### 🔍 What Changed Under the Hood

**Complete Module Restructure**
- `core/` - Configuration, errors, models, sessions
- `generators/` - Image and text generation logic
- `utils/` - Caching, reasoning, file reading, CLI

**New Components**
- `parameter_builder.py` - Type-safe parameter construction
- `streaming_mixin.py` - SSE streaming support
- `base_generator.py` - Unified sync/async base
- `session_manager.py` - Smart connection pooling

**Improved Patterns**
- Context managers for automatic cleanup
- Frozen dataclasses for immutability
- Mixins for code reuse
- Protocol-based interfaces

---

### 📚 Documentation

**New Guides**
- [Vision Support](docs/VISION.md) - Image analysis with AI
- [Web Applications](docs/WEB_APP.md) - FastAPI/Flask integration
- [Multimodal Guide](docs/MULTIMODAL.md) - Text, images, audio
- [Security Policy](SECURITY.md) - Updated for v0.5.0

**Updated Guides**
- Complete rewrite of all existing documentation
- Production-ready examples
- Best practices for security
- Migration guide from v0.4.x

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

---

### 💔 Breaking Changes

If you're upgrading from v0.4.x, please note:

1. **V1 API Removed** - Only V2 API supported
2. **Import Changes** - Some utilities moved to `blossom_ai.utils`
3. **Parameter Names** - Standardized for consistency
4. **Error Types** - New error hierarchy
5. **Audio** - TTS temporarily unavailable in V2 (coming soon)

**Migration Guide:** See [V1_TO_V2_MIGRATION.md](docs/V1_TO_V2_MIGRATION.md)

---

### 🙏 Acknowledgments

This massive rewrite wouldn't be possible without:
- The Pollinations.AI team for the amazing V2 API
- Community feedback and bug reports
- Contributors who tested early versions

---

## 📦 v0.4.7 (November 2024)

### Features
- 🖥️ CLI Interface for terminal access
- ⚡ 100x faster import time (5s → 50ms)
- 🧠 Smart model caching with TTL
- 📉 19x less memory usage

### Improvements
- Integration tests with VCR.py
- Intelligent retry with API delays
- Better error handling

### Security
- Tokens only in headers
- SSL certificate verification enforced
- No token exposure in logs

---

## 📦 v0.4.6 (November 2024)

### Features
- Production-ready reliability
- Enhanced error recovery
- Memory optimization

---

## 📦 v0.4.5 (November 2024)

### Features
- Security improvements
- Performance optimizations
- Bug fixes

---

## 📦 v0.4.0 - v0.4.4

Initial stable releases with core functionality:
- Image generation
- Text generation
- Audio generation (V1 API)
- Basic streaming
- Caching module
- Reasoning enhancement

---

## 🔮 Future Plans

### Coming Soon
- Audio generation in V2 API
- More vision models
- Advanced multimodal features
- Batch processing support
- Webhook integrations

### Under Consideration
- Custom model fine-tuning
- Local model support
- Plugin system
- WebSocket streaming

---

## 📊 Version History Summary

| Version | Release Date | Highlights |
|---------|-------------|------------|
| **0.5.0** | Dec 2024 | 🌟 Complete rewrite, Vision support, V2 API only |
| 0.4.7 | Nov 2024 | CLI interface, Performance boost |
| 0.4.6 | Nov 2024 | Production hardening |
| 0.4.5 | Nov 2024 | Security enhancements |
| 0.4.0 | Oct 2024 | Stable release |

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Help
- 🐛 Report bugs
- 💡 Suggest features  
- 📝 Improve documentation
- 🧪 Write tests
- 🌐 Translate guides

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

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