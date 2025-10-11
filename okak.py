import asyncio
from blossom_ai import AsyncBlossom, BlossomError

# Замените на ваш токен, если есть (обязателен для аудио и nologo)
API_TOKEN = "nwMWyfBzIpPQRdkr"  # или "ваш_токен_здесь"


async def main():
    # Инициализация асинхронного клиента
    async_ai = AsyncBlossom(api_token=API_TOKEN, timeout=60)

    try:
        print("🚀 Тест асинхронной генерации изображения...")
        image_path = await async_ai.image.save(
            prompt="a cyberpunk cat wearing neon sunglasses",
            filename="test_image.jpg",
            width=512,
            height=512,
            model="flux"
        )
        print(f"✅ Изображение сохранено: {image_path}")

        print("\n📝 Тест асинхронной генерации текста...")
        try:
            # Простой короткий промпт для теста
            text_response = await async_ai.text.generate(
                prompt="Hello"
            )
            print(f"✅ Текст (простой): {text_response}")

            # Добавим задержку между запросами (rate limit = 3 секунды)
            await asyncio.sleep(3)

            # Теперь более сложный промпт БЕЗ ТОЧКИ В КОНЦЕ
            text_response = await async_ai.text.generate(
                prompt="Explain async programming in one sentence",  # Убрали точку!
                model="openai"
            )
            print(f"✅ Текст (сложный): {text_response}")

        except BlossomError as e:
            print(f"⚠️ GET endpoint ошибка: {e.message}")
            print("   Пробуем через POST chat endpoint...")

            try:
                # Попробуем через chat API (POST endpoint)
                await asyncio.sleep(3)
                text_response = await async_ai.text.chat(
                    messages=[
                        {"role": "user", "content": "Explain async programming"}
                    ]
                )
                print(f"✅ Текст (через POST chat): {text_response}")
            except Exception as e2:
                print(f"⚠️ POST endpoint тоже не работает: {e2}")

        print("\n🎙️ Тест асинхронной генерации аудио...")
        if API_TOKEN:
            audio_path = await async_ai.audio.save(
                text="Hello from asynchronous Blossom AI!",
                filename="test_audio.mp3",
                voice="nova"
            )
            print(f"✅ Аудио сохранено: {audio_path}")
        else:
            print("⚠️ Пропущено: требуется API_TOKEN для генерации аудио")

        # Опционально: проверка списка голосов и моделей
        print("\n📋 Получение информации о доступных ресурсах...")
        voices = await async_ai.audio.voices()
        print(f"ℹ️ Доступные голоса: {voices}")

        try:
            models = await async_ai.text.models()
            print(f"ℹ️ Доступные текстовые модели: {models}")
        except BlossomError as e:
            print(f"⚠️ Не удалось получить список моделей: {e.message}")

        try:
            image_models = await async_ai.image.models()
            print(f"ℹ️ Доступные модели изображений: {image_models}")
        except BlossomError as e:
            print(f"⚠️ Не удалось получить список моделей изображений: {e.message}")

    except BlossomError as e:
        print(f"❌ Ошибка Blossom: {e.message}")
        print(f"💡 Предложение: {e.suggestion}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    finally:
        # Всегда закрывайте сессию!
        await async_ai.close()
        print("\n🔒 Сессия закрыта.")


if __name__ == "__main__":
    asyncio.run(main())