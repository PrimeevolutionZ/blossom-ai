"""
Blossom AI – Error Handling (v0.5.4)
Blossom520Error + centralized suggestions + public logging helpers.
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any, Union, NamedTuple, Final

import aiohttp
import requests

logger = logging.getLogger("blossom_ai")

# --------------------------------------------------------------------------- #
# Central suggestions
# --------------------------------------------------------------------------- #

_SUGGESTIONS: Final[Dict[str, str]] = {
    "auth": "Check your API token at https://enter.pollinations.ai",
    "timeout": "Try increasing timeout or check your connection",
    "rate_limit": "Please wait {retry_after}s before retrying",
    "payment": "Visit https://auth.pollinations.ai to upgrade or check your API token",
    "validation": "See allowed values in documentation",
    "file_large": "Reduce file size or compress before upload",
    "stream_fail": "Try non-streaming mode or check your connection",
}

# --------------------------------------------------------------------------- #
# Error types
# --------------------------------------------------------------------------- #

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
    HTTP_520 = "HTTP_520_ERROR"

# --------------------------------------------------------------------------- #
# Error context
# --------------------------------------------------------------------------- #

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

# --------------------------------------------------------------------------- #
# Base error
# --------------------------------------------------------------------------- #

class BlossomError(Exception):
    __slots__ = ("message", "error_type", "suggestion", "context", "original_error", "retry_after")

    def __init__(
        self,
        message: str,
        error_type: str = ErrorType.UNKNOWN,
        suggestion: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        original_error: Optional[Exception] = None,
        retry_after: Optional[int] = None,
    ) -> None:
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
        return (
            f"BlossomError(type={self.error_type}, message={self.message!r}, "
            f"suggestion={self.suggestion!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "message": self.message,
            "suggestion": self.suggestion,
            "context": self.context.to_dict() if self.context else None,
            "retry_after": self.retry_after,
            "original_error": str(self.original_error) if self.original_error else None,
        }

# --------------------------------------------------------------------------- #
# Concrete errors
# --------------------------------------------------------------------------- #

class NetworkError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message, ErrorType.NETWORK, **kwargs)

class APIError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message, ErrorType.API, **kwargs)

class AuthenticationError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        kwargs.setdefault("suggestion", _SUGGESTIONS["auth"])
        super().__init__(message, ErrorType.AUTH, **kwargs)

class ValidationError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        kwargs.setdefault("suggestion", _SUGGESTIONS["validation"])
        super().__init__(message, ErrorType.INVALID_PARAM, **kwargs)

class RateLimitError(BlossomError):
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs: Any):
        if retry_after:
            kwargs.setdefault("suggestion", _SUGGESTIONS["rate_limit"].format(retry_after=retry_after))
        super().__init__(message, ErrorType.RATE_LIMIT, retry_after=retry_after, **kwargs)

class StreamError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        kwargs.setdefault("suggestion", _SUGGESTIONS["stream_fail"])
        super().__init__(message, ErrorType.STREAM, **kwargs)

class FileTooLargeError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        kwargs.setdefault("suggestion", _SUGGESTIONS["file_large"])
        super().__init__(message, ErrorType.FILE_TOO_LARGE, **kwargs)

class TimeoutError(BlossomError):
    def __init__(self, message: str, **kwargs: Any):
        kwargs.setdefault("suggestion", _SUGGESTIONS["timeout"])
        super().__init__(message, ErrorType.TIMEOUT, **kwargs)

class Blossom520Error(APIError):
    """Special handling for Cloudflare 520 (unknown error)."""
    def __init__(self, message: str = "Cloudflare 520 Unknown Error", **kwargs: Any):
        super().__init__(message, error_type=ErrorType.HTTP_520, **kwargs)

# --------------------------------------------------------------------------- #
# Handlers
# --------------------------------------------------------------------------- #

def _extract_retry_after(response_or_headers: Any) -> int:
    try:
        headers = getattr(response_or_headers, "headers", response_or_headers)
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        return int(retry_after) if retry_after else 60
    except (ValueError, TypeError, AttributeError):
        return 60

def handle_request_error(
    exc: Exception,
    operation: str,
    url: Optional[str] = None,
    method: Optional[str] = None,
    request_id: Optional[str] = None,
) -> BlossomError:
    context = ErrorContext(operation=operation, url=url, method=method, request_id=request_id)

    if isinstance(exc, aiohttp.ClientResponseError):
        return _handle_aiohttp_error(exc, context)
    if isinstance(exc, requests.exceptions.RequestException):
        return _handle_requests_error(exc, context)
    return BlossomError(
        f"Unexpected error: {exc}",
        context=context,
        original_error=exc,
    )

def _handle_aiohttp_error(exc: aiohttp.ClientResponseError, ctx: ErrorContext) -> BlossomError:
    ctx = ctx._replace(status_code=exc.status)
    if exc.status == 401:
        return AuthenticationError("Authentication failed", context=ctx, original_error=exc)
    if exc.status == 429:
        retry_after = _extract_retry_after(exc)
        return RateLimitError("Rate limit exceeded", retry_after=retry_after, context=ctx, original_error=exc)
    if exc.status == 520:
        return Blossom520Error(context=ctx, original_error=exc)
    if exc.status >= 500:
        return APIError(f"Server error {exc.status}", context=ctx, original_error=exc)
    return APIError(f"HTTP {exc.status}: {exc.message}", context=ctx, original_error=exc)

def _handle_requests_error(exc: requests.exceptions.RequestException, ctx: ErrorContext) -> BlossomError:
    if isinstance(exc, requests.exceptions.HTTPError):
        status = exc.response.status_code
        ctx = ctx._replace(status_code=status)
        if status == 401:
            return AuthenticationError("Authentication failed", context=ctx, original_error=exc)
        if status == 429:
            retry_after = _extract_retry_after(exc.response)
            return RateLimitError("Rate limit exceeded", retry_after=retry_after, context=ctx, original_error=exc)
        if status == 520:
            return Blossom520Error(context=ctx, original_error=exc)
        if status >= 500:
            return APIError(f"Server error {status}", context=ctx, original_error=exc)
        return APIError(f"HTTP {status}: {exc.response.text[:200]}", context=ctx, original_error=exc)
    if isinstance(exc, requests.exceptions.ConnectionError):
        return NetworkError("Connection failed", context=ctx, original_error=exc)
    if isinstance(exc, requests.exceptions.Timeout):
        return TimeoutError("Request timed out", context=ctx, original_error=exc)
    return NetworkError(f"Network error: {exc}", context=ctx, original_error=exc)

def handle_validation_error(
    param_name: str,
    param_value: Any,
    reason: str,
    allowed: Optional[tuple[str, ...]] = None,
) -> ValidationError:
    meta: Dict[str, Any] = {"parameter": param_name, "value": str(param_value)}
    if allowed:
        meta["allowed_values"] = allowed
    ctx = ErrorContext(operation="parameter_validation", metadata=meta)
    msg = f"Invalid parameter '{param_name}': {reason}"
    if allowed:
        msg += f"\nAllowed values: {', '.join(allowed)}"
    return ValidationError(msg, context=ctx)

# --------------------------------------------------------------------------- #
# Logging utilities – публичные, чтобы не было «неразрешённых ссылок»
# --------------------------------------------------------------------------- #

def print_info(message: str) -> None:
    logger.info(message)

def print_warning(message: str) -> None:
    logger.warning(message)

def print_error(message: str) -> None:
    logger.error(message)

def print_debug(message: str) -> None:
    logger.debug(message)

def print_success(message: str) -> None:
    logger.info(message)