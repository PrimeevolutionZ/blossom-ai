"""
Blossom AI - Integration Tests
"""

import os
import pytest
import vcr
from pathlib import Path

from blossom_ai import Blossom
from blossom_ai.core.errors import BlossomError, RateLimitError, AuthenticationError

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# VCR configuration for recording HTTP interactions
CASSETTES_DIR = Path(__file__).parent / "cassettes"
CASSETTES_DIR.mkdir(exist_ok=True)

vcr_config = vcr.VCR(
    cassette_library_dir=str(CASSETTES_DIR),
    record_mode='once',  # Only record if cassette doesn't exist
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query'],
    filter_headers=['authorization'],  # Don't record API tokens
    filter_query_parameters=['token'],  # Don't record tokens in URLs
)

# Use real API token from environment or skip tests
API_TOKEN = os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
SKIP_IF_NO_TOKEN = pytest.mark.skipif(
    not API_TOKEN,
    reason="No API token found. Set POLLINATIONS_API_KEY or BLOSSOM_API_KEY"
)


# ==============================================================================
# TEXT GENERATION TESTS (V2 API)
# ==============================================================================

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_generate_simple.yaml")
def test_text_generate_simple():
    """Test basic text generation"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        result = client.text.generate("Say hello in 3 words")

        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) < 100  # Should be short

    finally:
        client.close_sync()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_generate_stream.yaml")
def test_text_generate_stream():
    """Test streaming text generation"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        chunks = []
        for chunk in client.text.generate("Count to 5", stream=True):
            chunks.append(chunk)
            assert isinstance(chunk, str)

        full_text = "".join(chunks)
        assert len(full_text) > 0

    finally:
        client.close_sync()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_chat.yaml")
def test_text_chat():
    """Test chat completion"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is 2+2?"}
        ]

        result = client.text.chat(messages)

        assert isinstance(result, str)
        assert "4" in result or "four" in result.lower()

    finally:
        client.close_sync()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("text_models_list.yaml")
def test_text_models_list():
    """Test fetching available text models"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        models = client.text.models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "openai" in models or "openai-fast" in models

    finally:
        client.close_sync()


# ==============================================================================
# IMAGE GENERATION TESTS (V2 API)
# ==============================================================================

@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_generate.yaml")
def test_image_generate():
    """Test basic image generation"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        image_data = client.image.generate(
            "a red circle",
            width=256,
            height=256,
            seed=42
        )

        assert isinstance(image_data, bytes)
        assert len(image_data) > 1000  # Should be at least 1KB

        # Check for PNG or JPEG signature
        assert image_data[:4] == b'\x89PNG' or image_data[:2] == b'\xff\xd8'

    finally:
        client.close_sync()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_generate_url.yaml")
def test_image_generate_url():
    """Test URL generation (no download)"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        url = client.image.generate_url(
            "a blue square",
            width=256,
            height=256,
            seed=123
        )

        assert isinstance(url, str)
        assert url.startswith("https://")
        assert "pollinations.ai" in url

        # FIX: Token should NOT be in URL
        assert "token=" not in url.lower()
        assert "authorization" not in url.lower()

    finally:
        client.close_sync()


@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("image_models_list.yaml")
def test_image_models_list():
    """Test fetching available image models"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        models = client.image.models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "flux" in models or "turbo" in models

    finally:
        client.close_sync()


# ==============================================================================
# ERROR HANDLING TESTS
# ==============================================================================

def test_invalid_token():
    """Test that invalid token raises proper error"""
    client = Blossom(api_token="invalid_token_12345", api_version="v2")

    with pytest.raises((AuthenticationError, BlossomError)):
        client.text.generate("test")

    client.close_sync()


@SKIP_IF_NO_TOKEN
def test_rate_limit_handling():
    """Test that rate limits are handled gracefully"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        # Make many rapid requests to trigger rate limit
        for i in range(10):
            try:
                client.text.generate(f"test {i}", max_tokens=10)
            except RateLimitError as e:
                # Should have retry_after
                assert e.retry_after is not None
                assert e.retry_after > 0
                break
    finally:
        client.close_sync()


# ==============================================================================
# ASYNC TESTS
# ==============================================================================

@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_text_generate.yaml")
async def test_async_text_generate():
    """Test async text generation"""
    async with Blossom(api_token=API_TOKEN, api_version="v2") as client:
        result = await client.text.generate("Say hi")

        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_image_generate.yaml")
async def test_async_image_generate():
    """Test async image generation"""
    async with Blossom(api_token=API_TOKEN, api_version="v2") as client:
        image_data = await client.image.generate(
            "a cat",
            width=256,
            height=256
        )

        assert isinstance(image_data, bytes)
        assert len(image_data) > 1000


@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
@vcr_config.use_cassette("async_stream.yaml")
async def test_async_stream():
    """Test async streaming"""
    async with Blossom(api_token=API_TOKEN, api_version="v2") as client:
        chunks = []
        async for chunk in await client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)

        assert len(chunks) > 0


# ==============================================================================
# MODEL CACHING TESTS
# ==============================================================================

@SKIP_IF_NO_TOKEN
def test_model_cache_ttl():
    """Test that model cache respects TTL"""
    from blossom_ai.core.models import TextModel
    import time

    # Reset cache
    TextModel.reset()

    # First fetch
    TextModel.initialize_from_api(api_token=API_TOKEN)
    first_timestamp = TextModel._cache_timestamp

    # Immediate second fetch should use cache
    TextModel.initialize_from_api(api_token=API_TOKEN)
    assert TextModel._cache_timestamp == first_timestamp

    # Simulate TTL expiry
    TextModel._cache_timestamp = time.time() - 400  # > 300s TTL

    # Should refetch
    TextModel.initialize_from_api(api_token=API_TOKEN)
    assert TextModel._cache_timestamp > first_timestamp


# ==============================================================================
# MEMORY LEAK TESTS
# ==============================================================================

@pytest.mark.asyncio
async def test_no_session_leak():
    """Test that sessions are properly cleaned up"""
    from blossom_ai.core.session_manager import AsyncSessionManager

    initial_sessions = len(AsyncSessionManager._global_sessions)

    # Create and destroy multiple managers
    for _ in range(5):
        async with Blossom(api_version="v2") as client:
            await client.text.generate("test")

    # Should not accumulate sessions (weakref cleans them up)
    final_sessions = len(AsyncSessionManager._global_sessions)
    assert final_sessions <= initial_sessions + 1  # At most 1 active session


# ==============================================================================
# SECURITY TESTS
# ==============================================================================

@SKIP_IF_NO_TOKEN
def test_token_not_in_url():
    """Test that API tokens never appear in URLs"""
    client = Blossom(api_token=API_TOKEN, api_version="v2")

    try:
        # Generate URL
        url = client.image.generate_url("test", seed=42)

        # Token should NOT be in URL (security)
        assert API_TOKEN not in url
        assert "token=" not in url.lower()

    finally:
        client.close_sync()


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def cleanup_cassettes():
    """Remove all cassette files (for clean testing)"""
    for cassette in CASSETTES_DIR.glob("*.yaml"):
        cassette.unlink()


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_integration.py -v
    pytest.main([__file__, "-v", "--tb=short"])