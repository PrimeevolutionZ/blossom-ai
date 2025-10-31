"""
Blossom AI - Usage Examples
Comparing V1 (legacy) and V2 (new enter.pollinations.ai) APIs
"""

from blossom_ai import Blossom, create_client
import asyncio


# ============================================================================
# IMAGE GENERATION
# ============================================================================

def image_examples():
    """Image generation examples"""

    print("=" * 60)
    print("IMAGE GENERATION EXAMPLES")
    print("=" * 60)

    # V1 API (legacy) - basic features
    print("\n1. V1 API - Basic image generation:")
    client_v1 = Blossom(api_version="v1", api_token="pk_eWXggKxdW7BYRZGrFGSsGJ")

    image = client_v1.image.generate(
        prompt="a beautiful sunset over mountains",
        model="flux",
        width=1024,
        height=1024,
        seed=42,
        nologo=True
    )
    print(f"Generated image: {len(image)} bytes")

    # V2 API (new) - advanced features
    print("\n2. V2 API - Advanced image generation:")
    client_v2 = Blossom(api_version="v2", api_token="pk_eWXggKxdW7BYRZGrFGSsGJ")

    image = client_v2.image.generate(
        prompt="a beautiful sunset over mountains",
        model="flux",
        width=1024,
        height=1024,
        seed=42,
        quality="hd",  # NEW in V2: quality levels
        guidance_scale=7.5,  # NEW in V2: guidance control
        negative_prompt="blurry, low quality",  # NEW in V2: negative prompts
        enhance=True,  # Auto-enhance prompt
        transparent=False,  # NEW in V2: transparent backgrounds
        nologo=True,
        nofeed=True,  # NEW in V2: don't add to public feed
        safe=False
    )
    print(f"Generated HD image: {len(image)} bytes")

    # Get available models
    print("\n3. Available models:")
    v2_models = client_v2.image.models()
    print(f"V2 models: {v2_models}")

    client_v1.close_sync()
    client_v2.close_sync()


# ============================================================================
# TEXT GENERATION
# ============================================================================

def text_examples():
    """Text generation examples"""

    print("\n" + "=" * 60)
    print("TEXT GENERATION EXAMPLES")
    print("=" * 60)

    # V1 API - simple text generation
    print("\n1. V1 API - Simple generation:")
    client_v1 = Blossom(api_version="v1")

    response = client_v1.text.generate(
        prompt="Write a short poem about AI",
        model="openai",
        temperature=0.7
    )
    print(f"Response: {response[:100]}...")

    # V2 API - OpenAI-compatible with advanced features
    print("\n2. V2 API - Advanced generation with parameters:")
    client_v2 = Blossom(api_version="v2", api_token="your_token")

    response = client_v2.text.generate(
        prompt="Write a short poem about AI",
        model="openai",
        system="You are a creative poet",
        temperature=0.8,  # 0-2 range in V2
        max_tokens=200,  # NEW in V2: token limit
        top_p=0.9,  # NEW in V2: nucleus sampling
        frequency_penalty=0.5,  # NEW in V2: reduce repetition
        presence_penalty=0.3,  # NEW in V2: encourage diversity
    )
    print(f"Response: {response[:100]}...")

    # Streaming example
    print("\n3. V2 API - Streaming:")
    print("Streaming response: ", end="")
    for chunk in client_v2.text.generate(
            prompt="Count from 1 to 5",
            model="openai-fast",  # Use fast model for streaming
            stream=True
    ):
        print(chunk, end="", flush=True)
    print()

    # Chat with history
    print("\n4. V2 API - Chat with conversation history:")
    messages = [
        {"role": "system", "content": "You are a helpful math tutor"},
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "2+2 equals 4"},
        {"role": "user", "content": "What about 3+3?"}
    ]

    response = client_v2.text.chat(
        messages=messages,
        model="openai",
        temperature=0.7
    )
    print(f"Chat response: {response}")

    # JSON mode
    print("\n5. V2 API - JSON mode:")
    response = client_v2.text.generate(
        prompt="Generate a JSON object with name, age, and city for a fictional person",
        model="openai",
        json_mode=True  # Force JSON response
    )
    print(f"JSON response: {response}")

    # Function calling (NEW in V2)
    print("\n6. V2 API - Function calling:")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather in a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = client_v2.text.chat(
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"}
        ],
        model="openai",
        tools=tools,
        tool_choice="auto"
    )
    print(f"Function calling response: {response}")

    # Get available models with details
    print("\n7. Available models:")
    v2_models = client_v2.text.models()
    print(f"V2 text models: {v2_models}")

    client_v1.close_sync()
    client_v2.close_sync()


# ============================================================================
# ASYNC EXAMPLES
# ============================================================================

async def async_examples():
    """Async examples with V2 API"""

    print("\n" + "=" * 60)
    print("ASYNC EXAMPLES (V2 API)")
    print("=" * 60)

    async with Blossom(api_version="v2", api_token="your_token") as client:
        # Parallel generation
        print("\n1. Parallel image generation:")
        tasks = [
            client.image.generate(f"image {i}", seed=i)
            for i in range(3)
        ]
        images = await asyncio.gather(*tasks)
        print(f"Generated {len(images)} images in parallel")

        # Async streaming
        print("\n2. Async text streaming:")
        print("Stream: ", end="")
        async for chunk in await client.text.generate(
                "Tell me a joke",
                stream=True
        ):
            print(chunk, end="", flush=True)
        print()

        # Async chat
        print("\n3. Async chat:")
        response = await client.text.chat(
            messages=[
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "Hello!"}
            ],
            model="openai-fast"
        )
        print(f"Chat: {response}")


# ============================================================================
# MIGRATION GUIDE
# ============================================================================

def migration_guide():
    """Migration guide from V1 to V2"""

    print("\n" + "=" * 60)
    print("MIGRATION GUIDE: V1 → V2")
    print("=" * 60)

    print("""
    🚀 KEY IMPROVEMENTS IN V2:

    IMAGE GENERATION:
    - ✅ Quality levels: low, medium, high, hd
    - ✅ Guidance scale control
    - ✅ Transparent backgrounds
    - ✅ Img2img support
    - ✅ Negative prompts
    - ✅ Feed control (nofeed parameter)

    TEXT GENERATION:
    - ✅ Full OpenAI compatibility
    - ✅ Function calling / Tools
    - ✅ JSON mode (forced structured output)
    - ✅ Advanced parameters (frequency_penalty, presence_penalty)
    - ✅ Max tokens control
    - ✅ Better streaming
    - ✅ Multiple models with aliases

    AUTHENTICATION:
    - ✅ Better rate limits with API tokens
    - ✅ Secret keys vs Publishable keys
    - ✅ Anonymous access still supported

    BREAKING CHANGES:
    - Temperature range changed to 0-2 (was 0-1)
    - Different endpoint structure
    - Some model names may differ

    MIGRATION STEPS:

    1. Change api_version parameter:
       OLD: client = Blossom()  # defaults to v1
       NEW: client = Blossom(api_version="v2")

    2. Get API token (optional but recommended):
       - Visit: https://enter.pollinations.ai
       - Create account and generate token
       - Use: client = Blossom(api_version="v2", api_token="your_token")

    3. Update model names if needed:
       - Check available models: client.text.models()
       - Some models have aliases for compatibility

    4. Leverage new features:
       - Add quality="hd" for better images
       - Use json_mode=True for structured output
       - Try function calling for agentic workflows

    5. Test thoroughly:
       - V1 and V2 can coexist in your code
       - Gradually migrate features
       - V1 remains supported (for now)
    """)


# ============================================================================
# COMPARISON TABLE
# ============================================================================

def comparison_table():
    """Feature comparison table"""

    print("\n" + "=" * 60)
    print("FEATURE COMPARISON: V1 vs V2")
    print("=" * 60)

    print("""
    ┌─────────────────────────────┬──────────┬──────────┐
    │ Feature                     │    V1    │    V2    │
    ├─────────────────────────────┼──────────┼──────────┤
    │ Basic image generation      │    ✅    │    ✅    │
    │ Quality levels              │    ❌    │    ✅    │
    │ Guidance scale              │    ❌    │    ✅    │
    │ Transparent backgrounds     │    ❌    │    ✅    │
    │ Negative prompts            │    ❌    │    ✅    │
    │ Img2img                     │    ❌    │    ✅    │
    ├─────────────────────────────┼──────────┼──────────┤
    │ Basic text generation       │    ✅    │    ✅    │
    │ Chat / Conversation         │    ✅    │    ✅    │
    │ Streaming                   │    ✅    │    ✅    │
    │ JSON mode                   │    ✅    │    ✅    │
    │ Function calling            │    ❌    │    ✅    │
    │ Max tokens control          │    ❌    │    ✅    │
    │ Frequency penalty           │    ❌    │    ✅    │
    │ Presence penalty            │    ❌    │    ✅    │
    │ Top-p sampling              │    ❌    │    ✅    │
    ├─────────────────────────────┼──────────┼──────────┤
    │ Audio generation            │    ✅    │    🚧    │
    │ Multiple voices             │    ✅    │    🚧    │
    ├─────────────────────────────┼──────────┼──────────┤
    │ API token support           │    ✅    │    ✅    │
    │ Rate limiting               │   Basic  │ Advanced │
    │ Anonymous access            │    ✅    │    ✅    │
    └─────────────────────────────┴──────────┴──────────┘

    Legend:
    ✅ Supported
    ❌ Not supported
    🚧 Coming soon / In development
    """)


# ============================================================================
# RUN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n🌸 BLOSSOM AI - API COMPARISON\n")

    # Uncomment to run specific examples:

    # image_examples()
    # text_examples()
    # asyncio.run(async_examples())

    migration_guide()
    comparison_table()

    print("\n✨ Done! Check the examples above.")
    print("📝 Remember to set your API token for V2: api_token='your_token'")
    print("🔗 Get token at: https://enter.pollinations.ai")