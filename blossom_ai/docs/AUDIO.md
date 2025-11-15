# 🔊 Audio Support Guide

> **Generate audio responses with text-to-speech capabilities**

Learn how to use audio output features in Blossom AI V2 API for creating voice-enabled applications.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Voice Selection](#voice-selection)
- [Audio Formats](#audio-formats)
- [Modalities](#modalities)
- [Advanced Usage](#advanced-usage)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)

---

## 🌟 Overview

### Audio Capabilities

**What's Supported:**
- 🔊 **Text-to-Speech**: Generate audio from text responses
- 🎤 **Voice Selection**: Multiple voice options
- 📦 **Format Options**: WAV, MP3, OPUS
- 🔄 **Multimodal**: Combine text + audio output

**Current Limitations:**
- ⚠️ Audio **output** only (no audio input yet)
- ⚠️ Only works with `openai` model
- ⚠️ Experimental feature - may have limited availability

### Model Support

| Model        | Audio Output | Audio Input |
|--------------|--------------|-------------|
| `openai`     | ✅ Yes        | ❌ Not yet   |
| `gemini`     | ❌ No         | ❌ No        |
| Other models | ❌ No         | ❌ No        |

---

## 🚀 Quick Start

### Basic Audio Generation

```python
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    messages = [
        {"role": "user", "content": "Say hello"}
    ]
    
    # Request audio output
    response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={
            "voice": "alloy",
            "format": "wav"
        }
    )
    
    print("Text response:", response)
    # Audio data would be available in response metadata
```

### Text-Only vs Audio Output

```python
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    messages = [{"role": "user", "content": "Hello"}]
    
    # Text only (default)
    text_response = client.text.chat(messages, model="openai")
    
    # Text + Audio
    audio_response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={"voice": "nova", "format": "mp3"}
    )
```

---

## 🎤 Voice Selection

### Available Voices

```python
# Voice options with characteristics
VOICES = {
    "alloy": "Neutral, balanced voice",
    "echo": "Deep, resonant voice",
    "fable": "British accent, expressive",
    "onyx": "Deep, authoritative voice",
    "nova": "Warm, friendly voice",
    "shimmer": "Soft, gentle voice"
}
```

### Voice Examples

```python
from blossom_ai import Blossom

def test_voices():
    """Test different voices"""
    with Blossom(api_token="your_token") as client:
        text = "Hello, this is a test of the audio system."
        
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        
        for voice in voices:
            print(f"\n🔊 Testing voice: {voice}")
            
            response = client.text.chat(
                messages=[{"role": "user", "content": text}],
                model="openai",
                modalities=["text", "audio"],
                audio={
                    "voice": voice,
                    "format": "wav"
                }
            )
            
            print(f"Response: {response[:50]}...")

test_voices()
```

### Voice Selection Guide

```python
from blossom_ai import Blossom

def choose_voice_for_context(context: str) -> str:
    """Choose appropriate voice based on context"""
    voice_map = {
        "professional": "onyx",      # Deep, authoritative
        "friendly": "nova",          # Warm, approachable
        "storytelling": "fable",     # Expressive, engaging
        "technical": "echo",         # Clear, resonant
        "assistant": "alloy",        # Neutral, balanced
        "calm": "shimmer"            # Soft, soothing
    }
    return voice_map.get(context, "alloy")

# Usage
with Blossom(api_token="your_token") as client:
    voice = choose_voice_for_context("professional")
    
    response = client.text.chat(
        messages=[{"role": "user", "content": "Present quarterly results"}],
        model="openai",
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "mp3"}
    )
```

---

## 📦 Audio Formats

### Supported Formats

```python
# Format options
FORMATS = {
    "wav": {
        "quality": "High",
        "size": "Large",
        "compatibility": "Universal",
        "streaming": "No"
    },
    "mp3": {
        "quality": "Good",
        "size": "Medium",
        "compatibility": "Universal",
        "streaming": "Yes"
    },
    "opus": {
        "quality": "Excellent",
        "size": "Small",
        "compatibility": "Modern browsers",
        "streaming": "Yes"
    }
}
```

### Format Selection

```python
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    messages = [{"role": "user", "content": "Hello"}]
    
    # WAV: High quality, large files
    wav_response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"}
    )
    
    # MP3: Balanced quality/size
    mp3_response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "mp3"}
    )
    
    # OPUS: Best compression, modern
    opus_response = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "opus"}
    )
```

### Format Recommendations

```python
def choose_format(use_case: str) -> str:
    """Choose format based on use case"""
    if use_case == "web_streaming":
        return "opus"  # Best for web streaming
    elif use_case == "mobile_app":
        return "mp3"   # Good compatibility
    elif use_case == "high_quality":
        return "wav"   # Maximum quality
    elif use_case == "storage":
        return "opus"  # Best compression
    else:
        return "mp3"   # Default balanced choice

# Usage
format_choice = choose_format("web_streaming")
```

---

## 🔄 Modalities

### Understanding Modalities

```python
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    messages = [{"role": "user", "content": "Hello"}]
    
    # Text only (default)
    text_only = client.text.chat(
        messages,
        model="openai"
        # modalities defaults to ["text"]
    )
    
    # Text + Audio
    multimodal = client.text.chat(
        messages,
        model="openai",
        modalities=["text", "audio"],  # Request both
        audio={"voice": "nova", "format": "mp3"}
    )
```

### Modality Options

```python
# Available modalities
MODALITIES = {
    "text": "Text output (always available)",
    "audio": "Audio output (requires audio config)"
}

# Examples
with Blossom(api_token="token") as client:
    messages = [{"role": "user", "content": "Test"}]
    
    # Only text
    response = client.text.chat(
        messages,
        modalities=["text"]  # Explicit text only
    )
    
    # Text and audio
    response = client.text.chat(
        messages,
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "mp3"}
    )
```

---

## 🔧 Advanced Usage

### Custom Audio Configuration

```python
from blossom_ai import Blossom

class AudioConfig:
    """Custom audio configuration"""
    
    def __init__(
        self,
        voice: str = "alloy",
        format: str = "mp3",
        enable_audio: bool = True
    ):
        self.voice = voice
        self.format = format
        self.enable_audio = enable_audio
    
    def to_dict(self) -> dict:
        """Convert to API format"""
        return {
            "voice": self.voice,
            "format": self.format
        }
    
    def get_modalities(self) -> list:
        """Get modalities list"""
        if self.enable_audio:
            return ["text", "audio"]
        return ["text"]

# Usage
config = AudioConfig(voice="nova", format="opus")

with Blossom(api_token="token") as client:
    response = client.text.chat(
        messages=[{"role": "user", "content": "Hello"}],
        model="openai",
        modalities=config.get_modalities(),
        audio=config.to_dict()
    )
```

### Async Audio Generation

```python
import asyncio
from blossom_ai import Blossom

async def generate_audio_async():
    """Generate audio asynchronously"""
    async with Blossom(api_token="token") as client:
        response = await client.text.chat(
            messages=[{"role": "user", "content": "Hello"}],
            model="openai",
            modalities=["text", "audio"],
            audio={"voice": "nova", "format": "mp3"}
        )
        return response

# Run
result = asyncio.run(generate_audio_async())
```

### Batch Audio Generation

```python
import asyncio
from blossom_ai import Blossom

async def batch_audio_generation(texts: list[str], voice: str = "alloy"):
    """Generate audio for multiple texts"""
    async with Blossom(api_token="token") as client:
        tasks = []
        
        for text in texts:
            task = client.text.chat(
                messages=[{"role": "user", "content": text}],
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": voice, "format": "mp3"}
            )
            tasks.append(task)
        
        return await asyncio.gather(*tasks)

# Usage
texts = [
    "Welcome to our service",
    "Thank you for your order",
    "Your request has been processed"
]

results = asyncio.run(batch_audio_generation(texts, voice="nova"))
```

---

## 💼 Use Cases

### Use Case 1: Voice Assistant

```python
from blossom_ai import Blossom

class VoiceAssistant:
    """Voice-enabled assistant"""
    
    def __init__(self, api_token: str, voice: str = "nova"):
        self.api_token = api_token
        self.voice = voice
        self.conversation = []
    
    def speak(self, text: str) -> str:
        """Generate spoken response"""
        self.conversation.append({
            "role": "user",
            "content": text
        })
        
        with Blossom(api_token=self.api_token) as client:
            response = client.text.chat(
                self.conversation,
                model="openai",
                modalities=["text", "audio"],
                audio={
                    "voice": self.voice,
                    "format": "mp3"
                }
            )
        
        self.conversation.append({
            "role": "assistant",
            "content": response
        })
        
        return response

# Usage
assistant = VoiceAssistant("your_token", voice="nova")
response = assistant.speak("What's the weather like?")
print(response)
```

### Use Case 2: Text-to-Speech Service

```python
from blossom_ai import Blossom

class TextToSpeechService:
    """TTS service with audio output"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
    
    def convert(
        self,
        text: str,
        voice: str = "alloy",
        format: str = "mp3"
    ) -> dict:
        """Convert text to speech"""
        with Blossom(api_token=self.api_token) as client:
            response = client.text.chat(
                messages=[{"role": "user", "content": text}],
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": voice, "format": format}
            )
        
        return {
            "text": response,
            "voice": voice,
            "format": format
        }

# Usage
tts = TextToSpeechService("your_token")
result = tts.convert(
    "Hello, welcome to our application",
    voice="nova",
    format="mp3"
)
```

### Use Case 3: Audiobook Generator

```python
from blossom_ai import Blossom
import asyncio

class AudiobookGenerator:
    """Generate audiobook from text"""
    
    def __init__(self, api_token: str, voice: str = "fable"):
        self.api_token = api_token
        self.voice = voice
    
    async def generate_chapter(self, chapter_text: str) -> dict:
        """Generate audio for one chapter"""
        async with Blossom(api_token=self.api_token) as client:
            response = await client.text.chat(
                messages=[{
                    "role": "user",
                    "content": f"Read this chapter:\n\n{chapter_text}"
                }],
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": self.voice, "format": "mp3"}
            )
            
            return {
                "text": response,
                "voice": self.voice
            }
    
    async def generate_book(self, chapters: list[str]) -> list:
        """Generate audio for entire book"""
        tasks = [
            self.generate_chapter(chapter)
            for chapter in chapters
        ]
        return await asyncio.gather(*tasks)

# Usage
generator = AudiobookGenerator("your_token", voice="fable")
chapters = [
    "Chapter 1: The Beginning...",
    "Chapter 2: The Journey...",
    "Chapter 3: The End..."
]
audiobook = asyncio.run(generator.generate_book(chapters))
```

### Use Case 4: Multi-Language Voice

```python
from blossom_ai import Blossom

class MultiLanguageVoice:
    """Multi-language voice system"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.voice_map = {
            "en": "nova",      # English: friendly
            "es": "fable",     # Spanish: expressive
            "fr": "shimmer",   # French: elegant
            "de": "echo",      # German: clear
            "it": "alloy"      # Italian: balanced
        }
    
    def speak(self, text: str, language: str = "en") -> str:
        """Speak text in specified language"""
        voice = self.voice_map.get(language, "alloy")
        
        with Blossom(api_token=self.api_token) as client:
            # First, translate if needed
            if language != "en":
                translation_prompt = f"Translate to {language}: {text}"
                text = client.text.generate(translation_prompt)
            
            # Then generate audio
            response = client.text.chat(
                messages=[{"role": "user", "content": text}],
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": voice, "format": "mp3"}
            )
            
            return response

# Usage
voice = MultiLanguageVoice("your_token")
response = voice.speak("Hello, how are you?", language="es")
```

---

## ✅ Best Practices

### 1. Choose Appropriate Voice

```python
# ❌ Don't use same voice for everything
voice = "alloy"  # Always alloy

# ✅ Choose voice based on context
def select_voice(context: str) -> str:
    contexts = {
        "professional": "onyx",
        "friendly": "nova",
        "calm": "shimmer"
    }
    return contexts.get(context, "alloy")
```

### 2. Select Right Format

```python
from blossom_ai import Blossom

# ❌ Don't always use WAV (large files)
audio_config = {"voice": "alloy", "format": "wav"}

# ✅ Choose format based on use case
def select_format(use_case: str) -> str:
    if use_case == "streaming":
        return "opus"
    elif use_case == "storage":
        return "mp3"
    return "mp3"  # Default

audio_config = {
    "voice": "alloy",
    "format": select_format("streaming")
}
```

### 3. Handle Audio Gracefully

```python
from blossom_ai import Blossom, BlossomError

with Blossom(api_token="token") as client:
    try:
        response = client.text.chat(
            messages=[{"role": "user", "content": "Hello"}],
            model="openai",
            modalities=["text", "audio"],
            audio={"voice": "nova", "format": "mp3"}
        )
    except BlossomError as e:
        if "audio" in str(e).lower():
            # Fallback to text only
            response = client.text.chat(
                messages=[{"role": "user", "content": "Hello"}],
                model="openai"
            )
```

### 4. Cache Audio Responses

```python
from blossom_ai.utils import cached

@cached(ttl=7200)  # Cache for 2 hours
def generate_audio_cached(text: str, voice: str = "alloy"):
    """Generate audio with caching"""
    with Blossom(api_token="token") as client:
        return client.text.chat(
            messages=[{"role": "user", "content": text}],
            model="openai",
            modalities=["text", "audio"],
            audio={"voice": voice, "format": "mp3"}
        )

# First call: generates
result = generate_audio_cached("Welcome")

# Second call: instant from cache
result = generate_audio_cached("Welcome")
```

### 5. Test Audio Availability

```python
from blossom_ai import Blossom

def check_audio_support() -> bool:
    """Check if audio is supported"""
    try:
        with Blossom(api_token="token") as client:
            response = client.text.chat(
                messages=[{"role": "user", "content": "test"}],
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "mp3"}
            )
            return True
    except Exception as e:
        if "audio" in str(e).lower() or "not support" in str(e).lower():
            return False
        raise

# Use at startup
if check_audio_support():
    print("✅ Audio support available")
else:
    print("⚠️ Audio not supported, using text-only mode")
```

---

## ⚠️ Limitations & Notes

### Current Limitations

1. **Output Only**: Audio input not yet supported
2. **Model Support**: Only `openai` model supports audio
3. **Experimental**: Feature may have limited availability
4. **No Direct Download**: Audio data in response metadata (implementation-specific)

### Coming Soon

- 🎤 Audio input support
- 🔊 More voice options
- 🌍 Language-specific voices
- 🎛️ Voice customization (speed, pitch)

---

## 🔗 Related Documentation

- [Multimodal Guide](MULTIMODAL.md) - Combine audio with vision
- [Text Generation](TEXT_GENERATION.md) - Text generation basics
- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Error Handling](ERROR_HANDLING.md) - Handle audio errors

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Multimodal Guide](MULTIMODAL.md) | [Vision Guide](VISION.md) →

</div>