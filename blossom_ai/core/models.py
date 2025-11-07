"""
Blossom AI - Models and Enums
"""

from typing import Set, Optional, List, ClassVar, Type
from abc import ABC, abstractmethod
import threading
import time
from dataclasses import dataclass

from .config import ENDPOINTS
from .session_manager import SyncSessionManager
from .errors import print_warning, print_debug


@dataclass(frozen=True)
class ModelInfo:
    """Structured model information from API"""
    name: str
    aliases: List[str]
    description: Optional[str] = None
    tier: Optional[str] = None

    @property
    def all_identifiers(self) -> Set[str]:
        """Get all valid identifiers (name + aliases)"""
        return {self.name, *self.aliases}


class DynamicModel(ABC):
    """
    Base class for dynamic model names with TTL cache
    """

    # Class-level state
    _known_values: ClassVar[Set[str]] = set()
    _model_info: ClassVar[List[ModelInfo]] = []
    _initialized: ClassVar[bool] = False
    _init_lock: ClassVar[threading.Lock] = threading.Lock()

    # Cache TTL
    _cache_timestamp: ClassVar[float] = 0
    _cache_ttl: ClassVar[int] = 300  # 5 minutes

    @classmethod
    @abstractmethod
    def get_defaults(cls) -> List[str]:
        """Get default model names"""
        pass

    @classmethod
    @abstractmethod
    def get_api_endpoints(cls) -> List[str]:
        """Get API endpoints to fetch models from"""
        pass

    @classmethod
    def _is_cache_valid(cls) -> bool:
        """Check if cache is still valid (within TTL)"""
        if not cls._initialized:
            return False
        return (time.time() - cls._cache_timestamp) < cls._cache_ttl

    @classmethod
    def _fetch_models_from_endpoint(
        cls,
        endpoint: str,
        api_token: Optional[str] = None,
        timeout: int = 5  # Reduced timeout
    ) -> List[ModelInfo]:
        """
        Fetch models from a single endpoint with timeout
        """
        try:
            with SyncSessionManager() as session_manager:
                session = session_manager.get_session()

                headers = {}
                if api_token:
                    headers['Authorization'] = f'Bearer {api_token}'

                response = session.get(
                    endpoint,
                    headers=headers,
                    timeout=timeout,
                    verify=True
                )

                # Don't crash on HTTP errors
                if response.status_code != 200:
                    print_debug(f"API returned {response.status_code} from {endpoint}")
                    return []

                data = response.json()
                return cls._parse_api_response(data)

        except Exception as e:
            print_debug(f"Failed to fetch from {endpoint}: {type(e).__name__}: {e}")
            return []

    @classmethod
    def _parse_api_response(cls, data: any) -> List[ModelInfo]:
        """Parse API response into structured ModelInfo objects"""
        models = []

        if not isinstance(data, list):
            return models

        for item in data:
            try:
                if isinstance(item, str):
                    models.append(ModelInfo(name=item, aliases=[]))

                elif isinstance(item, dict):
                    name = item.get('name') or item.get('id') or item.get('model')
                    if not name:
                        continue

                    aliases = item.get('aliases', [])
                    if not isinstance(aliases, list):
                        aliases = []

                    models.append(ModelInfo(
                        name=name,
                        aliases=aliases,
                        description=item.get('description'),
                        tier=item.get('tier')
                    ))
            except Exception as e:
                # Skip malformed items
                print_debug(f"Skipping malformed model item: {e}")
                continue

        return models

    @classmethod
    def initialize_from_api(
        cls,
        api_token: Optional[str] = None,
        force_refresh: bool = False
    ) -> bool:
        """
        Initialize known values from API (lazy, with TTL)
        Returns:
            True if successfully fetched from API, False if using fallback
        """
        # FIX: Fast path - cache is still valid
        if not force_refresh and cls._is_cache_valid():
            return True

        # Thread-safe initialization
        with cls._init_lock:
            # Double-check after acquiring lock
            if not force_refresh and cls._is_cache_valid():
                return True

            # Always start with defaults
            cls._known_values.update(cls.get_defaults())

            try:
                endpoints = cls.get_api_endpoints()
                all_models = []

                # Fetch from all endpoints
                for endpoint in endpoints:
                    models = cls._fetch_models_from_endpoint(endpoint, api_token)
                    all_models.extend(models)

                if all_models:
                    # Store structured info
                    cls._model_info = all_models

                    # Update known values with all identifiers
                    for model in all_models:
                        cls._known_values.update(model.all_identifiers)

                    cls._cache_timestamp = time.time()
                    cls._initialized = True

                    print_debug(
                        f"Initialized {cls.__name__} with {len(all_models)} models "
                        f"from API (TTL: {cls._cache_ttl}s)"
                    )
                    return True
                else:
                    # FIX: Still mark as initialized to prevent retry storms
                    cls._cache_timestamp = time.time()
                    cls._initialized = True
                    print_warning(f"Using fallback defaults for {cls.__name__}")
                    return False

            except Exception as e:
                # Never crash, always have defaults
                print_warning(f"Failed to initialize {cls.__name__}: {e}")
                cls._cache_timestamp = time.time()
                cls._initialized = True
                return False

    @classmethod
    def from_string(cls, value: str) -> str:
        """
        Validate and register a model name
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid model name: {value}")

        if not cls._initialized:
            cls.initialize_from_api()

        # Add to known values (allows custom models)
        cls._known_values.add(value)
        return value

    @classmethod
    def get_all_known(cls) -> List[str]:
        """Get all known model identifiers"""
        if not cls._initialized:
            cls.initialize_from_api()

        defaults = set(cls.get_defaults())
        return sorted(defaults | cls._known_values)

    @classmethod
    def get_model_info(cls, name: str) -> Optional[ModelInfo]:
        """Get structured info for a specific model"""
        if not cls._initialized:
            cls.initialize_from_api()

        for model in cls._model_info:
            if name in model.all_identifiers:
                return model
        return None

    @classmethod
    def is_known(cls, name: str) -> bool:
        """Check if a model name is known"""
        if not cls._initialized:
            cls.initialize_from_api()
        return name in cls._known_values or name in cls.get_defaults()

    @classmethod
    def reset(cls):
        """Reset initialization state (useful for testing)"""
        with cls._init_lock:
            cls._known_values.clear()
            cls._model_info.clear()
            cls._initialized = False
            cls._cache_timestamp = 0


class TextModel(DynamicModel):
    """Text generation models with OpenAI-compatible API"""

    # Primary models
    OPENAI = "openai"
    OPENAI_FAST = "openai-fast"
    OPENAI_LARGE = "openai-large"
    OPENAI_REASONING = "openai-reasoning"

    # Alternative providers
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    GEMINI_SEARCH = "gemini-search"
    MISTRAL = "mistral"
    CLAUDE = "claude"

    # Specialized models
    QWEN_CODER = "qwen-coder"
    PERPLEXITY_FAST = "perplexity-fast"
    PERPLEXITY_REASONING = "perplexity-reasoning"

    # Community/experimental
    UNITY = "unity"
    EVIL = "evil"
    NAUGHTY = "naughty"
    CHICKYTUTOR = "chickytutor"
    MIDIJOURNEY = "midijourney"

    @classmethod
    def get_defaults(cls) -> List[str]:
        """Default text models"""
        return [
            "openai", "openai-fast", "openai-large", "openai-reasoning",
            "deepseek", "gemini", "gemini-search", "mistral", "claude",
            "qwen-coder", "perplexity-fast", "perplexity-reasoning",
            "unity", "evil", "naughty", "chickytutor", "midijourney"
        ]

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        """Endpoints to fetch text models from"""
        return [ENDPOINTS.V2_TEXT_MODELS]


class ImageModel(DynamicModel):
    """Image generation models"""

    FLUX = "flux"
    TURBO = "turbo"
    GPTIMAGE = "gptimage"
    SEEDREAM = "seedream"
    KONTEXT = "kontext"
    NANOBANANA = "nanobanana"

    @classmethod
    def get_defaults(cls) -> List[str]:
        """Default image models"""
        return [
            "flux", "turbo", "gptimage",
            "seedream", "kontext", "nanobanana"
        ]

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        """Endpoints to fetch image models from"""
        return [ENDPOINTS.V2_IMAGE_MODELS]


class Voice(DynamicModel):
    """Text-to-speech voices"""

    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"

    @classmethod
    def get_defaults(cls) -> List[str]:
        """Default TTS voices"""
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        """Voices are typically hardcoded, not fetched from API"""
        return []


# Convenience lists
DEFAULT_TEXT_MODELS = TextModel.get_defaults()
DEFAULT_IMAGE_MODELS = ImageModel.get_defaults()
DEFAULT_VOICES = Voice.get_defaults()