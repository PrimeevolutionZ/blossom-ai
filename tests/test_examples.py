"""
🌸 Blossom AI - Unified Test Suite
Run all examples in one place!

Usage:
    # Run all tests
    python test_examples.py

    # Run only sync tests
    python test_examples.py --sync

    # Run only async tests
    python test_examples.py --async

    # Run specific test
    python test_examples.py --test image_generation
"""

import asyncio
import sys
import argparse
from pathlib import Path

from blossom_ai import Blossom, BlossomError


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Set your API token here or pass as environment variable
API_TOKEN = "nwMWyfBzIpPQRdkr"  # Get yours at https://auth.pollinations.ai

# Test output directory
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================================================================
# SYNCHRONOUS TESTS
# ==============================================================================

def test_image_generation_sync():
    """Test synchronous image generation"""
    print("\n🖼️  Testing Image Generation (Sync)...")

    ai = Blossom(api_token=API_TOKEN)

    try:
        # Basic image generation
        print("  → Generating basic image...")
        ai.image.save(
            prompt="a cute robot painting a landscape",
            filename=OUTPUT_DIR / "robot_sync.jpg",
            width=512,
            height=512,
            model="flux"
        )
        print("  ✅ Basic image saved!")

        # Image with seed (reproducible)
        print("  → Generating reproducible image...")
        ai.image.save(
            prompt="a majestic dragon in a mystical forest",
            filename=OUTPUT_DIR / "dragon_sync.jpg",
            seed=42,
            width=768,
            height=768
        )
        print("  ✅ Reproducible image saved!")

        # Enhanced prompt
        print("  → Generating with enhanced prompt...")
        ai.image.save(
            prompt="sunset over mountains",
            filename=OUTPUT_DIR / "sunset_sync.jpg",
            enhance=True,
            width=1024,
            height=576
        )
        print("  ✅ Enhanced image saved!")

        # List models
        models = ai.image.models()
        print(f"  ℹ️  Available models: {models}")

        print("✅ Image generation tests passed!\n")

    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        print(f"   Suggestion: {e.suggestion}\n")
        return False

    return True


def test_text_generation_sync():
    """Test synchronous text generation"""
    print("\n📝 Testing Text Generation (Sync)...")

    ai = Blossom(api_token=API_TOKEN)

    try:
        # Simple generation
        print("  → Simple text generation...")
        response = ai.text.generate("Explain quantum computing in one sentence")
        print(f"  💬 Response: {response[:100]}...")

        # With system message
        print("  → Generation with system message...")
        response = ai.text.generate(
            prompt="Write a haiku about coding",
            system="You are a creative poet who loves technology"
        )
        print(f"  💬 Haiku:\n{response}")

        # Reproducible with seed
        print("  → Reproducible generation...")
        response1 = ai.text.generate("Random creative idea", seed=42)
        response2 = ai.text.generate("Random creative idea", seed=42)
        print(f"  ✅ Seeds match: {response1 == response2}")

        # JSON mode
        print("  → JSON mode generation...")
        response = ai.text.generate(
            prompt="List 3 programming languages with their use cases",
            json_mode=True
        )
        print(f"  💬 JSON: {response[:150]}...")

        # Chat completion
        print("  → Chat completion...")
        response = ai.text.chat([
            {"role": "system", "content": "You are a helpful coding assistant"},
            {"role": "user", "content": "What is Python best for?"}
        ])
        print(f"  💬 Chat response: {response[:100]}...")

        # List models
        models = ai.text.models()
        print(f"  ℹ️  Available models: {models}")

        print("✅ Text generation tests passed!\n")

    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        print(f"   Suggestion: {e.suggestion}\n")
        return False

    return True


def test_audio_generation_sync():
    """Test synchronous audio generation"""
    print("\n🎙️  Testing Audio Generation (Sync)...")

    if not API_TOKEN:
        print("  ⚠️  Skipping: Audio generation requires API token")
        print("     Get yours at https://auth.pollinations.ai\n")
        return True

    ai = Blossom(api_token=API_TOKEN)

    try:
        # Basic audio generation
        print("  → Generating basic audio...")
        ai.audio.save(
            text="Welcome to Blossom AI, the beautiful Python SDK for Pollinations",
            filename=OUTPUT_DIR / "welcome_sync.mp3",
            voice="nova"
        )
        print("  ✅ Basic audio saved!")

        # Different voices
        voices_to_test = ["alloy", "echo", "shimmer"]
        for voice in voices_to_test:
            print(f"  → Testing voice: {voice}...")
            ai.audio.save(
                text=f"This is the {voice} voice",
                filename=OUTPUT_DIR / f"voice_{voice}_sync.mp3",
                voice=voice
            )
        print("  ✅ All voices tested!")

        # List available voices
        voices = ai.audio.voices()
        print(f"  ℹ️  Available voices: {voices}")

        print("✅ Audio generation tests passed!\n")

    except BlossomError as e:
        print(f"❌ Error: {e.message}")
        print(f"   Suggestion: {e.suggestion}\n")
        return False

    return True


def test_error_handling_sync():
    """Test error handling"""
    print("\n🛡️  Testing Error Handling (Sync)...")

    ai = Blossom(api_token=API_TOKEN)

    # Test invalid prompt length
    try:
        print("  → Testing prompt length validation...")
        very_long_prompt = "a" * 300
        ai.image.generate(very_long_prompt)
        print("  ❌ Should have raised an error!")
        return False
    except BlossomError as e:
        print(f"  ✅ Caught expected error: {e.error_type}")

    # Test authentication requirement
    try:
        print("  → Testing authentication requirement...")
        ai_no_auth = Blossom(api_token=None)
        ai_no_auth.audio.generate("test")
        print("  ⚠️  Audio might work without auth (API change?)")
    except BlossomError as e:
        print(f"  ✅ Caught expected error: {e.error_type}")

    print("✅ Error handling tests passed!\n")
    return True


# ==============================================================================
# ASYNCHRONOUS TESTS
# ==============================================================================

async def test_image_generation_async():
    """Test asynchronous image generation"""
    print("\n🖼️  Testing Image Generation (Async)...")

    async with Blossom(api_token=API_TOKEN) as ai:
        try:
            # Basic image generation
            print("  → Generating basic image...")
            await ai.image.save(
                prompt="a cute robot painting a landscape",
                filename=OUTPUT_DIR / "robot_async.jpg",
                width=512,
                height=512
            )
            print("  ✅ Basic image saved!")

            # Parallel generation
            print("  → Parallel image generation...")
            tasks = [
                ai.image.save("sunset", OUTPUT_DIR / "sunset_async.jpg", width=512, height=512),
                ai.image.save("forest", OUTPUT_DIR / "forest_async.jpg", width=512, height=512),
                ai.image.save("ocean", OUTPUT_DIR / "ocean_async.jpg", width=512, height=512)
            ]
            await asyncio.gather(*tasks)
            print("  ✅ All parallel images saved!")

            # List models
            models = await ai.image.models()
            print(f"  ℹ️  Available models: {models}")

            print("✅ Async image generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False

    return True


async def test_text_generation_async():
    """Test asynchronous text generation"""
    print("\n📝 Testing Text Generation (Async)...")

    async with Blossom(api_token=API_TOKEN) as ai:
        try:
            # Simple generation
            print("  → Simple text generation...")
            response = await ai.text.generate("Explain AI in one sentence")
            print(f"  💬 Response: {response[:100]}...")

            # Parallel generation
            print("  → Parallel text generation...")
            tasks = [
                ai.text.generate("What is Python?"),
                ai.text.generate("What is JavaScript?"),
                ai.text.generate("What is Rust?")
            ]
            responses = await asyncio.gather(*tasks)
            print(f"  ✅ Generated {len(responses)} responses in parallel!")

            # Chat completion
            print("  → Async chat completion...")
            response = await ai.text.chat([
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "What is async programming?"}
            ])
            print(f"  💬 Chat: {response[:100]}...")

            print("✅ Async text generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False

    return True


async def test_audio_generation_async():
    """Test asynchronous audio generation"""
    print("\n🎙️  Testing Audio Generation (Async)...")

    if not API_TOKEN:
        print("  ⚠️  Skipping: Audio generation requires API token")
        print("     Get yours at https://auth.pollinations.ai\n")
        return True

    async with Blossom(api_token=API_TOKEN) as ai:
        try:
            # Basic audio
            print("  → Generating basic audio...")
            await ai.audio.save(
                text="Async audio generation test",
                filename=OUTPUT_DIR / "test_async.mp3",
                voice="nova"
            )
            print("  ✅ Basic audio saved!")

            # Parallel audio generation
            print("  → Parallel audio generation...")
            tasks = [
                ai.audio.save(f"Voice test {i}", OUTPUT_DIR / f"parallel_{i}.mp3", voice="alloy")
                for i in range(3)
            ]
            await asyncio.gather(*tasks)
            print("  ✅ All parallel audio saved!")

            print("✅ Async audio generation tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False

    return True


async def test_mixed_async():
    """Test mixed async operations"""
    print("\n🔀 Testing Mixed Async Operations...")

    async with Blossom(api_token=API_TOKEN) as ai:
        try:
            # All operations in parallel!
            print("  → Running ALL operations in parallel...")

            image_task = ai.image.save("robot", OUTPUT_DIR / "mixed_robot.jpg", width=512, height=512)
            text_task = ai.text.generate("Fun fact about AI")

            results = await asyncio.gather(image_task, text_task)

            print(f"  ✅ Image saved: {results[0]}")
            print(f"  💬 Text generated: {results[1][:50]}...")

            print("✅ Mixed async tests passed!\n")

        except BlossomError as e:
            print(f"❌ Error: {e.message}")
            print(f"   Suggestion: {e.suggestion}\n")
            return False

    return True


# ==============================================================================
# TEST RUNNER
# ==============================================================================

def run_sync_tests():
    """Run all synchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - SYNCHRONOUS TESTS")
    print("=" * 70)

    results = []

    results.append(("Image Generation", test_image_generation_sync()))
    results.append(("Text Generation", test_text_generation_sync()))
    results.append(("Audio Generation", test_audio_generation_sync()))
    results.append(("Error Handling", test_error_handling_sync()))

    return results


async def run_async_tests():
    """Run all asynchronous tests"""
    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI - ASYNCHRONOUS TESTS")
    print("=" * 70)

    results = []

    results.append(("Image Generation (Async)", await test_image_generation_async()))
    results.append(("Text Generation (Async)", await test_text_generation_async()))
    results.append(("Audio Generation (Async)", await test_audio_generation_async()))
    results.append(("Mixed Operations (Async)", await test_mixed_async()))

    return results


def print_summary(sync_results, async_results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    all_results = sync_results + async_results

    total = len(all_results)
    passed = sum(1 for _, result in all_results if result)
    failed = total - passed

    print("\nSynchronous Tests:")
    for name, result in sync_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status} - {name}")

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
    async_results = []

    try:
        if args.run_async:
            # Run only async tests
            async_results = asyncio.run(run_async_tests())
        elif args.sync:
            # Run only sync tests
            sync_results = run_sync_tests()
        else:
            # Run all tests
            sync_results = run_sync_tests()
            async_results = asyncio.run(run_async_tests())

        # Print summary
        success = print_summary(sync_results, async_results)

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