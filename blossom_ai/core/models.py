"""
Blossom AI - Models and Enums
Fixed imports for core/ directory structure
"""

from typing import Set, Optional, List, Dict, Any
import requests


from .config import ENDPOINTS
from .session_manager import SyncSessionManager
from .errors import handle_request_error, print_warning



class DynamicModel:
    """Base class for dynamic model names that can be extended at runtime"""

    _known_values: Set[str] = set()
    _initialized = False

    @classmethod
    def _fetch_models_from_api(cls, endpoint: str, api_token: Optional[str] = None) -> List[str]:
        """Fetch actual models from API with proper error handling"""
        try:
            with SyncSessionManager() as session_manager:
                session = session_manager.get_session()

                headers = {}
                if api_token:
                    headers['Authorization'] = f'Bearer {api_token}'

                response = session.get(endpoint, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                # Handle different response formats
                models = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            # Format from /generate/openai/models
                            if 'name' in item:
                                models.append(item['name'])
                            elif 'id' in item:
                                models.append(item['id'])
                            # Also add aliases if present
                            if 'aliases' in item and isinstance(item['aliases'], list):
                                models.extend(item['aliases'])
                        elif isinstance(item, str):
                            # Simple string array format
                            models.append(item)

                print_warning(f"Fetched {len(models)} models from API: {models}")
                return models

        except Exception as e:
            print_warning(f"Failed to fetch models from {endpoint}: {e}")
            return []

    @classmethod
    def initialize_from_api(cls, api_token: Optional[str] = None, api_version: str = "v2"):
        """Initialize known values from API"""
        if cls._initialized:
            return

        try:
            if api_version == "v2":
                # Try multiple endpoints to get complete model list
                endpoints_to_try = [
                    ENDPOINTS.V2_TEXT_MODELS,  # /generate/openai/models
                    f"{ENDPOINTS.V2_BASE}/generate/text/models",
                ]

                all_models = set()
                for endpoint in endpoints_to_try:
                    models = cls._fetch_models_from_api(endpoint, api_token)
                    all_models.update(models)

                if all_models:
                    cls._known_values.update(all_models)
                    print_warning(f"Initialized {cls.__name__} with {len(all_models)} models from API")
                else:
                    # Fallback to defaults if API fails
                    cls._known_values.update(cls.get_defaults())
                    print_warning(f"Using fallback defaults for {cls.__name__}")

            cls._initialized = True

        except Exception as e:
            print_warning(f"Failed to initialize {cls.__name__} from API: {e}")
            cls._known_values.update(cls.get_defaults())
            cls._initialized = True

    @classmethod
    def from_string(cls, value: str) -> str:
        """Get model value from string, adds to known values if not exists"""
        cls._known_values.add(value)
        return value

    @classmethod
    def update_known_values(cls, values: list) -> None:
        """Update known values from API response - FIXED VERSION"""
        if not values:
            return

        new_models = set()

        for value in values:
            if isinstance(value, dict):
                # Extract from object format
                model_name = value.get('name') or value.get('id') or value.get('model')
                if model_name:
                    new_models.add(model_name)

                # Also add aliases
                aliases = value.get('aliases', [])
                if isinstance(aliases, list):
                    new_models.update(aliases)

            elif isinstance(value, str):
                # Simple string
                new_models.add(value)

        if new_models:
            cls._known_values.update(new_models)

    @classmethod
    def get_all_known(cls) -> list:
        """Get all known values (defaults + dynamic from API)"""
        defaults = cls.get_defaults()
        return list(set(defaults) | cls._known_values)

    @classmethod
    def get_defaults(cls) -> list:
        """Get default values (to be overridden)"""
        return []


class TextModel(DynamicModel):
    """
    Text generation models
    Fixed version that properly fetches from API
    """

    # Constants for IDE autocomplete
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    MISTRAL = "mistral"
    QWEN_CODER = "qwen-coder"
    CLAUDYCLAUDE = "claudyclaude"
    OPENAI_FAST = "openai-fast"
    OPENAI_LARGE = "openai-large"
    GEMINI_SEARCH = "gemini-search"
    PERPLEXITY_FAST = "perplexity-fast"
    PERPLEXITY_REASONING = "perplexity-reasoning"

    @classmethod
    def get_defaults(cls) -> list:
        return [
            "deepseek", "gemini", "mistral", "openai", "qwen-coder",
            "claudyclaude", "openai-fast", "openai-large", "gemini-search",
            "perplexity-fast", "perplexity-reasoning"
        ]


class ImageModel(DynamicModel):
    """Image generation models"""

    FLUX = "flux"
    KONTEXT = "kontext"
    TURBO = "turbo"
    GPTIMAGE = "gptimage"
    NANOBANANA = "nanobanana"
    SEEDREAM = "seedream"

    @classmethod
    def get_defaults(cls) -> list:
        return ["flux", "kontext", "turbo", "gptimage", "nanobanana", "seedream"]


class Voice(DynamicModel):
    """Text-to-speech voices"""

    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"

    @classmethod
    def get_defaults(cls) -> list:
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


# Fallback lists (extended with all known models)
DEFAULT_IMAGE_MODELS = ImageModel.get_defaults()
DEFAULT_TEXT_MODELS = TextModel.get_defaults()
DEFAULT_VOICES = Voice.get_defaults()