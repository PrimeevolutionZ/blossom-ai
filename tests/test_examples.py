"""
🌸 Blossom AI - Unified Test Suite (with Streaming)
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
"""

import asyncio
import sys
import argparse
from pathlib import Path
import time

# Import from the current package
try:
    from blossom_ai import Blossom, BlossomError
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from blossom_ai import Blossom, BlossomError, ErrorType


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

            # Chat with temperature
            print("  → Chat with temperature...")
            response = ai.text.chat([
                {"role": "user", "content": "Tell me a short story"}
            ], temperature=1.0)
            print(f"  💬 Story: {response[:100]}...")
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

    if not API_TOKEN:
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
    try:
        print("  → Testing authentication requirement...")
        with Blossom(api_token=None) as ai_no_auth:
            ai_no_auth.audio.generate("test")
            print("  ⚠️  Audio might work without auth (API change?)")
    except BlossomError as e:
        print(f"  ✅ Caught expected error: {e.error_type}")

    print("✅ Error handling tests passed!\n")


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

            # Test async generate method
            print("  → Testing async generate method...")
            image_data = await ai.image.generate(
                prompt="async test image",
                width=256,
                height=256
            )
            print(f"  ✅ Generated async image: {len(image_data)} bytes")
            assert len(image_data) > 0, "Image data should not be empty"

            # List models
            models = await ai.image.models()
            print(f"  ℹ️  Available models: {models}")
            assert isinstance(models, list), "Models should be a list"
            assert len(models) > 0, "Should have at least one model"

            print("✅ Async image generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
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

            # Chat completion
            print("  → Async chat completion...")
            response = await ai.text.chat([
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "What is async programming?"}
            ])
            print(f"  💬 Chat: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            # Chat with JSON mode
            print("  → Async chat with JSON mode...")
            response = await ai.text.chat([
                {"role": "user", "content": "List 2 colors in JSON format"}
            ], json_mode=True)
            print(f"  💬 JSON response: {response[:100]}...")
            assert len(response) > 0, "Response should not be empty"

            print("✅ Async text generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False


async def _test_audio_generation_async():
    """Test asynchronous audio generation"""
    print("\n🎙️  Testing Audio Generation (Async)...")

    if not API_TOKEN:
        print("  ⚠️  Skipping: Audio generation requires API token")
        print("     Get yours at https://auth.pollinations.ai\n")
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

            # Parallel audio generation
            print("  → Parallel audio generation...")
            tasks = [
                ai.audio.save(f"Voice test {i}", OUTPUT_DIR / f"parallel_{i}.mp3", voice="alloy")
                for i in range(3)
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                assert Path(result).exists(), "Audio file should exist"
            print(f"  ✅ All parallel audio saved: {len(results)} files")

            # Test async generate method
            print("  → Testing async generate method...")
            audio_data = await ai.audio.generate(
                text="Test async audio generation",
                voice="echo"
            )
            print(f"  ✅ Generated async audio: {len(audio_data)} bytes")
            assert len(audio_data) > 0, "Audio data should not be empty"

            # List voices
            voices = await ai.audio.voices()
            print(f"  ℹ️  Available voices: {voices}")
            assert isinstance(voices, list), "Voices should be a list"
            assert len(voices) > 0, "Should have at least one voice"

            print("✅ Async audio generation tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
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
            print(f"  ✅ Total length: {len(full_response)} chars")
            assert chunks_received > 0, "Should receive chunks"
            assert len(full_response) > 0, "Response should not be empty"

            # Async streaming chat
            print("\n  → Testing async streaming chat...")
            print("  💬 Chat streaming: ", end='', flush=True)

            messages = [
                {"role": "user", "content": "Say hello in 3 different languages"}
            ]

            chat_chunks = 0
            async for chunk in await ai.text.chat(messages, stream=True):
                print(chunk, end='', flush=True)
                chat_chunks += 1

            print()
            print(f"  ✅ Received {chat_chunks} chunks")
            assert chat_chunks > 0, "Should receive chat chunks"

            # Parallel streaming (collect results)
            print("\n  → Testing parallel async streaming...")

            async def collect_stream(prompt):
                chunks = []
                async for chunk in await ai.text.generate(prompt, stream=True):
                    chunks.append(chunk)
                return ''.join(chunks)

            results = await asyncio.gather(
                collect_stream("Say 'Hello'"),
                collect_stream("Say 'World'"),
                collect_stream("Say 'Python'")
            )

            print(f"  ✅ Collected {len(results)} parallel streams")
            for i, result in enumerate(results):
                print(f"    Stream {i+1}: {len(result)} chars")
                assert len(result) > 0, "Stream result should not be empty"

            # Async streaming with timeout
            print("\n  → Testing async streaming with timeout...")
            try:
                start_time = time.time()
                chunks = 0

                async with asyncio.timeout(3):  # 3 second timeout
                    async for chunk in await ai.text.generate(
                        "Write a very short sentence",
                        stream=True
                    ):
                        chunks += 1

                elapsed = time.time() - start_time
                print(f"  ✅ Completed in {elapsed:.2f}s with {chunks} chunks")

            except asyncio.TimeoutError:
                print(f"  ⚠️  Timeout reached (this is OK for testing)")

            # Async streaming to file
            print("\n  → Testing async streaming to file...")
            output_file = OUTPUT_DIR / "async_streaming_output.txt"

            async with asyncio.create_task(ai.text.generate(
                "Write a sentence about programming",
                stream=True
            )) as stream_task:
                with open(output_file, 'w', encoding='utf-8') as f:
                    async for chunk in await stream_task:
                        f.write(chunk)
                        f.flush()

            # Fallback simple method
            with open(output_file, 'w', encoding='utf-8') as f:
                async for chunk in await ai.text.generate(
                    "Write about async programming",
                    stream=True
                ):
                    f.write(chunk)
                    f.flush()

            assert output_file.exists(), "Output file should exist"
            content = output_file.read_text(encoding='utf-8')
            print(f"  ✅ Saved {len(content)} chars to async file")
            assert len(content) > 0, "File should have content"

            print("\n✅ Async streaming tests passed!\n")
            return True

        except BlossomError as e:
            print(f"\n❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            import traceback
            traceback.print_exc()
            return False


async def _test_mixed_async():
    """Test mixed async operations"""
    print("\n🔀 Testing Mixed Async Operations...")

    async with Blossom(api_token=API_TOKEN, timeout=60) as ai:
        try:
            # All operations in parallel!
            print("  → Running ALL operations in parallel...")

            image_task = ai.image.save("robot", OUTPUT_DIR / "mixed_robot.jpg", width=512, height=512)
            text_task = ai.text.generate("Fun fact about AI")

            if API_TOKEN:
                audio_task = ai.audio.save("Mixed operation test", OUTPUT_DIR / "mixed_audio.mp3", voice="alloy")
                results = await asyncio.gather(image_task, text_task, audio_task)
                print(f"  🔊 Audio saved: {results[2]}")
                assert Path(results[2]).exists(), "Audio file should exist"
            else:
                results = await asyncio.gather(image_task, text_task)

            print(f"  ✅ Image saved: {results[0]}")
            assert Path(results[0]).exists(), "Image file should exist"
            print(f"  💬 Text generated: {results[1][:50]}...")
            assert len(results[1]) > 0, "Text should not be empty"

            print("✅ Mixed async tests passed!\n")
            return True

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
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
    results.append(("Mixed Operations (Async)", await _test_mixed_async()))

    return results


def print_summary(sync_results, streaming_results, async_results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    all_results = sync_results + streaming_results + async_results

    total = len(all_results)
    passed = sum(1 for _, result in all_results if result)
    failed = total - passed

    if sync_results:
        print("\nSynchronous Tests:")
        for name, result in sync_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    if streaming_results:
        print("\nStreaming Tests:")
        for name, result in streaming_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    if async_results:
        print("\nAsynchronous Tests:")
        for name, result in async_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {status} - {name}")

    print(f"\n{'=' * 70}")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
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
    parser.add_argument("--token", type=str, help="API token for authentication")

    args = parser.parse_args()

    # Set token if provided
    global API_TOKEN
    if args.token:
        API_TOKEN = args.token

    print("\n🌸 Blossom AI - Unified Test Suite")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")

    if not API_TOKEN:
        print("⚠️  No API token provided - audio tests will be skipped")
        print("   Get your token at: https://auth.pollinations.ai")

    sync_results = []
    streaming_results = []
    async_results = []

    try:
        if args.streaming:
            # Run only streaming tests
            streaming_results = run_streaming_tests()
            async_results = asyncio.run(run_async_tests())  # Includes async streaming
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
            async_results = asyncio.run(run_async_tests())

        # Print summary
        success = print_summary(sync_results, streaming_results, async_results)

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