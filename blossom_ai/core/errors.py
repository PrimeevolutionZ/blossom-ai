"""
Blossom AI - Error Handling
Clean error handling with context and better diagnostics
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

import requests


# ============================================================================
# ERROR TYPES
# ============================================================================

class ErrorType:
    """Error type constants"""
    NETWORK = "NETWORK_ERROR"
    API = "API_ERROR"
    INVALID_PARAM = "INVALID_PARAMETER"
    AUTH = "AUTHENTICATION_ERROR"
    RATE_LIMIT = "RATE_LIMIT_ERROR"
    STREAM = "STREAM_ERROR"
    FILE_TOO_LARGE = "FILE_TOO_LARGE_ERROR"
    UNKNOWN = "UNKNOWN_ERROR"


# ============================================================================
# ERROR CONTEXT
# ============================================================================

@dataclass
class ErrorContext:
    """Context information for errors"""
    operation: str
    url: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
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


# ============================================================================
# BLOSSOM ERROR
# ============================================================================

class BlossomError(Exception):
    """Base exception for all Blossom AI errors"""

    def __init__(
            self,
            message: str,
            error_type: str = ErrorType.UNKNOWN,
            suggestion: Optional[str] = None,
            context: Optional[ErrorContext] = None,
            original_error: Optional[Exception] = None,
            retry_after: Optional[int] = None
    ):
        self.message = message
        self.error_type = error_type
        self.suggestion = suggestion
        self.context = context
        self.original_error = original_error
        self.retry_after = retry_after

        # Build error message
        error_parts = [f"[{error_type}] {message}"]

        if context:
            error_parts.append(f"Context: {context}")

        if suggestion:
            error_parts.append(f"Suggestion: {suggestion}")

        if retry_after:
            error_parts.append(f"Retry after: {retry_after}s")

        if original_error:
            error_parts.append(f"Original: {type(original_error).__name__}: {str(original_error)}")

        super().__init__("\n".join(error_parts))

    def __repr__(self) -> str:
        return (
            f"BlossomError(type={self.error_type}, message={self.message!r}, "
            f"suggestion={self.suggestion!r})"
        )


# ============================================================================
# SPECIFIC ERRORS
# ============================================================================

class NetworkError(BlossomError):
    """Network-related errors"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.NETWORK, **kwargs)


class APIError(BlossomError):
    """API-related errors"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.API, **kwargs)


class AuthenticationError(BlossomError):
    """Authentication errors"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.AUTH, **kwargs)


class ValidationError(BlossomError):
    """Parameter validation errors"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.INVALID_PARAM, **kwargs)


class RateLimitError(BlossomError):
    """Rate limit errors"""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, error_type=ErrorType.RATE_LIMIT, retry_after=retry_after, **kwargs)


class StreamError(BlossomError):
    """Streaming-related errors"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.STREAM, **kwargs)


class FileTooLargeError(BlossomError):
    """File content exceeds API limits"""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.FILE_TOO_LARGE, **kwargs)


# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger("blossom_ai")


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
    """Print debug message"""
    logger.debug(message)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

def handle_request_error(
        e: Exception,
        operation: str,
        url: Optional[str] = None,
        method: Optional[str] = None,
        request_id: Optional[str] = None
) -> BlossomError:
    """
    Convert request exceptions to BlossomError

    Args:
        e: The original exception
        operation: Description of the operation
        url: Request URL if available
        method: HTTP method if available
        request_id: Request ID for tracing

    Returns:
        BlossomError with appropriate context
    """
    context = ErrorContext(
        operation=operation,
        url=url,
        method=method,
        request_id=request_id
    )

    # Handle aiohttp client errors
    if "aiohttp" in str(type(e)):
        if hasattr(e, 'status'):  # ClientResponseError
            context.status_code = e.status

            if e.status == 401:
                return AuthenticationError(
                    message=f"Authentication failed: {e.message}",
                    context=context,
                    suggestion="Check your API token at https://auth.pollinations.ai",
                    original_error=e
                )

            if e.status == 429:
                # Try to extract retry-after header
                retry_after = None
                if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                    try:
                        retry_after = int(e.headers['Retry-After'])
                    except (ValueError, TypeError):
                        retry_after = 60

                return RateLimitError(
                    message=f"Rate limit exceeded: {e.message}",
                    context=context,
                    retry_after=retry_after or 60,
                    suggestion=f"Please wait {retry_after or 60} seconds before making more requests",
                    original_error=e
                )

            return APIError(
                message=f"HTTP {e.status}: {e.message}",
                context=context,
                suggestion="Check API status or your request parameters",
                original_error=e
            )
        else:
            return NetworkError(
                message=f"Connection error: {str(e)}",
                context=context,
                suggestion="Check your internet connection",
                original_error=e
            )

    # Handle requests library errors
    if isinstance(e, requests.exceptions.HTTPError):
        context.status_code = e.response.status_code

        if e.response.status_code == 401:
            return AuthenticationError(
                message="Authentication failed",
                context=context,
                suggestion="Check your API token at https://auth.pollinations.ai",
                original_error=e
            )

        if e.response.status_code == 429:
            # Extract Retry-After header
            retry_after = None
            if 'Retry-After' in e.response.headers:
                try:
                    retry_after = int(e.response.headers['Retry-After'])
                except (ValueError, TypeError):
                    retry_after = 60

            return RateLimitError(
                message="Rate limit exceeded",
                context=context,
                retry_after=retry_after or 60,
                suggestion=f"Please wait {retry_after or 60} seconds before making more requests",
                original_error=e
            )

        return APIError(
            message=f"HTTP {e.response.status_code}: {e.response.text}",
            context=context,
            suggestion="Check API status or your request parameters",
            original_error=e
        )

    if isinstance(e, requests.exceptions.ConnectionError):
        return NetworkError(
            message="Connection failed",
            context=context,
            suggestion="Check your internet connection",
            original_error=e
        )

    if isinstance(e, requests.exceptions.Timeout):
        return NetworkError(
            message="Request timed out",
            context=context,
            suggestion="Try increasing timeout or check your connection",
            original_error=e
        )

    # Fallback for unknown errors
    return BlossomError(
        message=f"Unexpected error: {str(e)}",
        error_type=ErrorType.UNKNOWN,
        context=context,
        suggestion="Please report this issue if it persists",
        original_error=e
    )


def handle_validation_error(param_name: str, param_value: Any, reason: str) -> ValidationError:
    """
    Create a validation error

    Args:
        param_name: Name of the invalid parameter
        param_value: Value that failed validation
        reason: Reason for validation failure

    Returns:
        ValidationError
    """
    context = ErrorContext(
        operation="parameter_validation",
        metadata={"parameter": param_name, "value": str(param_value)}
    )

    return ValidationError(
        message=f"Invalid parameter '{param_name}': {reason}",
        context=context,
        suggestion=f"Check the value of '{param_name}' parameter"
    )