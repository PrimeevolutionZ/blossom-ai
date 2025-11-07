# 🛡️ Error Handling Guide

> **Comprehensive guide to handling errors in Blossom AI (V1 & V2)**

Blossom AI provides robust error handling with clear, actionable error messages for both V1 and V2 APIs.

---

## 📋 Table of Contents

- [Error Types](#-error-types)
- [V2 Specific Errors](#-v2-specific-errors)
- [Basic Error Handling](#-basic-error-handling)
- [V2 Error Examples](#-v2-error-examples)
- [Streaming Errors](#-streaming-errors)
- [Best Practices](#-best-practices)

---

## 🔴 Error Types

All errors inherit from the base `BlossomError` class, which provides context and suggestions.

### Available Error Classes

| Error Type            | Description               | When It Occurs                  |
|-----------------------|---------------------------|---------------------------------|
| `BlossomError`        | Base error class          | All errors inherit from this    |
| `NetworkError`        | Network/connection issues | Connection failed, timeout      |
| `APIError`            | API-related errors        | Invalid response, server error  |
| `AuthenticationError` | Authentication failures   | Invalid/missing API token       |
| `ValidationError`     | Invalid parameters        | Bad prompt, invalid model       |
| `RateLimitError`      | Rate limit exceeded       | Too many requests               |
| `StreamError`         | Streaming issues          | Stream timeout, connection lost |
| `FileTooLargeError`   | File content too large    | File exceeds API limits         |

### Error Attributes

All `BlossomError` instances have:

```python
error.message          # Human-readable error message
error.error_type       # Error type constant (e.g., ErrorType.NETWORK)
error.suggestion       # Actionable suggestion for fixing the error
error.context          # ErrorContext with operation details
error.original_error   # Original exception if wrapped
error.retry_after      # Seconds to wait (for RateLimitError)
```

### ErrorContext Attributes

```python
context.operation      # Operation that failed (e.g., "image_generation")
context.url           # Request URL
context.method        # HTTP method (GET, POST)
context.status_code   # HTTP status code
context.request_id    # Unique request ID for tracing
context.metadata      # Additional context data
```

---

## 🆕 V2 Specific Errors

### 402 Payment Required

**V2 API** enforces payment requirements for premium features.

```python
from blossom_ai import Blossom, APIError

client = Blossom(api_version="v2", api_token="pk_free_token")

try:
    image = client.image.generate(
        "sunset",
        quality="hd"  # HD may require payment
    )
except APIError as e:
    if e.context and e.context.status_code == 402:
        print(f"Payment required: {e.message}")
        print(f"Suggestion: {e.suggestion}")
        # Suggestion: Visit https://auth.pollinations.ai to upgrade
```

### Authentication Differences

**V1 API:**
- Token optional for most features
- Audio generation requires token

**V2 API:**
- Token recommended for better rate limits
- Secret keys (`sk_...`) for server-side
- Publishable keys (`pk_...`) for client-side

```python
from blossom_ai import Blossom, AuthenticationError

try:
    # V2 with invalid token
    client = Blossom(api_version="v2", api_token="invalid_token")
    image = client.image.generate("test")
    
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    # Check your API token at https://auth.pollinations.ai
```

---

## 🔧 Basic Error Handling

### Simple Try-Except

```python
from blossom_ai import Blossom, BlossomError

client = Blossom(api_version="v2", api_token="your_token")

try:
    image = client.image.generate("a sunset")
    
except BlossomError as e:
    print(f"Error: {e.message}")
    print(f"Type: {e.error_type}")
    if e.suggestion:
        print(f"Suggestion: {e.suggestion}")
finally:
    client.close_sync()
```

### Handling Specific Error Types

```python
from blossom_ai import (
    Blossom,
    NetworkError,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

client = Blossom(api_version="v2", api_token="token")

try:
    response = client.text.generate(
        "Explain quantum computing",
        max_tokens=200
    )
    print(response)
    
except NetworkError as e:
    print(f"Network issue: {e.message}")
    print("Check your internet connection")
    
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print("Get a valid token from https://enter.pollinations.ai")
    
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    print(f"Retry after {e.retry_after} seconds")
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except APIError as e:
    print(f"API error: {e.message}")
    if e.context:
        print(f"Status: {e.context.status_code}")
    
finally:
    client.close_sync()
```

---

## 🆕 V2 Error Examples

### Example 1: Image Generation with Quality

```python
from blossom_ai import Blossom, APIError, ValidationError

client = Blossom(api_version="v2", api_token="token")

try:
    image = client.image.generate(
        prompt="beautiful landscape",
        quality="ultra",  # Invalid quality level
        guidance_scale=7.5
    )
    
except ValidationError as e:
    print(f"Invalid parameter: {e.message}")
    # Quality must be one of: low, medium, high, hd
    
except APIError as e:
    if e.context and e.context.status_code == 402:
        print("Payment required for HD quality")
    else:
        print(f"API error: {e.message}")
        
finally:
    client.close_sync()
```

### Example 2: Text Generation with Function Calling

```python
from blossom_ai import Blossom, ValidationError, APIError

client = Blossom(api_version="v2", api_token="token")

# Invalid tool definition
invalid_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            # Missing required 'parameters' field
        }
    }
]

try:
    response = client.text.chat(
        messages=[{"role": "user", "content": "What's the weather?"}],
        tools=invalid_tools,
        tool_choice="auto"
    )
    
except ValidationError as e:
    print(f"Invalid tool definition: {e.message}")
    print("Tools must have 'parameters' field")
    
except APIError as e:
    print(f"API error: {e.message}")
    if e.context:
        print(f"Context: {e.context}")
        
finally:
    client.close_sync()
```

### Example 3: JSON Mode with Validation

```python
from blossom_ai import Blossom, APIError
import json

client = Blossom(api_version="v2", api_token="token")

try:
    response = client.text.generate(
        prompt="Generate a user profile with name, age, email",
        json_mode=True,
        max_tokens=100
    )
    
    # Validate JSON
    data = json.loads(response)
    
    # Custom validation
    if "name" not in data or "age" not in data:
        raise ValidationError(
            message="JSON missing required fields",
            suggestion="Specify required fields in prompt"
        )
    
    print(f"Valid JSON: {data}")
    
except json.JSONDecodeError as e:
    print(f"Invalid JSON response: {e}")
    print("Try rephrasing your prompt")
    
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    
except APIError as e:
    print(f"API error: {e.message}")
    
finally:
    client.close_sync()
```

---

## 🌊 Streaming Errors

Streaming has specific error handling requirements.

### V2 Streaming with Error Handling

```python
from blossom_ai import Blossom, StreamError, NetworkError

client = Blossom(api_version="v2", api_token="token")

chunks = []

try:
    print("Streaming: ", end="", flush=True)
    
    for chunk in client.text.generate(
        "Write a short story about robots",
        model="openai",
        stream=True,
        max_tokens=200
    ):
        print(chunk, end="", flush=True)
        chunks.append(chunk)
        
    print()  # Newline
    
except StreamError as e:
    print(f"\nStream error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
    # Save partial result
    if chunks:
        partial = "".join(chunks)
        print(f"Partial result ({len(partial)} chars): {partial[:100]}...")
        
except NetworkError as e:
    print(f"\nNetwork error during streaming: {e.message}")
    print("Check your connection and retry")
    
finally:
    full_text = "".join(chunks)
    print(f"\nReceived {len(chunks)} chunks, {len(full_text)} total characters")
    client.close_sync()
```

### Async Streaming Error Handling

```python
import asyncio
from blossom_ai import Blossom, StreamError

async def stream_with_error_handling():
    async with Blossom(api_version="v2", api_token="token") as client:
        chunks = []
        
        try:
            async for chunk in await client.text.generate(
                "Explain AI",
                stream=True,
                max_tokens=150
            ):
                print(chunk, end="", flush=True)
                chunks.append(chunk)
                
        except StreamError as e:
            print(f"\nStream error: {e.message}")
            if e.original_error:
                print(f"Original error: {e.original_error}")
                
        finally:
            result = "".join(chunks)
            print(f"\n\nTotal: {len(result)} characters")

asyncio.run(stream_with_error_handling())
```

---

## ✅ Best Practices

### 1. Always Use Context Managers

Context managers ensure proper cleanup even when errors occur.

```python
from blossom_ai import Blossom

# ✅ GOOD: Automatic cleanup
try:
    with Blossom(api_version="v2", api_token="token") as client:
        image = client.image.generate("sunset")
except Exception as e:
    print(f"Error: {e}")
# Client automatically closed

# ❌ BAD: Manual cleanup required
client = Blossom(api_version="v2", api_token="token")
try:
    image = client.image.generate("sunset")
finally:
    client.close_sync()  # Easy to forget!
```

### 2. Handle Rate Limits Gracefully

```python
import time
from blossom_ai import Blossom, RateLimitError

client = Blossom(api_version="v2", api_token="token")

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.text.generate(prompt, max_tokens=100)
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = e.retry_after or 60
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts")
                raise

try:
    result = generate_with_retry("Explain AI")
    print(result)
finally:
    client.close_sync()
```

### 3. Log Errors for Debugging

```python
import logging
from blossom_ai import Blossom, BlossomError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = Blossom(api_version="v2", api_token="token")

try:
    image = client.image.generate(
        "test",
        quality="hd",
        guidance_scale=7.5
    )
    
except BlossomError as e:
    # Log full error details
    logger.error(f"Error Type: {e.error_type}")
    logger.error(f"Message: {e.message}")
    
    if e.context:
        logger.error(f"Context: {e.context}")
        logger.error(f"Request ID: {e.context.request_id}")
        
    if e.original_error:
        logger.error(f"Original: {e.original_error}")
        
    # Re-raise or handle
    raise
    
finally:
    client.close_sync()
```

### 4. Validate Parameters Before API Calls

```python
from blossom_ai import Blossom, ValidationError

client = Blossom(api_version="v2", api_token="token")

def validate_and_generate(prompt, quality="medium"):
    # Client-side validation
    valid_qualities = ["low", "medium", "high", "hd"]
    
    if quality not in valid_qualities:
        raise ValidationError(
            message=f"Invalid quality: {quality}",
            suggestion=f"Use one of: {', '.join(valid_qualities)}"
        )
    
    if len(prompt) > 200:
        raise ValidationError(
            message=f"Prompt too long: {len(prompt)} chars",
            suggestion="Shorten your prompt to 200 characters or less"
        )
    
    # API call
    try:
        return client.image.generate(prompt, quality=quality)
    finally:
        client.close_sync()

# Usage
try:
    image = validate_and_generate("sunset", quality="hd")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

### 5. Handle V1/V2 Differences

```python
from blossom_ai import Blossom, BlossomError

def generate_with_fallback(prompt, api_token=None):
    """Try V2, fallback to V1 if needed"""
    
    # Try V2 first
    try:
        with Blossom(api_version="v2", api_token=api_token) as client:
            return client.text.generate(
                prompt,
                max_tokens=200,
                frequency_penalty=0.5
            )
    except BlossomError as e:
        print(f"V2 failed: {e.message}")
        print("Falling back to V1...")
        
        # Fallback to V1 (no advanced parameters)
        try:
            with Blossom(api_version="v1") as client:
                return client.text.generate(prompt)
        except BlossomError as e2:
            print(f"V1 also failed: {e2.message}")
            raise

# Usage
try:
    result = generate_with_fallback("Explain quantum computing")
    print(result)
except BlossomError as e:
    print(f"Both V1 and V2 failed: {e.message}")
```

### 6. Async Error Handling

```python
import asyncio
from blossom_ai import Blossom, BlossomError, RateLimitError

async def async_generate_with_retry(prompt, max_retries=3):
    async with Blossom(api_version="v2", api_token="token") as client:
        for attempt in range(max_retries):
            try:
                return await client.text.generate(
                    prompt,
                    max_tokens=150
                )
                
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = e.retry_after or 60
                    print(f"Rate limited. Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
                    
            except BlossomError as e:
                print(f"Error on attempt {attempt + 1}: {e.message}")
                if attempt == max_retries - 1:
                    raise

# Usage
async def main():
    try:
        result = await async_generate_with_retry("Explain AI")
        print(result)
    except BlossomError as e:
        print(f"All attempts failed: {e.message}")

asyncio.run(main())
```

---

## 🆘 Common Error Scenarios

### Scenario 1: Network Issues

```python
from blossom_ai import Blossom, NetworkError

try:
    with Blossom(api_version="v2", api_token="token", timeout=10) as client:
        image = client.image.generate("sunset")
        
except NetworkError as e:
    print(f"Network error: {e.message}")
    print("Troubleshooting:")
    print("1. Check your internet connection")
    print("2. Try increasing timeout")
    print("3. Check firewall settings")
```

### Scenario 2: Invalid Model Name

```python
from blossom_ai import Blossom, ValidationError

client = Blossom(api_version="v2", api_token="token")

try:
    # Check available models first
    available = client.text.models()
    print(f"Available models: {available}")
    
    response = client.text.generate(
        "test",
        model="invalid_model"  # Wrong model name
    )
    
except ValidationError as e:
    print(f"Invalid model: {e.message}")
    print(f"Available: {available}")
    
finally:
    client.close_sync()
```

### Scenario 3: Token Expiration

```python
from blossom_ai import Blossom, AuthenticationError

def refresh_token_and_retry(prompt, old_token):
    """Handle token expiration"""
    try:
        with Blossom(api_version="v2", api_token=old_token) as client:
            return client.text.generate(prompt)
            
    except AuthenticationError as e:
        print(f"Token expired: {e.message}")
        print("Get new token from: https://enter.pollinations.ai")
        
        # In production: implement token refresh logic here
        # new_token = refresh_token_from_service()
        # return retry_with_new_token(prompt, new_token)
        
        raise
```

---

## 🔗 Related Documentation

- **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)** - Migrate from V1 to V2
- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API documentation
- **[Resource Management](RESOURCE_MANAGEMENT.md)** - Best practices for cleanup

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>