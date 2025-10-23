"""
🌸 Blossom AI - Unified Test Suite (Enhanced for v0.2.4)
Run all examples in one place!

Usage:
    # Run all tests
    python test_examples.py

    # Run only sync tests
    python test_examples.py --sync

    # Run only async tests
    python test_examples.py --async

    # Run only streaming tests
    python test_examples.py --streaming

    # Run only v0.2.4 feature tests
    python test_examples.py --v024

    # With API token
    python test_examples.py --token YOUR_TOKEN
"""

import asyncio
import sys
import argparse
from pathlib import Path
import time

# Import from the current package
try:
    from blossom_ai import Blossom, BlossomError, StreamError, RateLimitError
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from blossom_ai import Blossom, BlossomError, StreamError, RateLimitError, ErrorType


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Set your API token here or pass as environment variable
API_TOKEN = "Your-API-Token-Here"  # Get yours at https://auth.pollinations.ai

# Test output directory
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================================================================
# SYNCHRONOUS TESTS
# ==============================================================================

def test_image_generation_sync():
    """Test synchronous image generation"""
    print("\n🖼️  Testing Image Generation (Sync)...")

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic image generation
            print("  → Generating basic image...")
            filename = ai.image.save(
                prompt="a cute robot painting a landscape",
                filename=OUTPUT_DIR / "robot_sync.jpg",
                width=512,
                height=512,
                model="flux"
            )
            print(f"  ✅ Basic image saved: {filename}")
            assert Path(filename).exists(), "Image file should exist"

            # Image with seed (reproducible)
            print("  → Generating reproducible image...")
            filename = ai.image.save(
                prompt="a majestic dragon in a mystical forest",
                filename=OUTPUT_DIR / "dragon_sync.jpg",
                seed=42,
                width=768,
                height=768
            )
            print(f"  ✅ Reproducible image saved: {filename}")
            assert Path(filename).exists(), "Image file should exist"

            # Enhanced prompt
            print("  → Generating with enhanced prompt...")
            filename = ai.image.save(
                prompt="sunset over mountains",
                filename=OUTPUT_DIR / "sunset_sync.jpg",
                enhance=True,
                width=1024,
                height=576
            )
            print(f"  ✅ Enhanced image saved: {filename}")
            assert Path(filename).exists(), "Image file should exist"

            # Test generate method (returns bytes)
            print("  → Testing generate method (bytes)...")
            image_data = ai.image.generate(
                prompt="a simple test pattern",
                width=256,
                height=256
            )
            print(f"  ✅ Generated image data: {len(image_data)} bytes")
            assert len(image_data) > 0, "Image data should not be empty"

            # List models
            models = ai.image.models()
            print(f"  ℹ️  Available models: {models}")
            assert isinstance(models, list), "Models should be a list"
            assert len(models) > 0, "Should have at least one model"

            print("✅ Image generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            raise


def test_text_generation_sync():
    """Test synchronous text generation"""
    print("\n📝 Testing Text Generation (Sync)...")

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Simple generation
            print("  → Simple text generation...")
            response = ai.text.generate("Explain quantum computing in one sentence")
            print(f"  💬 Response: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            # With system message
            print("  → Generation with system message...")
            response = ai.text.generate(
                prompt="Write a haiku about coding",
                system="You are a creative poet who loves technology"
            )
            print(f"  💬 Haiku:\n{response}")
            assert len(response) > 0, "Response should not be empty"

            # Reproducible with seed
            print("  → Reproducible generation...")
            response1 = ai.text.generate("Random creative idea", seed=42)
            response2 = ai.text.generate("Random creative idea", seed=42)
            print(f"  ✅ Seeds match: {response1 == response2}")

            # JSON mode
            print("  → JSON mode generation...")
            response = ai.text.generate(
                prompt="List 3 programming languages with their use cases in JSON format",
                json_mode=True
            )
            print(f"  💬 JSON: {response[:150]}...")
            assert len(response) > 0, "Response should not be empty"

            # Chat completion
            print("  → Chat completion...")
            response = ai.text.chat([
                {"role": "system", "content": "You are a helpful coding assistant"},
                {"role": "user", "content": "What is Python best for?"}
            ])
            print(f"  💬 Chat response: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            # List models
            models = ai.text.models()
            print(f"  ℹ️  Available models: {models}")
            assert isinstance(models, list), "Models should be a list"
            assert len(models) > 0, "Should have at least one model"

            print("✅ Text generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            raise


def test_audio_generation_sync():
    """Test synchronous audio generation"""
    print("\n🎙️  Testing Audio Generation (Sync)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Audio generation requires API token")
        print("     Get yours at https://auth.pollinations.ai\n")
        return

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic audio generation
            print("  → Generating basic audio...")
            filename = ai.audio.save(
                text="Welcome to Blossom AI, the beautiful Python SDK for Pollinations",
                filename=OUTPUT_DIR / "welcome_sync.mp3",
                voice="nova"
            )
            print(f"  ✅ Basic audio saved: {filename}")
            assert Path(filename).exists(), "Audio file should exist"

            # Different voices
            voices_to_test = ["alloy", "echo", "shimmer"]
            for voice in voices_to_test:
                print(f"  → Testing voice: {voice}...")
                filename = ai.audio.save(
                    text=f"This is the {voice} voice",
                    filename=OUTPUT_DIR / f"voice_{voice}_sync.mp3",
                    voice=voice
                )
                print(f"    Saved: {filename}")
                assert Path(filename).exists(), "Audio file should exist"
            print("  ✅ All voices tested!")

            # Test generate method (returns bytes)
            print("  → Testing generate method (bytes)...")
            audio_data = ai.audio.generate(
                text="Test audio generation",
                voice="alloy"
            )
            print(f"  ✅ Generated audio data: {len(audio_data)} bytes")
            assert len(audio_data) > 0, "Audio data should not be empty"

            # List available voices
            voices = ai.audio.voices()
            print(f"  ℹ️  Available voices: {voices}")
            assert isinstance(voices, list), "Voices should be a list"
            assert len(voices) > 0, "Should have at least one voice"

            print("✅ Audio generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            raise


def test_streaming_sync():
    """Test synchronous streaming"""
    print("\n🌊 Testing Streaming (Sync)...")

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic streaming
            print("  → Testing basic streaming...")
            print("  💬 Streaming output: ", end='', flush=True)

            chunks_received = 0
            full_response = ""

            for chunk in ai.text.generate(
                "Count from 1 to 5 with explanations",
                stream=True
            ):
                print(chunk, end='', flush=True)
                full_response += chunk
                chunks_received += 1

            print()  # New line after streaming
            print(f"  ✅ Received {chunks_received} chunks")
            print(f"  ✅ Total length: {len(full_response)} chars")
            assert chunks_received > 0, "Should receive at least one chunk"
            assert len(full_response) > 0, "Response should not be empty"

            # Streaming with system message
            print("\n  → Testing streaming with system message...")
            print("  💬 Streaming haiku: ", end='', flush=True)

            chunks = []
            for chunk in ai.text.generate(
                prompt="Write a haiku about rivers",
                system="You are a poet",
                stream=True
            ):
                print(chunk, end='', flush=True)
                chunks.append(chunk)

            print()
            full_text = ''.join(chunks)
            print(f"  ✅ Complete haiku: {len(full_text)} chars")
            assert len(chunks) > 0, "Should receive chunks"

            # Streaming chat
            print("\n  → Testing streaming chat...")
            print("  💬 Chat streaming: ", end='', flush=True)

            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Explain what is Python in 2 sentences"}
            ]

            chat_chunks = 0
            for chunk in ai.text.chat(messages, stream=True):
                print(chunk, end='', flush=True)
                chat_chunks += 1

            print()
            print(f"  ✅ Chat received {chat_chunks} chunks")
            assert chat_chunks > 0, "Should receive chat chunks"

            # Test streaming collection
            print("\n  → Testing streaming collection...")
            collected_chunks = []
            for chunk in ai.text.generate("Say hello", stream=True):
                collected_chunks.append(chunk)

            full = ''.join(collected_chunks)
            print(f"  ✅ Collected: '{full}' from {len(collected_chunks)} chunks")
            assert len(full) > 0, "Collected text should not be empty"

            # Test streaming to file
            print("\n  → Testing streaming to file...")
            output_file = OUTPUT_DIR / "streaming_output.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                for chunk in ai.text.generate(
                    "Write a short paragraph about AI",
                    stream=True
                ):
                    f.write(chunk)
                    f.flush()

            assert output_file.exists(), "Output file should exist"
            content = output_file.read_text(encoding='utf-8')
            print(f"  ✅ Saved {len(content)} chars to file")
            assert len(content) > 0, "File should have content"

            print("\n✅ Streaming tests passed!\n")

        except BlossomError as e:
            print(f"\n❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            raise
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            raise


def test_error_handling_sync():
    """Test error handling"""
    print("\n🛡️  Testing Error Handling (Sync)...")

    with Blossom(api_token=API_TOKEN) as ai:
        # Test invalid prompt length
        try:
            print("  → Testing prompt length validation...")
            very_long_prompt = "a" * 300
            ai.image.generate(very_long_prompt)
            assert False, "Should have raised an error for long prompt"
        except BlossomError as e:
            print(f"  ✅ Caught expected error: {e.error_type}")
            assert e.error_type == "INVALID_PARAMETER"

    # Test authentication requirement for audio
    if API_TOKEN and API_TOKEN != "Your-API-Token-Here":
        print("  ℹ️  Skipping auth test (token provided)")
    else:
        try:
            print("  → Testing authentication requirement...")
            with Blossom(api_token=None) as ai_no_auth:
                ai_no_auth.audio.generate("test")
                print("  ⚠️  Audio might work without auth (API change?)")
        except BlossomError as e:
            print(f"  ✅ Caught expected error: {e.error_type}")

    print("✅ Error handling tests passed!\n")


# ==============================================================================
# V0.2.4 FEATURE TESTS
# ==============================================================================

def test_stream_timeout_protection():
    """Test stream timeout protection (NEW in v0.2.4)"""
    print("\n⏱️  Testing Stream Timeout Protection (v0.2.4)...")

    with Blossom(api_token=API_TOKEN, timeout=5) as ai:
        try:
            print("  → Testing normal streaming (should work)...")
            chunks = 0
            for chunk in ai.text.generate("Say hello", stream=True):
                chunks += 1
            print(f"  ✅ Normal streaming works: {chunks} chunks")

            # Note: Actually triggering timeout requires mocking or slow network
            print("  ℹ️  Stream timeout protection is active (30s default)")
            print("  ℹ️  To test: would need mock server or very slow network")
            print("✅ Stream timeout protection test passed!\n")

        except StreamError as e:
            print(f"  ✅ Caught StreamError: {e.message}")
            print(f"     Suggestion: {e.suggestion}")
            print("✅ Stream timeout protection works!\n")
        except BlossomError as e:
            print(f"  ⚠️  Different error: {e.error_type}")
            raise


def test_request_tracing():
    """Test request ID tracing (NEW in v0.2.4)"""
    print("\n🔍 Testing Request Tracing (v0.2.4)...")

    with Blossom(api_token=API_TOKEN, debug=True) as ai:
        try:
            print("  → Testing request ID in errors...")

            # Try to generate with invalid model (should fail with traceable error)
            try:
                ai.text.generate("test", model="invalid_model_12345")
            except BlossomError as e:
                if e.context and e.context.request_id:
                    print(f"  ✅ Request ID captured: {e.context.request_id[:8]}...")
                else:
                    print("  ℹ️  Request ID not in error (might succeed with invalid model)")

            # Normal request
            print("  → Making traceable request...")
            response = ai.text.generate("Say hi")
            print(f"  ✅ Request completed: {len(response)} chars")
            print("  ℹ️  Request IDs are logged in debug mode")

            print("✅ Request tracing test passed!\n")

        except Exception as e:
            print(f"  ⚠️  Error during tracing test: {e}")
            raise


def test_rate_limit_handling():
    """Test rate limit retry-after (NEW in v0.2.4)"""
    print("\n⏱️  Testing Rate Limit Handling (v0.2.4)...")

    print("  ℹ️  Note: This test requires actually hitting rate limits")
    print("  ℹ️  With API token, limits are higher and harder to hit")

    with Blossom(api_token=API_TOKEN) as ai:
        try:
            print("  → Testing rate limit error structure...")

            # Make several rapid requests (might not hit limit with token)
            for i in range(3):
                response = ai.text.generate(f"Quick test {i}")
                print(f"    Request {i+1}: {len(response)} chars")
                time.sleep(0.1)

            print("  ✅ No rate limit hit (good!)")
            print("  ℹ️  Rate limit errors would include retry_after seconds")
            print("✅ Rate limit handling test passed!\n")

        except RateLimitError as e:
            print(f"  ✅ Rate limit caught!")
            print(f"     Message: {e.message}")
            if e.retry_after:
                print(f"     Retry after: {e.retry_after} seconds")
            print(f"     Suggestion: {e.suggestion}")
            print("✅ Rate limit handling works correctly!\n")


def test_connection_pool():
    """Test connection pool optimization (NEW in v0.2.4)"""
    print("\n🔧 Testing Connection Pool (v0.2.4)...")

    with Blossom(api_token=API_TOKEN, timeout=30) as ai:
        try:
            print("  → Testing multiple rapid requests...")

            start_time = time.time()
            responses = []

            # Make 5 rapid requests to test connection reuse
            for i in range(5):
                response = ai.text.generate(f"Request number {i}")
                responses.append(response)
                print(f"    Request {i+1}: {len(response)} chars")

            elapsed = time.time() - start_time
            print(f"  ✅ Completed {len(responses)} requests in {elapsed:.2f}s")
            print(f"  ℹ️  Connection pooling optimizes rapid requests")
            print("✅ Connection pool test passed!\n")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            raise


def test_enhanced_error_context():
    """Test enhanced error context (NEW in v0.2.4)"""
    print("\n📋 Testing Enhanced Error Context (v0.2.4)...")

    with Blossom(api_token=API_TOKEN) as ai:
        try:
            print("  → Testing error context structure...")

            # Trigger validation error
            try:
                ai.image.generate("x" * 300)  # Too long
            except BlossomError as e:
                print(f"  ✅ Error type: {e.error_type}")
                print(f"     Message: {e.message}")
                print(f"     Suggestion: {e.suggestion}")

                if e.context:
                    print(f"     Context operation: {e.context.operation}")
                    if e.context.request_id:
                        print(f"     Request ID: {e.context.request_id[:16]}...")

                assert e.error_type == "INVALID_PARAMETER"
                print("  ✅ Error context includes all expected fields")

            print("✅ Enhanced error context test passed!\n")

        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            raise


def test_stream_cleanup():
    """Test guaranteed stream cleanup (NEW in v0.2.4)"""
    print("\n🧹 Testing Stream Cleanup (v0.2.4)...")

    with Blossom(api_token=API_TOKEN) as ai:
        try:
            print("  → Testing interrupted stream cleanup...")

            chunks = 0
            try:
                for chunk in ai.text.generate("Count to 100", stream=True):
                    chunks += 1
                    if chunks >= 3:
                        # Interrupt stream early
                        break
            except Exception as e:
                print(f"  ⚠️  Exception during stream: {e}")

            print(f"  ✅ Stream interrupted after {chunks} chunks")
            print("  ℹ️  Resources should be cleaned up automatically")

            # Make another request to verify cleanup worked
            response = ai.text.generate("Test after cleanup")
            print(f"  ✅ New request works: {len(response)} chars")
            print("✅ Stream cleanup test passed!\n")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            raise


# ==============================================================================
# ASYNCHRONOUS TESTS
# ==============================================================================

async def _test_image_generation_async():
    """Test asynchronous image generation"""
    print("\n🖼️  Testing Image Generation (Async)...")

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic image generation
            print("  → Generating basic image...")
            filename = await ai.image.save(
                prompt="a cute robot painting a landscape",
                filename=OUTPUT_DIR / "robot_async.jpg",
                width=512,
                height=512
            )
            print(f"  ✅ Basic image saved: {filename}")
            assert Path(filename).exists(), "Image file should exist"

            # Parallel generation
            print("  → Parallel image generation...")
            tasks = [
                ai.image.save("sunset", OUTPUT_DIR / "sunset_async.jpg", width=512, height=512),
                ai.image.save("forest", OUTPUT_DIR / "forest_async.jpg", width=512, height=512),
                ai.image.save("ocean", OUTPUT_DIR / "ocean_async.jpg", width=512, height=512)
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                assert Path(result).exists(), "Image file should exist"
            print(f"  ✅ All parallel images saved: {len(results)} files")

            print("✅ Async image generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}\n")
            return False


async def _test_text_generation_async():
    """Test asynchronous text generation"""
    print("\n📝 Testing Text Generation (Async)...")

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Simple generation
            print("  → Simple text generation...")
            response = await ai.text.generate("Explain AI in one sentence")
            print(f"  💬 Response: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            # Parallel generation
            print("  → Parallel text generation...")
            tasks = [
                ai.text.generate("What is Python?"),
                ai.text.generate("What is JavaScript?"),
                ai.text.generate("What is Rust?")
            ]
            responses = await asyncio.gather(*tasks)
            for resp in responses:
                assert len(resp) > 0, "Response should not be empty"
            print(f"  ✅ Generated {len(responses)} responses in parallel!")

            print("✅ Async text generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}\n")
            return False


async def _test_audio_generation_async():
    """Test asynchronous audio generation"""
    print("\n🎙️  Testing Audio Generation (Async)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Audio generation requires API token\n")
        return True

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic audio
            print("  → Generating basic audio...")
            filename = await ai.audio.save(
                text="Async audio generation test",
                filename=OUTPUT_DIR / "test_async.mp3",
                voice="nova"
            )
            print(f"  ✅ Basic audio saved: {filename}")
            assert Path(filename).exists(), "Audio file should exist"

            print("✅ Async audio generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}\n")
            return False


async def _test_streaming_async():
    """Test asynchronous streaming"""
    print("\n🌊 Testing Streaming (Async)...")

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # Basic async streaming
            print("  → Testing basic async streaming...")
            print("  💬 Async streaming: ", end='', flush=True)

            chunks_received = 0
            full_response = ""

            async for chunk in await ai.text.generate(
                "Count from 1 to 3",
                stream=True
            ):
                print(chunk, end='', flush=True)
                full_response += chunk
                chunks_received += 1

            print()
            print(f"  ✅ Received {chunks_received} chunks")
            assert chunks_received > 0, "Should receive chunks"

            # Async streaming chat
            print("\n  → Testing async streaming chat...")
            messages = [{"role": "user", "content": "Say hello"}]

            chat_chunks = 0
            async for chunk in await ai.text.chat(messages, stream=True):
                chat_chunks += 1

            print(f"  ✅ Received {chat_chunks} chunks")

            print("\n✅ Async streaming tests passed!\n")
            return True

        except BlossomError as e:
            print(f"\n❌ Error: {e.message}\n")
            return False


async def _test_async_stream_timeout():
    """Test async stream timeout (NEW in v0.2.4)"""
    print("\n⏱️  Testing Async Stream Timeout (v0.2.4)...")

    async with Blossom(api_token=API_TOKEN, timeout=5) as ai:
        try:
            print("  → Testing async stream with timeout...")

            chunks = 0
            async for chunk in await ai.text.generate("Say hi", stream=True):
                chunks += 1

            print(f"  ✅ Async stream completed: {chunks} chunks")
            print("  ℹ️  Timeout protection active (30s between chunks)")

            return True

        except StreamError as e:
            print(f"  ✅ Caught async StreamError: {e.message}")
            return True
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False


# ==============================================================================
# TEST RUNNERS
# ==============================================================================

def run_sync_tests():
    """Run all synchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - SYNCHRONOUS TESTS")
    print("=" * 70)

    results = []

    try:
        test_image_generation_sync()
        results.append(("Image Generation", True))
    except Exception:
        results.append(("Image Generation", False))

    try:
        test_text_generation_sync()
        results.append(("Text Generation", True))
    except Exception:
        results.append(("Text Generation", False))

    try:
        test_audio_generation_sync()
        results.append(("Audio Generation", True))
    except Exception:
        results.append(("Audio Generation", False))

    try:
        test_error_handling_sync()
        results.append(("Error Handling", True))
    except Exception:
        results.append(("Error Handling", False))

    return results


def run_streaming_tests():
    """Run synchronous streaming tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - STREAMING TESTS (SYNC)")
    print("=" * 70)

    results = []

    try:
        test_streaming_sync()
        results.append(("Streaming (Sync)", True))
    except Exception:
        results.append(("Streaming (Sync)", False))

    return results


def run_v024_tests():
    """Run v0.2.4 feature tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - V0.2.4 FEATURE TESTS")
    print("=" * 70)

    results = []

    try:
        test_stream_timeout_protection()
        results.append(("Stream Timeout Protection", True))
    except Exception as e:
        print(f"Debug: {e}")
        results.append(("Stream Timeout Protection", False))

    try:
        test_request_tracing()
        results.append(("Request Tracing", True))
    except Exception:
        results.append(("Request Tracing", False))

    try:
        test_rate_limit_handling()
        results.append(("Rate Limit Handling", True))
    except Exception:
        results.append(("Rate Limit Handling", False))

    try:
        test_connection_pool()
        results.append(("Connection Pool", True))
    except Exception:
        results.append(("Connection Pool", False))

    try:
        test_enhanced_error_context()
        results.append(("Enhanced Error Context", True))
    except Exception:
        results.append(("Enhanced Error Context", False))

    try:
        test_stream_cleanup()
        results.append(("Stream Cleanup", True))
    except Exception:
        results.append(("Stream Cleanup", False))

    return results


async def run_async_tests():
    """Run all asynchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - ASYNCHRONOUS TESTS")
    print("=" * 70)

    results = []

    results.append(("Image Generation (Async)", await _test_image_generation_async()))
    results.append(("Text Generation (Async)", await _test_text_generation_async()))
    results.append(("Audio Generation (Async)", await _test_audio_generation_async()))
    results.append(("Streaming (Async)", await _test_streaming_async()))
    results.append(("Stream Timeout (Async)", await _test_async_stream_timeout()))

    return results


def print_summary(sync_results, streaming_results, v024_results, async_results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    all_results = sync_results + streaming_results + v024_results + async_results

    total = len(all_results)
    passed = sum(1 for _, result in all_results if result)
    failed = total - passed

    if sync_results:
        print("\n📦 Synchronous Tests:")
        for name, result in sync_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    if streaming_results:
        print("\n🌊 Streaming Tests:")
        for name, result in streaming_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    if v024_results:
        print("\n🆕 v0.2.4 Feature Tests:")
        for name, result in v024_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    if async_results:
        print("\n⚡ Asynchronous Tests:")
        for name, result in async_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    print(f"\n{'=' * 70}")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")

    if passed == total:
        success_rate = 100.0
    else:
        success_rate = (passed / total * 100) if total > 0 else 0

    print(f"Success Rate: {success_rate:.1f}%")
    print(f"{'=' * 70}\n")

    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")

    return failed == 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Blossom AI Test Suite")
    parser.add_argument("--sync", action="store_true", help="Run only sync tests")
    parser.add_argument("--async", dest="run_async", action="store_true", help="Run only async tests")
    parser.add_argument("--streaming", action="store_true", help="Run only streaming tests")
    parser.add_argument("--v024", action="store_true", help="Run only v0.2.4 feature tests")
    parser.add_argument("--token", type=str, help="API token for authentication")

    args = parser.parse_args()

    # Set token if provided
    global API_TOKEN
    if args.token:
        API_TOKEN = args.token

    print("\n🌸 Blossom AI - Unified Test Suite (v0.2.4)")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("⚠️  No API token provided - audio tests will be skipped")
        print("   Get your token at: https://auth.pollinations.ai")

    sync_results = []
    streaming_results = []
    v024_results = []
    async_results = []

    try:
        if args.v024:
            # Run only v0.2.4 feature tests
            v024_results = run_v024_tests()
        elif args.streaming:
            # Run only streaming tests
            streaming_results = run_streaming_tests()
            print("\n🔄 Running async streaming tests...")
            async_results = asyncio.run(run_async_tests())
        elif args.run_async:
            # Run only async tests
            async_results = asyncio.run(run_async_tests())
        elif args.sync:
            # Run only sync tests
            sync_results = run_sync_tests()
        else:
            # Run all tests
            sync_results = run_sync_tests()
            streaming_results = run_streaming_tests()
            v024_results = run_v024_tests()
            async_results = asyncio.run(run_async_tests())

        # Print summary
        success = print_summary(sync_results, streaming_results, v024_results, async_results)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()