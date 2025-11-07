"""
Blossom AI - Error Handling
Refactored version with better structure and error parsing
"""

import logging
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum

import requests


# ==============================================================================
# LOGGING SETUP
# ==============================================================================

logger = logging.getLogger("blossom_ai")


# ==============================================================================
# ERROR TYPES
# ==============================================================================

class ErrorType(str, Enum):
    """Error type enumeration for better type safety"""
    NETWORK = "NETWORK_ERROR"
    API = "API_ERROR"
    INVALID_PARAM = "INVALID_PARAMETER"
    AUTH = "AUTHENTICATION_ERROR"
    RATE_LIMIT = "RATE_LIMIT_ERROR"
    STREAM = "STREAM_ERROR"
    FILE_TOO_LARGE = "FILE_TOO_LARGE_ERROR"
    TIMEOUT = "TIMEOUT_ERROR"
    UNKNOWN = "UNKNOWN_ERROR"


# ==============================================================================
# ERROR CONTEXT
# ==============================================================================

@dataclass(frozen=True)
class ErrorContext:
    """
    Context information for errors with improved formatting
    """
    operation: str
    url: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Human-readable context string"""
        parts = [self.operation]

        if self.method and self.url:
            parts.append(f"{self.method} {self.url}")
        elif self.url:
            parts.append(self.url)

        if self.status_code:
            parts.append(f"status={self.status_code}")

        if self.request_id:
            parts.append(f"request_id={self.request_id}")

        if self.metadata:
            meta_str = ", ".join(f"{k}={v}" for k, v in self.metadata.items())
            parts.append(meta_str)

        return " | ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging"""
        return {
            "operation": self.operation,
            "url": self.url,
            "method": self.method,
            "status_code": self.status_code,
            "request_id": self.request_id,
            "metadata": self.metadata
        }


# ==============================================================================
# BASE ERROR
# ==============================================================================

class BlossomError(Exception):
    """
    Base exception for all Blossom AI errors

    Improvements:
    - Better formatting
    - Structured data access
    - Cleaner string representation
    """

    def __init__(
        self,
        message: str,
        error_type: Union[ErrorType, str] = ErrorType.UNKNOWN,
        suggestion: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        original_error: Optional[Exception] = None,
        retry_after: Optional[int] = None
    ):
        self.message = message
        self.error_type = error_type if isinstance(error_type, ErrorType) else ErrorType(error_type)
        self.suggestion = suggestion
        self.context = context
        self.original_error = original_error
        self.retry_after = retry_after

        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with all context"""
        parts = [f"[{self.error_type.value}] {self.message}"]

        if self.context:
            parts.append(f"Context: {self.context}")

        if self.suggestion:
            parts.append(f"💡 Suggestion: {self.suggestion}")

        if self.retry_after:
            parts.append(f"⏰ Retry after: {self.retry_after}s")

        if self.original_error:
            parts.append(
                f"Original error: {type(self.original_error).__name__}: "
                f"{str(self.original_error)}"
            )

        return "\n".join(parts)

    def __repr__(self) -> str:
        return (
            f"BlossomError("
            f"type={self.error_type.value}, "
            f"message={self.message!r}, "
            f"suggestion={self.suggestion!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for structured logging"""
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "suggestion": self.suggestion,
            "context": self.context.to_dict() if self.context else None,
            "retry_after": self.retry_after,
            "original_error": str(self.original_error) if self.original_error else None
        }


# ==============================================================================
# SPECIFIC ERRORS
# ==============================================================================

class NetworkError(BlossomError):
    """Network-related errors (connection, DNS, etc.)"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.NETWORK, **kwargs)


class APIError(BlossomError):
    """API-related errors (invalid response, server error, etc.)"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.API, **kwargs)


class AuthenticationError(BlossomError):
    """Authentication failures"""
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('suggestion', 'Check your API token at https://enter.pollinations.ai')
        super().__init__(message, error_type=ErrorType.AUTH, **kwargs)


class ValidationError(BlossomError):
    """Parameter validation errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.INVALID_PARAM, **kwargs)


class RateLimitError(BlossomError):
    """Rate limit exceeded"""
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        if retry_after:
            kwargs.setdefault('suggestion', f'Please wait {retry_after} seconds before retrying')
        super().__init__(
            message,
            error_type=ErrorType.RATE_LIMIT,
            retry_after=retry_after,
            **kwargs
        )


class StreamError(BlossomError):
    """Streaming-related errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.STREAM, **kwargs)


class FileTooLargeError(BlossomError):
    """File content exceeds API limits"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.FILE_TOO_LARGE, **kwargs)


class TimeoutError(BlossomError):
    """Request timeout"""
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('suggestion', 'Try increasing timeout or check your connection')
        super().__init__(message, error_type=ErrorType.TIMEOUT, **kwargs)


# ==============================================================================
# LOGGING UTILITIES
# ==============================================================================

def print_info(message: str):
    """Print info message"""
    logger.info(message)
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """Print warning message"""
    logger.warning(message)
    print(f"⚠️  {message}")


def print_error(message: str):
    """Print error message"""
    logger.error(message)
    print(f"❌ {message}")


def print_debug(message: str):
    """Print debug message (only to logger)"""
    logger.debug(message)


def print_success(message: str):
    """Print success message"""
    logger.info(message)
    print(f"✅ {message}")


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

def _extract_retry_after(response_or_headers) -> Optional[int]:
    """Extract retry-after value from response/headers"""
    try:
        headers = getattr(response_or_headers, 'headers', response_or_headers)
        retry_after = headers.get('Retry-After')

        if retry_after:
            return int(retry_after)
    except (ValueError, TypeError, AttributeError):
        pass

    return 60  # Default fallback


def handle_request_error(
    e: Exception,
    operation: str,
    url: Optional[str] = None,
    method: Optional[str] = None,
    request_id: Optional[str] = None
) -> BlossomError:
    """
    Convert request exceptions to BlossomError

    Improvements:
    - Better error classification
    - Cleaner code structure
    - More specific error messages
    """
    context = ErrorContext(
        operation=operation,
        url=url,
        method=method,
        request_id=request_id
    )

    # Handle aiohttp errors
    if "aiohttp" in str(type(e)):
        return _handle_aiohttp_error(e, context)

    # Handle requests errors
    if isinstance(e, requests.exceptions.RequestException):
        return _handle_requests_error(e, context)

    # Fallback for unknown errors
    return BlossomError(
        message=f"Unexpected error: {str(e)}",
        error_type=ErrorType.UNKNOWN,
        context=context,
        suggestion="Please report this issue if it persists",
        original_error=e
    )


def _handle_aiohttp_error(e: Exception, context: ErrorContext) -> BlossomError:
    """Handle aiohttp-specific errors"""
    if hasattr(e, 'status'):  # ClientResponseError
        context = ErrorContext(
            operation=context.operation,
            url=context.url,
            method=context.method,
            status_code=e.status,
            request_id=context.request_id
        )

        if e.status == 401:
            return AuthenticationError(
                message=f"Authentication failed: {e.message}",
                context=context,
                original_error=e
            )

        if e.status == 429:
            retry_after = _extract_retry_after(e)
            return RateLimitError(
                message=f"Rate limit exceeded: {e.message}",
                context=context,
                retry_after=retry_after,
                original_error=e
            )

        if e.status >= 500:
            return APIError(
                message=f"Server error {e.status}: {e.message}",
                context=context,
                suggestion="The API service may be experiencing issues. Try again later.",
                original_error=e
            )

        return APIError(
            message=f"HTTP {e.status}: {e.message}",
            context=context,
            original_error=e
        )

    # Connection error
    return NetworkError(
        message=f"Connection error: {str(e)}",
        context=context,
        suggestion="Check your internet connection and firewall settings",
        original_error=e
    )


def _handle_requests_error(e: requests.exceptions.RequestException, context: ErrorContext) -> BlossomError:
    """Handle requests library errors"""
    if isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code
        context = ErrorContext(
            operation=context.operation,
            url=context.url,
            method=context.method,
            status_code=status_code,
            request_id=context.request_id
        )

        if status_code == 401:
            return AuthenticationError(
                message="Authentication failed",
                context=context,
                original_error=e
            )

        if status_code == 429:
            retry_after = _extract_retry_after(e.response)
            return RateLimitError(
                message="Rate limit exceeded",
                context=context,
                retry_after=retry_after,
                original_error=e
            )

        if status_code >= 500:
            return APIError(
                message=f"Server error {status_code}",
                context=context,
                suggestion="The API service may be experiencing issues. Try again later.",
                original_error=e
            )

        return APIError(
            message=f"HTTP {status_code}: {e.response.text[:200]}",
            context=context,
            original_error=e
        )

    if isinstance(e, requests.exceptions.ConnectionError):
        return NetworkError(
            message="Connection failed",
            context=context,
            suggestion="Check your internet connection and firewall settings",
            original_error=e
        )

    if isinstance(e, requests.exceptions.Timeout):
        return TimeoutError(
            message="Request timed out",
            context=context,
            original_error=e
        )

    return NetworkError(
        message=f"Network error: {str(e)}",
        context=context,
        original_error=e
    )


def handle_validation_error(
    param_name: str,
    param_value: Any,
    reason: str,
    allowed_values: Optional[list] = None
) -> ValidationError:
    """
    Create a validation error with helpful context

    Improvements:
    - Show allowed values if provided
    - Better formatting
    """
    metadata = {"parameter": param_name, "value": str(param_value)}

    if allowed_values:
        metadata["allowed_values"] = allowed_values

    context = ErrorContext(
        operation="parameter_validation",
        metadata=metadata
    )

    message_parts = [f"Invalid parameter '{param_name}': {reason}"]

    if allowed_values:
        message_parts.append(f"Allowed values: {', '.join(map(str, allowed_values))}")

    return ValidationError(
        message="\n".join(message_parts),
        context=context,
        suggestion=f"Check the value of '{param_name}' parameter"
    )