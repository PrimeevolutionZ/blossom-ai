"""
Examples of using generate_url() method (V2 API)
Демонстрация работы с URL генерацией изображений
"""

from blossom_ai import Blossom
import asyncio


# ============================================================================
# SYNCHRONOUS USAGE
# ============================================================================

def sync_examples():
    """Synchronous examples"""

    client = Blossom()

    print("=" * 70)
    print("SYNCHRONOUS URL GENERATION EXAMPLES (V2 API)")
    print("=" * 70)

    # 1. Basic usage - get URL without downloading
    print("\n1. Basic URL generation:")
    url = client.image.generate_url("a beautiful sunset")
    print(f"   URL: {url}")

    # 2. With parameters for reproducibility
    print("\n2. With seed for reproducibility:")
    url = client.image.generate_url(
        "a cat sitting on a chair",
        seed=42,
        nologo=True,
        private=True
    )
    print(f"   URL: {url}")

    # 3. With custom dimensions and model
    print("\n3. Custom dimensions:")
    url = client.image.generate_url(
        "cyberpunk city at night",
        model="flux",
        width=1920,
        height=1080,
        enhance=True
    )
    print(f"   URL: {url}")

    # 4. High quality image
    print("\n4. High quality image:")
    url = client.image.generate_url(
        "anime style portrait",
        quality="hd",
        seed=12345,
        nologo=True
    )
    print(f"   URL: {url}")

    # 5. Can be used in different places
    print("\n5. Embedding in HTML:")
    html = f'<img src="{url}" alt="Generated Image">'
    print(f"   HTML: {html[:80]}...")


# ============================================================================
# ASYNCHRONOUS USAGE
# ============================================================================

async def async_examples():
    """Asynchronous examples"""

    print("\n" + "=" * 70)
    print("ASYNCHRONOUS URL GENERATION EXAMPLES (V2 API)")
    print("=" * 70)

    async with Blossom() as client:
        # 1. Basic usage
        print("\n1. Basic async URL generation:")
        url = await client.image.generate_url("a futuristic spaceship")
        print(f"   URL: {url}")

        # 2. Generate multiple URLs in parallel
        print("\n2. Parallel URL generation:")
        prompts = [
            "a red apple",
            "a blue ocean",
            "a green forest"
        ]

        urls = await asyncio.gather(*[
            client.image.generate_url(prompt, seed=i)
            for i, prompt in enumerate(prompts)
        ])

        for prompt, url in zip(prompts, urls):
            print(f"   {prompt}: {url[:60]}...")

        # 3. Fast generation
        print("\n3. Fast generation with safety filters:")
        user_prompt = "epic dragon breathing fire"
        url = await client.image.generate_url(
            user_prompt,
            nologo=True,
            private=True,
            safe=True  # Filter out unsafe content
        )
        print(f"   URL: {url[:60]}...")
        return url


# ============================================================================
# DISCORD BOT EXAMPLE
# ============================================================================

async def discord_bot_example(user_message: str):
    """Example usage in Discord bot"""
    print("\n" + "=" * 70)
    print("DISCORD BOT EXAMPLE (V2 API)")
    print("=" * 70)

    client = Blossom()

    # Generate URL instead of downloading image
    # This saves bandwidth and time
    url = await client.image.generate_url(
        user_message,
        nologo=True,
        private=True,
        seed=hash(user_message) % 100000  # Deterministic seed from text
    )

    print(f"\nUser message: {user_message}")
    print(f"Generated URL: {url[:60]}...")
    print("Discord will automatically show preview")

    return url


# ============================================================================
# URL vs DOWNLOAD COMPARISON
# ============================================================================

async def comparison():
    """Compare URL generation vs downloading"""
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON (V2 API)")
    print("=" * 70)

    client = Blossom()
    prompt = "a magical forest"

    # Method 1: Get URL only
    import time
    start = time.time()
    url = await client.image.generate_url(prompt, seed=42)
    url_time = time.time() - start
    print(f"\n1. URL generation: {url_time:.3f}s")
    print(f"   URL: {url[:60]}...")

    # Method 2: Download full image
    start = time.time()
    image_bytes = await client.image.generate(prompt, seed=42)
    download_time = time.time() - start
    print(f"\n2. Image download: {download_time:.3f}s")
    print(f"   Size: {len(image_bytes):,} bytes")

    print(f"\n📊 Speed improvement: {download_time / url_time:.1f}x faster with URL!")


# ============================================================================
# WITH AUTH TOKEN
# ============================================================================

def with_auth_token():
    """Usage with API token (V2 API)"""
    print("\n" + "=" * 70)
    print("AUTHENTICATED URL GENERATION (V2 API)")
    print("=" * 70)

    # IMPORTANT: Token is added to Authorization header, NOT to URL
    client = Blossom(api_token="your-api-token-here")

    url = client.image.generate_url(
        "premium quality image",
        private=True,
        enhance=True,
        quality="hd"
    )

    print(f"\nGenerated URL: {url[:60]}...")
    print("\n⚠️  SECURITY NOTE:")
    print("   Token is sent in Authorization header, NOT in URL")
    print("   URLs are safe to share publicly")


# ============================================================================
# HTML GALLERY GENERATION
# ============================================================================

def generate_gallery_html():
    """Generate HTML gallery with image URLs"""
    print("\n" + "=" * 70)
    print("HTML GALLERY GENERATION (V2 API)")
    print("=" * 70)

    client = Blossom()

    # Create multiple URLs for gallery
    themes = [
        ("sunset", "A beautiful sunset over the ocean"),
        ("mountains", "Majestic mountain peaks covered in snow"),
        ("city", "Futuristic cityscape at night"),
        ("nature", "Serene forest with sunlight streaming through trees")
    ]

    html = """<!DOCTYPE html>
<html>
<head>
    <title>AI Generated Gallery</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { text-align: center; color: #333; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .item { border: 1px solid #ddd; border-radius: 8px; padding: 15px; }
        .item img { width: 100%; height: auto; border-radius: 4px; }
        .item h3 { margin: 10px 0; color: #555; }
        .item p { color: #777; font-size: 14px; }
    </style>
</head>
<body>
    <h1>🌸 AI Generated Gallery</h1>
    <div class="gallery">
"""

    for name, prompt in themes:
        url = client.image.generate_url(
            prompt,
            seed=hash(name) % 100000,
            nologo=True,
            width=512,
            height=512
        )
        html += f"""
        <div class="item">
            <h3>{name.title()}</h3>
            <img src="{url}" alt="{prompt}" loading="lazy">
            <p>{prompt}</p>
        </div>
"""

    html += """
    </div>
</body>
</html>
"""

    # Save to file
    with open("gallery.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\n✅ Gallery saved to gallery.html")
    print("   Open it in your browser to see the AI-generated images!")


# ============================================================================
# SECURITY BEST PRACTICES
# ============================================================================

def security_examples():
    """Security best practices for V2 API"""
    print("\n" + "=" * 70)
    print("SECURITY BEST PRACTICES (V2 API)")
    print("=" * 70)

    client = Blossom(api_token="your-secret-token")

    # ✅ GOOD: Token is NOT in URL
    url = client.image.generate_url("test image")

    print("\n✅ CORRECT:")
    print(f"   URL: {url[:60]}...")
    print("   Token is sent in Authorization header (secure)")

    print("\n🔒 SECURITY NOTES:")
    print("   1. API token is NEVER exposed in URLs")
    print("   2. URLs can be safely shared publicly")
    print("   3. Token is only in Authorization header")
    print("   4. Private images still require authentication to view")


# ============================================================================
# MAIN RUNNER
# ============================================================================

if __name__ == "__main__":
    print("\n🌸 Blossom AI - URL Generation Examples (V2 API)")
    print("=" * 70)

    print("\n▶️  Running synchronous examples...")
    sync_examples()

    print("\n▶️  Running asynchronous examples...")
    asyncio.run(async_examples())

    print("\n▶️  Running performance comparison...")
    asyncio.run(comparison())

    print("\n▶️  Running Discord bot example...")
    asyncio.run(discord_bot_example("a cute anime cat girl"))

    print("\n▶️  Demonstrating authentication...")
    with_auth_token()

    print("\n▶️  Generating HTML gallery...")
    generate_gallery_html()

    print("\n▶️  Security best practices...")
    security_examples()

    print("\n" + "=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)