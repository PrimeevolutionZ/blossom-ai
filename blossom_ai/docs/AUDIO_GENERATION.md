# Audio Generation Guide (Text-to-Speech)

Blossom AI allows you to convert text into speech using various voices. **Note that Audio Generation requires an API token for authentication.**

## 🎙️ Generating and Saving Audio

Use the `save()` method to generate audio from text and save it to a file (e.g., MP3 format).

```python
from blossom_ai import Blossom

# Audio generation requires an API token
ai = Blossom(api_token="YOUR_TOKEN")

try:
    # Generate audio and save to 'welcome.mp3'
    ai.audio.save(
        text="Hello, welcome to Blossom AI! This is a text-to-speech example.",
        output_path="welcome.mp3",
        voice="nova" # Specify the voice model to use
    )
    print("Audio successfully generated and saved to welcome.mp3")

except Exception as e:
    print(f"An error occurred during audio generation. Did you provide a valid API token? Error: {e}")

# If you used a context manager, it would handle cleanup:
# with Blossom(api_token="YOUR_TOKEN") as ai:
#     ai.audio.save(...)
```

## Available Voices

You can specify different voices using the `voice` parameter. Consult the Pollinations.AI documentation for the full list of available voices. Common examples include:

- `nova` (default)
- `echo`
- `alloy`
- `shimmer`
- `onyx`
- `fable`

## Generating Audio Bytes

If you need the raw audio data (bytes) for in-memory processing or streaming, use the `generate()` method.

```python
from blossom_ai import Blossom

# Audio generation requires an API token
ai = Blossom(api_token="YOUR_TOKEN")

# Generate audio bytes
audio_bytes = ai.audio.generate(
    text="This is an in-memory audio generation test.",
    voice="echo"
)

# You can now process or save the bytes manually
# with open("test_audio.mp3", "wb") as f:
#     f.write(audio_bytes)
```
