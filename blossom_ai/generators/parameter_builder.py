"""
Blossom AI - Parameter Builders (v0.5.0)
Type-safe parameter construction for V2 API
"""

from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field, asdict

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
# CHAT PARAMETERS (V2)
# ============================================================================

@dataclass
class ChatParamsV2(BaseParams):
    """Parameters for V2 chat completion with extended OpenAI features"""

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

        # Stream options for better streaming
        if self.stream:
            body['stream_options'] = {'include_usage': True}

        # Add extra params (filtering out defaults)
        for key, value in self.extra_params.items():
            if value is not None and value != 0 and value is not False and value != 1.0:
                body[key] = value

        return body


# ============================================================================
# PARAMETER VALIDATORS
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