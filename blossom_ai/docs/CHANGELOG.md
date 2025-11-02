# Changelog

This document tracks the changes and updates across different versions of the Blossom AI SDK.

---

## v0.4.1 (Latest)

### 🚀 Major Update: Reasoning & Caching

This release introduces two powerful utility modules that enhance AI capabilities and reduce API costs.

#### ✨ New Features

##### Reasoning Module
**Structured thinking for better AI responses**

- **Multiple Reasoning Levels**:
  - `LOW` - Quick thinking for simple questions
  - `MEDIUM` - Systematic analysis (default)
  - `HIGH` - Deep reasoning with multiple approaches
  - `ADAPTIVE` - Automatic level selection

- **Configuration Options**:
  - `include_confidence` - Request confidence scores
  - `self_critique` - Enable self-evaluation
  - `alternative_approaches` - Consider multiple solutions
  - `step_verification` - Verify each reasoning step

- **Advanced Features**:
  - `ReasoningEnhancer` - Enhance prompts with reasoning
  - `ReasoningChain` - Multi-step problem solving
  - `extract_reasoning()` - Parse reasoning from responses
  - `add_reasoning_to_blossom()` - Direct integration

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()
enhanced = enhancer.enhance(
    "How do I optimize database queries?",
    level="high"
)

# Use with Blossom
with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced)
```

##### Caching Module
**Intelligent request caching to reduce costs**

- **Three Cache Backends**:
  - `MEMORY` - Fast in-memory cache
  - `DISK` - Persistent disk storage
  - `HYBRID` - Memory + Disk (recommended)

- **Features**:
  - TTL-based expiration
  - LRU eviction policy
  - Thread-safe and async-safe
  - Cache statistics (hit rate, misses, evictions)
  - Selective caching (text/images/audio)
  - Automatic key generation

- **Usage**:
  - `@cached()` decorator for functions
  - `CacheManager` for manual control
  - `get_cache()` for global cache
  - `configure_cache()` for setup

```python
from blossom_ai.utils import cached

@cached(ttl=3600)  # Cache for 1 hour
def generate_summary(text):
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(f"Summarize: {text}")

# First call: generates and caches
result = generate_summary("Long text...")

# Second call: instant from cache!
result = generate_summary("Long text...")
```

#### 📚 Documentation

**New Guides**:
- **[Reasoning Guide](docs/REASONING.md)** - Complete reasoning module documentation
- **[Caching Guide](docs/CACHING.md)** - Comprehensive caching guide

**Updated Guides**:
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Added reasoning and caching examples
- **[INDEX.md](docs/INDEX.md)** - Added utilities section with new guides

#### 🔧 Internal Improvements

**New Utils Modules**:
- `blossom_ai.utils.reasoning` - Reasoning enhancement
- `blossom_ai.utils.cache` - Caching system

**Exports Added**:
- Reasoning: `ReasoningLevel`, `ReasoningConfig`, `ReasoningEnhancer`, `ReasoningChain`
- Caching: `CacheBackend`, `CacheConfig`, `CacheManager`, `cached`

#### 📊 Performance Impact

**Caching Benefits**:
- ⚡ **99%+ faster** for cached responses (0.5ms vs 2000ms)
- 💰 **Reduced API costs** - avoid duplicate requests
- 🎯 **Better rate limit handling** - fewer API calls
- 📈 **Improved user experience** - instant responses

**Reasoning Benefits**:
- 🧠 **Better responses** - structured thinking improves quality
- 🎯 **More accurate** - systematic analysis reduces errors
- 📊 **Verifiable** - extract reasoning separately
- 🔄 **Adaptive** - automatic complexity detection

#### 🎯 Use Cases

**Reasoning Use Cases**:
- Complex problem solving
- Code analysis and optimization
- System design and architecture
- Multi-step workflows
- Decision support systems

**Caching Use Cases**:
- Chatbots with repeated questions
- Document analysis pipelines
- API rate limit protection
- Development and testing
- Cost optimization for production

#### 💡 Examples

**Combined Usage**:
```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)  # Cache + Reasoning = Efficient!
def analyze_code(code):
    enhanced = enhancer.enhance(
        f"Analyze this code:\n\n{code}",
        level="high"
    )
    
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=1000)

# Deep analysis with caching
result = analyze_code("def hello(): print('hi')")
```

**Cache Statistics**:
```python
from blossom_ai.utils import get_cache

cache = get_cache()

# Check performance
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate:.1f}%")
print(f"Hits: {stats.hits}, Misses: {stats.misses}")
```

#### ⚠️ Breaking Changes

**None!** This release is fully backward compatible:
- All existing code continues to work
- New features are opt-in
- No changes to existing APIs

#### 📝 Migration Notes

No migration needed! To use new features:

```python
# Add reasoning to existing code
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()
enhanced_prompt = enhancer.enhance(your_prompt, level="medium")

# Add caching to existing code
from blossom_ai.utils import cached

@cached(ttl=3600)
def your_existing_function():
    # Your code here
    pass
```

#### 🔗 Related Links

- [Reasoning Documentation](docs/REASONING.md)
- [Caching Documentation](docs/CACHING.md)
- [V2 API Documentation](docs/V2_API_REFERENCE.md)

---

## v0.4.0

### 🚀 Major Update: V2 API Support
This release introduces full support for the new Pollinations V2 API (`enter.pollinations.ai`), bringing significant improvements and new features while maintaining full backward compatibility with V1.

#### ✨ New Features

##### V2 API Integration
- **Opt-in V2 Support**: Use `api_version="v2"` parameter to access new API
- **Backward Compatible**: V1 remains default, all existing code works unchanged
- **Dual API Support**: Can use V1 and V2 simultaneously in same application

```python
# V2 API with new features
client = Blossom(api_version="v2", api_token="your_token")

# V1 API (existing code still works)
client = Blossom()  # Defaults to v1
```

##### Image Generation V2

**Quality Levels** - Control output quality vs generation time:
- `quality="low"` - Fast generation, smaller files (~10-30 KB)
- `quality="medium"` - Balanced (default, ~30-100 KB)
- `quality="high"` - Better details (~100-300 KB)
- `quality="hd"` - Best quality (~300-500 KB)

**Guidance Scale** - Fine-tune prompt adherence (1.0-20.0):
- Low (1.0-5.0): Creative freedom, artistic interpretation
- Medium (5.0-10.0): Balanced adherence (default: 7.5)
- High (10.0-20.0): Strict prompt following

**Negative Prompts** - Specify unwanted elements:
```python
negative_prompt="blurry, low quality, distorted, watermark"
```

**Transparent Backgrounds** - Generate PNG with alpha channel:
```python
transparent=True  # Perfect for logos, stickers, game assets
```

**Image-to-Image** - Transform existing images:
```python
image="https://example.com/source.jpg"  # Transform with prompt
```

**Feed Control** - Keep generations private:
```python
nofeed=True  # Don't add to public feed
```

##### Text Generation V2

**OpenAI Compatibility** - Full OpenAI API compatibility:
- Drop-in replacement for OpenAI endpoints
- Compatible with existing OpenAI tools

**Function Calling / Tool Use** - Build agentic AI applications:
```python
tools=[{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for location",
        "parameters": {...}
    }
}]
```

**Advanced Generation Control**:
- `max_tokens` - Limit response length (50-2000+)
- `frequency_penalty` (0-2) - Reduce word repetition
- `presence_penalty` (0-2) - Encourage topic diversity
- `top_p` (0.1-1.0) - Nucleus sampling for controlled randomness
- `n` (1-128) - Generate multiple completions

**Improved JSON Mode** - More reliable structured output:
```python
json_mode=True  # Guaranteed valid JSON responses
```

**Enhanced Streaming** - More stable real-time generation:
- Better timeout handling
- Improved error recovery
- Reduced stream interruptions

**Extended Temperature Range** - 0-2 (was 0-1 in V1):
- Enables more creative outputs above 1.0
- Better control over randomness

**Model Aliases** - Multiple names for same models:
- `"openai"` = `"gpt-4"` = `"chatgpt"`
- More flexible model selection

##### Authentication Improvements

**Secret Keys** (`sk_...`) - Server-side use:
- Best rate limits
- Full feature access
- Can spend Pollen credits
- Never expose in client-side code

**Publishable Keys** (`pk_...`) - Client-side use:
- IP-based rate limits
- Safe for browsers/client apps
- Free features only
- All models accessible

**Anonymous Access** - Still available:
- Free tier with basic limits
- Great for testing

#### 📚 Documentation

**New Guides**:
- **[V2 Migration Guide](docs/V2_MIGRATION_GUIDE.md)** - Step-by-step migration from V1
- **[V2 Image Generation](docs/V2_IMAGE_GENERATION.md)** - Complete guide to image features
- **[V2 Text Generation](docs/V2_TEXT_GENERATION.md)** - Advanced text generation guide
- **[V2 API Reference](docs/V2_API_REFERENCE.md)** - Full API documentation

**Updated Guides**:
- **[Error Handling](docs/ERROR_HANDLING.md)** - V2-specific error handling
- **[INDEX.md](docs/INDEX.md)** - Added V2 section and comparison table

#### 🔧 Internal Improvements

**New V2 Generators**:
- `ImageGeneratorV2` / `AsyncImageGeneratorV2`
- `TextGeneratorV2` / `AsyncTextGeneratorV2`
- Located in `generators_v2.py`

**V2 Endpoints**:
- Image: `https://enter.pollinations.ai/api/generate/image`
- Text: `https://enter.pollinations.ai/api/generate/openai`
- Models: Separate endpoints for image/text model lists

**Authentication Handling**:
- V2 uses Bearer token in Authorization header
- V1 uses query parameter (backward compatible)
- Automatic method selection based on API version

**Error Handling**:
- 402 Payment Required support for V2
- Better rate limit detection
- Improved error messages with context

#### ⚠️ Breaking Changes

**None!** This release is fully backward compatible:
- V1 API remains default (`api_version="v1"`)
- All existing code continues to work
- V2 is opt-in via `api_version="v2"` parameter

#### 📄 Migration Path

```python
# Before (V1 - still works!)
client = Blossom()
image = client.image.generate("sunset")

# After (V2 - opt-in)
client = Blossom(api_version="v2", api_token="token")
image = client.image.generate(
    "sunset",
    quality="hd",
    guidance_scale=7.5,
    negative_prompt="blurry"
)
```

See [V2 Migration Guide](docs/V2_MIGRATION_GUIDE.md) for detailed migration steps.

#### 📊 Feature Comparison

| Feature | V1 | V2 |
|---------|----|----|
| Basic generation | ✅ | ✅ |
| Quality levels | ❌ | ✅ |
| Guidance scale | ❌ | ✅ |
| Negative prompts | ❌ | ✅ |
| Transparent images | ❌ | ✅ |
| Image-to-image | ❌ | ✅ |
| Function calling | ❌ | ✅ |
| Max tokens | ❌ | ✅ |
| Frequency penalty | ❌ | ✅ |
| Presence penalty | ❌ | ✅ |
| Top-P sampling | ❌ | ✅ |
| Temperature | 0-1 | 0-2 |
| Streaming | ✅ | ✅ (improved) |
| JSON mode | ✅ | ✅ (more reliable) |

#### 🎯 Use Cases

**Use V2 when you need:**
- HD quality images
- Fine control over image generation
- Function calling for AI agents
- Advanced text parameters
- Better streaming reliability
- Structured JSON outputs

**Use V1 when you need:**
- Simple, quick integration
- Backward compatibility
- No authentication required
- Basic features are sufficient

#### 🔗 Related Links

- [V2 API Documentation](https://docs.pollinations.ai/v2)
- [Get API Token](https://enter.pollinations.ai)
- [V2 Migration Guide](docs/V2_MIGRATION_GUIDE.md)

---

## v0.3.2

### 📚 Documentation & Standardization

- **PyPI Page Enhancement**: Updated package metadata for better PyPI presentation
  - Changed development status to `Production/Stable`
  - Added direct links to documentation, changelog, and security policy
  - Improved project discoverability and user navigation

- **Project Standardization**: Added essential project documentation files
  - **CONTRIBUTING.md** - Comprehensive guide for contributors
  - **SECURITY.md** - Detailed security policy and best practices
  - **bug_report.md** - Standardized bug report template
  - **feature_request.md** - Standardized feature request template

- **Metadata Updates** in `pyproject.toml`:
  - Updated development status classifier to `Production/Stable`
  - Added direct documentation links:
    - Documentation Index
    - Changelog
    - Security Policy

### 🎯 Impact

- **Better PyPI Presence**: Enhanced package page with clear documentation links
- **Improved Onboarding**: New contributors can easily understand contribution process
- **Security Transparency**: Clear security policy builds user trust
- **Standardized Reporting**: Consistent issue and feature request templates

### 📝 Notes

- **No code changes** - This is a documentation and metadata update only
- **All existing functionality remains unchanged**

---

## v0.3.1

### 🔧 Internal Improvements

- **Major Code Refactoring**: Eliminated ResourceWarnings and improved code quality
  - Added centralized configuration in `config.py` with `ENDPOINTS`, `LIMITS`, `DEFAULTS`
  - Implemented DRY principles with `@with_retry` decorator for consistent retry logic
  - Unified error handling across all generators
  - Improved session cleanup with `atexit` handlers and explicit `close()` methods
  - Standardized all comments to English for professional consistency

- **Performance & Stability**:
  - No more ResourceWarnings in output
  - Better memory management with guaranteed session cleanup
  - Code optimization ~35%
  - Improved type hints and documentation (in code)

### 📝 File Changes
- **New**: `blossom_ai/core/config.py` - Centralized configuration
- **Refactored**: `session_manager.py`, `base_generator.py`, `generators.py`, `blossom.py`, `errors.py`
- **Removed**: `base_client.py` (logic moved to base_generator)

### ⚠️ Important Notes
- **Zero breaking changes** - All existing code continues to work unchanged
- **Public API remains 100% compatible**

---

## v0.3.0 

### ✨ New Features

- **File Content Reader Utility**: New utility module for reading text files and integrating them with AI prompts
  - Read text files with automatic validation against configurable limits
  - Auto-truncate large files to fit within API prompt limits (10,000 characters total)
  - **Default file limit: 8,000 characters** (reserves 2,000 for prompt text)
  - Support for multiple encodings (UTF-8, Latin-1, CP1252, etc.)
  - Combine multiple files into a single prompt
  - Calculate available space for file content
  - Validate combined prompt + file length before API calls
  - Support for 20+ text file formats (.txt, .md, .json, .py, .csv, etc.)
  
- **New Utils Module**: Added `blossom_ai.utils` package with file handling utilities
  - `FileContentReader` - Main class for file operations with configurable limits
  - `FileContent` - Data class for file metadata
  - `read_file_for_prompt()` - Quick function for simple use cases (defaults to 8,000 char limit)
  - `get_file_info()` - Get file metadata without reading content

- **New Error Type**: Added `FileTooLargeError` for better error handling
  - Specific error when file content exceeds configured limits
  - Clear error messages with actionable solutions
  - Separate from general `ValidationError` for easier error handling

### 📚 Documentation

- **New Guide**: Added comprehensive [File Content Reader Guide](docs/FILE_READER.md)
  - Complete API reference for all methods
  - Clear explanation of API limits (10,000 chars total)
  - 4 practical use case examples
  - Error handling best practices with `FileTooLargeError`
  - Advanced usage patterns
- **Updated INDEX.md**: Added utilities section with file reader documentation links
- **Updated README**: Added file reader to features list

### 🔧 API Changes

- **New Exports** in main `blossom_ai` package:
  - `FileContentReader` - Main file reader class
  - `FileContent` - File metadata container
  - `read_file_for_prompt` - Quick file reading function
  - `get_file_info` - File info getter
  - `FileTooLargeError` - New error type
  - `API_MAX_TOTAL_LENGTH` - API limit constant (10,000)
  - `DEFAULT_MAX_FILE_LENGTH` - Default file limit (8,000)
  - `DEFAULT_PROMPT_SPACE` - Default prompt space (2,000)
  - `SUPPORTED_TEXT_EXTENSIONS` - Supported file types

### ⚠️ Important Notes

**API Limits:**
- The Pollinations AI text generation API has a **total limit of 10,000 characters**
- This includes your prompt text + file content combined
- `FileContentReader` defaults to limiting files to **8,000 characters** to leave space for prompts
- **Users are responsible** for ensuring their final prompt doesn't exceed 10,000 characters
- Use `validate_prompt_length()` to check before sending to API

---

## v0.2.92

### 🐛 Bug Fixes

- **Documentation**: Fixed links for docs in `README.md`

---

## v0.2.91

### 📚 Documentation Updates

- **API Reference Fix**: Restored complete parameter tables that were missing in v0.2.8-0.2.9
  - Added full parameter tables for `Blossom` class initialization
  - Added complete parameter documentation for all `image`, `text`, and `audio` methods
  - Added detailed error types and attributes documentation
- **New Documentation Files**:
  - Added `EXAMPLES.md` - Comprehensive practical examples from original documentation
  - Added `INDEX.md` - Central navigation hub for all documentation
- **README Update**: Added link to new `EXAMPLES.md` in documentation section

---

## v0.2.9

### 🐛 Bug Fixes

- **Critical Path Fix**: Fixed missing `/` in file paths that caused import errors

---

## v0.2.8

### 🐛 Bug Fixes

- **README Links**: Corrected incorrect documentation links in README.md

---

## v0.2.7

### ✨ New Features

- **Documentation Restructuring**: The project documentation has been fully modularized and restructured for improved clarity, navigation, and maintainability
- **Updated README**: The main README now serves as a concise project overview with links to the detailed guides

---

## v0.2.6

### ✨ New Features

- **Enhanced Resource Management**: Implemented proper session cleanup using `atexit` hooks and improved context manager support for both sync and async operations
- **Global Session Registry**: Centralized tracking of all active sessions for better resource control

### 🛠️ Bug Fixes

- Fixed `ResourceWarning` regarding unclosed sessions in certain scenarios
- Improved thread-safety for resource cleanup in complex async environments

---

## v0.2.5

### ✨ New Features

- **Image URL Generation**: Added the `ai.image.generate_url()` method for instant retrieval of image URLs without downloading bytes. This is significantly faster and more efficient for bot and web integrations
- **Private Generation Support**: Added the `private` parameter to image generation methods

---

## v0.2.0

### ✨ New Features

- **Initial Release**: Core functionality for Image, Text, and Audio generation
- **Unified API**: Single `Blossom` class for both synchronous and asynchronous operations
- **Streaming Support**: Real-time text generation with built-in timeout protection

---

<div align="center">

**[View Full Documentation](docs/INDEX.md)** • **[GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)**

</div>