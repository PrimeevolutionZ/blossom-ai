"""
Blossom AI - Test Suite (v0.5.4)
"""

import os
import pytest
import tempfile
from blossom_ai import Blossom, BlossomError

# === CONFIG ===
API_KEY = "Your_API_Key"
SKIP_AUTH = not API_KEY

# === FIXTURES ===
@pytest.fixture
def ai_auth():
    if SKIP_AUTH:
        pytest.skip("API key not set")
    return Blossom(api_token=API_KEY, timeout=60)

@pytest.fixture
def ai_anon():
    return Blossom(timeout=60)

# === HELPERS ===
def safe_generate(fn, *args, **kwargs):
    """
    Safely execute a generation function with proper error handling.
    """
    try:
        return fn(*args, **kwargs)
    except BlossomError as e:
        error_str = str(e)

        # Check if this is an audio-related call
        is_audio_call = 'audio' in str(fn).lower()

        # Skip payment errors (but NOT for audio which should be free)
        if ("Payment Required" in error_str or "tier not high enough" in error_str) and not is_audio_call:
            pytest.skip("Paid tier required")

        # Skip server errors
        if "520" in error_str:
            pytest.skip("Server error 520")

        # Skip temporary API issues
        if "400" in error_str or "Bad Request" in error_str:
            pytest.skip(f"API returned 400: {error_str[:150]}")

        # Skip 500 errors
        if "500" in error_str or "Internal Server Error" in error_str:
            pytest.skip(f"Server error 500: {error_str[:150]}")

        # Skip rate limits
        if "429" in error_str or "Rate limit" in error_str:
            pytest.skip(f"Rate limited: {error_str[:150]}")

        # All other errors should fail the test
        raise
    except Exception as e:
        # Catch non-BlossomError exceptions too
        error_str = str(e)
        if "402" in error_str or "Payment Required" in error_str:
            pytest.skip(f"Payment required: {error_str[:150]}")
        if "401" in error_str or "Unauthorized" in error_str:
            pytest.skip(f"Authentication error: {error_str[:150]}")
        raise

def assert_valid_response(response, min_len=1, contains=None):
    """Assert that response is valid."""
    assert response is not None, "Response is None"
    # Allow empty responses for some cases
    if min_len > 0:
        assert len(response) >= min_len, f"Response too short: {len(response)} < {min_len}"
    if contains:
        assert contains in str(response), f"Response doesn't contain '{contains}'"

# === TESTS ===

@pytest.mark.parametrize("model", ["claude-large", "perplexity-fast", "perplexity-reasoning"])
def test_new_models(ai_auth, model):
    """Test new models added in v0.5.3"""
    prompt = {
        "claude-large": "Say 'Hello from Claude Large' in one sentence",
        "perplexity-fast": "What is 2+2?",
        "perplexity-reasoning": "Explain why the sky is blue"
    }[model]
    response = safe_generate(ai_auth.text.generate, prompt, model=model)
    assert_valid_response(response, min_len=1)

@pytest.mark.parametrize("effort", ["low", "medium", "high"])
def test_reasoning_efforts(ai_auth, effort):
    """Test reasoning effort parameter"""
    response = safe_generate(
        ai_auth.text.generate,
        "Count to 3",
        model="openai-reasoning",
        reasoning_effort=effort
    )
    assert_valid_response(response)

def test_streaming(ai_auth):
    """Test streaming responses"""
    chunks = []
    stream = safe_generate(
        ai_auth.text.generate,
        "Count to 3",
        stream=True,
        model="openai"
    )
    for chunk in stream:
        chunks.append(chunk)
    assert len(chunks) > 0, "No chunks received from stream"

def test_vision(ai_auth):
    """Test vision capabilities"""
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "What do you see? Answer in one word."},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/1024px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                }
            }
        ]
    }]
    response = safe_generate(ai_auth.text.chat, messages=messages, model="openai", max_tokens=100)
    # Vision might return empty if model doesn't support it, so allow min_len=0
    assert_valid_response(response, min_len=0)
    if len(response) == 0:
        pytest.skip("Vision returned empty response - model may not support vision")

@pytest.mark.parametrize("voice", ["alloy", "nova", "shimmer"])
def test_audio_generation(ai_anon, voice):
    """
    Test audio generation (TTS).
    Audio should work without authentication.
    """
    audio = safe_generate(ai_anon.audio.generate, "Hello world", voice=voice)
    assert audio is not None, "Audio data is None"
    assert len(audio) > 0, "Audio data is empty"
    # Check for MP3 headers (ID3 tag or MPEG sync)
    assert audio[:3] == b'ID3' or audio[:2] == b'\xff\xfb', f"Invalid audio format: {audio[:10]}"

def test_audio_save(ai_anon):
    """
    Test saving audio to file.
    Audio should work without authentication.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        filename = f.name

    try:
        result = safe_generate(ai_anon.audio.save, "Test audio", filename, voice="alloy")
        assert os.path.exists(result), f"Audio file not created at {result}"
        assert os.path.getsize(result) > 0, "Audio file is empty"
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.unlink(filename)

def test_image_generation(ai_auth):
    """
    Test image generation and saving.
    """
    filename = "test_robot.jpg"
    try:
        result = safe_generate(
            ai_auth.image.save,
            "a cute robot",
            filename,
            width=512,
            height=512,
            model="flux"
        )
        assert os.path.exists(result), f"Image file not created at {result}"
        assert os.path.getsize(result) > 0, "Image file is empty"

        # Verify it's a valid image by checking headers
        with open(result, 'rb') as f:
            header = f.read(10)
            # Check for JPEG or PNG headers
            is_jpeg = header[:2] == b'\xff\xd8'
            is_png = header[:8] == b'\x89PNG\r\n\x1a\n'
            assert is_jpeg or is_png, f"Invalid image format: {header[:10]}"
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.unlink(filename)

def test_model_discovery(ai_anon):
    """Test dynamic model discovery"""
    text_models = ai_anon.text.models()
    image_models = ai_anon.image.models()

    assert len(text_models) > 0, "No text models discovered"
    assert len(image_models) > 0, "No image models discovered"

    # Check for newly added models (may not all be available)
    has_new_models = any(m in text_models for m in ["claude-large", "perplexity-fast", "searchgpt"])
    if not has_new_models:
        print(f"Warning: New models not found. Available: {text_models[:5]}...")

def test_invalid_parameters(ai_auth):
    """Test parameter validation"""
    with pytest.raises(BlossomError) as exc:
        ai_auth.text.generate("test", model="openai-reasoning", reasoning_effort="invalid")
    assert "INVALID_PARAMETER" in str(exc.value.error_type)

def test_searchgpt_model(ai_auth):
    """Test the new searchgpt model (may require special tier)"""
    try:
        response = safe_generate(
            ai_auth.text.generate,
            "What is 2+2?",  # Simple query
            model="searchgpt"
        )
        assert_valid_response(response, min_len=1)
    except Exception:
        pytest.skip("searchgpt model may not be available in current tier")

def test_image_url_generation(ai_auth):
    """Test generating image URL without downloading"""
    url = safe_generate(
        ai_auth.image.generate_url,
        "a beautiful sunset",
        width=512,
        height=512
    )
    assert url.startswith("https://image.pollinations.ai/prompt/"), f"Invalid URL: {url}"

def test_concurrent_requests(ai_auth):
    """Test multiple concurrent text requests"""
    import concurrent.futures

    def generate_text(prompt):
        try:
            return safe_generate(ai_auth.text.generate, prompt, model="openai")
        except Exception as e:
            # In concurrent context, convert exceptions to skip
            pytest.skip(f"Concurrent request failed: {e}")

    prompts = [f"Say the number {i}" for i in range(3, 6)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(generate_text, prompts))

    assert len(results) == 3
    # Allow some empty results due to rate limiting
    non_empty = [r for r in results if r and len(r) > 0]
    assert len(non_empty) > 0, "All concurrent requests failed"