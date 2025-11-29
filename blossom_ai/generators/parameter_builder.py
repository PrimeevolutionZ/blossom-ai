"""
Blossom AI – Parameter Builders (v0.5.4)
Frozen + __slots__, single source of validators.
"""

from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Final

from blossom_ai.core.config import DEFAULTS, LIMITS, AUDIO, REASONING
from blossom_ai.core.errors import BlossomError, ErrorType

# --------------------------------------------------------------------------- #
# Low-level helpers
# --------------------------------------------------------------------------- #

def _b64_from_path(path: Path) -> str:
    """Return data-URI for file."""
    if not path.exists():
        raise FileNotFoundError(path)
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()

def _drop_defaults(data: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Return dict without keys whose values == defaults."""
    return {k: v for k, v in data.items() if k not in defaults or v != defaults[k]}

# --------------------------------------------------------------------------- #
# Validator namespace – single source of truth
# --------------------------------------------------------------------------- #

class _Validators:
    __slots__ = ()

    @staticmethod
    def positive_int(value: int, name: str) -> int:
        if value <= 0:
            raise BlossomError(f"{name} must be positive", ErrorType.INVALID_PARAM)
        return value

    @staticmethod
    def range_check(value: float, low: float, high: float, name: str) -> float:
        if not (low <= value <= high):
            raise BlossomError(f"{name} must be in [{low}, {high}]", ErrorType.INVALID_PARAM)
        return value

    @staticmethod
    def choice(value: str, choices: tuple[str, ...], name: str) -> str:
        if value not in choices:
            raise BlossomError(
                f"Invalid {name}: {value}",
                ErrorType.INVALID_PARAM,
                suggestion=f"Choose from: {', '.join(choices)}",
            )
        return value

    @staticmethod
    def prompt_length(prompt: str, max_len: int, name: str = "prompt") -> None:
        if len(prompt) > max_len:
            raise BlossomError(
                f"{name} exceeds {max_len:,} characters",
                ErrorType.INVALID_PARAM,
                suggestion=f"Shorten the {name} or use read_file_truncated().",
            )

    @staticmethod
    def dimensions(width: int, height: int, *, min_: int = 64, max_: int = 2048) -> None:
        if not (min_ <= width <= max_ and min_ <= height <= max_):
            raise BlossomError(
                f"Dimensions must be within [{min_}..{max_}]",
                ErrorType.INVALID_PARAM,
            )

    @staticmethod
    def audio_voice(voice: str) -> str:
        return _Validators.choice(voice, AUDIO.VOICES, "voice")

    @staticmethod
    def audio_format(fmt: str) -> str:
        return _Validators.choice(fmt.lower(), AUDIO.FORMATS, "audio format")

    @staticmethod
    def reasoning_effort(effort: str) -> str:
        return _Validators.choice(effort, REASONING.EFFORTS, "reasoning effort")

# --------------------------------------------------------------------------- #
# Base frozen parameter block
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class BaseParams:
    """Immutable base – safe repr, no accidental mutation."""

    def to_dict(self, *, include_none: bool = False, include_defaults: bool = False) -> Dict[str, Any]:
        raw = asdict(self)
        if not include_none:
            raw = {k: v for k, v in raw.items() if v is not None}
        if not include_defaults:
            raw = _drop_defaults(raw, self._default_map())
        return raw

    def _default_map(self) -> Dict[str, Any]:
        """Override in subclass: {field: default_value}."""
        return {}

    def __repr__(self) -> str:
        klass = self.__class__.__name__
        public = self.to_dict()
        return f"{klass}({', '.join(f'{k}=*' for k in public)})"

# --------------------------------------------------------------------------- #
# Image
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class ImageParamsV2(BaseParams):
    model: str = DEFAULTS.IMAGE_MODEL
    width: int = DEFAULTS.IMAGE_WIDTH
    height: int = DEFAULTS.IMAGE_HEIGHT
    seed: int = 42
    enhance: bool = False
    negative_prompt: str = DEFAULTS.IMAGE_NEGATIVE_PROMPT
    private: bool = False
    nologo: bool = False
    nofeed: bool = False
    safe: bool = False
    quality: str = DEFAULTS.IMAGE_QUALITY
    image: Optional[str] = None  # img2img URL
    transparent: bool = False
    guidance_scale: Optional[float] = None

    def __post_init__(self) -> None:
        _Validators.positive_int(self.width, "width")
        _Validators.positive_int(self.height, "height")
        _Validators.prompt_length(self.negative_prompt, LIMITS.MAX_IMAGE_PROMPT_LENGTH, "negative_prompt")

    def _default_map(self) -> Dict[str, Any]:
        return {
            "model": DEFAULTS.IMAGE_MODEL,
            "width": DEFAULTS.IMAGE_WIDTH,
            "height": DEFAULTS.IMAGE_HEIGHT,
            "seed": 42,
            "enhance": False,
            "negative_prompt": DEFAULTS.IMAGE_NEGATIVE_PROMPT,
            "private": False,
            "nologo": False,
            "nofeed": False,
            "safe": False,
            "quality": DEFAULTS.IMAGE_QUALITY,
            "transparent": False,
        }

    def to_query(self) -> str:
        """Return query-string fragment."""
        from urllib.parse import urlencode
        return urlencode(self.to_dict())

# --------------------------------------------------------------------------- #
# Audio
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class AudioParamsV2(BaseParams):
    voice: Optional[str] = None
    format: str = AUDIO.DEFAULT_FORMAT  # wav, mp3, flac, opus, pcm16

    def __post_init__(self) -> None:
        if self.voice is not None:
            _Validators.audio_voice(self.voice)
        _Validators.audio_format(self.format)

    def _default_map(self) -> Dict[str, Any]:
        return {"format": AUDIO.DEFAULT_FORMAT}

# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #

@dataclass(frozen=True, slots=True)
class ChatParamsV2(BaseParams):
    model: str = DEFAULTS.TEXT_MODEL
    messages: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    stream: bool = False
    json_mode: bool = False
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Dict[str, Any] | str] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    top_p: float = 1.0
    n: int = 1
    reasoning_effort: Optional[str] = None
    thinking_budget: Optional[int] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _Validators.range_check(self.temperature, 0.0, 2.0, "temperature")
        _Validators.range_check(self.top_p, 0.0, 1.0, "top_p")
        if self.reasoning_effort is not None:
            _Validators.reasoning_effort(self.reasoning_effort)
        if self.max_tokens is not None:
            _Validators.positive_int(self.max_tokens, "max_tokens")

    # ---------- wire body ----------
    def to_body(self) -> Dict[str, Any]:
        body = self.to_dict(include_defaults=False)

        if "model" not in body:
            body["model"] = self.model

        if self.json_mode and "response_format" not in body:
            body["response_format"] = {"type": "json_object"}

        if self.stream:
            body["stream_options"] = {"include_usage": True}

        # drop internal keys
        body.pop("json_mode", None)
        body.pop("extra_params", None)

        # merge extra_params last
        for k, v in self.extra_params.items():
            if v is None or v == 0 or v is False:
                continue
            body[k] = v

        # rough length check
        total_chars = sum(len(str(msg.get("content", ""))) for msg in self.messages)
        if total_chars > LIMITS.MAX_TEXT_PROMPT_LENGTH:
            raise BlossomError(
                f"Total message length ({total_chars:,}) exceeds limit ({LIMITS.MAX_TEXT_PROMPT_LENGTH:,})",
                ErrorType.INVALID_PARAM,
                suggestion="Shorten prompt or split into multiple requests.",
            )
        return body

    def _default_map(self) -> Dict[str, Any]:
        return {
            "model": DEFAULTS.TEXT_MODEL,
            "temperature": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "top_p": 1.0,
            "n": 1,
            "stream": False,
            "json_mode": False,
        }

# --------------------------------------------------------------------------- #
# Message helpers
# --------------------------------------------------------------------------- #

class MessageBuilder:
    __slots__ = ()

    @staticmethod
    def text(role: str, content: str, name: Optional[str] = None) -> Dict[str, Any]:
        msg = {"role": role, "content": content}
        if name:
            msg["name"] = name
        return msg

    @staticmethod
    def image(
        role: str,
        text: str,
        *,
        image_url: Optional[str] = None,
        image_path: Optional[Path | str] = None,
        image_data: Optional[bytes] = None,
        detail: str = "auto",
    ) -> Dict[str, Any]:
        if not (image_url or image_path or image_data):
            raise ValueError("One image source required")
        content: List[Dict[str, Any]] = [{"type": "text", "text": text}]
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url, "detail": detail}})
        elif image_path:
            uri = _b64_from_path(Path(image_path))
            content.append({"type": "image_url", "image_url": {"url": uri, "detail": detail}})
        else:  # image_data
            uri = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
            content.append({"type": "image_url", "image_url": {"url": uri, "detail": detail}})
        return {"role": role, "content": content}

    @staticmethod
    def audio(
        role: str,
        text: Optional[str] = None,
        *,
        audio_url: Optional[str] = None,
        audio_path: Optional[Path | str] = None,
        audio_data: Optional[bytes] = None,
        format: str = "wav",
    ) -> Dict[str, Any]:
        raise NotImplementedError(
            "Audio input in chat messages is not supported by Pollinations API. "
            "Use ai.audio.generate(text, voice='alloy') for TTS."
        )