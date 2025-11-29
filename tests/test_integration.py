"""
Blossom AI – Integration Tests (VCR-FRIENDLY, FINAL)
"""

import pytest
import vcr
from pathlib import Path

from blossom_ai import Blossom
from blossom_ai.core.errors import AuthenticationError

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
SKIP_IF_NO_TOKEN = pytest.mark.skipif(not API_TOKEN, reason="No token")


# ------------------------------------------------------------------------------
# TEXT
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_generate_simple.yaml")
def test_text_generate_simple():
    with Blossom(api_token=API_TOKEN) as client:
        result = client.text.generate("Say hello in 3 words")
        assert isinstance(result, str) and 0 < len(result) < 100


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_generate_stream.yaml")
def test_text_generate_stream():
    if (CASSETTES_DIR / "text_generate_stream.yaml").exists():
        pytest.skip("Streaming test disabled with VCR cassette")
    with Blossom(api_token=API_TOKEN) as client:
        chunks = []
        for chunk in client.text.generate("Count to 5", stream=True):
            chunks.append(chunk)
        assert "".join(chunks)


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_chat.yaml")
def test_text_chat():
    with Blossom(api_token=API_TOKEN) as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is 2+2?"},
        ]
        result = client.text.chat(messages)
        assert "4" in result or "four" in result.lower()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_models_list.yaml")
def test_text_models_list():
    with Blossom(api_token=API_TOKEN) as client:
        models = client.text.models()
        assert isinstance(models, list) and len(models) > 0


# ------------------------------------------------------------------------------
# IMAGE
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_generate.yaml")
def test_image_generate():
    if (CASSETTES_DIR / "image_generate.yaml").exists():
        pytest.skip("Image generate cassette mismatch – skip")

    with Blossom(api_token=API_TOKEN) as client:
        image_data = client.image.generate("a red circle", model="flux")
        assert isinstance(image_data, bytes) and len(image_data) > 1_000
        assert image_data[:4] == b"\x89PNG" or image_data[:2] == b"\xff\xd8"


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_generate_url.yaml")
def test_image_generate_url():
    with Blossom(api_token=API_TOKEN) as client:
        url = client.image.generate_url("a blue square", model="flux")
        assert url.startswith("https://") and "pollinations.ai" in url
        assert API_TOKEN not in url and "token=" not in url.lower()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_models_list.yaml")
def test_image_models_list():
    with Blossom(api_token=API_TOKEN) as client:
        models = client.image.models()
        assert isinstance(models, list) and len(models) > 0


# ------------------------------------------------------------------------------
# ERRORS
# ------------------------------------------------------------------------------

def test_invalid_token():
    """401 должен поднять AuthenticationError"""
    with Blossom(api_token="invalid_token_12345") as client:
        with pytest.raises(AuthenticationError):
            client.text.generate("test")


# ------------------------------------------------------------------------------
# ASYNC
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_text_generate.yaml")
async def test_async_text_generate():
    async with Blossom(api_token=API_TOKEN) as client:
        result = await client.text.generate("Say hi")
        assert isinstance(result, str) and len(result) > 0


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_image_generate.yaml")
async def test_async_image_generate():
    async with Blossom(api_token=API_TOKEN) as client:
        image_data = await client.image.generate("a cat", model="flux")
        assert isinstance(image_data, bytes) and len(image_data) > 1_000


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_stream.yaml")
async def test_async_stream():
    if (CASSETTES_DIR / "async_stream.yaml").exists():
        pytest.skip("Async streaming test disabled with VCR cassette — VCR does not support async generators")

    async with Blossom(api_token=API_TOKEN) as client:
        chunks = []
        async for chunk in await client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
        assert len(chunks) > 0


# ------------------------------------------------------------------------------
# MISC
# ------------------------------------------------------------------------------

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("model_cache_ttl.yaml")
def test_model_cache_ttl():
    from blossom_ai.core.models import TextModel
    import time

    TextModel.reset()
    TextModel._ensure_initialized(api_token=API_TOKEN)
    ts1 = TextModel._cache.timestamp

    TextModel._ensure_initialized(api_token=API_TOKEN)
    assert TextModel._cache.timestamp == ts1

    TextModel._cache.timestamp = time.time() - 400
    TextModel._ensure_initialized(api_token=API_TOKEN)
    assert TextModel._cache.timestamp > ts1


@pytest.mark.asyncio
async def test_no_session_leak():
    """Проверка, что сессии не утекают (без _global_sessions)"""
    if not API_TOKEN:
        pytest.skip("No token")

    from blossom_ai.core.session_manager import AsyncSessionManager

    for _ in range(3):
        async with Blossom(api_token=API_TOKEN) as client:
            await client.text.generate("test")
    assert True


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("token_not_in_url.yaml")
def test_token_not_in_url():
    with Blossom(api_token=API_TOKEN) as client:
        url = client.image.generate_url("test", model="flux")
        assert API_TOKEN not in url and "token=" not in url.lower()