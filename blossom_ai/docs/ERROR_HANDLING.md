# Error Handling Guide - Blossom AI V2

> **Based on real-world usage patterns from test suite**

---

## Table of Contents

1. [Error Types](#error-types)
2. [Common Error Scenarios](#common-error-scenarios)
3. [Error Handling Patterns](#error-handling-patterns)
4. [Retry Strategies](#retry-strategies)
5. [Cleanup and Resource Management](#cleanup-and-resource-management)
6. [Streaming Error Handling](#streaming-error-handling)
7. [Async Error Handling](#async-error-handling)
8. [Best Practices](#best-practices)

---

## Error Types

### Core Error Hierarchy

```python
from blossom_ai import BlossomError, ErrorType
from blossom_ai.core.errors import (
    AuthenticationError,
    ValidationError,
    FileTooLargeError,
    StreamError,
    RateLimitError,
    Blossom520Error  # NEW in v0.5.4
)
```

### Error Type Enum

From real code usage:

```python
class ErrorType:
    INVALID_PARAM = "invalid_parameter"
    AUTH_ERROR = "authentication_error"
    RATE_LIMIT = "rate_limit_exceeded"
    SERVER_ERROR = "server_error"
    STREAM_ERROR = "stream_error"
    FILE_ERROR = "file_error"
    HTTP_520 = "HTTP_520_ERROR"  # NEW in v0.5.4
    # ... other types
```

### BlossomError Structure

All errors inherit from `BlossomError`:

```python
try:
    client.text.generate("prompt")
except BlossomError as e:
    print(f"Error type: {e.error_type}")
    print(f"Message: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    print(f"Status code: {e.status_code}")  # HTTP status if available
```

---

## Common Error Scenarios

### 1. Authentication Errors

**From test_integration.py:**

```python
from blossom_ai import Blossom
from blossom_ai.core.errors import AuthenticationError

# Invalid token raises AuthenticationError
try:
    with Blossom(api_token="invalid_token_12345") as client:
        client.text.generate("test")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    # Output: "Authentication failed: Invalid API token"
```

**Best Practice:**

```python
import os
from blossom_ai import Blossom, AuthenticationError

def create_client():
    """Create client with proper token validation"""
    api_token = os.getenv("BLOSSOM_API_TOKEN")
    
    if not api_token:
        raise ValueError("BLOSSOM_API_TOKEN environment variable not set")
    
    try:
        return Blossom(api_token=api_token)
    except AuthenticationError:
        raise ValueError("Invalid API token - get yours at https://enter.pollinations.ai")

# Usage
try:
    with create_client() as client:
        response = client.text.generate("Hello")
except ValueError as e:
    print(f"Setup error: {e}")
```

### 2. Validation Errors

**From v2_tests.py:**

```python
from blossom_ai import Blossom, BlossomError, ErrorType

with Blossom(api_token=API_TOKEN) as client:
    try:
        # Prompt too long (>256 chars)
        very_long_prompt = "a" * 300
        client.image.generate(very_long_prompt)
    except BlossomError as e:
        assert e.error_type == ErrorType.INVALID_PARAM
        print(f"Validation failed: {e.message}")
        print(f"Suggestion: {e.suggestion}")
```

**Common Validation Errors:**

```python
# 1. Prompt length validation
try:
    client.image.generate("x" * 300)  # Too long for image prompts
except ValidationError as e:
    print(f"Prompt exceeds maximum length: {e.message}")

# 2. File size validation
try:
    reader.read_file("huge_file.txt")  # >8000 chars
except FileTooLargeError as e:
    print(f"File too large: {e.message}")
    print(f"Try: {e.suggestion}")  # "Use read_file_truncated() instead"

# 3. Invalid parameters
try:
    client.image.generate("test", width=99999)  # Invalid dimension
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
```

### 3. Rate Limit Errors

**From test_reasoning_cache.py with retry logic:**

```python
import time
import requests
from blossom_ai import Blossom, RateLimitError

def retry_on_server_error(max_attempts=3, initial_wait=1.0):
    """Decorator for exponential backoff on server errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code in [502, 503, 504, 520]:  # Added 520
                        if attempt < max_attempts - 1:
                            wait = initial_wait * (2 ** attempt)
                            print(f"⏳ Server error {e.response.status_code}, retrying in {wait}s...")
                            time.sleep(wait)
                            continue
                    raise
        return wrapper
    return decorator

# Usage
@retry_on_server_error(max_attempts=5)
def generate_with_retry(prompt):
    with Blossom(api_token=API_TOKEN) as client:
        return client.text.generate(prompt)
```

### 4. Cloudflare 520 Errors (NEW in v0.5.4)

**Handling Cloudflare 520 (Unknown Error):**

```python
from blossom_ai import Blossom, Blossom520Error
import time

try:
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("Your prompt")
except Blossom520Error as e:
    print(f"Cloudflare 520 Error: {e.message}")
    print(f"Context: {e.context}")
    print(f"Suggestion: {e.suggestion}")
    
    # The library automatically retries 520 errors
    # but you can add custom handling here
    time.sleep(5)
    # Retry manually if needed
```

**Automatic Retry for 520:**

```python
# v0.5.4+ automatically retries 520 errors with exponential backoff
with Blossom(api_token=API_TOKEN) as client:
    # Will retry up to 3 times on 520 errors
    # Delays: 2s, 4s, 8s
    response = client.text.generate("Your prompt")
    # If all retries fail, raises Blossom520Error
```

**Custom 520 Handling:**

```python
from blossom_ai import Blossom, Blossom520Error
import time

def generate_with_520_fallback(prompt: str, max_retries: int = 5):
    """Handle 520 errors with extended retry"""
    for attempt in range(max_retries):
        try:
            with Blossom(api_token=API_TOKEN) as client:
                return client.text.generate(prompt)
        
        except Blossom520Error as e:
            if attempt < max_retries - 1:
                wait = (2 ** attempt) * 2  # Double the usual wait
                print(f"Cloudflare 520, attempt {attempt + 1}/{max_retries}")
                print(f"Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"Failed after {max_retries} attempts")
                raise

# Usage
response = generate_with_520_fallback("Generate text", max_retries=5)
```

### 5. File Handling Errors

**From test_file_reader.py:**

```python
from blossom_ai.utils import FileContentReader
from blossom_ai.core.errors import ValidationError, FileTooLargeError

reader = FileContentReader()

# 1. File not found
try:
    reader.read_file("nonexistent.txt")
except ValidationError as e:
    print(f"File error: {e.message}")  # "File not found: nonexistent.txt"

# 2. File too large
try:
    reader.read_file("huge_file.txt")  # 9000+ chars
except FileTooLargeError as e:
    print(f"Size error: {e.message}")
    print(f"Actual size: 9,000 chars")
    print(f"Max allowed: 8,000 chars")
    print(f"Solution: {e.suggestion}")  # "Use read_file_truncated()"

# 3. Unsupported file type
try:
    reader.read_file("program.exe")
except ValidationError as e:
    print(f"Type error: {e.message}")  # "Unsupported file type: .exe"

# 4. Empty file
try:
    reader.read_file("empty.txt")
except ValidationError as e:
    print(f"Content error: {e.message}")  # "File is empty"
```

---

## Error Handling Patterns

### Pattern 1: Graceful Degradation

```python
from blossom_ai import Blossom, BlossomError

def generate_with_fallback(prompt, fallback="Unable to generate response"):
    """Generate with fallback on error"""
    try:
        with Blossom(api_token=API_TOKEN) as client:
            return client.text.generate(prompt)
    except BlossomError as e:
        print(f"Error: {e.message}")
        return fallback

# Usage
response = generate_with_fallback("Explain AI")
print(response)  # Either real response or fallback
```

### Pattern 2: Error Classification

```python
from blossom_ai import BlossomError, ErrorType, Blossom520Error

def handle_error(error: BlossomError) -> str:
    """Classify and handle different error types"""
    if error.error_type == ErrorType.AUTH_ERROR:
        return "Authentication failed. Check your API token."
    
    elif error.error_type == ErrorType.RATE_LIMIT:
        return f"Rate limit exceeded. {error.suggestion}"
    
    elif error.error_type == ErrorType.INVALID_PARAM:
        return f"Invalid request: {error.message}"
    
    elif error.error_type == ErrorType.HTTP_520:
        return "Cloudflare error. The service will retry automatically."
    
    elif error.error_type == ErrorType.SERVER_ERROR:
        return "Server error. Please retry later."
    
    else:
        return f"Unexpected error: {error.message}"

# Usage
try:
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("x" * 1000)
except BlossomError as e:
    user_message = handle_error(e)
    print(user_message)
```

### Pattern 3: Context-Aware Error Handling

```python
def safe_generate(prompt: str, context: str = "general"):
    """Generate with context-aware error handling"""
    try:
        with Blossom(api_token=API_TOKEN) as client:
            return client.text.generate(prompt)
    
    except AuthenticationError:
        raise RuntimeError(f"[{context}] Authentication failed - check API token")
    
    except ValidationError as e:
        raise ValueError(f"[{context}] Invalid input: {e.message}")
    
    except RateLimitError:
        raise RuntimeError(f"[{context}] Rate limit exceeded - slow down requests")
    
    except Blossom520Error:
        raise RuntimeError(f"[{context}] Cloudflare error - retrying automatically")
    
    except BlossomError as e:
        raise RuntimeError(f"[{context}] Generation failed: {e.message}")

# Usage with context
try:
    response = safe_generate("Hello", context="user_onboarding")
except RuntimeError as e:
    log_error(str(e))  # Logs: "[user_onboarding] ..."
```

---

## Retry Strategies

### Strategy 1: Exponential Backoff (Production-Ready)

**From test_reasoning_cache.py with 520 support:**

```python
import time
from blossom_ai import Blossom, BlossomError, RateLimitError, Blossom520Error

def generate_with_exponential_backoff(
    prompt: str,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """Generate with exponential backoff on transient errors"""
    
    for attempt in range(max_retries):
        try:
            with Blossom(api_token=API_TOKEN) as client:
                return client.text.generate(prompt)
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = initial_delay * (backoff_factor ** attempt)
                print(f"Rate limited, retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise
        
        except (Blossom520Error, BlossomError) as e:
            # Server errors (502, 503, 504, 520) - retry
            if hasattr(e, 'status_code') and e.status_code in [502, 503, 504, 520]:
                if attempt < max_retries - 1:
                    delay = initial_delay * (backoff_factor ** attempt)
                    print(f"Server error {e.status_code}, retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    raise
            else:
                # Other errors - don't retry
                raise

# Usage
response = generate_with_exponential_backoff("Explain quantum computing")
```

### Strategy 2: Retry with Jitter

```python
import random
import time

def generate_with_jitter(prompt: str, max_retries: int = 3):
    """Retry with jitter to avoid thundering herd"""
    
    for attempt in range(max_retries):
        try:
            with Blossom(api_token=API_TOKEN) as client:
                return client.text.generate(prompt)
        
        except (RateLimitError, Blossom520Error):
            if attempt < max_retries - 1:
                # Base delay with random jitter
                base_delay = 2 ** attempt
                jitter = random.uniform(0, base_delay * 0.3)
                delay = base_delay + jitter
                print(f"Retry {attempt + 1} after {delay:.2f}s...")
                time.sleep(delay)
            else:
                raise

# Usage
response = generate_with_jitter("Generate text")
```

### Strategy 3: Circuit Breaker

```python
import time
from collections import deque

class CircuitBreaker:
    """Circuit breaker to prevent cascading failures"""
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = deque(maxlen=failure_threshold)
        self.state = "closed"  # closed, open, half_open
        self.last_failure_time = None
    
    def record_failure(self):
        """Record a failure"""
        now = time.time()
        self.failures.append(now)
        self.last_failure_time = now
        
        if len(self.failures) >= self.failure_threshold:
            self.state = "open"
    
    def record_success(self):
        """Record a success"""
        self.failures.clear()
        self.state = "closed"
    
    def can_attempt(self):
        """Check if request can be attempted"""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            # Check if timeout has elapsed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half_open"
                return True
            return False
        
        # half_open state
        return True

# Usage
breaker = CircuitBreaker(failure_threshold=5, timeout=60)

def generate_with_circuit_breaker(prompt: str):
    """Generate with circuit breaker protection"""
    
    if not breaker.can_attempt():
        raise RuntimeError("Circuit breaker is open - too many failures")
    
    try:
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(prompt)
        
        breaker.record_success()
        return response
    
    except BlossomError as e:
        breaker.record_failure()
        raise

# Usage
try:
    response = generate_with_circuit_breaker("Hello")
except RuntimeError as e:
    print(f"Circuit breaker: {e}")
```

---

## Cleanup and Resource Management

### Context Manager (Recommended)

**From v2_tests.py pattern:**

```python
from blossom_ai import Blossom

# ✅ CORRECT: Automatic cleanup
with Blossom(api_token=API_TOKEN) as client:
    response = client.text.generate("Hello")
# Cleanup happens automatically

# ✅ CORRECT: With error handling
try:
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")
# Cleanup still happens even with error!
```

### Reusable Client Pattern

**From v2_tests.py helper functions:**

```python
# Global client management
client: Blossom | None = None

def _get_client() -> Blossom:
    """Get or create client"""
    global client
    if client is None:
        client = Blossom(api_token=API_TOKEN)
    return client

def _close_client() -> None:
    """Close and cleanup client"""
    global client
    if client is not None:
        # Client will cleanup on context exit
        client = None

# Usage in tests
def test_something():
    """Test with shared client"""
    c = _get_client()
    try:
        result = c.text.generate("test")
        assert result
    finally:
        _close_client()
```

### Multiple Operations Pattern

```python
from blossom_ai import Blossom

def batch_process(prompts: list[str]) -> list[str]:
    """Process multiple prompts with single client"""
    results = []
    
    with Blossom(api_token=API_TOKEN) as client:
        for prompt in prompts:
            try:
                result = client.text.generate(prompt)
                results.append(result)
            except BlossomError as e:
                print(f"Error on '{prompt}': {e.message}")
                results.append(None)
    
    # Client cleaned up here
    return results

# Usage
prompts = ["What is AI?", "What is ML?", "What is DL?"]
responses = batch_process(prompts)
```

---

## Streaming Error Handling

### Synchronous Streaming

**From test_examples.py:**

```python
from blossom_ai import Blossom, StreamError

with Blossom(api_token=API_TOKEN) as client:
    try:
        chunks = []
        
        for chunk in client.text.generate("Count to 5", stream=True):
            chunks.append(chunk)
            print(chunk, end='', flush=True)
        
        print()  # Newline after streaming
        
        # Verify we got data
        assert len(chunks) > 0, "Should receive chunks"
        
    except StreamError as e:
        print(f"\nStream error: {e.message}")
        print(f"Partial data: {''.join(chunks)}")
    
    except BlossomError as e:
        print(f"\nGeneral error: {e.message}")
```

### Streaming with Timeout

```python
import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def timeout(seconds):
    """Context manager for timeout"""
    def handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds}s")
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# Usage
with Blossom(api_token=API_TOKEN) as client:
    try:
        with timeout(30):  # 30 second timeout
            for chunk in client.text.generate("Long task", stream=True):
                print(chunk, end='', flush=True)
    
    except TimeoutError as e:
        print(f"\n{e}")
    
    except StreamError as e:
        print(f"\nStream failed: {e.message}")
```

### Streaming with Buffer Management

```python
from blossom_ai import Blossom, StreamError

def stream_with_buffer(prompt: str, max_buffer_size: int = 1000):
    """Stream with buffer size management"""
    buffer = []
    buffer_size = 0
    
    with Blossom(api_token=API_TOKEN) as client:
        try:
            for chunk in client.text.generate(prompt, stream=True):
                buffer.append(chunk)
                buffer_size += len(chunk)
                
                # Flush buffer if too large
                if buffer_size >= max_buffer_size:
                    yield ''.join(buffer)
                    buffer = []
                    buffer_size = 0
            
            # Flush remaining
            if buffer:
                yield ''.join(buffer)
        
        except StreamError as e:
            # Return partial data
            if buffer:
                yield ''.join(buffer)
            raise

# Usage
for buffered_chunk in stream_with_buffer("Long generation"):
    print(buffered_chunk)
```

---

## Async Error Handling

### Basic Async Errors

**From test_reasoning_cache.py:**

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def async_generate_safe(prompt: str):
    """Safe async generation with error handling"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            return await client.text.generate(prompt)
    
    except AuthenticationError as e:
        print(f"Auth error: {e.message}")
        return None
    
    except BlossomError as e:
        print(f"Generation error: {e.message}")
        return None

# Usage
response = await async_generate_safe("Hello")
```

### Async Parallel with Error Collection

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def generate_many_safe(prompts: list[str]):
    """Generate many prompts, collecting errors"""
    results = []
    errors = []
    
    async with Blossom(api_token=API_TOKEN) as client:
        tasks = []
        
        for i, prompt in enumerate(prompts):
            async def generate_one(idx, p):
                try:
                    result = await client.text.generate(p)
                    return (idx, result, None)
                except BlossomError as e:
                    return (idx, None, str(e))
            
            tasks.append(generate_one(i, prompt))
        
        outcomes = await asyncio.gather(*tasks)
        
        for idx, result, error in outcomes:
            if error:
                errors.append((idx, prompts[idx], error))
            else:
                results.append((idx, result))
    
    return results, errors

# Usage
prompts = ["Q1", "Q2", "Q3"]
results, errors = await generate_many_safe(prompts)

print(f"Succeeded: {len(results)}")
print(f"Failed: {len(errors)}")
for idx, prompt, error in errors:
    print(f"  [{idx}] '{prompt}' failed: {error}")
```

### Async Streaming Errors

**From test_integration.py:**

```python
import asyncio
from blossom_ai import Blossom, StreamError

async def async_stream_safe(prompt: str):
    """Safe async streaming"""
    chunks = []
    
    async with Blossom(api_token=API_TOKEN) as client:
        try:
            stream = await client.text.generate(prompt, stream=True)
            
            async for chunk in stream:
                chunks.append(chunk)
                print(chunk, end='', flush=True)
            
            print()  # Newline
            return ''.join(chunks)
        
        except StreamError as e:
            print(f"\nStream error: {e.message}")
            # Return partial data
            return ''.join(chunks)

# Usage
result = await async_stream_safe("Count to 10")
```

---

## Best Practices

### 1. Always Use Context Managers

```python
# ✅ GOOD
with Blossom(api_token=API_TOKEN) as client:
    response = client.text.generate("Hello")

# ❌ BAD
client = Blossom(api_token=API_TOKEN)
response = client.text.generate("Hello")
# Forgot cleanup!
```

### 2. Handle Specific Exceptions First

```python
from blossom_ai import Blossom, AuthenticationError, ValidationError, Blossom520Error, BlossomError

try:
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("Hello")

except AuthenticationError:
    print("Check your API token")

except ValidationError as e:
    print(f"Invalid input: {e.message}")

except Blossom520Error:
    print("Cloudflare error - retry in progress")

except BlossomError as e:
    print(f"Other error: {e.message}")
```

### 3. Log Errors with Context

```python
import logging

logger = logging.getLogger(__name__)

def generate_with_logging(prompt: str, user_id: str):
    """Generate with comprehensive logging"""
    try:
        with Blossom(api_token=API_TOKEN) as client:
            logger.info(f"Generating for user {user_id}")
            response = client.text.generate(prompt)
            logger.info(f"Success for user {user_id}")
            return response
    
    except BlossomError as e:
        logger.error(
            f"Generation failed for user {user_id}",
            extra={
                "error_type": e.error_type,
                "message": e.message,
                "status_code": getattr(e, 'status_code', None),
                "prompt_length": len(prompt)
            }
        )
        raise
```

### 4. Provide User-Friendly Messages

```python
from blossom_ai import BlossomError, ErrorType, Blossom520Error

def get_user_message(error: BlossomError) -> str:
    """Convert technical error to user-friendly message"""
    messages = {
        ErrorType.AUTH_ERROR: "Authentication failed. Please check your API key in settings.",
        ErrorType.RATE_LIMIT: "Too many requests. Please wait a moment and try again.",
        ErrorType.INVALID_PARAM: "Invalid input. Please check your request and try again.",
        ErrorType.HTTP_520: "Service temporarily experiencing issues. We're retrying automatically.",
        ErrorType.SERVER_ERROR: "Service temporarily unavailable. Please try again in a few minutes.",
    }
    
    return messages.get(
        error.error_type,
        f"An error occurred: {error.message}"
    )

# Usage
try:
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate(prompt)
except BlossomError as e:
    user_message = get_user_message(e)
    print(user_message)  # Show to user
    logger.error(f"Technical details: {e}")  # Log technical details
```

### 5. Test Error Paths

```python
import pytest
from blossom_ai import Blossom, ValidationError

def test_error_handling():
    """Test that errors are handled correctly"""
    with Blossom(api_token=API_TOKEN) as client:
        # Test invalid input
        with pytest.raises(ValidationError):
            client.image.generate("x" * 300)
        
        # Test recovery
        response = client.text.generate("Valid prompt")
        assert response is not None
```

### 6. Use Timeouts

```python
from blossom_ai import Blossom

# Set timeout in client
with Blossom(api_token=API_TOKEN, timeout=30) as client:
    try:
        response = client.text.generate("Long task")
    except TimeoutError:
        print("Request took too long")
```

### 7. Implement Health Checks

```python
from blossom_ai import Blossom, BlossomError

def health_check() -> bool:
    """Check if API is accessible"""
    try:
        with Blossom(api_token=API_TOKEN, timeout=5) as client:
            # Quick test
            client.text.generate("test")
            return True
    except BlossomError:
        return False

# Usage
if not health_check():
    print("API unavailable")
```

---

## Error Recovery Examples

### Example 1: User Input Validation

```python
from blossom_ai import Blossom, ValidationError

def process_user_prompt(user_input: str):
    """Validate and process user input"""
    # Pre-validation
    if not user_input.strip():
        return "Error: Please enter a prompt"
    
    if len(user_input) > 1000:
        return "Error: Prompt too long (max 1000 characters)"
    
    # API call
    try:
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(user_input)
            return response
    
    except ValidationError as e:
        return f"Invalid input: {e.message}"
    
    except BlossomError as e:
        return f"Service error: Please try again later"

# Usage
user_input = input("Enter prompt: ")
result = process_user_prompt(user_input)
print(result)
```

### Example 2: File Processing with Fallback

```python
from blossom_ai.utils import FileContentReader
from blossom_ai.core.errors import FileTooLargeError

def process_file_safe(file_path: str) -> str:
    """Process file with automatic truncation fallback"""
    reader = FileContentReader()
    
    try:
        # Try normal read
        content = reader.read_file(file_path)
        return content.content
    
    except FileTooLargeError:
        # Fallback to truncated read
        print("File too large, truncating...")
        content = reader.read_file_truncated(file_path, max_chars=5000)
        return content.content