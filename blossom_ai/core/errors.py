"""
Blossom AI - Error Handling (v0.5.0)
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any, Union, NamedTuple

import aiohttp
import requests

logger = logging.getLogger("blossom_ai")

# ==============================================================================
# ERROR TYPES
# ==============================================================================

class ErrorType:
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

class ErrorContext(NamedTuple):
    operation: str
    url: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

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
            parts.append(", ".join(f"{k}={v}" for k, v in self.metadata.items()))
        return " | ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

# ==============================================================================
# BASE ERROR
# ==============================================================================

class BlossomError(Exception):
    def __init__(
        self,
        message: str,
        error_type: str = ErrorType.UNKNOWN,
        suggestion: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        original_error: Optional[Exception] = None,
        retry_after: Optional[int] = None,
    ):
        self.message = message
        self.error_type = error_type
        self.suggestion = suggestion
        self.context = context
        self.original_error = original_error
        self.retry_after = retry_after
        super().__init__(self._format())

    def _format(self) -> str:
        parts = [f"[{self.error_type}] {self.message}"]
        if self.context:
            parts.append(f"Context: {self.context}")
        if self.suggestion:
            parts.append(f"Suggestion: {self.suggestion}")
        if self.retry_after:
            parts.append(f"Retry after: {self.retry_after}s")
        if self.original_error:
            parts.append(f"Original error: {type(self.original_error).__name__}: {self.original_error}")
        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"BlossomError(type={self.error_type}, message={self.message!r}, suggestion={self.suggestion!r})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "suggestion": self.suggestion,
            "context": self.context.to_dict() if self.context else None,
            "retry_after": self.retry_after,
            "original_error": str(self.original_error) if self.original_error else None,
        }

# ==============================================================================
# SPECIFIC ERRORS
# ==============================================================================

class NetworkError(BlossomError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.NETWORK, **kwargs)

class APIError(BlossomError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.API, **kwargs)

class AuthenticationError(BlossomError):
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("suggestion", "Check your API token at https://enter.pollinations.ai")
        super().__init__(message, error_type=ErrorType.AUTH, **kwargs)

class ValidationError(BlossomError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.INVALID_PARAM, **kwargs)

class RateLimitError(BlossomError):
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        if retry_after:
            kwargs.setdefault("suggestion", f"Please wait {retry_after} seconds before retrying")
        super().__init__(message, error_type=ErrorType.RATE_LIMIT, retry_after=retry_after, **kwargs)

class StreamError(BlossomError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.STREAM, **kwargs)

class FileTooLargeError(BlossomError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type=ErrorType.FILE_TOO_LARGE, **kwargs)

class TimeoutError(BlossomError):
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("suggestion", "Try increasing timeout or check your connection")
        super().__init__(message, error_type=ErrorType.TIMEOUT, **kwargs)

# ==============================================================================
# LOGGING UTILITIES
# ==============================================================================

def print_info(message: str):
    logger.info(message)

def print_warning(message: str):
    logger.warning(message)

def print_error(message: str):
    logger.error(message)

def print_debug(message: str):
    logger.debug(message)

def print_success(message: str):
    logger.info(message)

# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

def _extract_retry_after(response_or_headers) -> Optional[int]:
    try:
        headers = getattr(response_or_headers, "headers", response_or_headers)
        retry_after = headers.get("Retry-After")
        return int(retry_after) if retry_after else None
    except (ValueError, TypeError, AttributeError):
        logger.warning("Retry-After header missing or invalid, using fallback: 60s")
        return 60

def handle_request_error(
    e: Exception,
    operation: str,
    url: Optional[str] = None,
    method: Optional[str] = None,
    request_id: Optional[str] = None,
) -> BlossomError:
    context = ErrorContext(operation=operation, url=url, method=method, request_id=request_id)

    if isinstance(e, aiohttp.ClientResponseError):
        return _handle_aiohttp_error(e, context)
    if isinstance(e, requests.exceptions.RequestException):
        return _handle_requests_error(e, context)

    return BlossomError(
        message=f"Unexpected error: {e}",
        error_type=ErrorType.UNKNOWN,
        context=context,
        suggestion="Please report this issue if it persists",
        original_error=e,
    )

def _handle_aiohttp_error(e: aiohttp.ClientResponseError, context: ErrorContext) -> BlossomError:
    context = context._replace(status_code=e.status)
    if e.status == 401:
        return AuthenticationError(f"Authentication failed: {e.message}", context=context, original_error=e)
    if e.status == 429:
        retry_after = _extract_retry_after(e)
        return RateLimitError(f"Rate limit exceeded: {e.message}", context=context, retry_after=retry_after, original_error=e)
    if e.status >= 500:
        return APIError(f"Server error {e.status}: {e.message}", context=context, original_error=e)
    return APIError(f"HTTP {e.status}: {e.message}", context=context, original_error=e)

def _handle_requests_error(e: requests.exceptions.RequestException, context: ErrorContext) -> BlossomError:
    if isinstance(e, requests.exceptions.HTTPError):
        status = e.response.status_code
        context = context._replace(status_code=status)
        if status == 401:
            return AuthenticationError("Authentication failed", context=context, original_error=e)
        if status == 429:
            retry_after = _extract_retry_after(e.response)
            return RateLimitError("Rate limit exceeded", context=context, retry_after=retry_after, original_error=e)
        if status >= 500:
            return APIError(f"Server error {status}", context=context, original_error=e)
        return APIError(f"HTTP {status}: {e.response.text[:200]}", context=context, original_error=e)

    if isinstance(e, requests.exceptions.ConnectionError):
        return NetworkError("Connection failed", context=context, original_error=e)
    if isinstance(e, requests.exceptions.Timeout):
        return TimeoutError("Request timed out", context=context, original_error=e)
    return NetworkError(f"Network error: {e}", context=context, original_error=e)

def handle_validation_error(
    param_name: str,
    param_value: Any,
    reason: str,
    allowed_values: Optional[list] = None,
) -> ValidationError:
    metadata = {"parameter": param_name, "value": str(param_value)}
    if allowed_values:
        metadata["allowed_values"] = allowed_values
    context = ErrorContext(operation="parameter_validation", metadata=metadata)
    msg = f"Invalid parameter '{param_name}': {reason}"
    if allowed_values:
        msg += f"\nAllowed values: {', '.join(map(str, allowed_values))}"
    return ValidationError(msg, context=context, suggestion=f"Check '{param_name}'")