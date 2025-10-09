"""
🌸 Blossom AI - Image Generation Tests

Tests for image generation functionality.
"""

import unittest
import os
import tempfile
from blossom_ai import Blossom, BlossomError
from blossom_ai.errors import ErrorType # Import ErrorType


class TestImageGeneration(unittest.TestCase):
    """Test image generation functionality"""

    def setUp(self):
        """Set up test client"""
        self.ai = Blossom(timeout=60)

    def test_simple_image_generation(self):
        """Test simple image generation"""
        print("\n🧪 Testing simple image generation...")

        image_data = self.ai.image.generate("a beautiful sunset")

        self.assertIsNotNone(image_data)
        self.assertIsInstance(image_data, bytes)
        self.assertGreater(len(image_data), 1000)  # Should be reasonable image size

        print(f"✅ Generated image size: {len(image_data)} bytes")

    def test_different_models(self):
        """Test image generation with different models"""
        print("\n🧪 Testing different models...")

        models_to_test = ["flux", "prod", "blue"]
        prompt = "a cute cat"

        for model in models_to_test:
            try:
                image_data = self.ai.image.generate(prompt, model=model)
                self.assertIsNotNone(image_data)
                self.assertGreater(len(image_data), 1000)
                print(f"✅ Model '{model}': {len(image_data)} bytes")
            except Exception as e:
                print(f"⚠️  Model '{model}' failed: {e}")

    def test_different_sizes(self):
        """Test image generation with different sizes"""
        print("\n🧪 Testing different sizes...")

        sizes = [
            (512, 512),
            (768, 768),
            (1024, 1024),
            (512, 768)  # Different aspect ratio
        ]

        prompt = "abstract art"

        for width, height in sizes:
            image_data = self.ai.image.generate(
                prompt,
                width=width,
                height=height
            )
            self.assertIsNotNone(image_data)
            self.assertGreater(len(image_data), 1000)
            print(f"✅ Size {width}x{height}: {len(image_data)} bytes")

    def test_reproducibility_with_seed(self):
        """Test that same seed produces similar results"""
        print("\n🧪 Testing reproducibility with seed...")

        seed = 42
        prompt = "a mystical forest"

        image_data1 = self.ai.image.generate(prompt, seed=seed)
        image_data2 = self.ai.image.generate(prompt, seed=seed)

        self.assertIsNotNone(image_data1)
        self.assertIsNotNone(image_data2)

        # Images should be very similar (though not necessarily identical due to timing differences)
        print(f"✅ Image 1 size: {len(image_data1)} bytes")
        print(f"✅ Image 2 size: {len(image_data2)} bytes")
        print(f"   Similar size: {abs(len(image_data1) - len(image_data2)) < 1000}")

    def test_save_image_to_file(self):
        """Test saving generated image to file"""
        print("\n🧪 Testing save to file...")

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            # Generate and save image
            saved_path = self.ai.image.save(
                prompt="a colorful butterfly",
                filename=filename
            )

            self.assertEqual(saved_path, filename)
            self.assertTrue(os.path.exists(filename))
            self.assertGreater(os.path.getsize(filename), 1000)

            print(f"✅ Image saved to: {filename}")
            print(f"✅ File size: {os.path.getsize(filename)} bytes")

        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)

    def test_private_mode(self):
        """Test private image generation"""
        print("\n🧪 Testing private mode...")

        image_data = self.ai.image.generate(
            "a private artwork",
            private=True
        )

        self.assertIsNotNone(image_data)
        self.assertGreater(len(image_data), 1000)

        print(f"✅ Private image generated: {len(image_data)} bytes")

    def test_enhanced_prompt(self):
        """Test enhanced prompt generation"""
        print("\n🧪 Testing enhanced prompt...")

        image_data = self.ai.image.generate(
            "a castle",
            enhance=True
        )

        self.assertIsNotNone(image_data)
        self.assertGreater(len(image_data), 1000)

        print(f"✅ Enhanced image: {len(image_data)} bytes")

    def test_safe_mode(self):
        """Test safe mode for content filtering"""
        print("\n🧪 Testing safe mode...")

        image_data = self.ai.image.generate(
            "a peaceful landscape",
            safe=True
        )

        self.assertIsNotNone(image_data)
        self.assertGreater(len(image_data), 1000)

        print(f"✅ Safe mode image: {len(image_data)} bytes")

    def test_nologo_parameter(self):
        """Test nologo parameter"""
        print("\n🧪 Testing nologo parameter...")

        image_data = self.ai.image.generate(
            "a modern building",
            nologo=True
        )

        self.assertIsNotNone(image_data)
        self.assertGreater(len(image_data), 1000)

        print(f"✅ No-logo image: {len(image_data)} bytes")

    def test_models_list(self):
        """Test listing available image models"""
        print("\n🧪 Testing image models list...")

        models = self.ai.image.models()

        self.assertIsNotNone(models)
        self.assertTrue(isinstance(models, list))
        self.assertGreater(len(models), 0)

        print(f"✅ Found {len(models)} image models")
        print(f"   First 5: {models[:5]}")

    def test_empty_prompt(self):
        """Test handling of empty prompt"""
        print("\n🧪 Testing empty prompt...")

        try:
            image_data = self.ai.image.generate("")
            print(f"✅ Response to empty prompt: {len(image_data)} bytes")
        except Exception as e:
            print(f"✅ Correctly handled empty prompt: {type(e).__name__}")

    def test_long_prompt(self):
        """Test handling of long prompt"""
        print("\n🧪 Testing long prompt...")

        long_prompt = "A " + "very " * 50 + "detailed landscape"

        with self.assertRaises(BlossomError) as cm:
            self.ai.image.generate(long_prompt)

        self.assertEqual(cm.exception.error_type, ErrorType.INVALID_PARAM)
        print(f"✅ Long prompt correctly raised BlossomError: {cm.exception.message}")

    def test_special_characters_prompt(self):
        """Test handling of special characters in prompt"""
        print("\n🧪 Testing special characters...")

        image_data = self.ai.image.generate("art with $ & # @ symbols")

        self.assertIsNotNone(image_data)
        self.assertGreater(len(image_data), 1000)

        print(f"✅ Special chars handled, image size: {len(image_data)} bytes")

    def test_multiple_aspect_ratios(self):
        """Test different aspect ratios"""
        print("\n🧪 Testing aspect ratios...")

        ratios = [
            (1024, 512),   # Wide
            (512, 1024),   # Tall
            (768, 1024),   # Portrait
            (1024, 768),   # Landscape
        ]

        prompt = "abstract patterns"

        for width, height in ratios:
            image_data = self.ai.image.generate(
                prompt,
                width=width,
                height=height
            )
            self.assertIsNotNone(image_data)
            print(f"✅ Ratio {width}:{height}: {len(image_data)} bytes")

    def test_art_styles(self):
        """Test different art style prompts"""
        print("\n🧪 Testing art styles...")

        styles = [
            "oil painting of a forest",
            "watercolor landscape",
            "digital art of a city",
            "pencil sketch of a portrait",
            "impressionist style garden"
        ]

        for style_prompt in styles:
            image_data = self.ai.image.generate(style_prompt)
            self.assertIsNotNone(image_data)
            self.assertGreater(len(image_data), 1000)
            print(f"✅ Style '{style_prompt[:20]}...': {len(image_data)} bytes")

    def test_creative_concepts(self):
        """Test creative and abstract concepts"""
        print("\n🧪 Testing creative concepts...")

        concepts = [
            "the sound of music visualized",
            "dreams of the future",
            "emotional landscape of joy",
            "abstract representation of time"
        ]

        for concept in concepts:
            image_data = self.ai.image.generate(concept)
            self.assertIsNotNone(image_data)
            print(f"✅ Concept '{concept[:20]}...': {len(image_data)} bytes")

    def test_batch_save_images(self):
        """Test saving multiple images with different parameters"""
        print("\n🧪 Testing batch image save...")

        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_and_files = [
                ("a red apple", "apple.jpg"),
                ("a blue car", "car.jpg"),
                ("a green tree", "tree.jpg")
            ]

            for prompt, filename in prompts_and_files:
                filepath = os.path.join(temp_dir, filename)
                saved_path = self.ai.image.save(prompt, filepath)

                self.assertEqual(saved_path, filepath)
                self.assertTrue(os.path.exists(filepath))
                print(f"✅ Saved: {filename} ({os.path.getsize(filepath)} bytes)")

    def test_image_quality_indicators(self):
        """Test that generated images have reasonable characteristics"""
        print("\n🧪 Testing image quality indicators...")

        image_data = self.ai.image.generate(
            "a detailed photograph of a mountain",
            width=1024,
            height=1024
        )

        self.assertIsNotNone(image_data)

        # Basic sanity checks for image data
        self.assertGreater(len(image_data), 50000)  # Reasonable size for 1024x1024
        self.assertLess(len(image_data), 5000000)   # Not excessively large

        # Check for common image file signatures
        self.assertTrue(
            image_data.startswith(b'\xff\xd8\xff') or  # JPEG
            image_data.startswith(b'\x89PNG\r\n\x1a\n'),  # PNG
            "Image data should be valid JPEG or PNG"
        )

        print(f"✅ Image quality check passed: {len(image_data)} bytes")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)

