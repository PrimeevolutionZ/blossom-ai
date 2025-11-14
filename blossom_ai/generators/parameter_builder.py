"""
Blossom AI – Parameter Builders (v0.5.0-refactored)
Type-safe, single-source builders for V2 API.

"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field, asdict
from mimetypes import guess_type
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from blossom_ai.core.config import DEFAULTS
from blossom_ai.core.errors import BlossomError, ErrorType

# --------------------------------------------------------------------------- #
# Low-level helpers
# --------------------------------------------------------------------------- #
def _b64_from_path(path: Path) -> str:
    """Read file and return base64 data-URI."""
    if not path.exists():
        raise FileNotFoundError(path)
    mime, _ = guess_type(path.name)
    mime = mime or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _drop_defaults(data: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Return dict without keys whose values == defaults."""
    return {k: v for k, v in data.items() if k not in defaults or v != defaults[k]}


# --------------------------------------------------------------------------- #
# Base – immutable + safe repr
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class BaseParams:
    """Frozen base – no accidental mutation, safe repr()."""

    def to_dict(
        self, *, include_none: bool = False, include_defaults: bool = False
    ) -> Dict[str, Any]:
        """Convert to dict, filter None and defaults unless requested."""
        raw = asdict(self)
        if not include_none:
            raw = {k: v for k, v in raw.items() if v is not None}
        if not include_defaults:
            raw = _drop_defaults(raw, self._default_map())
        return raw

    def _default_map(self) -> Dict[str, Any]:
        """Override in subclass – return flat {field: default_value}."""
        return {}

    def __repr__(self) -> str:  # hide potential secrets
        klass = self.__class__.__name__
        public = self.to_dict()
        return f"{klass}({', '.join(f'{k}=*' for k in public)})"


# --------------------------------------------------------------------------- #
# Image
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class ImageParamsV2(BaseParams):
    """V2 image generation parameters – only fields that exist on wire."""

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

    # strict defaults map
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


# --------------------------------------------------------------------------- #
# Audio
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class AudioParamsV2(BaseParams):
    """Audio generation / input parameters."""

    model: str = "openai"
    voice: Optional[str] = None
    modalities: List[str] = field(default_factory=lambda: ["text"])
    audio: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        # normalise to lower-case unique list
        object.__setattr__(self, "modalities", list({m.lower() for m in self.modalities}))

    def _default_map(self) -> Dict[str, Any]:
        return {"model": "openai", "modalities": ["text"]}


# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class ChatParamsV2(BaseParams):
    """OpenAI-compatible chat completion + vision/audio/reasoning."""

    model: str = DEFAULTS.TEXT_MODEL
    messages: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    stream: bool = False
    json_mode: bool = False
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    frequency_penalty: float = 0
    presence_penalty: float = 0
    top_p: float = 1.0
    n: int = 1
    thinking: Optional[Dict[str, Any]] = None
    modalities: Optional[List[str]] = None
    audio: Optional[Dict[str, Any]] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.modalities is not None:
            object.__setattr__(self, "modalities", list({m.lower() for m in self.modalities}))

    # ---------- wire body builder ----------
    def to_body(self) -> Dict[str, Any]:
        """Build JSON body for POST /generate/v1/chat/completions ."""
        defaults = self._default_map()
        body = self.to_dict(include_defaults=False)

        # inject response_format when json_mode
        if self.json_mode and "response_format" not in body:
            body["response_format"] = {"type": "json_object"}

        # stream_options for usage stats
        if self.stream:
            body["stream_options"] = {"include_usage": True}

        # merge extra_params last, skip None / zeros / False
        for k, v in self.extra_params.items():
            if v is None or v == 0 or v is False:
                continue
            body[k] = v

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
# Message helpers – secrets safe
# --------------------------------------------------------------------------- #
class MessageBuilder:
    """Factory for OpenAI-style messages (text, image, audio)."""

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
        """Build vision message. One image source required."""
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
        """Build audio-input message. One audio source required."""
        if not (audio_url or audio_path or audio_data):
            raise ValueError("One audio source required")

        content: List[Dict[str, Any]] = []
        if text:
            content.append({"type": "text", "text": text})

        if audio_url:
            content.append({"type": "input_audio", "input_audio": {"url": audio_url, "format": format}})
        elif audio_path:
            uri = _b64_from_path(Path(audio_path))
            content.append({"type": "input_audio", "input_audio": {"url": uri, "format": format}})
        else:  # audio_data
            b64 = base64.b64encode(audio_data).decode()
            content.append({"type": "input_audio", "input_audio": {"data": b64, "format": format}})

        return {"role": role, "content": content}


# --------------------------------------------------------------------------- #
# Validators – pure functions, no side effects
# --------------------------------------------------------------------------- #
class ParameterValidator:
    """Pure validators – raise BlossomError on failure."""

    VALID_MODALITIES = {"text", "audio", "image"}
    VALID_AUDIO_FMT = {"wav", "mp3", "pcm16", "g711_ulaw", "g711_alaw"}

    @staticmethod
    def prompt_length(prompt: str, max_len: int, name: str = "prompt") -> None:
        if len(prompt) > max_len:
            raise BlossomError(
                message=f"{name} exceeds {max_len} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Shorten the {name}.",
            )

    @staticmethod
    def dimensions(width: int, height: int, *, min_: int = 64, max_: int = 2048) -> None:
        if not (min_ <= width <= max_ and min_ <= height <= max_):
            raise BlossomError(
                message=f"Dimensions must be within [{min_}..{max_}]",
                error_type=ErrorType.INVALID_PARAM,
            )

    @staticmethod
    def temperature(value: float) -> None:
        if not (0 <= value <= 2):
            raise BlossomError(
                message="Temperature must be in [0..2]",
                error_type=ErrorType.INVALID_PARAM,
            )

    @staticmethod
    def modalities(values: List[str]) -> None:
        extra = set(values) - ParameterValidator.VALID_MODALITIES
        if extra:
            raise BlossomError(
                message=f"Invalid modalities: {extra}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Choose from {ParameterValidator.VALID_MODALITIES}",
            )

    @staticmethod
    def audio_format(fmt: str) -> None:
        if fmt.lower() not in ParameterValidator.VALID_AUDIO_FMT:
            raise BlossomError(
                message=f"Unsupported audio format {fmt}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Use one of {ParameterValidator.VALID_AUDIO_FMT}",
            )