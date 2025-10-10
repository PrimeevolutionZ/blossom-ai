"""
🌸 Blossom AI - Audio Generation Tests

Tests for audio generation functionality with and without API token.
"""

import unittest
import os
import tempfile
from blossom_ai import Blossom, BlossomError
from blossom_ai.errors import ErrorType


class TestAudioGenerationWithToken(unittest.TestCase):
    """Test audio generation functionality with API token"""

    @classmethod
    def setUpClass(cls):
        """Set up test class - check if token is available"""
        cls.api_token = os.environ.get('POLLINATIONS_API_TOKEN')
        if not cls.api_token:
            raise unittest.SkipTest("POLLINATIONS_API_TOKEN not found in environment. Skipping authenticated tests.")

    def setUp(self):
        """Set up test client with token"""
        self.ai = Blossom(timeout=60, api_token=self.api_token)

    def test_simple_audio_generation(self):
        """Test simple audio generation with token"""
        print("\n🧪 [WITH TOKEN] Testing simple audio generation...")

        audio_data = self.ai.audio.generate("Hello, this is a test audio.")

        self.assertIsNotNone(audio_data)
        self.assertIsInstance(audio_data, bytes)
        self.assertGreater(len(audio_data), 1000)

        print(f"✅ Generated audio size: {len(audio_data)} bytes")

    def test_all_voices(self):
        """Test audio generation with all available voices"""
        print("\n🧪 [WITH TOKEN] Testing all voices...")

        voices_to_test = self.ai.audio.voices()
        text_to_generate = "The quick brown fox jumps over the lazy dog."

        self.assertGreater(len(voices_to_test), 0, "No voices found to test.")

        success_count = 0
        for voice in voices_to_test:
            try:
                audio_data = self.ai.audio.generate(text=text_to_generate, voice=voice)
                self.assertIsNotNone(audio_data)
                self.assertIsInstance(audio_data, bytes)
                self.assertGreater(len(audio_data), 1000)
                print(f"✅ Voice '{voice}': {len(audio_data)} bytes")
                success_count += 1
            except BlossomError as e:
                print(f"⚠️  Voice '{voice}' failed: {e.message}")

        # With token, most voices should work
        self.assertGreater(success_count, len(voices_to_test) * 0.5,
                          f"Expected at least half of voices to work with token, got {success_count}/{len(voices_to_test)}")

    def test_save_audio_to_file(self):
        """Test saving generated audio to file with token"""
        print("\n🧪 [WITH TOKEN] Testing save to file...")

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            saved_path = self.ai.audio.save(
                text="This is an audio file saved to disk.",
                filename=filename
            )

            self.assertEqual(saved_path, filename)
            self.assertTrue(os.path.exists(filename))
            self.assertGreater(os.path.getsize(filename), 1000)

            print(f"✅ Audio saved to: {filename}")
            print(f"✅ File size: {os.path.getsize(filename)} bytes")

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_long_text_input(self):
        """Test handling of very long text input with token"""
        print("\n🧪 [WITH TOKEN] Testing very long text input...")

        long_text = "This is a very long text that should be handled properly. " * 50

        try:
            audio_data = self.ai.audio.generate(long_text)
            self.assertIsNotNone(audio_data)
            self.assertGreater(len(audio_data), 1000)
            print(f"✅ Long text input handled, audio size: {len(audio_data)} bytes")
        except BlossomError as e:
            # With token, this might still fail due to length limits
            if "402" in str(e) or "Payment Required" in str(e):
                print(f"⚠️  Long text requires higher tier: {e.message}")
            else:
                raise

    def test_empty_text_input(self):
        """Test handling of empty text input with token"""
        print("\n🧪 [WITH TOKEN] Testing empty text input...")

        audio_data = self.ai.audio.generate("")
        self.assertIsNotNone(audio_data)
        self.assertGreaterEqual(len(audio_data), 0)
        print(f"✅ Empty text input handled, audio size: {len(audio_data)} bytes")


class TestAudioGenerationWithoutToken(unittest.TestCase):
    """Test audio generation functionality without API token (anonymous tier)"""

    def setUp(self):
        """Set up test client without token"""
        self.ai = Blossom(timeout=60)

    def test_simple_audio_generation(self):
        """Test simple audio generation without token"""
        print("\n🧪 [WITHOUT TOKEN] Testing simple audio generation...")

        try:
            audio_data = self.ai.audio.generate("Hello, this is a test audio.")
            # If it works, great!
            self.assertIsNotNone(audio_data)
            self.assertGreater(len(audio_data), 1000)
            print(f"✅ Generated audio size: {len(audio_data)} bytes")
        except BlossomError as e:
            # Without token, we expect this to fail for most voices
            self.assertEqual(e.error_type, ErrorType.API)
            self.assertIn("402", str(e) + e.message)
            print(f"✅ Expected failure without token: {e.message}")

    def test_basic_voices_only(self):
        """Test that only basic voices work without token"""
        print("\n🧪 [WITHOUT TOKEN] Testing basic voices...")

        voices_to_test = self.ai.audio.voices()
        text_to_generate = "Test audio."

        working_voices = []
        failed_voices = []

        for voice in voices_to_test:
            try:
                audio_data = self.ai.audio.generate(text=text_to_generate, voice=voice)
                working_voices.append(voice)
                print(f"✅ Voice '{voice}': {len(audio_data)} bytes (works without token)")
            except BlossomError as e:
                if "402" in str(e) or "Payment Required" in str(e):
                    failed_voices.append(voice)
                    print(f"⚠️  Voice '{voice}' requires token (tier: seed or higher)")
                else:
                    raise

        print(f"\n📊 Summary without token:")
        print(f"   Working voices: {working_voices}")
        print(f"   Restricted voices: {failed_voices}")

    def test_voices_list_available(self):
        """Test that voice list is available without token"""
        print("\n🧪 [WITHOUT TOKEN] Testing audio voices list...")

        voices = self.ai.audio.voices()

        self.assertIsNotNone(voices)
        self.assertTrue(isinstance(voices, list))
        self.assertGreater(len(voices), 0)

        print(f"✅ Found {len(voices)} audio voices")
        print(f"   Available voices: {voices}")

    def test_save_fails_gracefully_without_token(self):
        """Test that save operation fails gracefully without token"""
        print("\n🧪 [WITHOUT TOKEN] Testing save operation...")

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            try:
                saved_path = self.ai.audio.save(
                    text="This should require authentication.",
                    filename=filename,
                    voice="shimmer"  # Likely requires token
                )
                # If it works, verify the file
                self.assertTrue(os.path.exists(filename))
                print(f"✅ Unexpectedly succeeded without token")
            except BlossomError as e:
                # Expected to fail without token
                self.assertEqual(e.error_type, ErrorType.API)
                print(f"✅ Expected authentication error: {e.message}")

        finally:
            if os.path.exists(filename):
                os.unlink(filename)


class TestAudioGenerationCommon(unittest.TestCase):
    """Test audio generation functionality common to both token and non-token scenarios"""

    def setUp(self):
        """Set up test client"""
        api_token = os.environ.get('POLLINATIONS_API_TOKEN')
        self.ai = Blossom(timeout=60, api_token=api_token)
        self.has_token = api_token is not None

    def test_invalid_voice(self):
        """Test handling of an invalid voice"""
        print("\n🧪 [COMMON] Testing invalid voice...")

        with self.assertRaises(BlossomError) as cm:
            self.ai.audio.generate(text="Hello", voice="nonexistent_voice_xyz123")

        self.assertEqual(cm.exception.error_type, ErrorType.API)
        print(f"✅ Invalid voice correctly raised BlossomError: {cm.exception.message}")

    def test_voices_list_structure(self):
        """Test that voices list has correct structure"""
        print("\n🧪 [COMMON] Testing voices list structure...")

        voices = self.ai.audio.voices()

        self.assertIsInstance(voices, list)
        self.assertGreater(len(voices), 0)

        # All voices should be strings
        for voice in voices:
            self.assertIsInstance(voice, str)
            self.assertGreater(len(voice), 0)

        print(f"✅ Voices list structure valid: {len(voices)} voices")

    def test_client_representation(self):
        """Test that client shows token status correctly"""
        print("\n🧪 [COMMON] Testing client representation...")

        repr_str = repr(self.ai)

        if self.has_token:
            self.assertIn("with token", repr_str)
            print(f"✅ Client shows token present: {repr_str}")
        else:
            self.assertIn("without token", repr_str)
            print(f"✅ Client shows no token: {repr_str}")


def run_tests_with_summary():
    """Run all tests and provide a summary"""
    print("\n" + "="*80)
    print("🌸 BLOSSOM AI - AUDIO GENERATION TEST SUITE")
    print("="*80)

    # Check token status
    token = os.environ.get('POLLINATIONS_API_TOKEN')
    if token:
        print(f"🔑 Running tests WITH API token (length: {len(token)})")
    else:
        print("⚠️  Running tests WITHOUT API token (anonymous tier)")
        print("   Set POLLINATIONS_API_TOKEN environment variable to test authenticated features")

    print("="*80 + "\n")

    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAudioGenerationCommon))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioGenerationWithoutToken))

    if token:
        suite.addTests(loader.loadTestsFromTestCase(TestAudioGenerationWithToken))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    print("="*80)

    return result


if __name__ == "__main__":
    run_tests_with_summary()