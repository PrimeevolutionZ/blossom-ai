# 🛡️ Error Handling Guide

Complete guide to handling errors gracefully in Blossom AI V2 API.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Error Hierarchy](#error-hierarchy)
- [Common Errors](#common-errors)
- [Error Attributes](#error-attributes)
- [Handling Specific Errors](#handling-specific-errors)
- [Retry Strategies](#retry-strategies)
- [Best Practices](#best-practices)
- [Production Patterns](#production-patterns)
- [Debugging](#debugging)

---

## 🌟 Overview

Blossom AI provides a comprehensive error handling system with:

- 🎯 **Specific Exceptions** - Different error types for different problems
- 💡 **Helpful Suggestions** - Built-in advice on how to fix issues
- 🔄 **Retry Information** - Automatic retry-after hints for rate limits
- 📊 **Error Context** - Detailed information about what went wrong
- 🐛 **Debug Support** - Enhanced logging for troubleshooting

### Philosophy

Blossom AI errors are designed to be:
1. **Informative** - Clear messages about what went wrong
2. **Actionable** - Suggestions on how to fix the problem
3. **Catchable** - Specific exception types for targeted handling
4. **Debuggable** - Rich context for troubleshooting

---

## 🌳 Error Hierarchy

All Blossom AI errors inherit from `BlossomError`.

```
BlossomError (base exception)
│
├── NetworkError          # Connection/network issues
├── TimeoutError          # Request timeout
├── StreamError           # Streaming failures
├── FileTooLargeError     # File size exceeded
│
└── APIError (API-related errors)
    ├── AuthenticationError    # Invalid/missing token
    ├── RateLimitError        # Rate limit exceeded
    └── ValidationError       # Invalid parameters
```

### Import All Errors

```python
from blossom_ai import (
    BlossomError,          # Base exception
    NetworkError,          # Network issues
    TimeoutError,          # Timeouts
    StreamError,           # Streaming errors
    FileTooLargeError,     # File size issues
    APIError,              # API errors (base)
    AuthenticationError,   # Auth failures
    RateLimitError,        # Rate limiting
    ValidationError        # Invalid input
)
```

---

## ⚠️ Common Errors

### Quick Reference

| Error                 | When It Happens           | Quick Fix                                                             |
|-----------------------|---------------------------|-----------------------------------------------------------------------|
| `AuthenticationError` | Invalid/missing API token | Check token at [enter.pollinations.ai](https://enter.pollinations.ai) |
| `RateLimitError`      | Too many requests         | Wait or upgrade plan                                                  |
| `ValidationError`     | Invalid parameters        | Check parameter values/types                                          |
| `NetworkError`        | Connection failed         | Check internet connection                                             |
| `TimeoutError`        | Request took too long     | Increase timeout or retry                                             |
| `StreamError`         | Streaming interrupted     | Reconnect and retry                                                   |
| `FileTooLargeError`   | File exceeds limit        | Use truncation or smaller file                                        |

---

## 📦 Error Attributes

All Blossom AI errors have these attributes:

### BlossomError Base Attributes

```python
try:
    # API call
    pass
except BlossomError as e:
    # All errors have these:
    print(e.error_type)    # ErrorType enum
    print(e.message)       # Human-readable description
    print(e.suggestion)    # How to fix (or None)
    print(e.status_code)   # HTTP status (or None)
    print(e.retry_after)   # Retry delay (or None)
```

**Attributes:**

- `error_type` (ErrorType): Error type enum for programmatic handling
- `message` (str): Human-readable error description
- `suggestion` (str | None): Actionable advice on how to fix
- `status_code` (int | None): HTTP status code if applicable
- `retry_after` (int | None): Seconds to wait before retry (rate limits)

### ErrorType Enum

```python
from blossom_ai import ErrorType

ErrorType.NETWORK           # Network/connection error
ErrorType.TIMEOUT           # Request timeout
ErrorType.AUTH              # Authentication failed
ErrorType.RATE_LIMIT        # Rate limit exceeded
ErrorType.INVALID_PARAM     # Invalid parameter
ErrorType.API_ERROR         # General API error
ErrorType.STREAM_ERROR      # Streaming error
ErrorType.FILE_TOO_LARGE    # File size limit exceeded
```

**Example - Using ErrorType:**

```python
from blossom_ai import Blossom, BlossomError, ErrorType

try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
except BlossomError as e:
    if e.error_type == ErrorType.RATE_LIMIT:
        print("Rate limited - need to wait")
    elif e.error_type == ErrorType.AUTH:
        print("Authentication failed - check token")
    else:
        print(f"Other error: {e.message}")
```

---

## 🎯 Handling Specific Errors

### AuthenticationError

**Cause:** Invalid or missing API token.

**Status Code:** 401 Unauthorized

```python
from blossom_ai import Blossom, AuthenticationError

try:
    client = Blossom(api_token="invalid_token")
    response = client.text.generate("Hello")
    
except AuthenticationError as e:
    print(f"❌ Auth failed: {e.message}")
    print(f"💡 {e.suggestion}")
    # Suggestion: "Check your API token at https://enter.pollinations.ai"
```

**Common causes:**
- Typo in API token
- Token not set (env var missing)
- Token expired or revoked
- Wrong token for environment

**How to fix:**
```python
# 1. Verify token is set
import os
token = os.getenv("POLLINATIONS_API_KEY")
if not token:
    print("❌ Token not set!")
    
# 2. Test with explicit token
client = Blossom(api_token="your-actual-token-here")

# 3. Regenerate token if needed at:
# https://enter.pollinations.ai
```

### RateLimitError

**Cause:** Too many requests in short time.

**Status Code:** 429 Too Many Requests

```python
from blossom_ai import Blossom, RateLimitError
import time

try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
        
except RateLimitError as e:
    print(f"❌ Rate limited: {e.message}")
    
    if e.retry_after:
        print(f"⏳ Retry after {e.retry_after} seconds")
        time.sleep(e.retry_after)
        # Retry request here
    else:
        print("⏳ Wait a moment and retry")
```

**Common causes:**
- Sending requests too quickly
- Exceeding plan limits
- Burst traffic

**How to fix:**
```python
# 1. Implement exponential backoff
def api_call_with_backoff():
    for attempt in range(5):
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate("Hello")
        except RateLimitError as e:
            if attempt < 4:
                wait = e.retry_after or (2 ** attempt)
                print(f"Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise

# 2. Add delays between requests
import time

for prompt in prompts:
    response = client.text.generate(prompt)
    time.sleep(1)  # Add delay

# 3. Use caching to reduce requests
from blossom_ai.utils import cached

@cached(ttl=3600)
def generate_cached(prompt):
    with Blossom(api_token="your-token") as client:
        return client.text.generate(prompt)
```

### ValidationError

**Cause:** Invalid parameters or input.

**Status Code:** 400 Bad Request

```python
from blossom_ai import Blossom, ValidationError

try:
    with Blossom(api_token="your-token") as client:
        # Prompt too long
        response = client.image.generate("x" * 300)
        
except ValidationError as e:
    print(f"❌ Invalid: {e.message}")
    print(f"💡 {e.suggestion}")
```

**Common causes:**
- Prompt too long (>250 chars for images)
- Invalid width/height (not 64-2048)
- Invalid model name
- Invalid parameter values
- File not found
- Unsupported file type

**How to fix:**
```python
# 1. Validate before calling API
def safe_generate_image(prompt, width, height):
    # Check prompt length
    if len(prompt) > 250:
        raise ValueError("Prompt too long (max 250 chars)")
    
    # Check dimensions
    if not (64 <= width <= 2048 and 64 <= height <= 2048):
        raise ValueError("Dimensions must be 64-2048")
    
    # Now safe to call
    with Blossom(api_token="your-token") as client:
        return client.image.generate(prompt, width=width, height=height)

# 2. Truncate long prompts
def truncate_prompt(prompt, max_length=250):
    if len(prompt) > max_length:
        return prompt[:max_length-3] + "..."
    return prompt

prompt = truncate_prompt("very long prompt here...")

# 3. Validate file existence
from pathlib import Path

image_path = Path("photo.jpg")
if not image_path.exists():
    print(f"❌ File not found: {image_path}")
else:
    # Safe to use
    pass
```

### NetworkError

**Cause:** Connection or network issues.

**Status Code:** Various (502, 503, etc.)

```python
from blossom_ai import Blossom, NetworkError
import time

try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
        
except NetworkError as e:
    print(f"❌ Network error: {e.message}")
    print(f"💡 {e.suggestion}")
    
    # Retry after delay
    time.sleep(5)
    # Try again...
```

**Common causes:**
- No internet connection
- DNS resolution failure
- Server temporarily down
- Firewall blocking request
- Proxy issues

**How to fix:**
```python
# 1. Implement retry logic
def api_call_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate("Hello")
        except NetworkError as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                print(f"Attempt {attempt+1} failed, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("Max retries reached")
                raise

# 2. Check connection before calling
import socket

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

if check_internet():
    # Safe to call API
    pass
else:
    print("❌ No internet connection")
```

### TimeoutError

**Cause:** Request took longer than timeout limit.

```python
from blossom_ai import Blossom, TimeoutError

try:
    client = Blossom(api_token="your-token", timeout=10)
    response = client.text.generate("Complex task...")
    
except TimeoutError as e:
    print(f"❌ Timeout: {e.message}")
    print(f"💡 {e.suggestion}")
```

**Common causes:**
- Timeout too short for task
- Server overloaded
- Network latency
- Large file processing

**How to fix:**
```python
# 1. Increase timeout for slow operations
client = Blossom(api_token="your-token", timeout=60)

# 2. Set per-request timeout
response = client.text.generate(
    "Complex task",
    timeout=120  # 2 minutes for this specific call
)

# 3. Use streaming for long responses
for chunk in client.text.generate("Long task", stream=True, timeout=120):
    print(chunk, end="", flush=True)
```

### StreamError

**Cause:** Streaming connection interrupted.

```python
from blossom_ai import Blossom, StreamError

try:
    with Blossom(api_token="your-token") as client:
        for chunk in client.text.generate("Count to 100", stream=True):
            print(chunk, end="", flush=True)
            
except StreamError as e:
    print(f"\n❌ Stream error: {e.message}")
    print(f"💡 {e.suggestion}")
```

**Common causes:**
- Connection dropped mid-stream
- Client timeout during streaming
- Server-side stream termination
- Network instability

**How to fix:**
```python
# 1. Implement stream recovery
def stream_with_recovery(prompt):
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            with Blossom(api_token="your-token", timeout=60) as client:
                for chunk in client.text.generate(prompt, stream=True):
                    yield chunk
            break  # Success
            
        except StreamError as e:
            if attempt < max_attempts - 1:
                print(f"\n⚠️ Stream interrupted, reconnecting...")
                time.sleep(2)
            else:
                raise

# 2. Collect chunks with error handling
def safe_streaming(prompt):
    chunks = []
    
    try:
        with Blossom(api_token="your-token") as client:
            for chunk in client.text.generate(prompt, stream=True):
                chunks.append(chunk)
                print(chunk, end="", flush=True)
    except StreamError:
        print("\n⚠️ Stream interrupted")
        
    return "".join(chunks)
```

### FileTooLargeError

**Cause:** File exceeds API size limits.

```python
from blossom_ai import FileTooLargeError
from blossom_ai.utils import read_file_for_prompt

try:
    content = read_file_for_prompt("huge_file.txt")
    
except FileTooLargeError as e:
    print(f"❌ File too large: {e.message}")
    print(f"💡 {e.suggestion}")
    # Suggestion: "Use read_file_truncated() or reduce file size"
```

**Common causes:**
- File exceeds 8000-character limit
- Combined files too large
- Image file too big (>20MB)

**How to fix:**
```python
# 1. Use truncation
from blossom_ai.utils import read_file_for_prompt

content = read_file_for_prompt(
    "large_file.txt",
    max_length=5000,
    truncate_if_needed=True
)

# 2. Use FileContentReader directly
from blossom_ai.utils import FileContentReader

reader = FileContentReader()
file_content = reader.read_file_truncated(
    "large_file.txt",
    max_chars=5000
)

# 3. Resize images before sending
from PIL import Image

def resize_image(path, max_size_mb=10):
    img = Image.open(path)
    
    # Calculate new size
    import os
    size_mb = os.path.getsize(path) / (1024 * 1024)
    
    if size_mb > max_size_mb:
        ratio = (max_size_mb / size_mb) ** 0.5
        new_size = tuple(int(d * ratio) for d in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        resized_path = f"resized_{path}"
        img.save(resized_path, quality=85)
        return resized_path
    
    return path
```

---

## 🔄 Retry Strategies

### Basic Retry

```python
from blossom_ai import Blossom, BlossomError
import time

def api_call_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate(prompt)
        except BlossomError as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt+1} failed: {e.message}")
                time.sleep(1)
            else:
                print("Max retries reached")
                raise

# Use it
response = api_call_with_retry("Hello AI")
```

### Exponential Backoff

```python
from blossom_ai import Blossom, BlossomError
import time

def api_call_with_backoff(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate(prompt)
                
        except BlossomError as e:
            if attempt < max_retries - 1:
                # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                wait_time = 2 ** attempt
                print(f"Retry {attempt+1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise

# Use it
response = api_call_with_backoff("Hello AI")
```

### Smart Retry (Selective)

```python
from blossom_ai import (
    Blossom,
    NetworkError,
    TimeoutError,
    RateLimitError,
    AuthenticationError,
    ValidationError
)
import time

def smart_retry(prompt, max_retries=3):
    """Only retry on transient errors"""
    
    for attempt in range(max_retries):
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate(prompt)
                
        except (NetworkError, TimeoutError, RateLimitError) as e:
            # Transient errors - retry
            if attempt < max_retries - 1:
                wait = e.retry_after if hasattr(e, 'retry_after') and e.retry_after else 2 ** attempt
                print(f"Transient error, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
                
        except (AuthenticationError, ValidationError) as e:
            # Permanent errors - don't retry
            print(f"❌ Permanent error: {e.message}")
            raise

# Use it
response = smart_retry("Hello AI")
```

### Retry with Fallback

```python
from blossom_ai import Blossom, BlossomError

def api_call_with_fallback(prompt, fallback_models=["openai", "openai-fast"]):
    """Try multiple models if one fails"""
    
    for model in fallback_models:
        try:
            with Blossom(api_token="your-token") as client:
                return client.text.generate(prompt, model=model)
        except BlossomError as e:
            print(f"Model {model} failed: {e.message}")
            if model == fallback_models[-1]:
                print("All models failed")
                raise
            else:
                print(f"Trying next model...")

# Use it
response = api_call_with_fallback("Hello AI")
```

---

## ✅ Best Practices

### 1. Always Use Try-Except

```python
# ❌ Bad - no error handling
response = client.text.generate("Hello")

# ✅ Good - basic error handling
try:
    response = client.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")

# ✅ Better - specific error handling
try:
    response = client.text.generate("Hello")
except AuthenticationError as e:
    print(f"Auth error: {e.message}")
except RateLimitError as e:
    print(f"Rate limited: wait {e.retry_after}s")
except BlossomError as e:
    print(f"Other error: {e.message}")
```

### 2. Use Context Managers

```python
# ❌ Bad - manual cleanup needed
client = Blossom(api_token="your-token")
try:
    response = client.text.generate("Hello")
finally:
    client.close_sync()

# ✅ Good - automatic cleanup
with Blossom(api_token="your-token") as client:
    response = client.text.generate("Hello")
```

### 3. Log Errors for Debugging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
except BlossomError as e:
    logger.error(
        f"API call failed: {e.error_type.value}",
        extra={
            "message": e.message,
            "suggestion": e.suggestion,
            "status_code": e.status_code
        }
    )
    raise
```

### 4. Validate Input Before API Calls

```python
def safe_generate_image(prompt, width, height):
    # Validate prompt
    if not prompt or len(prompt) < 3:
        raise ValueError("Prompt too short (min 3 chars)")
    if len(prompt) > 250:
        raise ValueError("Prompt too long (max 250 chars)")
    
    # Validate dimensions
    if not (64 <= width <= 2048):
        raise ValueError(f"Width must be 64-2048, got {width}")
    if not (64 <= height <= 2048):
        raise ValueError(f"Height must be 64-2048, got {height}")
    
    # Now safe to call API
    with Blossom(api_token="your-token") as client:
        return client.image.generate(prompt, width=width, height=height)
```

### 5. Provide User-Friendly Error Messages

```python
def generate_with_friendly_errors(prompt):
    try:
        with Blossom(api_token="your-token") as client:
            return client.text.generate(prompt)
            
    except AuthenticationError:
        return "⚠️ Authentication failed. Please check your API token."
        
    except RateLimitError as e:
        wait = e.retry_after or 60
        return f"⚠️ Too many requests. Please wait {wait} seconds."
        
    except ValidationError as e:
        return f"⚠️ Invalid input: {e.message}"
        
    except NetworkError:
        return "⚠️ Network error. Please check your connection."
        
    except BlossomError as e:
        return f"⚠️ Error: {e.message}"
```

### 6. Use Timeouts Appropriately

```python
# Short timeout for quick tasks
client = Blossom(api_token="your-token", timeout=10)
response = client.text.generate("Quick question")

# Longer timeout for complex tasks
client = Blossom(api_token="your-token", timeout=60)
response = client.text.generate("Write detailed analysis...")

# Per-request timeout override
response = client.text.generate(
    "Very complex task",
    timeout=120
)
```

### 7. Implement Circuit Breaker

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failures = 0
        self.state = "closed"
    
    def on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = "open"

# Use it
breaker = CircuitBreaker()

def api_call():
    with Blossom(api_token="your-token") as client:
        return client.text.generate("Hello")

try:
    response = breaker.call(api_call)
except Exception as e:
    print(f"Circuit breaker: {e}")
```

---

## 🏭 Production Patterns

### Complete Error Handler

```python
from blossom_ai import (
    Blossom,
    BlossomError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NetworkError,
    TimeoutError,
    StreamError
)
import logging
import time

logger = logging.getLogger(__name__)

def production_api_call(prompt, max_retries=3):
    """Production-ready API call with comprehensive error handling"""
    
    for attempt in range(max_retries):
        try:
            with Blossom(api_token="your-token", timeout=60) as client:
                response = client.text.generate(prompt)
                logger.info(f"API call successful")
                return {"success": True, "result": response}
                
        except AuthenticationError as e:
            # Don't retry auth errors
            logger.error(f"Authentication failed: {e.message}")
            return {
                "success": False,
                "error": "authentication",
                "message": "Invalid API token. Please check credentials.",
                "retryable": False
            }
            
        except ValidationError as e:
            # Don't retry validation errors
            logger.error(f"Validation failed: {e.message}")
            return {
                "success": False,
                "error": "validation",
                "message": e.message,
                "suggestion": e.suggestion,
                "retryable": False
            }
            
        except RateLimitError as e:
            # Retry with wait time
            logger.warning(f"Rate limited: {e.message}")
            
            if attempt < max_retries - 1:
                wait_time = e.retry_after or (2 ** attempt)
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                return {
                    "success": False,
                    "error": "rate_limit",
                    "message": "Rate limit exceeded. Please try again later.",
                    "retry_after": e.retry_after,
                    "retryable": True
                }
                
        except (NetworkError, TimeoutError) as e:
            # Retry transient errors
            logger.warning(f"Transient error: {e.message}")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retry {attempt+1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return {
                    "success": False,
                    "error": "transient",
                    "message": "Service temporarily unavailable. Please try again.",
                    "retryable": True
                }
                
        except BlossomError as e:
            # Catch-all for other errors
            logger.error(f"API error: {e.message}", exc_info=True)
            return {
                "success": False,
                "error": "unknown",
                "message": e.message,
                "suggestion": e.suggestion,
                "retryable": False
            }

# Use it
result = production_api_call("Generate text")
if result["success"]:
    print(f"Result: {result['result']}")
else:
    print(f"Error: {result['message']}")
    if result.get("retryable"):
        print("You can retry this request")
```

### Async Error Handling

```python
import asyncio
from blossom_ai import Blossom, BlossomError

async def async_api_call_safe(prompt):
    """Async API call with error handling"""
    
    try:
        async with Blossom(api_token="your-token") as client:
            response = await client.text.generate(prompt)
            return {"success": True, "result": response}
            
    except BlossomError as e:
        return {
            "success": False,
            "error": e.error_type.value,
            "message": e.message
        }

# Use it
async def main():
    result = await async_api_call_safe("Hello")
    print(result)

asyncio.run(main())
```

### Batch Processing with Error Recovery

```python
from blossom_ai import Blossom, BlossomError

def batch_process_with_errors(prompts):
    """Process multiple prompts with error recovery"""
    
    results = []
    
    with Blossom(api_token="your-token") as client:
        for i, prompt in enumerate(prompts):
            try:
                response = client.text.generate(prompt)
                results.append({
                    "index": i,
                    "prompt": prompt,
                    "success": True,
                    "result": response
                })
                print(f"✅ {i+1}/{len(prompts)} completed")
                
            except BlossomError as e:
                results.append({
                    "index": i,
                    "prompt": prompt,
                    "success": False,
                    "error": e.message
                })
                print(f"❌ {i+1}/{len(prompts)} failed: {e.message}")
                
            # Small delay between requests
            time.sleep(0.5)
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    print(f"\n📊 Results: {successful} succeeded, {failed} failed")
    
    return results

# Use it
prompts = ["Question 1", "Question 2", "Question 3"]
results = batch_process_with_errors(prompts)
```

---

## 🐛 Debugging

### Enable Debug Mode

```python
from blossom_ai import Blossom

# Enable debug logging
client = Blossom(api_token="your-token", debug=True)

# Now all API calls will show debug info
response = client.text.generate("Hello")
```

### Custom Logging

```python
import logging
from blossom_ai import Blossom

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blossom_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in error handling
try:
    with Blossom(api_token="your-token", debug=True) as client:
        response = client.text.generate("Hello")
except Exception as e:
    logger.exception("API call failed")
    raise
```

### Error Context Inspection

```python
from blossom_ai import Blossom, BlossomError

try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
except BlossomError as e:
    print("=== ERROR DETAILS ===")
    print(f"Type: {e.error_type}")
    print(f"Message: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    print(f"Status Code: {e.status_code}")
    print(f"Retry After: {e.retry_after}")
    print("====================")
```

### Debug Helper Function

```python
from blossom_ai import Blossom, BlossomError
import traceback

def debug_api_call(prompt, **kwargs):
    """API call with detailed debugging"""
    
    print(f"🔍 DEBUG: Calling API with prompt: {prompt[:50]}...")
    print(f"🔍 DEBUG: Parameters: {kwargs}")
    
    try:
        with Blossom(api_token="your-token", debug=True) as client:
            response = client.text.generate(prompt, **kwargs)
            print(f"✅ DEBUG: Success! Response length: {len(response)}")
            return response
            
    except BlossomError as e:
        print(f"❌ DEBUG: Error occurred")
        print(f"   Type: {e.error_type.value}")
        print(f"   Message: {e.message}")
        print(f"   Status: {e.status_code}")
        print(f"   Suggestion: {e.suggestion}")
        print("\n🔍 DEBUG: Full traceback:")
        traceback.print_exc()
        raise

# Use it
response = debug_api_call("Hello", temperature=0.7, max_tokens=100)
```

### Test Error Scenarios

```python
from blossom_ai import Blossom, BlossomError

def test_error_scenarios():
    """Test different error conditions"""
    
    print("Testing error scenarios...\n")
    
    # Test 1: Invalid token
    print("1. Testing invalid token...")
    try:
        client = Blossom(api_token="invalid_token_xyz")
        client.text.generate("test")
    except BlossomError as e:
        print(f"   ✅ Caught: {e.error_type.value}")
    
    # Test 2: Invalid parameters
    print("2. Testing invalid parameters...")
    try:
        with Blossom(api_token="your-token") as client:
            client.image.generate("x" * 300)
    except BlossomError as e:
        print(f"   ✅ Caught: {e.error_type.value}")
    
    # Test 3: Timeout
    print("3. Testing timeout...")
    try:
        client = Blossom(api_token="your-token", timeout=0.001)
        client.text.generate("test")
    except BlossomError as e:
        print(f"   ✅ Caught: {e.error_type.value}")
    
    print("\n✅ All error scenarios tested")

# Run tests
test_error_scenarios()
```

---

## 📚 Complete Examples

### Example 1: Robust API Wrapper

```python
from blossom_ai import Blossom, BlossomError
import time
import logging

logger = logging.getLogger(__name__)

class RobustBlossomClient:
    """Wrapper with built-in error handling and retry logic"""
    
    def __init__(self, api_token, max_retries=3, timeout=60):
        self.api_token = api_token
        self.max_retries = max_retries
        self.timeout = timeout
    
    def generate_text(self, prompt, **kwargs):
        """Generate text with automatic retry"""
        
        for attempt in range(self.max_retries):
            try:
                with Blossom(api_token=self.api_token, timeout=self.timeout) as client:
                    return client.text.generate(prompt, **kwargs)
                    
            except BlossomError as e:
                logger.warning(f"Attempt {attempt+1} failed: {e.message}")
                
                if attempt < self.max_retries - 1:
                    wait = e.retry_after if hasattr(e, 'retry_after') and e.retry_after else 2 ** attempt
                    time.sleep(wait)
                else:
                    logger.error(f"All {self.max_retries} attempts failed")
                    raise
    
    def generate_image(self, prompt, filename, **kwargs):
        """Generate image with automatic retry"""
        
        for attempt in range(self.max_retries):
            try:
                with Blossom(api_token=self.api_token, timeout=self.timeout) as client:
                    return client.image.save(prompt, filename, **kwargs)
                    
            except BlossomError as e:
                logger.warning(f"Attempt {attempt+1} failed: {e.message}")
                
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    time.sleep(wait)
                else:
                    raise

# Use it
client = RobustBlossomClient(api_token="your-token")
response = client.generate_text("Hello AI")
```

### Example 2: Error Monitoring

```python
from blossom_ai import Blossom, BlossomError
from collections import defaultdict
from datetime import datetime

class ErrorMonitor:
    """Monitor and track API errors"""
    
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.error_log = []
    
    def track_error(self, error):
        """Track error occurrence"""
        self.error_counts[error.error_type.value] += 1
        self.error_log.append({
            "timestamp": datetime.now(),
            "type": error.error_type.value,
            "message": error.message,
            "status_code": error.status_code
        })
    
    def get_stats(self):
        """Get error statistics"""
        return {
            "total_errors": len(self.error_log),
            "error_counts": dict(self.error_counts),
            "recent_errors": self.error_log[-5:]
        }
    
    def api_call(self, func, *args, **kwargs):
        """Make API call with monitoring"""
        try:
            return func(*args, **kwargs)
        except BlossomError as e:
            self.track_error(e)
            raise

# Use it
monitor = ErrorMonitor()

with Blossom(api_token="your-token") as client:
    for prompt in ["Q1", "Q2", "Q3"]:
        try:
            result = monitor.api_call(
                client.text.generate,
                prompt
            )
            print(f"✅ {prompt}: {result[:50]}")
        except BlossomError as e:
            print(f"❌ {prompt}: {e.message}")

# View stats
stats = monitor.get_stats()
print(f"\n📊 Error Stats: {stats}")
```

### Example 3: Graceful Degradation

```python
from blossom_ai import Blossom, BlossomError

def generate_with_fallback(prompt, fallback_text="Error: Unable to generate response"):
    """Generate with graceful fallback"""
    
    try:
        with Blossom(api_token="your-token") as client:
            return client.text.generate(prompt)
            
    except BlossomError as e:
        # Log error but return fallback
        print(f"⚠️ Generation failed: {e.message}")
        print(f"💡 Using fallback response")
        return fallback_text

# Use it
response = generate_with_fallback(
    "Hello AI",
    fallback_text="Hello! I'm temporarily unavailable. Please try again later."
)
print(response)
```

---

## 🎓 Summary

### Key Takeaways

1. **Always handle errors** - Use try-except blocks for all API calls
2. **Catch specific exceptions** - Handle different error types appropriately
3. **Implement retries** - Use exponential backoff for transient errors
4. **Validate input** - Check parameters before making API calls
5. **Log errors** - Track errors for debugging and monitoring
6. **Provide feedback** - Give users helpful error messages
7. **Use context managers** - Ensure proper cleanup with `with` statements
8. **Test error scenarios** - Verify error handling works correctly

### Quick Error Reference

```python
from blossom_ai import (
    BlossomError,          # Base - catch all errors
    AuthenticationError,   # 401 - invalid token
    RateLimitError,        # 429 - too many requests
    ValidationError,       # 400 - invalid input
    NetworkError,          # Connection issues
    TimeoutError,          # Request timeout
    StreamError,           # Streaming failures
    FileTooLargeError      # File size exceeded
)

# Basic pattern
try:
    with Blossom(api_token="your-token") as client:
        response = client.text.generate("Hello")
except AuthenticationError:
    # Handle auth
    pass
except RateLimitError as e:
    # Handle rate limit with e.retry_after
    pass
except ValidationError:
    # Handle invalid input
    pass
except BlossomError as e:
    # Handle other errors
    print(f"Error: {e.message}")
```

---

## 🔗 Related Documentation

- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Quick Start](QUICKSTART.md)** - Get started quickly
- **[Image Generation](IMAGE_GENERATION.md)** - Image generation guide
- **[Text Generation](TEXT_GENERATION.md)** - Text generation guide
- **[Production Guide](RESOURCE_MANAGEMENT.md)** - Best practices for production

---

## 🆘 Need Help?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to API Reference](API_REFERENCE.md) | [Index](INDEX.md) | [Next: Production Guide →](RESOURCE_MANAGEMENT.md)

</div>