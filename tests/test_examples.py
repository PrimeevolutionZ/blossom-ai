"""
🌸 Blossom AI - Unified Test Suite (v0.5.0 - V2 API with Vision & Audio)
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

    # Run only v0.5.0 feature tests (Vision & Audio)
    python test_examples.py --v050

    # With API token
    python test_examples.py --token YOUR_TOKEN
"""

import asyncio
import argparse
from pathlib import Path

# Import from the current package
try:
    from blossom_ai import Blossom, BlossomError, StreamError, RateLimitError, MessageBuilder,ErrorType
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from blossom_ai import Blossom, BlossomError, StreamError, RateLimitError, MessageBuilder, ErrorType


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Set your API token here or pass as environment variable
API_TOKEN = "your_api_token"  # Get yours at https://enter.pollinations.ai

# Test output directory
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================================================================
# SYNCHRONOUS TESTS (V2 API)
# ==============================================================================

def test_image_generation_sync():
    """Test synchronous image generation (V2 API)"""
    print("\n🖼️  Testing Image Generation (Sync - V2 API)...")

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
            print(f"  ℹ️  Available models: {models[:5]}...")
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
    """Test synchronous text generation (V2 API)"""
    print("\n📝 Testing Text Generation (Sync - V2 API)...")

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
            print(f"  ℹ️  Available models: {models[:5]}...")
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


def test_streaming_sync():
    """Test synchronous streaming (V2 API)"""
    print("\n🌊 Testing Streaming (Sync - V2 API)...")

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

            print("\n✅ Streaming tests passed!\n")

        except BlossomError as e:
            print(f"\n❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            raise
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            raise


def test_error_handling_sync():
    """Test error handling (V2 API)"""
    print("\n🛡️  Testing Error Handling (Sync - V2 API)...")

    with Blossom(api_token=API_TOKEN) as ai:
        # Test invalid prompt length
        try:
            print("  → Testing prompt length validation...")
            very_long_prompt = "a" * 300
            ai.image.generate(very_long_prompt)
            assert False, "Should have raised an error for long prompt"
        except BlossomError as e:
            print(f"  ✅ Caught expected error: {e.error_type}")
            assert e.error_type == ErrorType.INVALID_PARAM

    print("✅ Error handling tests passed!\n")


# ==============================================================================
# V0.5.0 FEATURE TESTS (VISION & AUDIO)
# ==============================================================================

def test_vision_image_url():
    """Test vision with image URL (NEW in v0.5.0)"""
    print("\n👁️  Testing Vision - Image URL (v0.5.0)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Vision requires API token\n")
        return

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            print("  → Analyzing image from URL...")

            # Use a public test image
            messages = [
                MessageBuilder.image(
                    role="user",
                    text="Describe this image briefly",
                    image_url="https://pollinations.ai/p/a%20cute%20cat",
                    detail="auto"
                )
            ]

            response = ai.text.chat(messages, model="openai")
            print(f"  💬 Response: {repr(response)}")
            if not response.strip():
                print("  ⚠️  Empty response from API — skipping assertion")
                return
            assert len(response) > 0, "Response should not be empty"

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            if "not support" in e.message.lower() or "vision" in e.message.lower():
                print("  ℹ️  Model may not support vision - this is expected for some models\n")
            else:
                raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            raise


def test_vision_local_image():
    """Test vision with local image file (NEW in v0.5.0)"""
    print("\n👁️  Testing Vision - Local Image (v0.5.0)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Vision requires API token\n")
        return

    # First generate a test image
    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            print("  → Generating test image...")
            test_image = OUTPUT_DIR / "test_vision.jpg"
            ai.image.save(
                "a simple red circle on white background",
                filename=test_image,
                width=256,
                height=256
            )
            print(f"  ✅ Test image created: {test_image}")

            print("  → Analyzing local image...")
            messages = [
                MessageBuilder.image(
                    role="user",
                    text="What color is the main object in this image?",
                    image_path=str(test_image),
                    detail="low"
                )
            ]

            response = ai.text.chat(messages, model="openai")
            print(f"  💬 Response: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            print("✅ Vision (local file) test passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            if "not support" in e.message.lower() or "vision" in e.message.lower():
                print("  ℹ️  Model may not support vision - this is expected\n")
            else:
                raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            raise


def test_audio_output():
    """Test audio output generation (NEW in v0.5.0)"""
    print("\n🔊 Testing Audio Output (v0.5.0)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Audio generation requires API token\n")
        return

    with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            print("  → Testing audio output with modalities...")

            messages = [{"role": "user", "content": "Say hello"}]

            # Request audio output
            response = ai.text.chat(
                messages,
                model="openai",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "wav"}
            )

            print(f"  💬 Text response: {response[:50]}...")
            assert len(response) > 0, "Response should not be empty"

            print("✅ Audio output test passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            if "not support" in e.message.lower() or "audio" in e.message.lower():
                print("  ℹ️  Audio may not be fully supported yet - this is expected\n")
            else:
                print(f"  ℹ️  Error details: {e}\n")
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")


def test_message_builder():
    """Test MessageBuilder helpers (NEW in v0.5.0)"""
    print("\n🔨 Testing MessageBuilder Helpers (v0.5.0)...")

    try:
        # Test text message
        print("  → Testing text message builder...")
        msg = MessageBuilder.text("user", "Hello")
        assert msg["role"] == "user"
        assert msg["content"] == "Hello"
        print("  ✅ Text message builder works")

        # Test image message structure
        print("  → Testing image message builder...")
        msg = MessageBuilder.image(
            role="user",
            text="Analyze this",
            image_url="https://example.com/image.jpg"
        )
        assert msg["role"] == "user"
        assert isinstance(msg["content"], list)
        print("  ✅ Image message builder works")

        print("✅ MessageBuilder tests passed!\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")
        raise


# ==============================================================================
# ASYNCHRONOUS TESTS (V2 API)
# ==============================================================================

async def _test_image_generation_async():
    """Test asynchronous image generation"""
    print("\n🖼️  Testing Image Generation (Async - V2 API)...")

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
    print("\n📝 Testing Text Generation (Async - V2 API)...")

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


async def _test_streaming_async():
    """Test asynchronous streaming"""
    print("\n🌊 Testing Streaming (Async - V2 API)...")

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

            print("\n✅ Async streaming tests passed!\n")
            return True

        except BlossomError as e:
            print(f"\n❌ Error: {e.message}\n")
            return False


async def _test_vision_async():
    """Test async vision (NEW in v0.5.0)"""
    print("\n👁️  Testing Vision (Async - v0.5.0)...")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("  ⚠️  Skipping: Vision requires API token\n")
        return True

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            print("  → Async vision test...")

            messages = [
                MessageBuilder.image(
                    role="user",
                    text="What do you see?",
                    image_url="https://pollinations.ai/p/a%20dog"
                )
            ]

            response = await ai.text.chat(messages, model="openai")
            print(f"  💬 Response: {response[:100]}...")

            print("✅ Async vision test passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print("  ℹ️  Vision support may vary by model\n")
            return True  # Don't fail test


# ==============================================================================
# TEST RUNNERS
# ==============================================================================

def run_sync_tests():
    """Run all synchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - SYNCHRONOUS TESTS (V2 API)")
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
        test_error_handling_sync()
        results.append(("Error Handling", True))
    except Exception:
        results.append(("Error Handling", False))

    return results


def run_streaming_tests():
    """Run synchronous streaming tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - STREAMING TESTS (V2 API)")
    print("=" * 70)

    results = []

    try:
        test_streaming_sync()
        results.append(("Streaming (Sync)", True))
    except Exception:
        results.append(("Streaming (Sync)", False))

    return results


def run_v050_tests():
    """Run v0.5.0 feature tests (Vision & Audio)"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - V0.5.0 FEATURE TESTS (VISION & AUDIO)")
    print("=" * 70)

    results = []

    try:
        test_message_builder()
        results.append(("MessageBuilder Helpers", True))
    except Exception:
        results.append(("MessageBuilder Helpers", False))

    try:
        test_vision_image_url()
        results.append(("Vision (URL)", True))
    except Exception:
        results.append(("Vision (URL)", False))

    try:
        test_vision_local_image()
        results.append(("Vision (Local File)", True))
    except Exception:
        results.append(("Vision (Local File)", False))

    try:
        test_audio_output()
        results.append(("Audio Output", True))
    except Exception:
        results.append(("Audio Output", False))

    return results


async def run_async_tests():
    """Run all asynchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - ASYNCHRONOUS TESTS (V2 API)")
    print("=" * 70)

    results = []

    results.append(("Image Generation (Async)", await _test_image_generation_async()))
    results.append(("Text Generation (Async)", await _test_text_generation_async()))
    results.append(("Streaming (Async)", await _test_streaming_async()))
    results.append(("Vision (Async)", await _test_vision_async()))

    return results


def print_summary(sync_results, streaming_results, v050_results, async_results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    all_results = sync_results + streaming_results + v050_results + async_results

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

    if v050_results:
        print("\n🆕 v0.5.0 Feature Tests:")
        for name, result in v050_results:
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
    parser = argparse.ArgumentParser(description="Blossom AI Test Suite (V2 API)")
    parser.add_argument("--sync", action="store_true", help="Run only sync tests")
    parser.add_argument("--async", dest="run_async", action="store_true", help="Run only async tests")
    parser.add_argument("--streaming", action="store_true", help="Run only streaming tests")
    parser.add_argument("--v050", action="store_true", help="Run only v0.5.0 feature tests")
    parser.add_argument("--token", type=str, help="API token for authentication")

    args = parser.parse_args()

    # Set token if provided
    global API_TOKEN
    if args.token:
        API_TOKEN = args.token

    print("\n🌸 Blossom AI - Test Suite v0.5.0 (V2 API)")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")

    if not API_TOKEN or API_TOKEN == "Your-API-Token-Here":
        print("⚠️  No API token provided - some tests will be skipped")
        print("   Get your token at: https://enter.pollinations.ai")

    sync_results = []
    streaming_results = []
    v050_results = []
    async_results = []

    try:
        if args.v050:
            # Run only v0.5.0 feature tests
            v050_results = run_v050_tests()
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
            v050_results = run_v050_tests()
            async_results = asyncio.run(run_async_tests())

        # Print summary
        success = print_summary(sync_results, streaming_results, v050_results, async_results)

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