 
"""
🌸 Blossom AI - Custom Errors and Handlers
"""
import requests
from typing import Optional

# Определение перечисления для типов ошибок
class ErrorType:
    NETWORK = "NETWORK_ERROR"
    API = "API_ERROR"
    INVALID_PARAM = "INVALID_PARAMETER"
    UNKNOWN = "UNKNOWN_ERROR"

# Определение базового класса исключения
class BlossomError(Exception):
    """Base exception for all Blossom AI errors."""
    def __init__(self, message: str, error_type: str = ErrorType.UNKNOWN, suggestion: Optional[str] = None):
        self.message = message
        self.error_type = error_type
        self.suggestion = suggestion
        super().__init__(f"[{error_type}] {message}" + (f" -> {suggestion}" if suggestion else ""))

# Вспомогательные функции для вывода в консоль
def print_info(message: str):
    print(f"ℹ️ {message}")

def print_warning(message: str):
    print(f"⚠️ {message}")

# Обработчик ошибок запросов
def handle_request_error(e: Exception, context: str) -> BlossomError:
    """Handles request exceptions (requests and aiohttp) and converts them to BlossomError."""
    # Handle aiohttp client errors
    if "aiohttp" in str(type(e)):
        if hasattr(e, 'status'): # ClientResponseError
            return BlossomError(
                message=f"HTTP Error {e.status} when {context}: {e.message}",
                error_type=ErrorType.API,
                suggestion="Check API status or your request parameters."
            )
        else: # Other client errors
            return BlossomError(
                message=f"Connection error when {context}: {e}",
                error_type=ErrorType.NETWORK,
                suggestion="Check your internet connection."
            )

    # Handle requests errors
    if isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code
        return BlossomError(
            message=f"HTTP Error {status_code} when {context}: {e.response.text}",
            error_type=ErrorType.API,
            suggestion="Check API status or your request parameters."
        )
    elif isinstance(e, requests.exceptions.ConnectionError):
        return BlossomError(
            message=f"Connection error when {context}.",
            error_type=ErrorType.NETWORK,
            suggestion="Check your internet connection."
        )
    
    # Fallback for other errors
    return BlossomError(
        message=f"An unexpected error occurred when {context}: {e}",
        error_type=ErrorType.UNKNOWN,
        suggestion="Retry the request later."
    )

