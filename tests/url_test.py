"""
Примеры использования нового метода generate_url()
"""

from blossom_ai import Blossom
import asyncio


# ============================================================================
# СИНХРОННОЕ ИСПОЛЬЗОВАНИЕ
# ============================================================================

def sync_examples():
    """Синхронные примеры"""

    client = Blossom()

    # 1. Базовое использование - получить URL без скачивания
    url = client.image.generate_url("a beautiful sunset")
    print(f"Image URL: {url}")

    # 2. С параметрами для воспроизводимости
    url = client.image.generate_url(
        "a cat sitting on a chair",
        seed=42,
        nologo=True,
        private=True
    )
    print(f"Image URL with seed: {url}")

    # 3. С пользовательскими размерами и моделью
    url = client.image.generate_url(
        "cyberpunk city at night",
        model="flux",
        width=1920,
        height=1080,
        enhance=True
    )
    print(f"Custom size URL: {url}")

    # 4. С referrer параметром (как у пользователя)
    url = client.image.generate_url(
        "anime style portrait",
        referrer="my-discord-bot",
        seed=12345,
        nologo=True
    )
    print(f"URL with referrer: {url}")

    # 5. Можно использовать URL в разных местах
    # Например, отправить в Discord, Telegram, или встроить в HTML
    html = f'<img src="{url}" alt="Generated Image">'
    print(f"HTML: {html}")


# ============================================================================
# АСИНХРОННОЕ ИСПОЛЬЗОВАНИЕ
# ============================================================================

async def async_examples():
    """Асинхронные примеры"""

    async with Blossom() as client:
        # 1. Базовое использование
        url = await client.image.generate_url("a futuristic spaceship")
        print(f"Async URL: {url}")

        # 2. Генерация нескольких URL параллельно
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
            print(f"{prompt}: {url}")

        # 3. fast generate
        user_prompt = "epic dragon breathing fire"
        url = await client.image.generate_url(
            user_prompt,
            nologo=True,
            private=True,
            safe=True  # filter out unsafe cont
        )
        return url


# ============================================================================
# usage in Discord bot
# ============================================================================

async def discord_bot_example(user_message: str):
    """Пример использования в Discord боте"""

    client = Blossom()

    # Генерируем URL вместо скачивания изображения
    # Это экономит трафик и время
    url = await client.image.generate_url(
        user_message,
        nologo=True,
        private=True,
        seed=hash(user_message) % 100000  # Детерминированный seed из текста
    )

    # Теперь можно просто отправить URL в Discord
    # Discord автоматически покажет превью
    return url


# ============================================================================
#  URL vs DOWNLOAD
# ============================================================================

async def comparison():

    client = Blossom()
    prompt = "a magical forest"

    # metod 1: get URL
    import time
    start = time.time()
    url = await client.image.generate_url(prompt, seed=42)
    url_time = time.time() - start
    print(f"URL generation: {url_time:.3f}s")
    print(f"URL: {url}")

    # Метод 2: get image
    start = time.time()
    image_bytes = await client.image.generate(prompt, seed=42)
    download_time = time.time() - start
    print(f"Image download: {download_time:.3f}s")
    print(f"Size: {len(image_bytes)} bytes")

    print(f"\nSpeed improvement: {download_time / url_time:.1f}x faster")


# ============================================================================
# auth token
# ============================================================================

def with_auth_token():
    """Использование с API токеном"""

    # Токен автоматически добавляется к URL
    client = Blossom(api_token="your-api-token-here")

    url = client.image.generate_url(
        "premium quality image",
        private=True,
        enhance=True
    )

    # URL будет содержать параметр token=your-api-token-here
    print(f"Authenticated URL: {url}")


# ============================================================================
# examples: EMBED in HTML
# ============================================================================

def generate_gallery_html():
    """generate HTML gallery"""

    client = Blossom()

    # Создаем несколько URL для галереи
    themes = [
        ("sunset", "A beautiful sunset over the ocean"),
        ("mountains", "Majestic mountain peaks covered in snow"),
        ("city", "Futuristic cityscape at night"),
        ("nature", "Serene forest with sunlight streaming through trees")
    ]

    html = "<html><body><h1>AI Generated Gallery</h1><div>"

    for name, prompt in themes:
        url = client.image.generate_url(
            prompt,
            seed=hash(name) % 100000,
            nologo=True
        )
        html += f'''
        <div style="margin: 20px;">
            <h3>{name.title()}</h3>
            <img src="{url}" width="512" alt="{prompt}">
            <p>{prompt}</p>
        </div>
        '''

    html += "</div></body></html>"

    # save to file
    with open("gallery.html", "w") as f:
        f.write(html)

    print("Gallery saved to gallery.html")


# ============================================================================
# play test
# ============================================================================

if __name__ == "__main__":
    print("=== Синхронные примеры ===")
    sync_examples()

    print("\n=== Асинхронные примеры ===")
    asyncio.run(async_examples())

    print("\n=== Сравнение производительности ===")
    asyncio.run(comparison())

    print("\n=== Генерация HTML галереи ===")
    generate_gallery_html()