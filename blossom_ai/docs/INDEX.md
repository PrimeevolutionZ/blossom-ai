# 📚 Blossom AI Documentation v0.5.0

> **Complete guide to building AI-powered applications with Blossom AI V2 API**

Welcome to the Blossom AI documentation! This library provides a beautiful Python SDK for the Pollinations.AI V2 API, supporting image generation, text generation with vision and audio capabilities.

---

## 🚀 Quick Start

Perfect for newcomers to Blossom AI.

| Guide                                       | Description                                        |
|---------------------------------------------|----------------------------------------------------|
| **[Installation & Setup](INSTALLATION.md)** | Install the package and configure your environment |
| **[Quick Start Guide](QUICKSTART.md)**      | 5-minute guide to your first generation            |
| **[CLI Interface](CLI.md)**                 | Terminal interface for quick AI generation         |

---

## 🎨 Core Features

### Image Generation

| Guide                                       | Description                                      |
|---------------------------------------------|--------------------------------------------------|
| **[Image Generation](IMAGE_GENERATION.md)** | Generate images with V2 API                      |
| 🎯 Advanced Parameters                      | Quality levels, guidance scale, negative prompts |
| 🌈 Special Effects                          | Transparent backgrounds, image-to-image          |
| 🔗 URL Generation                           | Get instant URLs without downloading             |

**New in V2:**
- ✨ Quality levels: `low`, `medium`, `high`, `hd`
- 🎯 Guidance scale control (1.0-20.0)
- 🚫 Negative prompts for better control
- 🌈 Transparent background support
- 🖼️ Image-to-image transformation

### Text Generation

| Guide                                     | Description                              |
|-------------------------------------------|------------------------------------------|
| **[Text Generation](TEXT_GENERATION.md)** | Generate text with OpenAI-compatible API |
| 🌊 Streaming                              | Real-time text generation                |
| 💬 Chat Mode                              | Multi-turn conversations                 |
| 🛠️ Function Calling                      | Tool use and function execution          |
| 📋 JSON Mode                              | Structured output                        |

**New in V2:**
- 🛠️ Function calling / Tool use
- 📋 Structured JSON output
- ⚙️ Advanced parameters: `max_tokens`, `frequency_penalty`, `presence_penalty`, `top_p`
- 🌊 Improved streaming with SSE
- 🌡️ Extended temperature range (0-2)

### Vision & Audio (NEW!)

| Guide                                 | Description                     |
|---------------------------------------|---------------------------------|
| **[Vision Support](VISION.md)**       | Analyze images with AI          |
| **[Audio Support](AUDIO.md)**         | Audio input/output capabilities |
| **[Multimodal Guide](MULTIMODAL.md)** | Combine text, images, and audio |

**New Features:**
- 👁️ Image analysis from URLs or local files
- 🔊 Audio output with voice selection
- 📸 Multiple images in one request
- 🎨 Image detail control (low/auto/high)

---

## 🛠️ Utilities

Tools to enhance your workflows.

### File Handling

| Guide                             | Description                            |
|-----------------------------------|----------------------------------------|
| **[File Reader](FILE_READER.md)** | Read and validate files for AI prompts |
| 📏 Size Validation                | Automatic API limit checking           |
| ✂️ Auto-Truncation                | Handle large files gracefully          |
| 📦 Multiple Files                 | Combine and process multiple files     |
| 🔤 Encoding Detection             | Automatic encoding handling            |

### Reasoning Module

| Guide                               | Description                              |
|-------------------------------------|------------------------------------------|
| **[Reasoning Guide](REASONING.md)** | Enhance prompts with structured thinking |
| 🧠 Reasoning Levels                 | LOW, MEDIUM, HIGH, ADAPTIVE              |
| 🔗 Multi-Step Solving               | Chain reasoning for complex problems     |
| ⚙️ Configurable                     | Custom reasoning patterns                |

**Reasoning Modes:**
- `PROMPT`: Universal, works with all models (prompt engineering)
- `NATIVE`: V2 OpenAI models only (built-in `thinking` parameter)
- `AUTO`: Automatically chooses best mode

### Caching Module

| Guide                           | Description                     |
|---------------------------------|---------------------------------|
| **[Caching Guide](CACHING.md)** | Cache responses to reduce costs |
| ⚡ Fast Responses                | 99%+ faster for cached requests |
| 💰 Cost Reduction               | Reduce API costs significantly  |
| 💾 Hybrid Storage               | Memory + Disk caching           |
| 📊 Statistics                   | Monitor cache performance       |

### CLI Interface

| Guide                   | Description                            |
|-------------------------|----------------------------------------|
| **[CLI Guide](CLI.md)** | Command-line interface for quick tasks |
| 🖥️ Interactive Mode    | Explore all features with menu         |
| ⚡ Quick Commands        | One-line generation commands           |
| 🔧 Shell Integration    | Use in scripts and automation          |

---

## 📖 API Reference

Complete technical documentation.

| Document                                | Description                    |
|-----------------------------------------|--------------------------------|
| **[API Reference](API_REFERENCE.md)**   | Complete V2 API documentation  |
| **[Error Handling](ERROR_HANDLING.md)** | Handle errors gracefully       |
| **[Configuration](CONFIGURATION.md)**   | Configure the client           |

---

## 💼 Development Guides

Build real-world applications.

| Guide                                        | Description                         |
|----------------------------------------------|-------------------------------------|
| **[Discord Bot Tutorial](DISCORD_BOT.md)**   | AI image generation bot for Discord |
| **[Telegram Bot Tutorial](TELEGRAM_BOT.md)** | Telegram bot with image generation  |
| **[Web Application Guide](WEB_APP.md)**      | Build web apps with FastAPI/Flask   |
| **[Async Best Practices](ASYNC_GUIDE.md)**   | Working with async/await            |

---

## 🤝 Contributing & Security

Get involved and keep the project secure.

| Document                                        | Description                                        |
|-------------------------------------------------|----------------------------------------------------|
| **[Contributing Guide](../../CONTRIBUTING.md)** | How to contribute code, docs, and ideas            |
| **[Security Policy](../../SECURITY.md)**        | Report vulnerabilities and security best practices |


---

## 🎯 Quick Links by Task

### Common Tasks

#### Getting Started
- **Install the library:** [Installation Guide](INSTALLATION.md)
- **First image generation:** [Quick Start - Images](QUICKSTART.md#image-generation)
- **First text generation:** [Quick Start - Text](QUICKSTART.md#text-generation)
- **Use CLI:** [CLI - Quick Start](CLI.md)

#### Image Generation
- **Generate HD images:** [Image Generation - Quality](IMAGE_GENERATION.md#quality-levels)
- **Use guidance scale:** [Image Generation - Guidance](IMAGE_GENERATION.md#guidance-scale)
- **Negative prompts:** [Image Generation - Negative Prompts](IMAGE_GENERATION.md#negative-prompts)
- **Transparent backgrounds:** [Image Generation - Transparency](IMAGE_GENERATION.md#transparent-backgrounds)
- **Image-to-image:** [Image Generation - Image2Image](IMAGE_GENERATION.md#image-to-image)

#### Text Generation
- **Stream responses:** [Text Generation - Streaming](TEXT_GENERATION.md#streaming)
- **Use function calling:** [Text Generation - Functions](TEXT_GENERATION.md#function-calling)
- **Get JSON output:** [Text Generation - JSON Mode](TEXT_GENERATION.md#json-mode)
- **Control length:** [Text Generation - Max Tokens](TEXT_GENERATION.md#max-tokens)
- **Multi-turn chat:** [Text Generation - Chat](TEXT_GENERATION.md#chat-mode)

#### Vision & Audio (New!)
- **Analyze images:** [Vision Guide](VISION.md)
- **Use local images:** [Vision - Local Files](VISION.md#local-images)
- **Multiple images:** [Vision - Multiple Images](VISION.md#multiple-images)
- **Audio output:** [Audio Guide](AUDIO.md)

#### Utilities (New!)
- **Read files for prompts:** [File Reader - Quick Start](FILE_READER.md#quick-start)
- **Handle large files:** [File Reader - Truncation](FILE_READER.md#auto-truncation)
- **Add reasoning:** [Reasoning - Quick Start](REASONING.md#quick-start)
- **Cache responses:** [Caching - Quick Start](CACHING.md#quick-start)
- **Reduce API costs:** [Caching - Best Practices](CACHING.md#cost-reduction)

#### Production
- **Handle errors:** [Error Handling Guide](ERROR_HANDLING.md)
- **Manage resources:** [Resource Management](RESOURCE_MANAGEMENT.md)
- **Async patterns:** [Async Guide](ASYNC_GUIDE.md)
- **Performance tuning:** [Performance Guide](PERFORMANCE.md)

### Examples by Use Case

| Use Case                  | Guide                                                         |
|---------------------------|---------------------------------------------------------------|
| **Quick Terminal Usage**  | [CLI Interface](CLI.md)                                       |
| **Shell Automation**      | [CLI - Automation](CLI.md#automation)                         |
| **Web Application**       | [Web App Guide](WEB_APP.md)                                   |
| **HD Image Generation**   | [Image Generation - HD](IMAGE_GENERATION.md#hd-quality)       |
| **AI Chatbot with Tools** | [Function Calling Guide](TEXT_GENERATION.md#function-calling) |
| **Image Analysis**        | [Vision Guide](VISION.md)                                     |
| **Discord Bot**           | [Discord Bot Tutorial](DISCORD_BOT.md)                        |
| **Telegram Bot**          | [Telegram Bot Tutorial](TELEGRAM_BOT.md)                      |
| **Code Analysis**         | [File Reader - Use Cases](FILE_READER.md#use-cases)           |
| **Document Processing**   | [File Reader - Documents](FILE_READER.md#documents)           |
| **Cached Responses**      | [Caching Guide](CACHING.md)                                   |
| **Structured Thinking**   | [Reasoning Guide](REASONING.md)                               |

---

## ⭐ Popular Recipes

Quick code snippets for common tasks:

### CLI Quick Usage

```bash
# Interactive mode - explore all features
python -m blossom_ai.utils.cli

# Quick image generation
python -m blossom_ai.utils.cli --image "sunset" --output sunset.png

# Quick text generation
python -m blossom_ai.utils.cli --text "Write a poem"

# Batch processing
for i in {1..5}; do
    python -m blossom_ai.utils.cli --image "cat $i" --output "cat_$i.png"
done
```

### Basic Image Generation

```python
from blossom_ai import Blossom

# Generate and save image
with Blossom(api_token="your_token") as client:
    client.image.save(
        "a beautiful sunset over mountains",
        "sunset.jpg",
        quality="hd",
        width=1920,
        height=1080
    )
    
# Get URL without downloading
with Blossom(api_token="your_token") as client:
    url = client.image.generate_url(
        "a cute robot",
        quality="high",
        guidance_scale=7.5
    )
    print(url)
```

### Basic Text Generation

```python
from blossom_ai import Blossom

# Simple generation
with Blossom(api_token="your_token") as client:
    response = client.text.generate(
        "Explain quantum computing in simple terms",
        max_tokens=200
    )
    print(response)

# Streaming
with Blossom(api_token="your_token") as client:
    for chunk in client.text.generate(
        "Tell me a story",
        stream=True
    ):
        print(chunk, end="", flush=True)
```

### Vision Analysis

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your_token") as client:
    # Analyze image from URL
    messages = [
        MessageBuilder.image(
            role="user",
            text="What's in this image?",
            image_url="https://example.com/image.jpg"
        )
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

### Reasoning + Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)  # Cache for 1 hour
def analyze_with_reasoning(question):
    # Enhance with structured thinking
    enhanced = enhancer.enhance(
        question,
        level="high",
        mode="auto",  # Auto-detects best mode
        api_version="v2",
        model="openai"
    )
    
    with Blossom(api_token="token") as client:
        if isinstance(enhanced, dict):
            # Native reasoning mode
            return client.text.chat(
                messages=[{"role": "user", "content": enhanced["prompt"]}],
                thinking=enhanced.get("thinking")
            )
        else:
            # Prompt reasoning mode
            return client.text.generate(enhanced, max_tokens=1000)

# First call: generates with reasoning and caches
result = analyze_with_reasoning("Design a microservices architecture")

# Second call: instant from cache!
result = analyze_with_reasoning("Design a microservices architecture")
```

---

## 📊 Feature Comparison

| Feature                     | v0.4.x (V1 API) | v0.5.0 (V2 API)         |
|-----------------------------|-----------------|-------------------------|
| **Image Quality Control**   | ❌               | ✅ (low/medium/high/hd)  |
| **Guidance Scale**          | ❌               | ✅ (1.0-20.0)            |
| **Negative Prompts**        | ❌               | ✅                       |
| **Transparent Images**      | ❌               | ✅                       |
| **Image-to-Image**          | ❌               | ✅                       |
| **Vision (Image Analysis)** | ❌               | ✅ **NEW!**              |
| **Audio Output**            | ❌               | ✅ **NEW!**              |
| **Function Calling**        | ❌               | ✅                       |
| **Max Tokens Control**      | ❌               | ✅                       |
| **Frequency Penalty**       | ❌               | ✅ (0-2)                 |
| **Presence Penalty**        | ❌               | ✅ (0-2)                 |
| **Top-P Sampling**          | ❌               | ✅                       |
| **Temperature Range**       | 0-1             | 0-2 (extended)          |
| **Basic Generation**        | ✅               | ✅                       |
| **Streaming**               | ✅               | ✅ (improved)            |
| **JSON Mode**               | ✅               | ✅ (more reliable)       |
| **CLI Interface**           | ✅               | ✅                       |
| **Reasoning Module**        | ✅               | ✅ (with native support) |
| **Caching Module**          | ✅               | ✅                       |
| **File Reader**             | ✅               | ✅                       |

---
- See [CHANGELOG.md](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/CHANGELOG.md) to Version history and updates
---
## 🆘 Need Help?

- 🐛 **Found a bug?** [Report it on GitHub](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 🔒 **Security issue?** See [Security Policy](../../SECURITY.md)
- 💡 **Have a question?** Check the [Error Handling Guide](ERROR_HANDLING.md)
- 📚 **Want examples?** See individual feature guides above
- 🤝 **Want to contribute?** Read the [Contributing Guide](../../CONTRIBUTING.md)
---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[PyPI Package](https://pypi.org/project/eclips-blossom-ai/) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

[Contributing](../../CONTRIBUTING.md) • [Security](../../SECURITY.md) • [License](../../LICENSE)

</div>