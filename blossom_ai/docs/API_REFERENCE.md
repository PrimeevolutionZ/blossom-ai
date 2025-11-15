# Message Builder - CORRECTED

Helper for creating messages with text, images, and audio (NEW in v0.5.0).

## MessageBuilder.text()

Create regular text message.

```python
from blossom_ai import MessageBuilder

message = MessageBuilder.text(
    role: str,
    content: str,
    name: str = None  # Optional speaker name
) -> dict
```

**Parameters:**
- `role` (str): "system", "user", or "assistant"
- `content` (str): Message text
- `name` (str, optional): Speaker name for multi-user chats

**Returns:** dict - Message object

**Example:**
```python
# Simple message
msg = MessageBuilder.text("user", "Hello!")
# Returns: {"role": "user", "content": "Hello!"}

# With name
msg = MessageBuilder.text("user", "Hello!", name="Alice")
# Returns: {"role": "user", "content": "Hello!", "name": "Alice"}
```

---

## MessageBuilder.image()

Create vision message with image.

```python
from blossom_ai import MessageBuilder

message = MessageBuilder.image(
    role: str,
    text: str,
    image_url: str = None,      # URL to image
    image_path: Path | str = None,  # Local file path
    image_data: bytes = None,   # Raw image bytes
    detail: str = "auto"        # "low", "auto", or "high"
) -> dict
```

**Parameters:**
- `role` (str): "user" (typically)
- `text` (str): Question/instruction about the image
- `image_url` (str, optional): URL to image
- `image_path` (Path | str, optional): Path to local image file
- `image_data` (bytes, optional): Raw image bytes (e.g., from upload)
- `detail` (str): "low", "auto", or "high". Default: "auto"

**Note:** Provide **exactly one** image source: `image_url`, `image_path`, OR `image_data`.

**Returns:** dict - Message object with image content

**Example - From URL:**
```python
msg = MessageBuilder.image(
    role="user",
    text="What's in this image?",
    image_url="https://example.com/photo.jpg",
    detail="auto"
)
```

**Example - From Local File:**
```python
from pathlib import Path

msg = MessageBuilder.image(
    role="user",
    text="Describe this photo",
    image_path="photos/sunset.jpg",
    detail="high"
)

# Or with Path object
msg = MessageBuilder.image(
    role="user",
    text="Analyze this",
    image_path=Path("images/chart.png")
)
```

**Example - From Raw Bytes:**
```python
# From file upload or API response
with open("image.jpg", "rb") as f:
    image_bytes = f.read()

msg = MessageBuilder.image(
    role="user",
    text="What's this?",
    image_data=image_bytes,
    detail="auto"
)
```

**Example - Multiple Images:**
```python
# For multiple images, create separate content blocks
messages = [
    MessageBuilder.image(
        role="user",
        text="Compare these images",
        image_url="https://example.com/image1.jpg"
    ),
    MessageBuilder.image(
        role="user", 
        text="",  # Empty text for additional images
        image_url="https://example.com/image2.jpg"
    )
]
```

---

## MessageBuilder.audio() - NEW

Create audio-input message.

```python
from blossom_ai import MessageBuilder

message = MessageBuilder.audio(
    role: str,
    text: str = None,           # Optional text prompt
    audio_url: str = None,      # URL to audio file
    audio_path: Path | str = None,  # Local audio file
    audio_data: bytes = None,   # Raw audio bytes
    format: str = "wav"         # Audio format
) -> dict
```

**Parameters:**
- `role` (str): "user" (typically)
- `text` (str, optional): Optional text prompt/question
- `audio_url` (str, optional): URL to audio file
- `audio_path` (Path | str, optional): Path to local audio file
- `audio_data` (bytes, optional): Raw audio bytes
- `format` (str): Audio format - "wav", "mp3", "pcm16", "g711_ulaw", "g711_alaw". Default: "wav"

**Note:** Provide **exactly one** audio source: `audio_url`, `audio_path`, OR `audio_data`.

**Returns:** dict - Message object with audio content

**Example - From URL:**
```python
msg = MessageBuilder.audio(
    role="user",
    text="Transcribe this audio",
    audio_url="https://example.com/speech.wav",
    format="wav"
)
```

**Example - From Local File:**
```python
msg = MessageBuilder.audio(
    role="user",
    text="What language is spoken?",
    audio_path="recordings/speech.mp3",
    format="mp3"
)
```

**Example - From Raw Bytes:**
```python
with open("audio.wav", "rb") as f:
    audio_bytes = f.read()

msg = MessageBuilder.audio(
    role="user",
    audio_data=audio_bytes,
    format="wav"
)
```

**Example - Audio + Text:**
```python
# Combine audio with text prompt
msg = MessageBuilder.audio(
    role="user",
    text="Transcribe and summarize the key points from this recording",
    audio_path="meeting.wav"
)
```

---

## Complete Usage Example

```python
from blossom_ai import Blossom, MessageBuilder

with Blossom(api_token="your-token") as client:
    # Text only
    msg1 = MessageBuilder.text("user", "Hello")
    
    # Image analysis
    msg2 = MessageBuilder.image(
        role="user",
        text="What's in this image?",
        image_url="https://example.com/photo.jpg",
        detail="high"
    )
    
    # Audio transcription
    msg3 = MessageBuilder.audio(
        role="user",
        text="Transcribe this",
        audio_path="recording.wav"
    )
    
    # Use in chat
    messages = [
        MessageBuilder.text("system", "You are a helpful assistant"),
        msg1,
        MessageBuilder.text("assistant", "Hello! How can I help?"),
        msg2
    ]
    
    response = client.text.chat(messages, model="openai")
    print(response)
```

---

## Error Handling

```python
from blossom_ai import MessageBuilder, BlossomError

try:
    # Error: No image source provided
    msg = MessageBuilder.image(
        role="user",
        text="What's this?"
        # Missing: image_url, image_path, or image_data
    )
except ValueError as e:
    print(f"Error: {e}")  # "One image source required"

try:
    # Error: File not found
    msg = MessageBuilder.image(
        role="user",
        text="Analyze",
        image_path="nonexistent.jpg"
    )
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

---

## Best Practices

### 1. Always Provide Exactly One Source

```python
# GOOD: One source
msg = MessageBuilder.image("user", "What's this?", image_url="...")

# BAD: No sources
msg = MessageBuilder.image("user", "What's this?")

#  BAD: Multiple sources (will use first available)
msg = MessageBuilder.image("user", "What's this?", 
                          image_url="...", 
                          image_path="...")
```

### 2. Use Appropriate Detail Level

```python
# Low detail - faster, cheaper (thumbnails, icons)
msg = MessageBuilder.image("user", "Is this a cat?", 
                          image_url="...", 
                          detail="low")

# Auto - balanced (default, recommended)
msg = MessageBuilder.image("user", "Describe this image", 
                          image_url="...", 
                          detail="auto")

# High detail - slower, more accurate (complex images)
msg = MessageBuilder.image("user", "Read all text in this image", 
                          image_url="...", 
                          detail="high")
```

### 3. Handle File Paths Safely

```python
from pathlib import Path

# Use Path for better error handling
image_path = Path("photos/image.jpg")

if not image_path.exists():
    print(f"File not found: {image_path}")
else:
    msg = MessageBuilder.image(
        "user", 
        "Analyze this",
        image_path=image_path
    )
```

### 4. Specify Audio Format Correctly

```python
# Match file extension to format parameter
audio_files = {
    "speech.wav": "wav",
    "music.mp3": "mp3",
    "recording.m4a": "wav"  # Convert or use appropriate format
}

for filepath, format in audio_files.items():
    msg = MessageBuilder.audio(
        "user",
        "Transcribe",
        audio_path=filepath,
        format=format
    )
```

---

## Related Documentation

- **[Vision Guide](VISION.md)** - Complete vision features guide
- **[Audio Guide](AUDIO.md)** - Complete audio features guide
- **[Text Generation](TEXT_GENERATION.md)** - Text generation with messages
- **[API Reference](API_REFERENCE.md)** - Full API documentation