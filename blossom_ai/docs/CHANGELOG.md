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
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Simplified and cleaned up
- **[INDEX.md](docs/INDEX.md)** - Added utilities section with new guides

#### 🔧 Internal Improvements

**New Utils Modules**:
- `blossom_ai.utils.reasoning` - Reasoning enhancement
- `blossom_ai.utils.cache` - Caching system

**Exports Added**:
- Reasoning: `ReasoningLevel`, `ReasoningConfig`, `ReasoningEnhancer`, `ReasoningChain`
- Caching: `CacheBackend`, `CacheConfig`, `CacheManager`, `cached`

**Documentation Cleanup**:
- Removed 100+ lines of confusing Native Reasoning examples from EXAMPLES.md
- Simplified reasoning examples to focus on practical usage
- Fixed all code examples to match actual API

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

#### 🐛 Bug Fixes

- **Documentation**: Fixed and simplified EXAMPLES.md
  - Removed confusing Native Reasoning section that didn't match user-facing API
  - Clarified distinction between internal implementation and public API
  - All code examples now tested and verified to work

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

<div align="center">

**[View Full Documentation](docs/INDEX.md)** • **[GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)**

</div>