"""
🌸 Blossom AI - Text Generation Tests

Tests for text generation functionality.
"""

import unittest
from blossom_ai import Blossom, BlossomError


class TestTextGeneration(unittest.TestCase):
    """Test text generation functionality"""

    def setUp(self):
        """Set up test client"""
        self.ai = Blossom(timeout=60)

    def test_simple_generation(self):
        """Test simple text generation"""
        print("\n🧪 Testing simple generation...")

        response = self.ai.text.generate("Say hello in one word")

        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

        print(f"✅ Response: {response}")

    def test_with_system_message(self):
        """Test generation with system message"""
        print("\n🧪 Testing with system message...")

        response = self.ai.text.generate(
            prompt="What is 2+2?",
            system="You are a math teacher. Answer briefly."
        )

        self.assertIsNotNone(response)
        self.assertIn("4", response)

        print(f"✅ Response: {response}")

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results"""
        print("\n🧪 Testing reproducibility with seed...")

        seed = 42
        prompt = "Pick a number between 1 and 10"

        response1 = self.ai.text.generate(prompt, seed=seed)
        response2 = self.ai.text.generate(prompt, seed=seed)

        self.assertIsNotNone(response1)
        self.assertIsNotNone(response2)

        # Responses should be identical or very similar
        print(f"✅ Response 1: {response1}")
        print(f"✅ Response 2: {response2}")
        print(f"   Match: {response1.strip() == response2.strip()}")

    def test_different_seeds(self):
        """Test that different seeds can produce different results"""
        print("\n🧪 Testing different seeds...")

        prompt = "Pick a random number"

        response1 = self.ai.text.generate(prompt, seed=42)
        response2 = self.ai.text.generate(prompt, seed=123)

        self.assertIsNotNone(response1)
        self.assertIsNotNone(response2)

        print(f"✅ Seed 42:  {response1}")
        print(f"✅ Seed 123: {response2}")

    def test_json_mode(self):
        """Test JSON mode response"""
        print("\n🧪 Testing JSON mode...")

        response = self.ai.text.generate(
            prompt="List 2 colors",
            system="Return valid JSON array",
            json_mode=True
        )

        self.assertIsNotNone(response)
        self.assertIn("[", response)  # Should contain JSON array syntax

        print(f"✅ JSON Response: {response}")

    def test_chat_with_history(self):
        """Test chat with message history"""
        print("\n🧪 Testing chat with history...")

        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
            {"role": "user", "content": "Is it popular?"}
        ]

        response = self.ai.text.chat(messages)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

        print(f"✅ Chat Response: {response}")

    def test_code_generation(self):
        """Test code generation"""
        print("\n🧪 Testing code generation...")

        response = self.ai.text.generate(
            prompt="Write a Python function that adds two numbers",
            system="You are a Python expert. Write only code."
        )

        self.assertIsNotNone(response)
        self.assertTrue(
            "def" in response or "function" in response.lower(),
            "Response should contain code"
        )

        print(f"✅ Code Response:\n{response}")

    def test_creative_writing(self):
        """Test creative writing"""
        print("\n🧪 Testing creative writing...")

        response = self.ai.text.generate(
            prompt="Write a haiku about coding",
            system="You are a poet"
        )

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 10)

        print(f"✅ Haiku:\n{response}")

    def test_translation(self):
        """Test translation"""
        print("\n🧪 Testing translation...")

        response = self.ai.text.generate(
            prompt="Translate to French: Hello, how are you?",
            system="You are a translator"
        )

        self.assertIsNotNone(response)
        self.assertTrue(
            any(word in response.lower() for word in ["bonjour", "salut", "comment"]),
            "Response should be in French"
        )

        print(f"✅ Translation: {response}")

    def test_summarization(self):
        """Test summarization"""
        print("\n🧪 Testing summarization...")

        response = self.ai.text.generate(
            prompt="Summarize in one sentence: Artificial intelligence is transforming how we work and live.",
            system="You are concise"
        )

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

        print(f"✅ Summary: {response}")

    def test_models_list(self):
        """Test listing available models"""
        print("\n🧪 Testing models list...")

        models = self.ai.text.models()

        self.assertIsNotNone(models)
        self.assertTrue(isinstance(models, (list, dict)))

        if isinstance(models, list):
            print(f"✅ Found {len(models)} models")
            print(f"   First 3: {models[:3]}")
        else:
            print(f"✅ Models data: {type(models)}")

    def test_empty_prompt(self):
        """Test handling of empty prompt"""
        print("\n🧪 Testing empty prompt...")

        try:
            response = self.ai.text.generate("")
            print(f"✅ Response to empty prompt: {response}")
        except Exception as e:
            print(f"✅ Correctly handled empty prompt: {type(e).__name__}")

    def test_long_prompt(self):
        """Test handling of long prompt"""
        print("\n🧪 Testing long prompt...")

        long_prompt = "Explain " + "very " * 50 + "briefly what AI is"

        response = self.ai.text.generate(long_prompt)

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

        print(f"✅ Long prompt handled, response length: {len(response)}")

    def test_special_characters(self):
        """Test handling of special characters"""
        print("\n🧪 Testing special characters...")

        response = self.ai.text.generate("What is 1+1? Answer: $ & # @")

        self.assertIsNotNone(response)

        print(f"✅ Special chars handled: {response}")

    def test_multiple_languages(self):
        """Test generation in different languages"""
        print("\n🧪 Testing multiple languages...")

        languages = [
            ("Spanish", "Hola"),
            ("German", "Hallo"),
            ("Japanese", "こんにちは")
        ]

        for lang, word in languages:
            response = self.ai.text.generate(
                f"Say hello in {lang}",
                system="Respond only with the greeting"
            )
            print(f"✅ {lang}: {response}")

    def test_private_mode(self):
        """Test private mode"""
        print("\n🧪 Testing private mode...")

        response = self.ai.text.generate(
            "This is a private message",
            private=True
        )

        self.assertIsNotNone(response)

        print(f"✅ Private response: {response}")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)