"""
Blossom AI – Models and Enums (v0.5.4)
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from typing import List, Optional, Set, NamedTuple, Final

from blossom_ai.core.config import ENDPOINTS
from blossom_ai.core.session_manager import get_sync_session, get_async_session

logger = logging.getLogger("blossom_ai")

# --------------------------------------------------------------------------- #
# Model info
# --------------------------------------------------------------------------- #

class ModelInfo(NamedTuple):
    name: str
    aliases: List[str]
    description: Optional[str] = None
    tier: Optional[str] = None

    @property
    def all_identifiers(self) -> Set[str]:
        return {self.name, *self.aliases}

# --------------------------------------------------------------------------- #
# Cache layer
# --------------------------------------------------------------------------- #

class _ModelCache:
    __slots__ = ("known", "info", "initialized", "timestamp", "lock")
    ttl: Final = 300  # 5 min

    def __init__(self) -> None:
        self.known: Set[str] = set()
        self.info: List[ModelInfo] = []
        self.initialized = False
        self.timestamp = 0.0
        self.lock = threading.Lock()

    def is_valid(self) -> bool:
        return self.initialized and (time.time() - self.timestamp) < self.ttl

    def reset(self) -> None:
        with self.lock:
            self.known.clear()
            self.info.clear()
            self.initialized = False
            self.timestamp = 0.0

# --------------------------------------------------------------------------- #
# Base dynamic model
# --------------------------------------------------------------------------- #

class DynamicModel:
    _cache = _ModelCache()

    @classmethod
    def get_defaults(cls) -> List[str]:
        raise NotImplementedError

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        raise NotImplementedError

    # ---------- sync fetch ----------
    @classmethod
    def _fetch_models(cls, endpoint: str, api_token: Optional[str] = None) -> List[ModelInfo]:
        try:
            with get_sync_session() as session:
                headers = {}
                if api_token:
                    headers["Authorization"] = f"Bearer {api_token}"
                resp = session.get(endpoint, headers=headers, timeout=5)
                if resp.status_code != 200:
                    logger.debug("API %s returned %s", endpoint, resp.status_code)
                    return []
                return cls._parse(resp.json())
        except Exception as exc:
            logger.debug("Failed to fetch from %s: %s", endpoint, exc)
            return []

    # ---------- async fetch ----------
    @classmethod
    async def _afetch_models(cls, endpoint: str, api_token: Optional[str] = None) -> List[ModelInfo]:
        try:
            async with get_async_session() as session:
                headers = {}
                if api_token:
                    headers["Authorization"] = f"Bearer {api_token}"
                async with session.get(endpoint, headers=headers, timeout=5) as resp:
                    if resp.status != 200:
                        logger.debug("API %s returned %s", endpoint, resp.status)
                        return []
                    data = await resp.json()
                    return cls._parse(data)
        except Exception as exc:
            logger.debug("Async fetch failed from %s: %s", endpoint, exc)
            return []

    # ---------- parse ----------
    @staticmethod
    def _parse(data: list) -> List[ModelInfo]:
        models: List[ModelInfo] = []
        for item in data:
            try:
                if isinstance(item, str):
                    models.append(ModelInfo(name=item, aliases=[]))
                elif isinstance(item, dict):
                    name = item.get("name") or item.get("id") or item.get("model")
                    if not name:
                        continue
                    aliases = item.get("aliases", [])
                    if not isinstance(aliases, list):
                        aliases = []
                    models.append(ModelInfo(
                        name=name,
                        aliases=aliases,
                        description=item.get("description"),
                        tier=item.get("tier"),
                    ))
            except Exception as e:
                logger.debug("Skipping malformed model item: %s", e)
        return models

    # ---------- initialization ----------
    @classmethod
    def _ensure_initialized(cls, api_token: Optional[str] = None, force: bool = False) -> bool:
        cache = cls._cache
        if not force and cache.is_valid():
            return True
        with cache.lock:
            if not force and cache.is_valid():
                return True
            cache.known.update(cls.get_defaults())
            endpoints = cls.get_api_endpoints()
            all_models: List[ModelInfo] = []
            for ep in endpoints:
                all_models.extend(cls._fetch_models(ep, api_token))
            if all_models:
                cache.info = all_models
                for m in all_models:
                    cache.known.update(m.all_identifiers)
                cache.timestamp = time.time()
                cache.initialized = True
                logger.debug("Initialized %s with %s models", cls.__name__, len(all_models))
                return True
            else:
                cache.timestamp = time.time()
                cache.initialized = True
                logger.warning("Using fallback defaults for %s", cls.__name__)
                return False

    @classmethod
    async def _aensure_initialized(cls, api_token: Optional[str] = None, force: bool = False) -> bool:
        cache = cls._cache
        if not force and cache.is_valid():
            return True
        # для async-ветки всё равно берём тот же тред-безопасный кеш
        # но запросы делаем асинхронно
        with cache.lock:
            if not force and cache.is_valid():
                return True
            cache.known.update(cls.get_defaults())
            endpoints = cls.get_api_endpoints()
            all_models: List[ModelInfo] = []
            for ep in endpoints:
                all_models.extend(await cls._afetch_models(ep, api_token))
            if all_models:
                cache.info = all_models
                for m in all_models:
                    cache.known.update(m.all_identifiers)
                cache.timestamp = time.time()
                cache.initialized = True
                logger.debug("Async initialized %s with %s models", cls.__name__, len(all_models))
                return True
            else:
                cache.timestamp = time.time()
                cache.initialized = True
                logger.warning("Async using fallback defaults for %s", cls.__name__)
                return False

    # ---------- public ----------
    @classmethod
    def from_string(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Model name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Model name cannot be empty or whitespace")
        cls._ensure_initialized()
        cls._cache.known.add(value)
        return value

    @classmethod
    async def afrom_string(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Model name must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Model name cannot be empty or whitespace")
        await cls._aensure_initialized()
        cls._cache.known.add(value)
        return value

    @classmethod
    def get_all_known(cls) -> List[str]:
        cls._ensure_initialized()
        return sorted(cls.get_defaults() + list(cls._cache.known))

    @classmethod
    async def aget_all_known(cls) -> List[str]:
        await cls._aensure_initialized()
        return sorted(cls.get_defaults() + list(cls._cache.known))

    @classmethod
    def get_model_info(cls, name: str) -> Optional[ModelInfo]:
        cls._ensure_initialized()
        for m in cls._cache.info:
            if name in m.all_identifiers:
                return m
        return None

    @classmethod
    async def aget_model_info(cls, name: str) -> Optional[ModelInfo]:
        await cls._aensure_initialized()
        for m in cls._cache.info:
            if name in m.all_identifiers:
                return m
        return None

    @classmethod
    def is_known(cls, name: str) -> bool:
        cls._ensure_initialized()
        return name in cls._cache.known or name in cls.get_defaults()

    @classmethod
    async def ais_known(cls, name: str) -> bool:
        await cls._aensure_initialized()
        return name in cls._cache.known or name in cls.get_defaults()

    @classmethod
    def reset(cls) -> None:
        cls._cache.reset()

# --------------------------------------------------------------------------- #
# Concrete models
# --------------------------------------------------------------------------- #

class TextModel(DynamicModel):
    @classmethod
    def get_defaults(cls) -> List[str]:
        return [
            "openai", "openai-fast", "openai-large", "openai-reasoning",
            "deepseek", "gemini", "gemini-search", "mistral", "mistral-fast",
            "claude", "claude-large", "qwen-coder", "grok",
            "perplexity-fast", "perplexity-reasoning", "searchgpt",
            "naughty", "chickytutor", "midijourney",
        ]

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        return [ENDPOINTS.TEXT_MODELS]

class ImageModel(DynamicModel):
    @classmethod
    def get_defaults(cls) -> List[str]:
        return ["flux", "turbo", "gptimage", "seedream", "kontext", "nanobanana"]

    @classmethod
    def get_api_endpoints(cls) -> List[str]:
        return [ENDPOINTS.IMAGE_MODELS]

# --------------------------------------------------------------------------- #
# Convenience lists (kept for compat)
# --------------------------------------------------------------------------- #

DEFAULT_TEXT_MODELS: Final = TextModel.get_defaults()
DEFAULT_IMAGE_MODELS: Final = ImageModel.get_defaults()