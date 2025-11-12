"""
Real API Integration Tests for V2 API with Native Reasoning
More resilient to API failures with better error handling
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
    ReasoningMode,
    CacheManager,
    cached,
    create_reasoning_enhancer
)
from blossom_ai.core.errors import BlossomError


API_TOKEN = os.getenv("BLOSSOM_API_TOKEN", "your-api-token")
pytestmark = pytest.mark.api


# ✅ Helper for retry with exponential backoff
def retry_on_server_error(max_attempts=3, initial_wait=1.0):
    """Decorator to retry tests on 502/503 errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code in [502, 503, 504] and attempt < max_attempts - 1:
                        wait = initial_wait * (2 ** attempt)
                        print(f"\n⏳ Server error {e.response.status_code}, retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                    raise
        return wrapper
    return decorator


# ============================================================================
# V2 API BASIC TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_text_generation():
    """Test V2 text generation"""
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate(
            "Say hello in one word",
            model="openai"
        )

        assert response is not None
        assert len(response) > 0
        print(f"\n✅ V2 Response: {response}")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_image_generation():
    """Test V2 image generation"""
    with Blossom(api_token=API_TOKEN) as client:
        image = client.image.generate(
            "a simple red circle",
            model="flux",
            width=256,
            height=256,
            seed=42
        )

        assert image is not None
        assert len(image) > 1000
        print(f"\n✅ V2 Image: {len(image)} bytes")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_json_mode():
    """Test V2 JSON mode"""
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate(
            "Generate JSON with name and age fields",
            json_mode=True
        )

        assert response is not None

        import json
        data = json.loads(response)
        assert isinstance(data, dict)
        print(f"\n✅ V2 JSON: {data}")


# ============================================================================
# V2 NATIVE REASONING TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_native_reasoning():
    """Test V2 native reasoning support"""
    enhancer = ReasoningEnhancer()

    # Create native reasoning config
    enhanced = enhancer.enhance(
        "How to optimize Python code?",
        level="high",
        mode="native",
        api_version="v2",
        model="openai"
    )

    # Should return dict with thinking parameter
    assert isinstance(enhanced, dict)
    assert "prompt" in enhanced
    assert "thinking" in enhanced
    assert enhanced["thinking"]["type"] == "enabled"
    print(f"\n✅ Native Reasoning Config: {enhanced['thinking']}")

    # Use with V2 API
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.chat(
            messages=[{"role": "user", "content": enhanced["prompt"]}],
            thinking=enhanced["thinking"]
        )

        assert response is not None
        print(f"\n✅ Native Reasoning Response: {response[:100]}...")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_auto_mode_reasoning():
    """Test auto-detection of reasoning mode"""
    enhancer = ReasoningEnhancer()

    # Auto mode with V2 + OpenAI should select native
    enhanced_v2 = enhancer.enhance(
        "Explain caching",
        level="medium",
        mode="auto",
        api_version="v2",
        model="openai"
    )

    assert isinstance(enhanced_v2, dict)
    assert "thinking" in enhanced_v2
    print(f"\n✅ Auto mode selected: native (V2 + OpenAI)")

    # Auto mode with different model should select prompt
    enhanced_other = enhancer.enhance(
        "Explain caching",
        level="medium",
        mode="auto",
        api_version="v2",
        model="gemini"
    )

    # Gemini might not support native reasoning
    if isinstance(enhanced_other, str):
        print(f"\n✅ Auto mode selected: prompt (non-OpenAI model)")
    else:
        print(f"\n✅ Auto mode selected: native (model supports it)")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_reasoning_levels():
    """Test different reasoning levels"""
    enhancer = ReasoningEnhancer()

    levels = ["low", "medium", "high"]

    for level in levels:
        enhanced = enhancer.enhance(
            "Solve this problem",
            level=level,
            mode="native",
            api_version="v2",
            model="openai"
        )

        assert "thinking" in enhanced
        budget = enhanced["thinking"]["budget_tokens"]
        print(f"  Level {level}: {budget} tokens")


# ============================================================================
# REASONING + V2 API
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_reasoning_with_v2_prompt_mode():
    """Test reasoning with V2 API (forced prompt mode)"""
    enhancer = ReasoningEnhancer()

    enhanced = enhancer.enhance(
        "How to optimize code?",
        level="medium",
        mode="prompt",  # Force prompt mode
        api_version="v2"
    )

    # Prompt mode returns string
    assert isinstance(enhanced, str)
    assert len(enhanced) > 0

    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate(enhanced)

        assert response is not None
        print(f"\n✅ Reasoning + V2 (prompt mode): {response[:100]}...")


# ============================================================================
# CACHING + V2 API
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_caching_with_v2_api():
    """Test caching with V2 API"""
    cache = CacheManager()

    prompt = f"Say hello {uuid.uuid4().hex[:8]}"
    cache_key = f"v2:text:{hash(prompt)}"

    # First call - no cache
    start = time.time()
    with Blossom(api_token=API_TOKEN) as client:
        response1 = client.text.generate(prompt)
    first_time = time.time() - start

    # Cache the response
    cache.set(cache_key, response1, ttl=3600)

    # Second call - from cache
    start = time.time()
    response2 = cache.get(cache_key)
    cached_time = time.time() - start

    assert response2 == response1
    assert cached_time < first_time / 10

    print(f"\n✅ Caching + V2:")
    print(f"First call: {first_time:.3f}s")
    print(f"Cached call: {cached_time:.6f}s")
    print(f"Speed improvement: {first_time/cached_time:.0f}x")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_decorator_with_v2_api():
    """Test @cached decorator with V2 API"""
    unique_prompt = f"Hello-{uuid.uuid4().hex[:8]}"
    call_count = [0]

    @cached(ttl=3600)
    def generate_cached(prompt):
        call_count[0] += 1
        with Blossom(api_token=API_TOKEN) as client:
            return client.text.generate(prompt)

    # First call - not cached
    result1 = generate_cached(unique_prompt)
    assert call_count[0] == 1

    # Second call - cached
    result2 = generate_cached(unique_prompt)
    assert call_count[0] == 1  # Should not increment
    assert result1 == result2

    print(f"\n✅ Decorator + V2: Cached successfully (calls={call_count[0]})")


@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_full_integration_v2_native():
    """Test full integration: Native Reasoning + Caching + V2 API"""
    enhancer = create_reasoning_enhancer(level="high", mode="native")

    unique_q = f"How does caching work? {uuid.uuid4().hex[:8]}"

    @cached(ttl=3600)
    def analyze_with_native_reasoning(question):
        enhanced = enhancer.enhance(
            question,
            api_version="v2",
            model="openai"
        )

        with Blossom(api_token=API_TOKEN) as client:
            return client.text.chat(
                messages=[{"role": "user", "content": enhanced["prompt"]}],
                thinking=enhanced.get("thinking")
            )

    # First call
    start = time.time()
    result1 = analyze_with_native_reasoning(unique_q)
    first_time = time.time() - start

    # Second call (cached)
    start = time.time()
    result2 = analyze_with_native_reasoning(unique_q)
    cached_time = time.time() - start

    assert result1 == result2
    assert cached_time < first_time / 10

    print(f"\n✅ Full Integration V2 (Native Reasoning):")
    print(f"First: {first_time:.3f}s")
    print(f"Cached: {cached_time:.6f}s")
    print(f"Response: {result1[:100]}...")


# ============================================================================
# ASYNC V2 API TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
async def test_async_v2_text():
    """Test async V2 text generation"""
    async with Blossom(api_token=API_TOKEN) as client:
        response = await client.text.generate("Hello")

        assert response is not None
        print(f"\n✅ Async V2: {response[:50]}...")


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
async def test_async_v2_image():
    """Test async V2 image generation"""
    async with Blossom(api_token=API_TOKEN) as client:
        image = await client.image.generate("a cat", model="flux", width=256, height=256)

        assert image is not None
        assert len(image) > 1000
        print(f"\n✅ Async V2 Image: {len(image)} bytes")


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
async def test_async_with_caching():
    """Test async with caching"""
    unique_prompt = f"Test-{uuid.uuid4().hex[:8]}"

    @cached(ttl=3600)
    async def async_generate(prompt):
        async with Blossom(api_token=API_TOKEN) as client:
            return await client.text.generate(prompt)

    result1 = await async_generate(unique_prompt)

    start = time.time()
    result2 = await async_generate(unique_prompt)
    cached_time = time.time() - start

    assert result1 == result2
    assert cached_time < 0.01

    print(f"\n✅ Async Caching: {cached_time:.6f}s")


# ============================================================================
# STREAMING TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error()
def test_v2_streaming():
    """Test V2 streaming"""
    with Blossom(api_token=API_TOKEN) as client:
        chunks = []

        for chunk in client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
            print(chunk, end="", flush=True)

        print()

        assert len(chunks) > 0
        print(f"\n✅ V2 Streaming: {len(chunks)} chunks")


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
async def test_v2_async_streaming():
    """Test V2 async streaming"""
    async with Blossom(api_token=API_TOKEN) as client:
        chunks = []

        async for chunk in await client.text.generate("Count to 3", stream=True):
            chunks.append(chunk)
            print(chunk, end="", flush=True)

        print()

        assert len(chunks) > 0
        print(f"\n✅ V2 Async Streaming: {len(chunks)} chunks")


# ============================================================================
# ERROR HANDLING
# ============================================================================

@pytest.mark.slow
def test_api_error_handling():
    """Test API error handling"""
    with Blossom(api_token="invalid_token_xyz") as client:
        from blossom_ai.core.errors import AuthenticationError

        with pytest.raises(AuthenticationError):
            client.text.generate("test", model="openai")


# ============================================================================
# CACHE STATISTICS
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error(max_attempts=5)
def test_cache_statistics_with_api():
    """Test cache statistics with real API calls"""
    cache = CacheManager()

    base = uuid.uuid4().hex[:8]
    prompts = [f"{base}-Q1", f"{base}-Q2", f"{base}-Q3",
               f"{base}-Q1", f"{base}-Q2", f"{base}-Q1"]

    for prompt in prompts:
        cache_key = f"stats:{hash(prompt)}"

        cached = cache.get(cache_key)
        if not cached:
            with Blossom(api_token=API_TOKEN) as client:
                response = client.text.generate(f"Answer: {prompt}")
                cache.set(cache_key, response)

    stats = cache.get_stats()

    print(f"\n✅ Cache Stats:")
    print(f"Hits: {stats.hits}")
    print(f"Misses: {stats.misses}")
    print(f"Hit rate: {stats.hit_rate:.1f}%")

    assert stats.misses == 3
    assert stats.hits == 3
    assert stats.hit_rate == 50.0


# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================

@pytest.mark.slow
@pytest.mark.skipif(not API_TOKEN or API_TOKEN == "your-api-token", reason="API token not set")
@retry_on_server_error(max_attempts=5)
def test_performance_comparison():
    """Test performance: without vs with caching"""
    prompt = f"Test {uuid.uuid4().hex[:8]}"

    # Single uncached call
    start = time.time()
    with Blossom(api_token=API_TOKEN) as client:
        client.text.generate(prompt)
    avg_uncached = time.time() - start

    # With caching
    cache = CacheManager()

    @cached(ttl=3600)
    def cached_generate(p):
        with Blossom(api_token=API_TOKEN) as client:
            return client.text.generate(p)

    # Prime cache
    cached_generate(prompt)

    # Measure cached calls
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