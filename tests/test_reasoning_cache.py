"""
Real API Integration Tests
Tests with actual Blossom AI API calls (V1 and V2)

NOTE: These tests require:
1. Internet connection
2. API token for V2 tests (set BLOSSOM_API_TOKEN env var)
3. Are slower than unit tests

Run with: pytest tests/test_reasoning_cache.py -v -m api
Skip with: pytest tests/ -v -m "not api"
"""

import pytest
import os
import time
import asyncio
import uuid
import requests
from blossom_ai import Blossom
from blossom_ai.utils import (
    ReasoningEnhancer,
    CacheManager,
    cached,
    create_reasoning_enhancer
)
from blossom_ai.core.errors import BlossomError


# Get API token from environment
API_TOKEN = os.getenv("BLOSSOM_API_TOKEN", None)

# Mark all tests in this module as API tests
pytestmark = pytest.mark.api


# ============================================================================
# V1 API TESTS (No token required)
# ============================================================================

@pytest.mark.slow
def test_v1_text_generation():
    """Test V1 text generation"""
    with Blossom(api_version="v1") as client:
        response = client.text.generate(
            "Say hello in one word",
            model="openai"
        )

        assert response is not None
        assert len(response) > 0
        print(f"\n✅ V1 Response: {response}")


@pytest.mark.slow
def test_v1_image_url_generation():
    """Test V1 image URL generation"""
    with Blossom(api_version="v1") as client:
        url = client.image.generate_url(
            "a simple red circle",
            seed=42,
            width=256,
            height=256
        )

        assert url is not None
        assert "image.pollinations.ai" in url
        assert "red" in url.lower() or "circle" in url.lower()
        print(f"\n✅ V1 Image URL: {url}")


# ============================================================================
# V2 API TESTS (Token recommended)
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
def test_v2_text_generation():
    """Test V2 text generation with advanced params"""
    with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        response = client.text.generate(
            "Explain AI in exactly 10 words",
            model="openai",
            max_tokens=50,
            temperature=0.7,
            frequency_penalty=0.3
        )

        assert response is not None
        assert len(response) > 0
        print(f"\n✅ V2 Response: {response}")


@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
def test_v2_image_generation_hd():
    """Test V2 HD image generation"""
    with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        image = client.image.generate(
            "a simple test image",
            quality="low",  # Use low for faster testing
            width=256,
            height=256,
            seed=42
        )

        assert image is not None
        assert len(image) > 0
        print(f"\n✅ V2 Image: {len(image)} bytes")


@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
def test_v2_json_mode():
    """Test V2 JSON mode"""
    with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        response = client.text.generate(
            "Generate JSON with name and age",
            json_mode=True,
            max_tokens=50
        )

        assert response is not None

        # Try to parse as JSON
        import json
        data = json.loads(response)
        assert isinstance(data, dict)
        print(f"\n✅ V2 JSON: {data}")


# ============================================================================
# REASONING + V1 API
# ============================================================================

@pytest.mark.slow
def test_reasoning_with_v1_api():
    """Test reasoning enhancement with V1 API"""
    enhancer = ReasoningEnhancer()

    # Enhance prompt
    enhanced = enhancer.enhance(
        "What is caching?",
        level="medium"
    )

    # Generate with V1
    with Blossom(api_version="v1") as client:
        response = client.text.generate(enhanced)

        assert response is not None
        print(f"\n✅ Reasoning + V1:\nPrompt length: {len(enhanced)}\nResponse: {response[:100]}...")


@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
def test_reasoning_with_v2_api():
    """Test reasoning enhancement with V2 API"""
    enhancer = ReasoningEnhancer()

    # Enhance with high-level reasoning
    enhanced = enhancer.enhance(
        "How do I optimize Python code?",
        level="high"
    )

    # Generate with V2
    with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        response = client.text.generate(
            enhanced,
            max_tokens=300,
            temperature=0.7
        )

        assert response is not None

        # Try to extract reasoning
        parsed = enhancer.extract_reasoning(response)
        print(f"\n✅ Reasoning + V2:")
        print(f"Reasoning: {parsed['reasoning'][:100] if parsed['reasoning'] else 'None'}...")
        print(f"Answer: {parsed['answer'][:100]}...")


# ============================================================================
# CACHING + API
# ============================================================================

@pytest.mark.slow
def test_caching_with_v1_api():
    """Test caching with V1 API"""
    cache = CacheManager()

    prompt = "Say hello"
    cache_key = f"v1:text:{hash(prompt)}"

    # First call - not cached
    start = time.time()
    with Blossom(api_version="v1") as client:
        response1 = client.text.generate(prompt)
    first_time = time.time() - start

    # Cache it
    cache.set(cache_key, response1, ttl=3600)

    # Second call - from cache
    start = time.time()
    response2 = cache.get(cache_key)
    cached_time = time.time() - start

    assert response2 == response1
    assert cached_time < first_time / 10  # Much faster

    print(f"\n✅ Caching + V1:")
    print(f"First call: {first_time:.3f}s")
    print(f"Cached call: {cached_time:.6f}s")
    print(f"Speed improvement: {first_time/cached_time:.0f}x")


@pytest.mark.slow
def test_decorator_with_v1_api():
    """Test @cached decorator with V1 API"""
    # ✅ FIX: Use unique prompt to avoid cache conflicts from previous tests
    unique_prompt = f"Hello-{uuid.uuid4().hex[:8]}"
    call_count = [0]

    @cached(ttl=3600)
    def generate_cached(prompt):
        call_count[0] += 1
        with Blossom(api_version="v1") as client:
            return client.text.generate(prompt)

    # First call
    result1 = generate_cached(unique_prompt)
    assert call_count[0] == 1, f"Expected 1 call, got {call_count[0]}"

    # Second call (cached)
    result2 = generate_cached(unique_prompt)
    assert call_count[0] == 1, f"Expected 1 call (cached), got {call_count[0]}"
    assert result1 == result2

    print(f"\n✅ Decorator + V1: Cached successfully (calls={call_count[0]})")


# ============================================================================
# REASONING + CACHING + API
# ============================================================================

@pytest.mark.slow
def test_full_integration_v1():
    """Test full integration: Reasoning + Caching + V1 API"""
    enhancer = ReasoningEnhancer()
    cache = CacheManager()

    def smart_generate(prompt):
        """Generate with reasoning and caching"""
        # Check cache
        cache_key = f"smart:{hash(prompt)}"
        cached = cache.get(cache_key)
        if cached:
            return cached, True

        # Enhance with reasoning
        enhanced = enhancer.enhance(prompt, level="medium")

        # Generate
        with Blossom(api_version="v1") as client:
            response = client.text.generate(enhanced)

        # Cache it
        cache.set(cache_key, response, ttl=3600)

        return response, False

    # First call
    start = time.time()
    response1, cached1 = smart_generate("What is Python?")
    first_time = time.time() - start

    assert not cached1

    # Second call (cached)
    start = time.time()
    response2, cached2 = smart_generate("What is Python?")
    cached_time = time.time() - start

    assert cached2
    assert response1 == response2

    print(f"\n✅ Full Integration V1:")
    print(f"First (enhanced + API): {first_time:.3f}s")
    print(f"Second (cached): {cached_time:.6f}s")
    print(f"Speed improvement: {first_time/cached_time:.0f}x")


@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
def test_full_integration_v2():
    """Test full integration: Reasoning + Caching + V2 API"""
    enhancer = create_reasoning_enhancer(level="high")

    @cached(ttl=3600)
    def analyze_with_reasoning(question):
        enhanced = enhancer.enhance(question)

        with Blossom(api_version="v2", api_token=API_TOKEN) as client:
            return client.text.generate(
                enhanced,
                max_tokens=200,
                frequency_penalty=0.5
            )

    # First call
    start = time.time()
    result1 = analyze_with_reasoning("How does caching work?")
    first_time = time.time() - start

    # Second call (cached)
    start = time.time()
    result2 = analyze_with_reasoning("How does caching work?")
    cached_time = time.time() - start

    assert result1 == result2
    assert cached_time < first_time / 10

    print(f"\n✅ Full Integration V2:")
    print(f"First: {first_time:.3f}s")
    print(f"Cached: {cached_time:.6f}s")
    print(f"Response: {result1[:100]}...")


# ============================================================================
# ASYNC API TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.slow
async def test_async_v1_text():
    """Test async V1 text generation"""
    async with Blossom(api_version="v1") as client:
        response = await client.text.generate("Hello")

        assert response is not None
        print(f"\n✅ Async V1: {response[:50]}...")


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(API_TOKEN is None, reason="API token not set")
async def test_async_v2_text():
    """Test async V2 text generation"""
    async with Blossom(api_version="v2", api_token=API_TOKEN) as client:
        response = await client.text.generate(
            "Say hi",
            max_tokens=20
        )

        assert response is not None
        print(f"\n✅ Async V2: {response[:50]}...")


@pytest.mark.asyncio
@pytest.mark.slow
async def test_async_with_caching():
    """Test async with caching"""
    @cached(ttl=3600)
    async def async_generate(prompt):
        async with Blossom(api_version="v1") as client:
            return await client.text.generate(prompt)

    # First call
    result1 = await async_generate("Test")

    # Second call (cached)
    start = time.time()
    result2 = await async_generate("Test")
    cached_time = time.time() - start

    assert result1 == result2
    assert cached_time < 0.01  # Very fast

    print(f"\n✅ Async Caching: {cached_time:.6f}s")


# ============================================================================
# STREAMING TESTS
# ============================================================================

@pytest.mark.slow
def test_v1_streaming():
    """Test V1 streaming"""
    with Blossom(api_version="v1") as client:
        chunks = []

        for chunk in client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
            print(chunk, end="", flush=True)

        print()  # Newline

        assert len(chunks) > 0
        full_text = "".join(chunks)
        assert len(full_text) > 0
        print(f"\n✅ V1 Streaming: {len(chunks)} chunks")


@pytest.mark.asyncio
@pytest.mark.slow
async def test_v1_async_streaming():
    """Test V1 async streaming"""
    async with Blossom(api_version="v1") as client:
        chunks = []

        async for chunk in await client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
            print(chunk, end="", flush=True)

        print()  # Newline

        assert len(chunks) > 0
        print(f"\n✅ V1 Async Streaming: {len(chunks)} chunks")


# ============================================================================
# ERROR HANDLING
# ============================================================================

@pytest.mark.slow
def test_api_error_handling():
    """Test API error handling with invalid model"""
    with Blossom(api_version="v1") as client:
        # ✅ FIX: API returns 404 for invalid models, which gets converted to HTTPError
        # The error is NOT wrapped in BlossomError because raise_for_status() is called
        # We expect the raw requests.HTTPError here
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            response = client.text.generate(
                "test",
                model="nonexistent_model_xyz_12345"
            )

        # Verify it's a 404 error
        assert exc_info.value.response.status_code == 404
        print(f"\n✅ Error handled correctly: 404 for invalid model")


# ============================================================================
# STATISTICS
# ============================================================================

@pytest.mark.slow
def test_cache_statistics_with_api():
    """Test cache statistics with real API calls"""
    cache = CacheManager()

    prompts = ["Q1", "Q2", "Q3", "Q1", "Q2", "Q1"]

    for prompt in prompts:
        cache_key = f"stats:{hash(prompt)}"

        cached = cache.get(cache_key)
        if not cached:
            with Blossom(api_version="v1") as client:
                response = client.text.generate(f"Answer: {prompt}")
                cache.set(cache_key, response)

    stats = cache.get_stats()

    print(f"\n✅ Cache Stats:")
    print(f"Hits: {stats.hits}")
    print(f"Misses: {stats.misses}")
    print(f"Hit rate: {stats.hit_rate:.1f}%")

    assert stats.misses == 3  # 3 unique prompts
    assert stats.hits == 3  # 3 repeated prompts
    assert stats.hit_rate == 50.0


# ============================================================================
# PERFORMANCE BENCHMARKS
# ============================================================================

@pytest.mark.slow
def test_performance_comparison():
    """Test performance comparison: without vs with caching"""
    prompt = "Test prompt for performance"

    # Without caching
    times_uncached = []
    for _ in range(3):
        start = time.time()
        with Blossom(api_version="v1") as client:
            client.text.generate(prompt)
        times_uncached.append(time.time() - start)

    avg_uncached = sum(times_uncached) / len(times_uncached)

    # With caching
    cache = CacheManager()

    @cached(ttl=3600)
    def cached_generate(p):
        with Blossom(api_version="v1") as client:
            return client.text.generate(p)

    # First call (uncached)
    cached_generate(prompt)

    # Subsequent calls (cached)
    times_cached = []
    for _ in range(10):
        start = time.time()
        cached_generate(prompt)
        times_cached.append(time.time() - start)

    avg_cached = sum(times_cached) / len(times_cached)

    print(f"\n✅ Performance Comparison:")
    print(f"Uncached: {avg_uncached:.3f}s")
    print(f"Cached: {avg_cached:.6f}s")
    print(f"Speed improvement: {avg_uncached/avg_cached:.0f}x")

    assert avg_cached < avg_uncached / 10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "-m", "api"])