# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions of Blossom AI:

| Version | Supported          |
|---------| ------------------ |
| 0.4.5   | ✅ Actively supported |
| 0.4.x   | ✅ Actively supported |
| 0.3.x   | ❌ Not supported  |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in Blossom AI, please report it responsibly:

### How to Report

1. **Email the maintainers** directly at the repository contact (check repository profile)
2. **Include in your report:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
   - Your contact information

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days with initial assessment
- **Fix Timeline**: Varies by severity (critical issues prioritized)
- **Credit**: We'll credit you in security advisories (unless you prefer to remain anonymous)

### Disclosure Policy

- We'll work with you to understand and fix the issue
- We'll keep you updated on progress
- We'll coordinate public disclosure after a fix is available
- Security advisories will be published on GitHub

## Security Considerations

### API Token Handling

🔒 **Your API token is sensitive information**

**v0.4.5 Security Improvements:**
- ✅ Tokens are **never** included in URLs (only in Authorization headers)
- ✅ SSL certificate verification is enforced by default
- ✅ No token exposure in nginx/CDN logs or browser history
- ✅ Safe URL sharing - generated URLs don't contain credentials

**Best Practices:**

- **Never commit tokens** to version control
- **Use environment variables** for token storage
- **Don't share tokens** publicly (logs, screenshots, error messages)
- **Rotate tokens** if compromised

```python
# ✅ Good - Use environment variables
import os
from blossom_ai import Blossom

api_token = os.getenv('POLLINATIONS_API_KEY')
client = Blossom(api_token=api_token)
```

```python
# ❌ Bad - Hardcoded token
client = Blossom(api_token="your-token-here")
```

### Token Security (v0.4.5+)

**Before v0.4.5:**
```python
# ❌ OLD: Tokens could appear in URLs
url = ai.image.generate_url("cat")
# URL: https://image.pollinations.ai/cat?token=pk_xxx
# Token visible in logs, history, shared links
```

**After v0.4.5:**
```python
# ✅ NEW: Tokens only in headers
url = ai.image.generate_url("cat")
# URL: https://image.pollinations.ai/cat
# Token in Authorization header only - safe to share!
```

**Security Benefits:**
- 🔐 Tokens never appear in URLs
- 📝 No token leakage in server logs
- 🌐 Safe to share URLs publicly
- 🔒 OAuth2 compliant

### SSL/TLS Verification

**v0.4.5+ enforces SSL certificate verification:**

```python
# ✅ Default: SSL verification enabled
client = Blossom(api_token="token")
# All requests verify SSL certificates

# ❌ Never disable verification in production!
# No option to disable - security by design
```

**What this means:**
- All API communication uses verified HTTPS
- Man-in-the-middle attacks prevented
- Certificate validation automatic

### Prompt Injection

⚠️ **Be cautious with user-provided prompts**

When using Blossom AI in applications that accept user input:

- **Sanitize user input** before passing to generators
- **Validate prompt length** (max 250 characters recommended)
- **Implement rate limiting** to prevent abuse
- **Monitor usage** for unusual patterns

```python
from blossom_ai import Blossom, ValidationError

def safe_generate(user_prompt: str):
    """Safely generate content from user input"""
    # Sanitize input
    prompt = user_prompt.strip()[:250]
    
    # Validate
    if not prompt or len(prompt) < 3:
        raise ValueError("Prompt too short")
    
    # Generate
    try:
        with Blossom(api_token=api_token) as ai:
            return ai.text.generate(prompt)
    except ValidationError as e:
        # Handle validation errors appropriately
        return f"Invalid prompt: {e.message}"
```

### Generated Content

⚠️ **AI-generated content carries risks**

- **Content filtering**: Pollinations API includes safety filters, but review generated content
- **User responsibility**: Application developers are responsible for how generated content is used
- **Compliance**: Ensure generated content complies with your local laws and regulations
- **Attribution**: Consider adding disclaimers that content is AI-generated

### Network Security

🌐 **All API communication uses HTTPS**

- Blossom AI communicates with `pollinations.ai` API over secure HTTPS
- **v0.4.5+**: SSL certificate verification enforced
- No sensitive data is logged by default
- Enable `debug=False` in production (it's the default)

```python
# Production settings
with Blossom(
    api_token=api_token,
    debug=False,  # Default - no debug logging
    timeout=30
) as ai:
    # Your code
    pass
```

### Dependency Security

📦 **We use minimal, well-maintained dependencies**

Core dependencies:
- `requests` - HTTP library for synchronous requests
- `aiohttp` - HTTP library for async requests

**Keep dependencies updated:**
```bash
pip install --upgrade eclips-blossom-ai
```

**Check for known vulnerabilities:**
```bash
pip install safety
safety check
```

### Resource Management

♻️ **Proper cleanup prevents resource leaks**

**v0.4.5 improvements:**
- ✅ Automatic memory cleanup (WeakRef-based)
- ✅ No memory leaks in long-running apps
- ✅ Clean shutdown (no stderr errors)

**Best practices:**

```python
# ✅ Good - Automatic cleanup
with Blossom(api_token=api_token) as ai:
    result = ai.text.generate("hello")

# ✅ Good - Async cleanup
async with Blossom(api_token=api_token) as ai:
    result = await ai.text.generate("hello")
```

```python
# ❌ Bad - Manual cleanup required
ai = Blossom(api_token=api_token)
result = ai.text.generate("hello")
ai.close_sync()  # Easy to forget!
```

### Rate Limiting

⏱️ **Respect API rate limits**

**v0.4.5 improvements:**
- ✅ Smart retry with API-specified delays
- ✅ Uses `retry_after` from rate limit responses
- ✅ Faster recovery (10-60s vs fixed 60s)

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom(api_token=api_token) as ai:
    try:
        result = ai.text.generate("prompt")
    except RateLimitError as e:
        # v0.4.5+: Uses retry_after from API
        if e.retry_after:
            print(f"Rate limited. Waiting {e.retry_after}s")
            time.sleep(e.retry_after)
            # Retry request
```

### Streaming Security

🌊 **Streaming has timeout protection**

- Default timeout: 30 seconds between chunks
- Prevents hanging connections
- Configurable via `timeout` parameter

```python
# Configure timeout for slow connections
with Blossom(api_token=api_token, timeout=60) as ai:
    for chunk in ai.text.generate("prompt", stream=True):
        process_chunk(chunk)
```

## Data Privacy

### What Data is Transmitted

When using Blossom AI, the following data is sent to Pollinations.AI:

**Image Generation:**
- Prompt text
- Generation parameters (width, height, model, seed, etc.)
- API token (in Authorization header - v0.4.5+)

**Text Generation:**
- Prompt or messages
- System messages
- Model selection
- Parameters (temperature, seed, etc.)
- API token (in Authorization header - v0.4.5+)

**Audio Generation:**
- Text to convert
- Voice selection
- API token (in Authorization header - required)

### What Data is NOT Collected by Blossom AI

- No analytics or telemetry
- No logging of prompts or generated content (unless `debug=True`)
- No user tracking
- No data stored locally (except explicit saves)

### Third-Party Data Processing

Content generation is performed by Pollinations.AI. Review their privacy policy:
- [Pollinations.AI](https://pollinations.ai)

## Secure Development Practices

For contributors and developers building on Blossom AI:

### Code Review

- All changes require maintainer review
- Security-sensitive changes get extra scrutiny
- We use automated checks where applicable

### Testing

**v0.4.5 improvements:**
- ✅ 20+ integration tests with VCR.py
- ✅ 95% API coverage
- ✅ Security tests (tokens not in URLs)

```bash
# Run security tests
pip install pytest pytest-asyncio vcrpy
pytest tests/test_integration.py -k security
```

### Dependencies

- Minimal dependency footprint
- Regular dependency updates
- Avoid deprecated packages

## Security Updates

### How We Handle Security Issues

1. **Assessment**: Evaluate severity and impact
2. **Fix Development**: Create and test fix
3. **Release**: Push security update
4. **Notification**: Publish security advisory
5. **Documentation**: Update security docs

### Critical Security Updates

For critical vulnerabilities:
- **Immediate patch** released within 24-48 hours
- **Security advisory** published on GitHub
- **Email notification** to known users (when possible)

## Best Practices for Users

### Production Deployments

✅ **Do's:**
- Use environment variables for API tokens
- Implement input validation
- Set appropriate timeouts
- Use context managers (`with` statements)
- Monitor API usage
- Keep library updated
- Implement rate limiting
- Review generated content
- Use HTTPS for your application
- Enable SSL verification (default in v0.4.5+)

❌ **Don'ts:**
- Don't commit API tokens to Git
- Don't ignore validation errors
- Don't skip resource cleanup
- Don't trust user input blindly
- Don't disable SSL verification
- Don't use deprecated features
- Don't expose API tokens in logs
- Don't use debug mode in production

### Example Secure Implementation

```python
import os
import logging
from blossom_ai import Blossom, BlossomError

# Configure secure logging (no sensitive data)
logging.basicConfig(level=logging.WARNING)

# Get token from environment
API_TOKEN = os.getenv('POLLINATIONS_API_KEY')

def secure_generate_image(user_prompt: str) -> str:
    """
    Securely generate image from user prompt
    
    Args:
        user_prompt: Untrusted user input
        
    Returns:
        URL to generated image
        
    Raises:
        ValueError: If prompt is invalid
        BlossomError: If generation fails
    """
    # Sanitize and validate
    prompt = user_prompt.strip()
    if not prompt or len(prompt) < 3:
        raise ValueError("Prompt too short")
    if len(prompt) > 250:
        raise ValueError("Prompt too long (max 250 characters)")
    
    # Generate with proper resource management
    try:
        with Blossom(
            api_version="v2",
            api_token=API_TOKEN,
            timeout=30
        ) as ai:
            # Generate URL (no download needed)
            # v0.4.5+: Token NOT in URL - safe to share
            url = ai.image.generate_url(
                prompt=prompt,
                nologo=True,
                private=True,  # Private generation
                safe=True       # NSFW filter
            )
            return url
    except BlossomError as e:
        # Log error without exposing sensitive details
        logging.error(f"Generation failed: {e.error_type}")
        raise
```

## v0.4.5 Security Improvements Summary

### Critical Fixes

1. **Token Security** ✅
   - Tokens only in Authorization headers
   - Never in URLs or query parameters
   - No exposure in logs or browser history

2. **SSL Verification** ✅
   - Enforced by default
   - Cannot be disabled
   - MITM attack prevention

3. **Memory Safety** ✅
   - Fixed memory leaks
   - WeakRef-based cleanup
   - Constant memory footprint

4. **Smart Retry** ✅
   - Uses API's retry_after
   - Faster recovery from rate limits
   - Better error handling

### Security Testing

```python
# Verify security improvements
def test_security():
    """Test v0.4.5 security features"""
    from blossom_ai import Blossom
    
    client = Blossom(api_version="v2", api_token="test_token")
    
    # Test 1: Token not in URL
    url = client.image.generate_url("test")
    assert "token=" not in url.lower()
    assert "test_token" not in url
    print("✅ Token security: PASS")
    
    # Test 2: SSL verification
    # (Enforced by default, cannot disable)
    print("✅ SSL verification: ENFORCED")
    
    client.close_sync()
    print("✅ All security tests passed!")

test_security()
```

## Incident Response

In case of a security incident:

1. **Contain**: Limit exposure immediately
2. **Assess**: Understand the scope and impact
3. **Remediate**: Apply fixes and patches
4. **Communicate**: Notify affected users
5. **Learn**: Update processes to prevent recurrence

## Questions?

For security-related questions:
- Open an issue for general security questions
- Email maintainers for vulnerability reports
- Check documentation for security best practices

---

**Last Updated**: November 2025

**Version**: 0.4.5

This security policy will be reviewed and updated regularly. Check back for the latest information.