"""
Blossom AI V2 – локальные быстрые тесты
Токен оставлен в коде для локального запуска
"""

from pathlib import Path
from blossom_ai import Blossom

API_TOKEN = "plln_sk_DWA2waYqiWBgSeS2C2Ir6X04bBdI5dDJmwwGffCkXpOKsxVmy0c3ZWjjcdsHesmF"

OUTPUT_DIR = Path(__file__).with_suffix("")  # папка рядом с файлом
OUTPUT_DIR.mkdir(exist_ok=True)

client: Blossom | None = None


# ---------- helpers ---------------------------------------------------------

def _get_client() -> Blossom:
    global client
    if client is None:
        client = Blossom(api_version="v2", api_token=API_TOKEN)
    return client


def _close_client() -> None:
    global client
    if client is not None:
        client.close_sync()
        client = None


# ---------- тесты ------------------------------------------------------------

def test_v2_image_simple() -> None:
    """Генерация картинки: минимум параметров, проверка контента."""
    print("\n🎨 V2 Image (flux) …")
    c = _get_client()

    try:
        img_bytes = c.image.generate(
            prompt="a cute cat",
            model="flux",  # V2 пока принимает только model + prompt
        )
        assert isinstance(img_bytes, bytes) and len(img_bytes) > 1_000
        out_file = OUTPUT_DIR / "test_v2_cat.png"
        out_file.write_bytes(img_bytes)
        print(f"✅ сохранено: {out_file}  ({len(img_bytes)} B)")
    finally:
        _close_client()


def test_v2_text_simple() -> None:
    print("\n💬 V2 Text …")
    c = _get_client()

    reply = c.text.generate("Say hello in one sentence", model="openai")
    assert isinstance(reply, str) and len(reply.strip()) > 0
    print(f"✅ {reply.strip()}")


def test_v2_json_mode() -> None:
    print("\n📋 V2 JSON mode …")
    c = _get_client()

    raw = c.text.generate(
        "Return JSON: name and age",
        model="openai",
        json_mode=True,
        max_tokens=60,
    )
    import json

    data = json.loads(raw)
    assert isinstance(data, dict) and data
    print(f"✅ {data}")


def test_v2_stream() -> None:
    print("\n🌊 V2 Stream …")
    c = _get_client()

    chunks: list[str] = []
    for ch in c.text.generate("Count 1 2 3", model="openai", stream=True):
        chunks.append(ch)
        print(ch, end="", flush=True)

    full = "".join(chunks)
    assert len(chunks) > 0 and len(full) > 0
    print("\n✅ завершено")


def test_v2_chat() -> None:
    print("\n💭 V2 Chat …")
    c = _get_client()

    messages = [
        {"role": "user", "content": "Hi, I am Alex"},
        {"role": "assistant", "content": "Hello Alex!"},
        {"role": "user", "content": "What is my name?"},
    ]
    answer = c.text.chat(messages, model="openai")
    assert "alex" in answer.lower()
    print(f"✅ {answer.strip()}")


def test_v2_models() -> None:
    print("\n📋 V2 Models …")
    c = _get_client()

    img_models = c.image.models()
    txt_models = c.text.models()

    assert isinstance(img_models, list) and len(img_models) > 0
    assert isinstance(txt_models, list) and len(txt_models) > 0

    print(f"✅ Image: {len(img_models)}  |  Text: {len(txt_models)}")


# ---------- запуск -----------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_v2_image_simple,
        test_v2_text_simple,
        test_v2_json_mode,
        test_v2_stream,
        test_v2_chat,
        test_v2_models,
    ]

    passed = failed = 0
    for t in tests:
        try:
            t()
            print("✅ PASSED\n")
            passed += 1
        except Exception as exc:
            print(f"❌ FAILED: {exc}\n")
            failed += 1

    print("=" * 50)
    print(f"📊 {passed} passed  |  {failed} failed")
    print("=" * 50)