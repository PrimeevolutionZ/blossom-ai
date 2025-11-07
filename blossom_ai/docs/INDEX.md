# 📚 Blossom AI Documentation

> **Complete guide to building AI-powered applications with Blossom AI**

Welcome to the Blossom AI documentation! This guide will help you get started with generating images, text, and audio using the Pollinations.AI platform.

---

## 🚀 Getting Started

Perfect for newcomers to Blossom AI.

| Guide                                       | Description                                        |
|---------------------------------------------|----------------------------------------------------|
| **[Installation & Setup](INSTALLATION.md)** | Install the package and configure your environment |

---

## 🆕 V2 API (New!)

The new Pollinations V2 API brings powerful improvements and new features.

| Guide                                             | Description                                                |
|---------------------------------------------------|------------------------------------------------------------|
| **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)**   | Migrate from V1 to V2 - step by step guide                 |
| **[V2 Image Generation](V2_IMAGE_GENERATION.md)** | HD quality, guidance scale, negative prompts, transparency |
| **[V2 Text Generation](V2_TEXT_GENERATION.md)**   | Function calling, advanced parameters, better streaming    |
| **[V2 API Reference](V2_API_REFERENCE.md)**       | Complete V2 API documentation with all parameters          |

### What's New in V2?

**Image Generation:**
- ✨ Quality levels: `low`, `medium`, `high`, `hd`
- 🎯 Guidance scale control (1.0-20.0)
- 🚫 Negative prompts
- 🌈 Transparent backgrounds
- 🖼️ Image-to-image transformation

**Text Generation:**
- 🛠️ Function calling / Tool use
- 📋 Structured JSON output
- ⚙️ Advanced parameters: `max_tokens`, `frequency_penalty`, `presence_penalty`, `top_p`
- 🌊 Improved streaming
- 🌡️ Extended temperature range (0-2)

---

## 🎨 Core Features (V1)

Learn how to use each generation type with the legacy V1 API.

### Image Generation
| Guide                                             | Description                                 |
|---------------------------------------------------|---------------------------------------------|
| **[Image Generation Guide](IMAGE_GENERATION.md)** | Create stunning images from text prompts    |
| 🔗 URL Generation                                 | Get instant image URLs without downloading  |
| 💾 Save to File                                   | Generate and save images locally            |
| 🎯 Advanced Parameters                            | Control dimensions, models, seeds, and more |

### Text Generation
| Guide                                           | Description                           |
|-------------------------------------------------|---------------------------------------|
| **[Text Generation Guide](TEXT_GENERATION.md)** | Generate text with various AI models  |
| 🌊 Streaming                                    | Real-time text generation with chunks |
| 💬 Chat Mode                                    | Multi-turn conversations with context |
| 🎯 JSON Mode                                    | Structured output for applications    |

### Audio Generation
| Guide                                             | Description                         |
|---------------------------------------------------|-------------------------------------|
| **[Audio Generation Guide](AUDIO_GENERATION.md)** | Text-to-speech with multiple voices |
| 🎙️ Voice Selection                               | Choose from various voice models    |
| 🔐 Authentication                                 | Requires API token                  |

---

## 🛠️ Utilities

Tools to enhance your workflows.

| Guide                                     | Description                                                                    |
|-------------------------------------------|--------------------------------------------------------------------------------|
| **[File Content Reader](FILE_READER.md)** | Read text files and integrate them with AI prompts while respecting API limits |
| **[Reasoning Module](REASONING.md)**      | **NEW!** Enhance prompts with structured thinking for better responses         |
| **[Caching Module](CAHCING.md)**          | **NEW!** Cache AI responses to reduce costs and improve performance            |
| 📄 File Validation                        | Automatic size and encoding validation                                         |
| ✂️ Auto-Truncation                        | Handle large files gracefully                                                  |
| 📦 Multiple Files                         | Combine and process multiple files                                             |

### ✨ New in v0.4.1: Reasoning & Caching

**Reasoning Module** - Structured thinking for AI:
- 🧠 Multiple reasoning levels (LOW, MEDIUM, HIGH, ADAPTIVE)
- 🔍 Extract reasoning from responses
- 🔗 Multi-step problem solving
- ⚙️ Configurable thinking patterns

**Caching Module** - Intelligent request caching:
- ⚡ 99%+ faster responses for cached requests
- 💰 Reduced API costs
- 💾 Memory + Disk storage (hybrid)
- 📊 Cache statistics and monitoring
- 🎯 Selective caching (text/images/audio)

---

## 🛠️ Development Guides

Build real-world applications.

| Guide                                             | Description                                   |
|---------------------------------------------------|-----------------------------------------------|
| **[Discord Bot Tutorial](DISCORD_BOT.md)**        | Create an AI image generation bot for Discord |
| **[Telegram Bot Tutorial](TELEGRAM_BOT.md)**      | Build a Telegram bot with image generation    |
| **[Resource Management](RESOURCE_MANAGEMENT.md)** | Best practices for production applications    |
| **[Error Handling](ERROR_HANDLING.md)**           | Handle errors gracefully (V1 & V2)            |

---

## 📖 Reference

Technical details and API specifications.

| Document                                    | Description                                   |
|---------------------------------------------|-----------------------------------------------|
| **[API Reference](API_REFERENCE.md)**       | Complete V1 API documentation for all methods |
| **[V2 API Reference](V2_API_REFERENCE.md)** | Complete V2 API documentation                 |
| **[Changelog](CHANGELOG.md)**               | Version history and updates                   |

---

## 🤝 Contributing & Security

Get involved and keep the project secure.

| Document                                        | Description                                        |
|-------------------------------------------------|----------------------------------------------------|
| **[Contributing Guide](../../CONTRIBUTING.md)** | How to contribute code, docs, and ideas            |
| **[Security Policy](../../SECURITY.md)**        | Report vulnerabilities and security best practices |

> **Note:** These files are located in the project root (`blossom-ai/`), one level above the package directory.

---

## 🎯 Quick Links

### Common Tasks

#### V2 API
- **Migrate to V2:** [V2 Migration Guide](V2_MIGRATION_GUIDE.md)
- **Generate HD images:** [V2 Image Generation - Quality](V2_IMAGE_GENERATION.md#-quality-levels)
- **Use function calling:** [V2 Text Generation - Functions](V2_TEXT_GENERATION.md#-function-calling)
- **Control text length:** [V2 Text Generation - Max Tokens](V2_TEXT_GENERATION.md#max-tokens)
- **Structured JSON:** [V2 Text Generation - JSON Mode](V2_TEXT_GENERATION.md#-json-mode)

#### V1 API (Legacy)
- **Generate an image URL:** [Image Generation - URL Method](IMAGE_GENERATION.md#-image-url-generation)
- **Stream text in real-time:** [Text Generation - Streaming](TEXT_GENERATION.md#-streaming-text-generation)
- **Read files for prompts:** [File Reader - Quick Start](FILE_READER.md#-quick-start)
- **Handle errors properly:** [Error Handling Guide](ERROR_HANDLING.md)
- **Use in async code:** [Resource Management - Async](RESOURCE_MANAGEMENT.md#asynchronous-context-manager)

#### Utilities (New!)
- **Add reasoning to prompts:** [Reasoning - Quick Start](REASONING.md#-quick-start)
- **Cache AI responses:** [Caching - Quick Start](CAHCING.md#-quick-start)
- **Reduce API costs:** [Caching - Best Practices](CAHCING.md#-best-practices)
- **Deep problem solving:** [Reasoning - Multi-Step](REASONING.md#-advanced-features)

#### Contributing
- **Contribute to project:** [Contributing Guide](../../CONTRIBUTING.md)
- **Report security issue:** [Security Policy](../../SECURITY.md)

### Examples by Use Case

| Use Case                  | Guide                                                                                                   |
|---------------------------|---------------------------------------------------------------------------------------------------------|
| **Web Application (V2)**  | [V2 API Reference - Complete Example](V2_API_REFERENCE.md#-complete-example)                            |
| **HD Image Generation**   | [V2 Image Generation - Quality](V2_IMAGE_GENERATION.md#-quality-levels)                                 |
| **AI Chatbot with Tools** | [V2 Text Generation - Function Calling](V2_TEXT_GENERATION.md#-function-calling)                        |
| **Chat Bot (Discord)**    | [Discord Bot Tutorial](DISCORD_BOT.md)                                                                  |
| **Chat Bot (Telegram)**   | [Telegram Bot Tutorial](TELEGRAM_BOT.md)                                                                |
| **CLI Tool**              | [Resource Management - Sync Usage](RESOURCE_MANAGEMENT.md#synchronous-context-manager)                  |
| **Background Worker**     | [Resource Management - Long-Running Apps](RESOURCE_MANAGEMENT.md#for-long-running-applications-eg-bots) |
| **Code Analysis**         | [File Reader - Code Analysis](FILE_READER.md#1-code-analysis)                                           |
| **Document Processing**   | [File Reader - Document Summarization](FILE_READER.md#2-document-summarization)                         |
| **Cached Responses**      | [Caching - Use Cases](CAHCING.md#-use-cases)                                                            |
| **Structured Thinking**   | [Reasoning - Examples](REASONING.md#-usage-examples)                                                    |

---

## 🆘 Need Help?

- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 🔒 **Security issue?** See [Security Policy](../../SECURITY.md) for responsible disclosure
- 💡 **Have a question?** Check the [Error Handling Guide](ERROR_HANDLING.md)
- 📚 **Want examples?** See individual feature guides above
- 🤝 **Want to contribute?** Read the [Contributing Guide](../../CONTRIBUTING.md)

---

## 🌟 Popular Recipes

Quick code snippets for common tasks:

### V2 API with Advanced Features

```python
from blossom_ai import Blossom

# Initialize V2 client
with Blossom(api_version="v2", api_token="your_token") as client:
    # HD image with advanced features
    image = client.image.generate(
        "sunset over mountains",
        quality="hd",
        guidance_scale=7.5,
        negative_prompt="blurry, low quality"
    )
    
    # Text with advanced parameters
    response = client.text.generate(
        "Explain quantum computing",
        max_tokens=200,
        frequency_penalty=0.5,
        presence_penalty=0.3
    )
```

### Reasoning + Caching (New!)

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)  # Cache for 1 hour
def analyze_with_reasoning(question):
    # Enhance with structured thinking
    enhanced = enhancer.enhance(question, level="high")
    
    # Generate with V2
    with Blossom(api_version="v2", api_token="token") as client:
        return client.text.generate(enhanced, max_tokens=1000)

# First call: generates with deep reasoning and caches
result = analyze_with_reasoning("Design a microservices architecture")

# Second call: instant from cache!
result = analyze_with_reasoning("Design a microservices architecture")
```

### V1 API (Legacy)

```python
from blossom_ai import Blossom

# Generate and Save an Image
with Blossom() as ai:
    ai.image.save("a beautiful sunset", "sunset.jpg")

# Get Image URL (Fast!)
with Blossom() as ai:
    url = ai.image.generate_url("a cute robot")
    print(url)

# Stream Text Generation
with Blossom() as ai:
    for chunk in ai.text.generate("Tell me a story", stream=True):
        print(chunk, end='', flush=True)

# Generate Audio (Requires Token)
with Blossom(api_token="YOUR_TOKEN") as ai:
    ai.audio.save("Hello world", "hello.mp3", voice="nova")

# Read File for AI Analysis
from blossom_ai.utils import read_file_for_prompt

content = read_file_for_prompt("data.txt", max_length=5000)

with Blossom() as ai:
    response = ai.text.generate(
        f"Analyze this data:\n\n{content}",
        model="deepseek"
    )
    print(response)
```

### Caching Statistics

```python
from blossom_ai.utils import get_cache

cache = get_cache()

# Generate some cached requests...
# ...

# Check performance
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate:.1f}%")
print(f"Hits: {stats.hits}, Misses: {stats.misses}")
print(f"Memory: {stats.memory_usage} items")
```

---

## 📄 Version Comparison

| Feature                   | V1 (Legacy) | V2 (New)               | Utils      |
|---------------------------|-------------|------------------------|------------|
| **Image Quality Control** | ❌           | ✅ (low/medium/high/hd) | -          |
| **Guidance Scale**        | ❌           | ✅ (1.0-20.0)           | -          |
| **Negative Prompts**      | ❌           | ✅                      | -          |
| **Transparent Images**    | ❌           | ✅                      | -          |
| **Image-to-Image**        | ❌           | ✅                      | -          |
| **Function Calling**      | ❌           | ✅                      | -          |
| **Max Tokens Control**    | ❌           | ✅                      | -          |
| **Frequency Penalty**     | ❌           | ✅ (0-2)                | -          |
| **Presence Penalty**      | ❌           | ✅ (0-2)                | -          |
| **Top-P Sampling**        | ❌           | ✅                      | -          |
| **Temperature Range**     | 0-1         | 0-2 (extended)         | -          |
| **Basic Generation**      | ✅           | ✅                      | -          |
| **Streaming**             | ✅           | ✅ (improved)           | -          |
| **JSON Mode**             | ✅           | ✅ (more reliable)      | -          |
| **Reasoning Enhancement** | -           | -                      | ✅ **NEW!** |
| **Response Caching**      | -           | -                      | ✅ **NEW!** |
| **File Reading**          | -           | -                      | ✅          |

**Recommendation:** Use V2 for new projects. Add Reasoning + Caching for production apps.

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[PyPI Package](https://pypi.org/project/eclips-blossom-ai/) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

[Contributing](../../CONTRIBUTING.md) • [Security](../../SECURITY.md) • [License](../../LICENSE)

</div>