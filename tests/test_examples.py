import os
import pytest
import tempfile
from blossom_ai import Blossom, BlossomError

# === CONFIG ===
API_KEY = os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
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
    try:
        return fn(*args, **kwargs)
    except BlossomError as e:
        if "Payment Required" in str(e) or "tier not high enough" in str(e):
            pytest.skip("Paid tier required")
        if "520" in str(e):
            pytest.skip("Server error 520")
        raise

def assert_valid_response(response, min_len=1, contains=None):
    assert len(response) >= min_len
    if contains:
        assert contains in response

# === TESTS ===

@pytest.mark.parametrize("model", ["claude-large", "perplexity-fast", "perplexity-reasoning"])
def test_new_models(ai_auth, model):
    prompt = {
        "claude-large": "Say 'Hello from Claude Large' in one sentence",
        "perplexity-fast": "What is 2+2?",
        "perplexity-reasoning": "Explain why the sky is blue"
    }[model]
    response = safe_generate(ai_auth.text.generate, prompt, model=model)
    assert_valid_response(response, contains="4" if model == "perplexity-fast" else None)

@pytest.mark.parametrize("effort", ["low", "medium", "high"])
def test_reasoning_efforts(ai_auth, effort):
    response = safe_generate(
        ai_auth.text.generate,
        "Count to 3",
        model="openai-reasoning",
        reasoning_effort=effort
    )
    assert_valid_response(response)

def test_streaming(ai_auth):
    chunks = []
    stream = safe_generate(
        ai_auth.text.generate,
        "Count to 3",
        stream=True,
        model="openai"
    )
    for chunk in stream:
        chunks.append(chunk)
    assert len(chunks) > 0

def test_vision(ai_auth):
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this briefly"},
            {"type": "image_url", "image_url": {"url": "https://pollinations.ai/p/a%20cat", "detail": "auto"}}
        ]
    }]
    response = safe_generate(ai_auth.text.chat, messages=messages, model="openai")
    assert_valid_response(response)

@pytest.mark.parametrize("voice", ["alloy", "nova", "shimmer"])
def test_audio_generation(ai_anon, voice):
    audio = safe_generate(ai_anon.audio.generate, "Hello world", voice=voice)
    assert audio[:3] == b'ID3' or audio[:2] == b'\xff\xfb'

def test_audio_save(ai_anon):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        filename = f.name
    result = safe_generate(ai_anon.audio.save, "Test audio", filename, voice="alloy")
    assert os.path.exists(result)
    os.unlink(result)

def test_image_generation(ai_auth):
    filename = safe_generate(ai_auth.image.save, "a cute robot", "test_robot.jpg", width=512, height=512)
    assert os.path.exists(filename)
    os.unlink(filename)

def test_model_discovery(ai_anon):
    text_models = ai_anon.text.models()
    image_models = ai_anon.image.models()
    assert len(text_models) > 0
    assert len(image_models) > 0
    assert any(m in text_models for m in ["claude-large", "perplexity-fast"])

def test_invalid_parameters(ai_auth):
    with pytest.raises(BlossomError) as exc:
        ai_auth.text.generate("test", model="openai-reasoning", reasoning_effort="invalid")
    assert "INVALID_PARAMETER" in str(exc.value.error_type)