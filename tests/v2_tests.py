"""
Blossom AI V2 – Quick Local Tests
Fast tests for local development with V2 API
"""

from pathlib import Path
from blossom_ai import Blossom, MessageBuilder

# ⚠️  Replace with your token from https://enter.pollinations.ai
API_TOKEN = "your-token-here"

OUTPUT_DIR = Path(__file__).parent / "test_output_v2"
OUTPUT_DIR.mkdir(exist_ok=True)

client: Blossom | None = None


# ---------- Helpers ---------------------------------------------------------

def _get_client() -> Blossom:
    """Get or create client"""
    global client
    if client is None:
        client = Blossom(api_token=API_TOKEN)
    return client


def _close_client() -> None:
    """Close client and cleanup"""
    global client
    if client is not None:
        client.close_sync()
        client = None


# ---------- Basic Tests -----------------------------------------------------

def test_v2_image_simple() -> None:
    """Test basic V2 image generation"""
    print("\n🎨 V2 Image Generation (flux)...")
    c = _get_client()

    try:
        img_bytes = c.image.generate(
            prompt="a cute cat",
            model="flux",
            width=256,
            height=256
        )
        assert isinstance(img_bytes, bytes) and len(img_bytes) > 1_000

        out_file = OUTPUT_DIR / "test_v2_cat.png"
        out_file.write_bytes(img_bytes)
        print(f"✅ Saved: {out_file}  ({len(img_bytes):,} bytes)")
    finally:
        _close_client()


def test_v2_text_simple() -> None:
    """Test basic V2 text generation"""
    print("\n💬 V2 Text Generation...")
    c = _get_client()

    try:
        reply = c.text.generate("Say hello in one sentence", model="openai")
        assert isinstance(reply, str) and len(reply.strip()) > 0
        print(f"✅ Response: {reply.strip()}")
    finally:
        _close_client()


def test_v2_json_mode() -> None:
    """Test V2 JSON mode"""
    print("\n📋 V2 JSON Mode...")
    c = _get_client()

    try:
        raw = c.text.generate(
            "Return JSON with keys: name and age",
            model="openai",
            json_mode=True,
            max_tokens=100,
        )

        import json
        data = json.loads(raw)
        assert isinstance(data, dict) and data
        print(f"✅ JSON Response: {data}")
    finally:
        _close_client()


def test_v2_stream() -> None:
    """Test V2 streaming"""
    print("\n🌊 V2 Streaming...")
    c = _get_client()

    try:
        chunks: list[str] = []
        print("   Response: ", end="", flush=True)

        for ch in c.text.generate("Count 1 2 3", model="openai", stream=True):
            chunks.append(ch)
            print(ch, end="", flush=True)

        print()  # New line

        full = "".join(chunks)
        assert len(chunks) > 0 and len(full) > 0
        print(f"✅ Received {len(chunks)} chunks")
    finally:
        _close_client()


def test_v2_chat() -> None:
    """Test V2 chat completion"""
    print("\n💭 V2 Chat Completion...")
    c = _get_client()

    try:
        messages = [
            {"role": "user", "content": "Hi, I am Alex"},
            {"role": "assistant", "content": "Hello Alex!"},
            {"role": "user", "content": "What is my name?"},
        ]
        answer = c.text.chat(messages, model="openai")
        assert "alex" in answer.lower()
        print(f"✅ Response: {answer.strip()}")
    finally:
        _close_client()


def test_v2_models() -> None:
    """Test V2 model listing"""
    print("\n📋 V2 Models Listing...")
    c = _get_client()

    try:
        img_models = c.image.models()
        txt_models = c.text.models()

        assert isinstance(img_models, list) and len(img_models) > 0
        assert isinstance(txt_models, list) and len(txt_models) > 0

        print(f"✅ Image models: {len(img_models)}")
        print(f"   First 5: {img_models[:5]}")
        print(f"✅ Text models: {len(txt_models)}")
        print(f"   First 5: {txt_models[:5]}")
    finally:
        _close_client()


# ---------- Advanced Features -----------------------------------------------

def test_v2_image_url() -> None:
    """Test V2 image URL generation"""
    print("\n🔗 V2 Image URL Generation...")
    c = _get_client()

    try:
        url = c.image.generate_url(
            "a red circle",
            model="flux",
            seed=42,
            width=256,
            height=256
        )

        assert isinstance(url, str)
        assert url.startswith("https://")
        assert "pollinations.ai" in url

        # CRITICAL: Token should NOT be in URL
        assert API_TOKEN not in url
        assert "token=" not in url.lower()

        print(f"✅ URL: {url[:80]}...")
        print("   ✅ Token NOT exposed in URL (secure)")
    finally:
        _close_client()


def test_v2_image_params() -> None:
    """Test V2 image with advanced parameters"""
    print("\n⚙️  V2 Image Advanced Parameters...")
    c = _get_client()

    try:
        img_bytes = c.image.generate(
            prompt="a beautiful landscape",
            model="flux",
            width=512,
            height=512,
            seed=42,
            enhance=True,
            nologo=True,
            quality="high"
        )

        assert isinstance(img_bytes, bytes) and len(img_bytes) > 1_000

        out_file = OUTPUT_DIR / "test_v2_landscape.png"
        out_file.write_bytes(img_bytes)
        print(f"✅ Saved: {out_file}  ({len(img_bytes):,} bytes)")
    finally:
        _close_client()


# ---------- V0.5.0 Features (Vision & Audio) --------------------------------

def test_v2_vision_url() -> None:
    """Test V2 vision with image URL (NEW in v0.5.0)"""
    print("\n👁️  V2 Vision (Image URL)...")
    c = _get_client()

    try:
        # Use MessageBuilder for vision
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="What do you see in this image?",
                image_url="https://pollinations.ai/p/a%20cute%20cat",
                detail="auto"
            )
        ]

        response = c.text.chat(messages, model="openai")
        assert isinstance(response, str) and len(response) > 0
        print(f"✅ Vision response: {response[:100]}...")
    except Exception as e:
        if "vision" in str(e).lower() or "not support" in str(e).lower():
            print("⚠️  Vision not supported by model - this is expected")
        else:
            raise
    finally:
        _close_client()


def test_v2_vision_local() -> None:
    """Test V2 vision with local image (NEW in v0.5.0)"""
    print("\n👁️  V2 Vision (Local Image)...")
    c = _get_client()

    try:
        # First create test image
        test_img = OUTPUT_DIR / "test_vision_input.jpg"
        img_data = c.image.generate(
            "a simple red circle on white background",
            width=256,
            height=256
        )
        test_img.write_bytes(img_data)
        print(f"   Created test image: {test_img}")

        # Now analyze it
        messages = [
            MessageBuilder.image_message(
                role="user",
                text="What color is the main object?",
                image_path=str(test_img),
                detail="low"
            )
        ]

        response = c.text.chat(messages, model="openai")
        assert isinstance(response, str) and len(response) > 0
        print(f"✅ Vision response: {response[:100]}...")
    except Exception as e:
        if "vision" in str(e).lower():
            print("⚠️  Vision not supported - this is expected")
        else:
            raise
    finally:
        _close_client()


def test_v2_message_builder() -> None:
    """Test MessageBuilder helpers (NEW in v0.5.0)"""
    print("\n🔨 V2 MessageBuilder Helpers...")

    try:
        # Test text message
        msg = MessageBuilder.text_message("user", "Hello")
        assert msg["role"] == "user"
        assert msg["content"] == "Hello"
        print("✅ Text message builder works")

        # Test image message structure
        msg = MessageBuilder.image_message(
            role="user",
            text="Analyze this",
            image_url="https://example.com/image.jpg"
        )
        assert msg["role"] == "user"
        assert isinstance(msg["content"], list)
        assert len(msg["content"]) == 2
        print("✅ Image message builder works")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


# ---------- Error Handling --------------------------------------------------

def test_v2_validation() -> None:
    """Test V2 parameter validation"""
    print("\n🛡️  V2 Parameter Validation...")
    c = _get_client()

    try:
        from blossom_ai.core.errors import ValidationError

        # Test prompt length validation
        try:
            c.image.generate("x" * 300)  # Too long
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            print(f"✅ Caught expected error: {e.error_type}")

    finally:
        _close_client()


# ---------- Test Runner -----------------------------------------------------

def run_all_tests():
    """Run all tests"""
    tests = [
        # Basic tests
        ("Image Generation", test_v2_image_simple),
        ("Text Generation", test_v2_text_simple),
        ("JSON Mode", test_v2_json_mode),
        ("Streaming", test_v2_stream),
        ("Chat Completion", test_v2_chat),
        ("Models Listing", test_v2_models),

        # Advanced features
        ("Image URL", test_v2_image_url),
        ("Image Parameters", test_v2_image_params),

        # V0.5.0 features
        ("Vision (URL)", test_v2_vision_url),
        ("Vision (Local)", test_v2_vision_local),
        ("MessageBuilder", test_v2_message_builder),

        # Error handling
        ("Validation", test_v2_validation),
    ]

    passed = failed = 0
    failed_tests = []

    print("\n" + "=" * 70)
    print("🌸 BLOSSOM AI V2 - LOCAL TEST SUITE")
    print("=" * 70)

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as exc:
            print(f"❌ FAILED: {exc}\n")
            failed += 1
            failed_tests.append(name)

    print("\n" + "=" * 70)
    print("📊 TEST RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")

    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for name in failed_tests:
            print(f"   - {name}")

    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)