"""
Blossom AI - Parameter Builders (v0.5.0)
Type-safe parameter construction for V2 API
"""

from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field, asdict
import base64
from pathlib import Path

from blossom_ai.core.config import DEFAULTS


# ============================================================================
# BASE PARAMETER BUILDER
# ============================================================================

@dataclass
class BaseParams:
    """Base class for API parameters"""

    def to_dict(self, include_none: bool = False, include_defaults: bool = False) -> Dict[str, Any]:
        """
        Convert to dictionary, filtering None and default values

        Args:
            include_none: Include None values
            include_defaults: Include default values

        Returns:
            Dictionary of parameters
        """
        result = {}

        for key, value in asdict(self).items():
            # Skip None values unless explicitly included
            if value is None and not include_none:
                continue

            # Skip default values unless explicitly included
            if not include_defaults and self._is_default_value(key, value):
                continue

            # Keep booleans as-is (V2 API expects true/false, not "true"/"false")
            result[key] = value

        return result

    def _is_default_value(self, key: str, value: Any) -> bool:
        """Check if value is default for this parameter"""
        # Override in subclasses for specific default checking
        return False


# ============================================================================
# IMAGE PARAMETERS (V2)
# ============================================================================

@dataclass
class ImageParamsV2(BaseParams):
    """Parameters for V2 image generation with extended features"""

    model: str = DEFAULTS.IMAGE_MODEL
    width: int = DEFAULTS.IMAGE_WIDTH
    height: int = DEFAULTS.IMAGE_HEIGHT
    seed: int = 42
    enhance: bool = False
    negative_prompt: str = "worst quality, blurry"
    private: bool = False
    nologo: bool = False
    nofeed: bool = False
    safe: bool = False
    quality: str = "medium"
    image: Optional[str] = None
    transparent: bool = False
    guidance_scale: Optional[float] = None

    def to_dict(self, include_none: bool = False, include_defaults: bool = False) -> Dict[str, Any]:
        """
        V2 API needs proper types, NOT string conversion
        The API expects: ?nologo=true (boolean), not ?nologo="true" (string)
        """
        result = {}

        for key, value in asdict(self).items():
            if value is None and not include_none:
                continue

            if not include_defaults and self._is_default_value(key, value):
                continue

            # Keep booleans as actual booleans for V2 API
            # requests library will convert them correctly in URL params
            result[key] = value

        return result

    def _is_default_value(self, key: str, value: Any) -> bool:
        """Check if value matches default"""
        defaults = {
            'model': DEFAULTS.IMAGE_MODEL,
            'width': DEFAULTS.IMAGE_WIDTH,
            'height': DEFAULTS.IMAGE_HEIGHT,
            'seed': 42,
            'enhance': False,
            'negative_prompt': "worst quality, blurry",
            'private': False,
            'nologo': False,
            'nofeed': False,
            'safe': False,
            'quality': "medium",
            'transparent': False,
        }
        return key in defaults and value == defaults[key]


# ============================================================================
# AUDIO PARAMETERS (NEW)
# ============================================================================

@dataclass
class AudioParamsV2(BaseParams):
    """Parameters for V2 audio generation"""

    model: str = "openai"
    voice: Optional[str] = None  # Voice ID for audio output
    modalities: List[str] = field(default_factory=lambda: ["text"])  # text, audio
    audio: Optional[Dict[str, Any]] = None  # Audio input config

    def to_dict(self, include_none: bool = False, include_defaults: bool = False) -> Dict[str, Any]:
        """Convert to dict for API request"""
        result = super().to_dict(include_none, include_defaults)

        # Ensure modalities is a list
        if "modalities" in result and not isinstance(result["modalities"], list):
            result["modalities"] = [result["modalities"]]

        return result


# ============================================================================
# CHAT PARAMETERS (V2) - UPDATED WITH VISION & AUDIO
# ============================================================================

@dataclass
class ChatParamsV2(BaseParams):
    """Parameters for V2 chat completion with vision, audio, and extended OpenAI features"""

    model: str = DEFAULTS.TEXT_MODEL
    messages: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    stream: bool = False
    json_mode: bool = False
    tools: Optional[List[Dict]] = None
    tool_choice: Optional[Union[str, Dict]] = None
    frequency_penalty: float = 0
    presence_penalty: float = 0
    top_p: float = 1.0
    n: int = 1
    thinking: Optional[Dict[str, Any]] = None

    # NEW: Audio/Vision support
    modalities: Optional[List[str]] = None  # ["text", "audio"]
    audio: Optional[Dict[str, Any]] = None  # Audio output config with voice

    # Additional kwargs stored here
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_body(self) -> Dict[str, Any]:
        """Convert to request body with smart defaults"""
        body = {
            'model': self.model,
            'messages': self.messages,
            'stream': self.stream,
        }

        # Only add non-default values
        if self.temperature != 1.0:
            body['temperature'] = self.temperature
        if self.max_tokens is not None:
            body['max_tokens'] = self.max_tokens
        if self.n != 1:
            body['n'] = self.n
        if self.top_p != 1.0:
            body['top_p'] = self.top_p
        if self.frequency_penalty != 0:
            body['frequency_penalty'] = self.frequency_penalty
        if self.presence_penalty != 0:
            body['presence_penalty'] = self.presence_penalty

        # JSON mode
        if self.json_mode:
            body['response_format'] = {'type': 'json_object'}

        # Tools
        if self.tools:
            body['tools'] = self.tools
            if self.tool_choice:
                body['tool_choice'] = self.tool_choice

        # Native reasoning
        if self.thinking:
            body['thinking'] = self.thinking

        # NEW: Modalities (for audio/vision)
        if self.modalities:
            body['modalities'] = self.modalities

        # NEW: Audio output config
        if self.audio:
            body['audio'] = self.audio

        # Stream options for better streaming
        if self.stream:
            body['stream_options'] = {'include_usage': True}

        # Add extra params (filtering out defaults)
        for key, value in self.extra_params.items():
            if value is not None and value != 0 and value is not False and value != 1.0:
                body[key] = value

        return body


# ============================================================================
# MESSAGE BUILDERS (NEW)
# ============================================================================

class MessageBuilder:
    """Helper for building messages with images, audio, etc."""

    @staticmethod
    def text_message(role: str, content: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Create a simple text message"""
        msg = {"role": role, "content": content}
        if name:
            msg["name"] = name
        return msg

    @staticmethod
    def image_message(
        role: str,
        text: str,
        image_url: Optional[str] = None,
        image_path: Optional[str] = None,
        image_data: Optional[bytes] = None,
        detail: str = "auto"
    ) -> Dict[str, Any]:
        """
        Create a message with image (vision)

        Args:
            role: Message role (user/assistant)
            text: Text content
            image_url: URL to image
            image_path: Path to local image file
            image_data: Raw image bytes
            detail: Image detail level (auto/low/high)

        Returns:
            Message dict with image content
        """
        content = [{"type": "text", "text": text}]

        # Handle different image sources
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": detail
                }
            })
        elif image_path:
            # Load and encode local image
            path = Path(image_path)
            if not path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            image_bytes = path.read_bytes()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            # Detect mime type from extension
            ext = path.suffix.lower()
            mime_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_map.get(ext, 'image/jpeg')

            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}",
                    "detail": detail
                }
            })
        elif image_data:
            # Encode raw bytes
            base64_image = base64.b64encode(image_data).decode('utf-8')
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail
                }
            })
        else:
            raise ValueError("Must provide one of: image_url, image_path, or image_data")

        return {"role": role, "content": content}

    @staticmethod
    def audio_message(
        role: str,
        text: Optional[str] = None,
        audio_url: Optional[str] = None,
        audio_path: Optional[str] = None,
        audio_data: Optional[bytes] = None,
        format: str = "wav"
    ) -> Dict[str, Any]:
        """
        Create a message with audio input

        Args:
            role: Message role
            text: Optional text content
            audio_url: URL to audio file
            audio_path: Path to local audio file
            audio_data: Raw audio bytes
            format: Audio format (wav, mp3, etc.)

        Returns:
            Message dict with audio content
        """
        content = []

        if text:
            content.append({"type": "text", "text": text})

        # Handle different audio sources
        if audio_url:
            content.append({
                "type": "input_audio",
                "input_audio": {
                    "url": audio_url,
                    "format": format
                }
            })
        elif audio_path:
            # Load and encode local audio
            path = Path(audio_path)
            if not path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            audio_bytes = path.read_bytes()
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

            content.append({
                "type": "input_audio",
                "input_audio": {
                    "data": base64_audio,
                    "format": format
                }
            })
        elif audio_data:
            # Encode raw bytes
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
            content.append({
                "type": "input_audio",
                "input_audio": {
                    "data": base64_audio,
                    "format": format
                }
            })
        else:
            raise ValueError("Must provide one of: audio_url, audio_path, or audio_data")

        return {"role": role, "content": content}


# ============================================================================
# PARAMETER VALIDATORS (UPDATED)
# ============================================================================

class ParameterValidator:
    """Validate parameters before API calls"""

    @staticmethod
    def validate_prompt_length(prompt: str, max_length: int, param_name: str = "prompt"):
        """Validate prompt length"""
        from blossom_ai.core.errors import BlossomError, ErrorType

        if len(prompt) > max_length:
            raise BlossomError(
                message=f"{param_name} exceeds maximum length of {max_length} characters",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Please shorten your {param_name}."
            )

    @staticmethod
    def validate_dimensions(width: int, height: int, min_size: int = 64, max_size: int = 2048):
        """Validate image dimensions"""
        from blossom_ai.core.errors import BlossomError, ErrorType

        if width < min_size or width > max_size:
            raise BlossomError(
                message=f"Width must be between {min_size} and {max_size}",
                error_type=ErrorType.INVALID_PARAM
            )

        if height < min_size or height > max_size:
            raise BlossomError(
                message=f"Height must be between {min_size} and {max_size}",
                error_type=ErrorType.INVALID_PARAM
            )

    @staticmethod
    def validate_temperature(temperature: float):
        """Validate temperature parameter"""
        from blossom_ai.core.errors import BlossomError, ErrorType

        if temperature < 0 or temperature > 2:
            raise BlossomError(
                message="Temperature must be between 0 and 2",
                error_type=ErrorType.INVALID_PARAM
            )

    @staticmethod
    def validate_modalities(modalities: List[str]):
        """Validate modalities list"""
        from blossom_ai.core.errors import BlossomError, ErrorType

        valid = {"text", "audio", "image"}
        invalid = set(modalities) - valid

        if invalid:
            raise BlossomError(
                message=f"Invalid modalities: {invalid}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Valid modalities are: {valid}"
            )

    @staticmethod
    def validate_audio_format(format: str):
        """Validate audio format"""
        from blossom_ai.core.errors import BlossomError, ErrorType

        valid_formats = {"wav", "mp3", "pcm16", "g711_ulaw", "g711_alaw"}

        if format.lower() not in valid_formats:
            raise BlossomError(
                message=f"Invalid audio format: {format}",
                error_type=ErrorType.INVALID_PARAM,
                suggestion=f"Valid formats: {valid_formats}"
            )