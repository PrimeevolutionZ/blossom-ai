"""
Blossom AI - Models and Enums
Dynamic model classes that can be extended from API responses
"""

from typing import Set, Optional


class DynamicModel:
    """Base class for dynamic model names that can be extended at runtime"""

    _known_values: Set[str] = set()

    @classmethod
    def from_string(cls, value: str) -> str:
        """
        Get model value from string, adds to known values if not exists
        This allows dynamic values from API
        """
        cls._known_values.add(value)
        return value

    @classmethod
    def update_known_values(cls, values: list) -> None:
        """Update known values from API response"""
        # API может возвращать как строки, так и словари
        for value in values:
            if isinstance(value, dict):
                # Если словарь, пытаемся извлечь имя модели
                model_name = value.get('name') or value.get('id') or value.get('model')
                if model_name:
                    cls._known_values.add(model_name)
            elif isinstance(value, str):
                # Если строка, добавляем напрямую
                cls._known_values.add(value)

    @classmethod
    def get_all_known(cls) -> list:
        """Get all known values (defaults + dynamic from API)"""
        defaults = cls.get_defaults()
        return list(set(defaults) | cls._known_values)

    @classmethod
    def get_defaults(cls) -> list:
        """Get default values (to be overridden)"""
        return []


class ImageModel(DynamicModel):
    """
    Image generation models
    Note: These are fallback defaults. Actual models fetched from API.
    """
    # Constants for IDE autocomplete
    FLUX = "flux"
    KONTEXT = "kontext"
    TURBO = "turbo"
    GPTIMAGE = "gptimage"

    @classmethod
    def get_defaults(cls) -> list:
        return ["flux", "kontext", "turbo", "gptimage"]


class TextModel(DynamicModel):
    """
    Text generation models
    Note: These are fallback defaults. Actual models fetched from API.
    """
    # Constants for IDE autocomplete
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    MISTRAL = "mistral"
    QWEN_CODER = "qwen-coder"

    @classmethod
    def get_defaults(cls) -> list:
        return ["deepseek", "gemini", "mistral", "openai", "qwen-coder"]


class Voice(DynamicModel):
    """
    Text-to-speech voices
    Note: These are fallback defaults. Actual voices fetched from API.
    """
    # Constants for IDE autocomplete
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"

    @classmethod
    def get_defaults(cls) -> list:
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class ErrorType:
    """Error types for BlossomError"""
    NETWORK = "NETWORK_ERROR"
    API = "API_ERROR"
    INVALID_PARAM = "INVALID_PARAMETER"
    AUTH = "AUTHENTICATION_ERROR"
    RATE_LIMIT = "RATE_LIMIT_ERROR"
    UNKNOWN = "UNKNOWN_ERROR"


# Fallback lists (used when API doesn't respond)
DEFAULT_IMAGE_MODELS = ["flux", "kontext", "turbo", "gptimage"]
DEFAULT_TEXT_MODELS = ["deepseek", "gemini", "mistral", "openai", "qwen-coder"]
DEFAULT_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]