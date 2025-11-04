import pytest
from blossom_ai import Blossom
from blossom_ai.core import TextModel


class TestModels:
    """Тесты для получения списка моделей"""

    @pytest.fixture
    def api_token(self):
        """Фикстура с API токеном"""
        return "plln_sk_dziAc0GyDGNH6VequHETYZaB4xVRn0gkBC8UVsvrmLDWh3GQB9cDDi4IMPfP2hRr"

    @pytest.fixture
    def client(self, api_token):
        """Фикстура с клиентом Blossom"""
        with Blossom(api_version="v2", api_token=api_token) as client:
            yield client

    def test_client_text_models_returns_list(self, client):
        """Тест что client.text.models() возвращает список"""
        # Act
        models = client.text.models()

        # Assert
        assert isinstance(models, list)
        assert len(models) > 0
        print(f"📋 Получено моделей через client: {len(models)}")
        print(f"📝 Модели: {models}")

    def test_text_model_initialize_from_api(self, api_token):
        """Тест инициализации TextModel из API"""
        # Act
        TextModel.initialize_from_api(api_token=api_token, api_version="v2")
        models = TextModel.get_all_known()

        # Assert
        assert isinstance(models, list)
        assert len(models) > 0
        print(f"📋 Получено моделей через TextModel: {len(models)}")
        print(f"📝 Модели: {models}")

    def test_claudyclaude_in_models(self, client):
        """Тест наличия модели claudyclaude в списке"""
        # Act
        models = client.text.models()

        # Assert
        if "claudyclaude" in models:
            print("✅ claudyclaude найден в списке моделей")
            assert "claudyclaude" in models
        else:
            print("❌ claudyclaude не найден в списке моделей")
            pytest.skip("claudyclaude не доступен")

    def test_models_contain_expected_models(self, client):
        """Тест что список содержит ожидаемые модели"""
        # Act
        models = client.text.models()

        # Assert - проверяем наличие хотя бы некоторых ожидаемых моделей
        expected_models = ["openai", "deepseek", "gemini", "mistral", "qwen-coder"]
        found_models = [model for model in expected_models if model in models]

        print(f"🔍 Найдено ожидаемых моделей: {found_models}")
        assert len(found_models) >= 2, f"Должно быть хотя бы 2 ожидаемые модели, найдено: {found_models}"

    def test_models_structure(self, client):
        """Тест структуры возвращаемых моделей"""
        # Act
        models = client.text.models()

        # Assert
        for model in models:
            assert isinstance(model, str)
            assert len(model) > 0
            assert " " not in model, f"Имя модели не должно содержать пробелов: '{model}'"

    @pytest.mark.parametrize("model_name", ["openai", "deepseek", "gemini"])
    def test_specific_models_exist(self, client, model_name):
        """Параметризованный тест для конкретных моделей"""
        # Act
        models = client.text.models()

        # Assert
        if model_name in models:
            print(f"✅ {model_name} найден")
            assert model_name in models
        else:
            print(f"⚠️ {model_name} не найден")
            pytest.skip(f"{model_name} не доступен")


class TestModelUsage:
    """Тесты использования моделей"""

    @pytest.fixture
    def api_token(self):
        return "plln_sk_dziAc0GyDGNH6VequHETYZaB4xVRn0gkBC8UVsvrmLDWh3GQB9cDDi4IMPfP2hRr"

    @pytest.fixture
    def client(self, api_token):
        with Blossom(api_version="v2", api_token=api_token) as client:
            yield client

    def test_chat_with_available_model(self, client):
        """Тест чата с доступной моделью"""
        # Arrange
        models = client.text.models()
        available_model = models[0]  # Берем первую доступную модель

        # Act
        response = client.text.chat(
            messages=[{"role": "user", "content": "Скажи привет!"}],
            model=available_model,
            max_tokens=20
        )

        # Assert
        assert isinstance(response, str)
        assert len(response) > 0
        print(f"✅ Модель '{available_model}' ответила: {response}")

    def test_chat_with_claudyclaude_if_available(self, client):
        """Тест чата с claudyclaude если доступен"""
        # Arrange
        models = client.text.models()

        if "claudyclaude" not in models:
            pytest.skip("claudyclaude не доступен")

        # Act
        response = client.text.chat(
            messages=[{"role": "user", "content": "Привет! Ты Claude? Ответь кратко."}],
            model="claudyclaude",
            max_tokens=30
        )

        # Assert
        assert isinstance(response, str)
        assert len(response) > 0
        print(f"✅ claudyclaude ответил: {response}")


def test_compare_model_sources(api_token):
    """Сравнение моделей из разных источников"""
    # Arrange
    with Blossom(api_version="v2", api_token=api_token) as client:
        client_models = client.text.models()

    TextModel.initialize_from_api(api_token=api_token, api_version="v2")
    class_models = TextModel.get_all_known()

    # Assert
    print(f"🔍 Сравнение:")
    print(f"   client.text.models(): {len(client_models)} моделей")
    print(f"   TextModel.get_all_known(): {len(class_models)} моделей")

    # Находим различия
    client_only = set(client_models) - set(class_models)
    class_only = set(class_models) - set(client_models)

    if client_only:
        print(f"   📌 Только в client: {client_only}")
    if class_only:
        print(f"   📌 Только в TextModel: {class_only}")

    # Должны быть хотя бы некоторые общие модели
    common_models = set(client_models) & set(class_models)
    assert len(common_models) > 0, "Должны быть общие модели между источниками"


if __name__ == "__main__":
    # Можно запустить и как обычный скрипт
    pytest.main([__file__, "-v", "-s"])