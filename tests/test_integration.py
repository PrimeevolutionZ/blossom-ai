"""
Blossom AI – Integration Tests (V2 API with Vision & Audio)
VCR-friendly tests for CI/CD
"""

import pytest
import vcr
from pathlib import Path

from blossom_ai import Blossom, MessageBuilder
from blossom_ai.core.errors import AuthenticationError, ValidationError

CASSETTES_DIR = Path(__file__).parent / "cassettes"
CASSETTES_DIR.mkdir(exist_ok=True)

vcr_config = vcr.VCR(
    cassette_library_dir=str(CASSETTES_DIR),
    record_mode="once",
    match_on=["method", "scheme", "host", "port", "path"],
    filter_headers=["authorization"],
    filter_query_parameters=["token"],
)

API_TOKEN = "your_token_here"
SKIP_IF_NO_TOKEN = pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your_token_here", reason="No token")


# ------------------------------------------------------------------------------
# TEXT GENERATION (V2 API)
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_text_generate_simple.yaml")
def test_v2_text_generate_simple():
    """Test basic V2 text generation"""
    with Blossom(api_token=API_TOKEN) as client:
        result = client.text.generate("Say hello in 3 words")
        assert isinstance(result, str) and 0 < len(result) < 100


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_text_generate_stream.yaml")
def test_v2_text_generate_stream():
    """Test V2 streaming"""
    if (CASSETTES_DIR / "v2_text_generate_stream.yaml").exists():
        pytest.skip("Streaming test disabled with VCR cassette")

    with Blossom(api_token=API_TOKEN) as client:
        chunks = []
        for chunk in client.text.generate("Count to 5", stream=True):
            chunks.append(chunk)
        assert len(chunks) > 0 and "".join(chunks)


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_text_chat.yaml")
def test_v2_text_chat():
    """Test V2 chat completion"""
    with Blossom(api_token=API_TOKEN) as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is 2+2?"},
        ]
        result = client.text.chat(messages)
        assert "4" in result or "four" in result.lower()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_text_json_mode.yaml")
def test_v2_text_json_mode():
    """Test V2 JSON mode"""
    with Blossom(api_token=API_TOKEN) as client:
        result = client.text.generate(
            "Return JSON with keys: name and age",
            json_mode=True
        )
        assert isinstance(result, str)

        import json
        data = json.loads(result)
        assert isinstance(data, dict)


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_text_models_list.yaml")
def test_v2_text_models_list():
    """Test V2 text models listing"""
    with Blossom(api_token=API_TOKEN) as client:
        models = client.text.models()
        assert isinstance(models, list) and len(models) > 0


# ------------------------------------------------------------------------------
# IMAGE GENERATION (V2 API)
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_image_generate.yaml")
def test_v2_image_generate():
    """Test V2 image generation"""
    if (CASSETTES_DIR / "v2_image_generate.yaml").exists():
        pytest.skip("Image generate cassette mismatch – skip")

    with Blossom(api_token=API_TOKEN) as client:
        image_data = client.image.generate("a red circle", model="flux")
        assert isinstance(image_data, bytes) and len(image_data) > 1_000
        # Check for PNG or JPEG signature
        assert image_data[:4] == b"\x89PNG" or image_data[:2] == b"\xff\xd8"


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_image_generate_url.yaml")
def test_v2_image_generate_url():
    """Test V2 image URL generation"""
    with Blossom(api_token=API_TOKEN) as client:
        url = client.image.generate_url("a blue square", model="flux")
        assert url.startswith("https://") and "pollinations.ai" in url
        # Security: token should NOT be in URL
        assert API_TOKEN not in url and "token=" not in url.lower()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_image_models_list.yaml")
def test_v2_image_models_list():
    """Test V2 image models listing"""
    with Blossom(api_token=API_TOKEN) as client:
        models = client.image.models()
        assert isinstance(models, list) and len(models) > 0


# ------------------------------------------------------------------------------
# VISION TESTS (NEW in v0.5.0)
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_vision_url.yaml")
def test_v2_vision_with_url():
    """Test V2 vision with image URL"""
    with Blossom(api_token=API_TOKEN) as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="What do you see in this image?",
                image_url="https://pollinations.ai/p/a%20cat",
                detail="auto"
            )
        ]

        try:
            result = client.text.chat(messages, model="openai")
            assert isinstance(result, str) and len(result) > 0
        except Exception as e:
            # Vision may not be available for all models
            if "vision" in str(e).lower() or "not support" in str(e).lower():
                pytest.skip("Vision not supported by model")
            raise


@SKIP_IF_NO_TOKEN
def test_v2_vision_message_builder():
    """Test MessageBuilder for vision"""
    # Test image URL message
    msg = MessageBuilder.image_message(
        role="user",
        text="Analyze this",
        image_url="https://example.com/image.jpg"
    )

    assert msg["role"] == "user"
    assert isinstance(msg["content"], list)
    assert len(msg["content"]) == 2  # text + image
    assert msg["content"][0]["type"] == "text"
    assert msg["content"][1]["type"] == "image_url"


# ------------------------------------------------------------------------------
# AUDIO TESTS (NEW in v0.5.0)
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_audio_output.yaml")
def test_v2_audio_output():
    """Test V2 audio output (TTS)"""
    with Blossom(api_token=API_TOKEN) as client:
        messages = [{"role": "user", "content": "Say hello"}]

        try:
            result = client.text.chat(
                messages,
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "wav"}
            )
            assert isinstance(result, str)
        except Exception as e:
            # Audio may not be fully available yet
            if "audio" in str(e).lower() or "modalities" in str(e).lower():
                pytest.skip("Audio not fully supported yet")
            raise


# ------------------------------------------------------------------------------
# ERROR HANDLING
# ------------------------------------------------------------------------------

def test_v2_invalid_token():
    """Test 401 authentication error"""
    with Blossom(api_token="invalid_token_12345") as client:
        with pytest.raises(AuthenticationError):
            client.text.generate("test")


def test_v2_prompt_validation():
    """Test prompt length validation"""
    with Blossom(api_token=API_TOKEN) as client:
        with pytest.raises(ValidationError):
            # Image prompts limited to 200 chars
            client.image.generate("x" * 300)


@SKIP_IF_NO_TOKEN
def test_v2_token_not_in_url():
    """Test that token is NOT exposed in URLs"""
    with Blossom(api_token=API_TOKEN) as client:
        url = client.image.generate_url("test", model="flux")
        # CRITICAL: Token should never be in URL
        assert API_TOKEN not in url
        assert "token=" not in url.lower()
        assert "key=" not in url.lower()


# ------------------------------------------------------------------------------
# ASYNC TESTS
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_async_text_generate.yaml")
async def test_v2_async_text_generate():
    """Test V2 async text generation"""
    async with Blossom(api_token=API_TOKEN) as client:
        result = await client.text.generate("Say hi")
        assert isinstance(result, str) and len(result) > 0


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_async_image_generate.yaml")
async def test_v2_async_image_generate():
    """Test V2 async image generation"""
    async with Blossom(api_token=API_TOKEN) as client:
        image_data = await client.image.generate("a cat", model="flux")
        assert isinstance(image_data, bytes) and len(image_data) > 1_000


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_async_stream.yaml")
async def test_v2_async_stream():
    """Test V2 async streaming"""
    if (CASSETTES_DIR / "v2_async_stream.yaml").exists():
        pytest.skip("Async streaming test disabled with VCR cassette")

    async with Blossom(api_token=API_TOKEN) as client:
        chunks = []
        async for chunk in await client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
        assert len(chunks) > 0


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
async def test_v2_async_vision():
    """Test V2 async vision"""
    async with Blossom(api_token=API_TOKEN) as client:
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="Describe this briefly",
                image_url="https://pollinations.ai/p/a%20dog"
            )
        ]

        try:
            result = await client.text.chat(messages, model="openai")
            assert isinstance(result, str) and len(result) > 0
        except Exception as e:
            if "vision" in str(e).lower():
                pytest.skip("Vision not supported")
            raise


# ------------------------------------------------------------------------------
# MISC & CLEANUP
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("v2_model_cache_ttl.yaml")
def test_v2_model_cache_ttl():
    """Test model cache TTL mechanism"""
    from blossom_ai.core.models import TextModel
    import time

    TextModel.reset()
    TextModel.initialize_from_api(api_token=API_TOKEN)
    ts1 = TextModel._cache_timestamp

    # Should use cache
    TextModel.initialize_from_api(api_token=API_TOKEN)
    assert TextModel._cache_timestamp == ts1

    # Expire cache
    TextModel._cache_timestamp = time.time() - 400
    TextModel.initialize_from_api(api_token=API_TOKEN)
    assert TextModel._cache_timestamp > ts1


@pytest.mark.asyncio
async def test_v2_no_session_leak():
    """Test that async sessions don't leak"""
    if not API_TOKEN or API_TOKEN == "your_token_here":
        pytest.skip("No token")

    from blossom_ai.core.session_manager import AsyncSessionManager

    initial = len(AsyncSessionManager._global_sessions)

    for _ in range(5):
        async with Blossom(api_token=API_TOKEN) as client:
            await client.text.generate("test")

    final = len(AsyncSessionManager._global_sessions)
    assert final <= initial + 1


# ------------------------------------------------------------------------------
# PARAMETER VALIDATION
# ------------------------------------------------------------------------------

def test_v2_message_builder_validation():
    """Test MessageBuilder validation"""
    # Should raise FileNotFoundError for non-existent file
    with pytest.raises(FileNotFoundError):
        MessageBuilder.image_message(
            role="user",
            text="test",
            image_path="/nonexistent/image.jpg"
        )

    # Should raise ValueError if no image source provided
    with pytest.raises(ValueError):
        MessageBuilder.image_message(
            role="user",
            text="test"
            # No image_url, image_path, or image_data
        )


@SKIP_IF_NO_TOKEN
def test_v2_modalities_validation():
    """Test modalities parameter validation"""
    from blossom_ai.generators import ParameterValidator

    # Valid modalities
    ParameterValidator.validate_modalities(["text", "audio"])

    # Invalid modality should raise
    with pytest.raises(ValidationError):
        ParameterValidator.validate_modalities(["text", "invalid_mode"])


# ------------------------------------------------------------------------------
# BACKWARDS COMPATIBILITY
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
def test_v2_backwards_compatibility():
    """Test that old code still works"""
    # Old-style usage should still work
    with Blossom(api_token=API_TOKEN) as client:
        # Text generation
        result = client.text.generate("Hello")
        assert isinstance(result, str)

        # Image generation
        img = client.image.generate("test", model="flux")
        assert isinstance(img, bytes)

        # Models listing
        models = client.text.models()
        assert isinstance(models, list)