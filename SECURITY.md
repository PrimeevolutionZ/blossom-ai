# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions of Blossom AI:

| Version | Supported          |
|---------|-------------------|
| 0.5.0   | ✅ Actively supported |
| < 0.5.0 | ❌ Not supported  |

**Note:** Only v0.5.0 is currently supported. Previous versions have been deprecated due to significant API changes and security improvements.

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

---

## Security Considerations

### API Token Handling

🔒 **Your API token is sensitive information**

**v0.5.0 Security Features:**
- ✅ Tokens are **never** included in URLs (only in Authorization headers)
- ✅ SSL certificate verification is enforced by default
- ✅ No token exposure in nginx/CDN logs or browser history
- ✅ Safe URL sharing - generated URLs don't contain credentials
- ✅ OAuth2 compliant authentication flow

**Best Practices:**

```python
# ✅ Good - Use environment variables
import os
from blossom_ai import Blossom

api_token = os.getenv('POLLINATIONS_API_KEY')
client = Blossom(api_token=api_token)
```

```python
# ❌ Bad - Hardcoded token
client = Blossom(api_token="pk_your-token-here")
```

**Security Checklist:**
- ✅ Never commit tokens to version control
- ✅ Use environment variables for token storage
- ✅ Don't share tokens publicly (logs, screenshots, error messages)
- ✅ Rotate tokens if compromised
- ✅ Use different tokens for development and production

### Token Security (v0.5.0)

**Secure by Design:**
```python
# ✅ Tokens only in headers
client = Blossom(api_token="token")
url = client.image.generate_url("cat")
# URL: https://image.pollinations.ai/cat
# Token in Authorization header only - safe to share!
```

**Security Benefits:**
- 🔒 Tokens never appear in URLs
- 📝 No token leakage in server logs
- 🌐 Safe to share URLs publicly
- 🔐 OAuth2 compliant
- 🛡️ No exposure in browser history

### SSL/TLS Verification

**v0.5.0 enforces SSL certificate verification:**

```python
# ✅ Default: SSL verification enabled
client = Blossom(api_token="token")
# All requests verify SSL certificates

# ❌ No option to disable - security by design
```

**What this means:**
- All API communication uses verified HTTPS
- Man-in-the-middle attacks prevented
- Certificate validation automatic
- No insecure connections allowed

---

## Input Validation & Prompt Safety

### Prompt Injection

⚠️ **Be cautious with user-provided prompts**

When using Blossom AI in applications that accept user input:

```python
from blossom_ai import Blossom, ValidationError

def safe_generate(user_prompt: str):
    """Safely generate content from user input"""
    # Sanitize input
    prompt = user_prompt.strip()[:250]  # Max 250 chars
    
    # Validate
    if not prompt or len(prompt) < 3:
        raise ValueError("Prompt too short")
    
    # Remove potentially harmful characters
    prompt = ''.join(c for c in prompt if c.isprintable())
    
    # Generate
    try:
        with Blossom(api_token=api_token) as client:
            return client.text.generate(prompt)
    except ValidationError as e:
        # Handle validation errors appropriately
        return f"Invalid prompt: {e.message}"
```

**Best Practices:**
- ✅ Sanitize user input before passing to generators
- ✅ Validate prompt length (max 250 characters for images)
- ✅ Implement rate limiting to prevent abuse
- ✅ Monitor usage for unusual patterns
- ✅ Filter special characters and control sequences
- ✅ Log suspicious requests for review

### Vision Input Validation

**When accepting image uploads:**

```python
from blossom_ai import Blossom, MessageBuilder
import magic  # python-magic library

def safe_analyze_image(image_path: str, user_prompt: str):
    """Safely analyze user-uploaded images"""
    # Validate file type
    mime = magic.from_file(image_path, mime=True)
    if mime not in ['image/jpeg', 'image/png', 'image/webp']:
        raise ValueError("Invalid image format")
    
    # Check file size (max 10MB)
    import os
    if os.path.getsize(image_path) > 10 * 1024 * 1024:
        raise ValueError("File too large")
    
    # Sanitize prompt
    prompt = user_prompt.strip()[:500]
    
    with Blossom(api_token=api_token) as client:
        messages = [
            MessageBuilder.image(
                role="user",
                text=prompt,
                image_path=image_path,
                detail="low"  # Start with low detail for safety
            )
        ]
        return client.text.chat(messages, model="openai")
```

---

## Generated Content Safety

### Content Filtering

⚠️ **AI-generated content carries risks**

**Pollinations API Safety:**
- Built-in content filters for harmful content
- NSFW detection (when `safe=True` parameter used)
- Automatic rejection of violating requests

**Your Responsibility:**
- ✅ Review generated content before display
- ✅ Implement additional filtering if needed
- ✅ Add content warnings for sensitive topics
- ✅ Comply with local laws and regulations
- ✅ Add disclaimers that content is AI-generated

```python
# Enable safe mode for image generation
with Blossom(api_token="token") as client:
    url = client.image.generate_url(
        user_prompt,
        safe=True,  # Enable NSFW filter
        private=True  # Private generation
    )
```

### Attribution & Compliance

**Legal Considerations:**
- 📋 Consider adding disclaimers that content is AI-generated
- ⚖️ Ensure compliance with your local laws
- 📝 Review content policies for your platform
- 👥 Respect user privacy and data protection laws

---

## Network Security

### HTTPS Enforcement

🌐 **All API communication uses HTTPS**

- Blossom AI communicates with `pollinations.ai` API over secure HTTPS
- **v0.5.0**: SSL certificate verification enforced (cannot be disabled)
- No sensitive data is logged by default
- Secure by design - no configuration needed

```python
# Production settings (secure by default)
with Blossom(
    api_token=api_token,
    timeout=30  # Connection timeout
) as client:
    # All requests automatically use HTTPS with SSL verification
    result = client.text.generate("prompt")
```

### Connection Security

**Built-in Protection:**
- ✅ SSL/TLS 1.2+ required
- ✅ Certificate validation enforced
- ✅ Secure cipher suites only
- ✅ No downgrade attacks possible
- ✅ Connection pooling with security

---

## Dependency Security

### Core Dependencies

🔦 **We use minimal, well-maintained dependencies**

Core dependencies:
- `requests` - HTTP library for synchronous requests
- `aiohttp` - HTTP library for async requests
- `pydantic` - Data validation

**Keep dependencies updated:**
```bash
pip install --upgrade eclips-blossom-ai
```

**Check for vulnerabilities:**
```bash
pip install safety
safety check --json
```

**Audit dependencies:**
```bash
pip install pip-audit
pip-audit
```

---

## Resource Management

### Memory Safety

♻️ **Proper cleanup prevents resource leaks**

**v0.5.0 improvements:**
- ✅ Automatic memory cleanup (WeakRef-based)
- ✅ No memory leaks in long-running apps
- ✅ Clean shutdown (no stderr errors)
- ✅ Connection pooling with limits

**Best practices:**

```python
# ✅ Good - Automatic cleanup
with Blossom(api_token=api_token) as client:
    result = client.text.generate("hello")

# ✅ Good - Async cleanup
async with Blossom(api_token=api_token) as client:
    result = await client.text.generate("hello")
```

```python
# ❌ Bad - Manual cleanup required (easy to forget!)
client = Blossom(api_token=api_token)
result = client.text.generate("hello")
client.close_sync()  # Must remember to call!
```

### Rate Limiting

⏱️ **Respect API rate limits**

**v0.5.0 improvements:**
- ✅ Smart retry with API-specified delays
- ✅ Uses `retry_after` from rate limit responses
- ✅ Exponential backoff for retries
- ✅ Automatic handling of 429 responses

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom(api_token=api_token) as client:
    try:
        result = client.text.generate("prompt")
    except RateLimitError as e:
        # v0.5.0: Uses retry_after from API
        if e.retry_after:
            print(f"Rate limited. Waiting {e.retry_after}s")
            time.sleep(e.retry_after)
            # Retry request
            result = client.text.generate("prompt")
```

---

## Vision Security (NEW in v0.5.0)

### Image Upload Safety

**When handling user-uploaded images:**

```python
import hashlib
from pathlib import Path

def safe_image_upload(file_content: bytes, user_id: str):
    """Securely handle image uploads"""
    # Verify file type by magic bytes
    if not file_content.startswith(b'\xff\xd8\xff'):  # JPEG
        if not file_content.startswith(b'\x89PNG'):     # PNG
            raise ValueError("Invalid image format")
    
    # Limit file size (10MB)
    if len(file_content) > 10 * 1024 * 1024:
        raise ValueError("File too large")
    
    # Generate safe filename
    file_hash = hashlib.sha256(file_content).hexdigest()
    safe_name = f"{user_id}_{file_hash[:16]}.jpg"
    
    # Save to secure location
    upload_dir = Path("/secure/uploads")
    upload_dir.mkdir(exist_ok=True, mode=0o700)
    
    file_path = upload_dir / safe_name
    file_path.write_bytes(file_content)
    
    return str(file_path)
```

### Privacy Considerations

**Vision API Privacy:**
- 🔒 Images sent to API are processed server-side
- ⏰ Consider data retention policies
- 🚫 Don't send sensitive personal data
- 🔐 Use `private=True` for sensitive images

```python
# Private image analysis (requires token)
with Blossom(api_token="token") as client:
    messages = [
        MessageBuilder.image(
            role="user",
            text="Analyze this medical image",
            image_path=secure_path,
            detail="high"
        )
    ]
    
    # Private request - not cached on server
    result = client.text.chat(
        messages,
        model="openai"
    )
```

---

## Production Deployment Security

### Environment Configuration

```bash
# .env file (never commit!)
POLLINATIONS_API_KEY=your_secret_token_here
API_KEYS=key1,key2,key3
ALLOWED_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
```

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pollinations_api_key: str
    api_keys: str
    allowed_origins: str = "https://yourdomain.com"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Use in application
client = Blossom(api_token=settings.pollinations_api_key)
```

### Docker Security

**Secure Dockerfile:**

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx Security Headers

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For streaming
        proxy_buffering off;
        proxy_cache off;
    }
}
```

---

## Security Best Practices

### Development

✅ **Do:**
- Use environment variables for secrets
- Enable SSL verification (default)
- Implement input validation
- Set appropriate timeouts
- Use context managers (`with` statements)
- Monitor API usage
- Keep library updated
- Implement rate limiting
- Review generated content
- Test security regularly

❌ **Don't:**
- Commit API tokens to Git
- Disable SSL verification
- Trust user input blindly
- Ignore validation errors
- Skip resource cleanup
- Use deprecated features
- Expose API tokens in logs
- Store sensitive data insecurely

### Production Checklist

**Before Deploying:**

- [ ] API tokens in environment variables (not code)
- [ ] SSL/TLS enabled and enforced
- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] Error handling comprehensive
- [ ] Logging properly configured (no sensitive data)
- [ ] CORS configured restrictively
- [ ] Security headers added
- [ ] Dependencies up to date
- [ ] Security audit completed
- [ ] Monitoring and alerts set up
- [ ] Backup and recovery plan
- [ ] Incident response plan

---

## Example Secure Implementation

### Complete Secure Web API

```python
import os
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from blossom_ai import Blossom, BlossomError, MessageBuilder
from pydantic import BaseModel, Field
import logging

# Configure logging (no sensitive data)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_TOKEN = os.getenv('POLLINATIONS_API_KEY')
ALLOWED_API_KEYS = set(os.getenv('API_KEYS', '').split(','))

if not API_TOKEN:
    raise ValueError("POLLINATIONS_API_KEY required")

app = FastAPI(title="Secure Blossom AI API")

# CORS (restrictive)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)

# Authentication
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in ALLOWED_API_KEYS:
        logger.warning(f"Invalid API key attempted")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Request models
class SecureTextRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=500)
    max_tokens: int = Field(default=200, ge=1, le=1000)

class SecureImageRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=250)
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)

# Endpoints
@app.post("/api/text/generate")
async def generate_text(
    request: SecureTextRequest,
    api_key: str = Depends(verify_api_key)
):
    """Securely generate text"""
    try:
        # Sanitize input
        prompt = request.prompt.strip()
        
        async with Blossom(api_token=API_TOKEN) as client:
            response = await client.text.generate(
                prompt,
                max_tokens=request.max_tokens
            )
            
        logger.info(f"Text generated successfully")
        return {"response": response}
        
    except BlossomError as e:
        logger.error(f"Generation error: {e.error_type}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/image/generate")
async def generate_image(
    request: SecureImageRequest,
    api_key: str = Depends(verify_api_key)
):
    """Securely generate image"""
    try:
        prompt = request.prompt.strip()
        
        async with Blossom(api_token=API_TOKEN) as client:
            url = await client.image.generate_url(
                prompt,
                width=request.width,
                height=request.height,
                safe=True,  # Enable NSFW filter
                private=True,
                nologo=True
            )
        
        logger.info(f"Image generated successfully")
        return {"url": url}
        
    except BlossomError as e:
        logger.error(f"Generation error: {e.error_type}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Public health check"""
    return {"status": "healthy", "version": "0.5.0"}
```

---

## Security Updates & Monitoring

### Stay Informed

- 📧 Watch the GitHub repository for security advisories
- 📢 Subscribe to release notifications
- 🔍 Regularly check for dependency updates
- 📊 Monitor application logs for suspicious activity

### Update Process

```bash
# Check current version
pip show eclips-blossom-ai

# Update to latest
pip install --upgrade eclips-blossom-ai

# Verify update
python -c "import blossom_ai; print(blossom_ai.__version__)"
```

### Security Monitoring

```python
import logging
from blossom_ai import Blossom, BlossomError

# Configure security logging
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.WARNING)

def monitored_generate(prompt: str):
    """Generate with security monitoring"""
    try:
        with Blossom(api_token=api_token) as client:
            return client.text.generate(prompt)
    except BlossomError as e:
        security_logger.warning(
            f"Generation error: {e.error_type}",
            extra={'prompt_length': len(prompt)}
        )
        raise
```

---

## Questions & Support

### For Security Issues

- 🔒 **Private vulnerabilities**: Email maintainers directly
- 📋 **General security questions**: Open a GitHub issue
- 📚 **Best practices**: Check this document and documentation
- 💬 **Community**: Discuss in GitHub Discussions

### Resources

- [Security Policy](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/SECURITY.md)
- [Contributing Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/CONTRIBUTING.md)
- [Documentation](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/INDEX.md)
- [Error Handling Guide](https://github.com/PrimeevolutionZ/blossom-ai/blob/master/blossom_ai/docs/ERROR_HANDLING.md)

---

**Last Updated**: December 2024  
**Version**: 0.5.0

This security policy will be reviewed and updated regularly. Check back for the latest information.

---

<div align="center">

**Made with 🌸 by [Eclips Team](https://github.com/PrimeevolutionZ)**

[Report Security Issue](mailto:security@example.com) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)

</div>