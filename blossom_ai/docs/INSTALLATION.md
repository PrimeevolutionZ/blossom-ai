# Installation & Setup

This guide will help you install and set up the Blossom AI Python SDK.

## 📦 Installation

Blossom AI is available on PyPI and can be easily installed using `pip`.

```bash
pip install eclips-blossom-ai
```

### Upgrading to v0.4.5

If you're upgrading from an earlier version:

```bash
pip install --upgrade eclips-blossom-ai
```

**What's new in v0.4.5:**
- ⚡ 100x faster imports
- 🔐 Enhanced security (tokens in headers only)
- 📉 19x less memory usage
- ✅ Comprehensive testing

## 🚀 Quick Setup

After installation, you can start using the SDK immediately.

### Basic Initialization

The most basic way to initialize the client is without any arguments.

```python
from blossom_ai import Blossom

# Initialize the client
ai = Blossom()
```

### Using a Context Manager (Recommended)

For proper resource management, especially in long-running applications, it is highly recommended to use the client with a context manager (`with` or `async with`).

```python
from blossom_ai import Blossom

with Blossom() as ai:
    # Your code here
    url = ai.image.generate_url("a beautiful sunset")
    print(url)
# The client session is automatically closed when exiting the 'with' block
```

### Providing an API Token

For features like **Audio Generation** or better rate limits with V2 API, you will need to provide an API token.

```python
from blossom_ai import Blossom

# Replace "YOUR_TOKEN" with your actual Pollinations.AI API token
ai = Blossom(api_token="YOUR_TOKEN")

# Now you can access token-required features
# ai.audio.save(...)
```

## 🔐 Secure Token Management

**v0.4.5+** enforces secure token handling. Follow these best practices:

### Using Environment Variables (Recommended)

```bash
# Set environment variable (Linux/Mac)
export POLLINATIONS_API_KEY="your_token_here"

# Or add to .env file
echo "POLLINATIONS_API_KEY=your_token_here" >> .env
```

```python
import os
from blossom_ai import Blossom

# Load from environment
api_token = os.getenv('POLLINATIONS_API_KEY')
client = Blossom(api_token=api_token)
```

### Getting an API Token

1. Visit [enter.pollinations.ai](https://enter.pollinations.ai)
2. Create an account or sign in
3. Generate an API key (Secret or Publishable)
4. Store securely in environment variable

**Token Types:**
- **Secret Keys (`sk_...`)**: Best rate limits, server-side only
- **Publishable Keys (`pk_...`)**: IP-based limits, client-side safe

## 🎯 API Version Selection

Blossom AI supports both V1 (legacy) and V2 (new) APIs.

### V1 API (Legacy)

```python
from blossom_ai import Blossom

# Default: uses V1 API
client = Blossom()

# Or explicitly specify
client = Blossom(api_version="v1")
```

### V2 API (Recommended for New Projects)

```python
from blossom_ai import Blossom

# Use V2 with token
client = Blossom(
    api_version="v2",
    api_token="your_token"
)
```

**V2 Benefits:**
- HD quality images
- Advanced text parameters
- Function calling
- Better rate limits

See [V2 Migration Guide](V2_MIGRATION_GUIDE.md) for details.

## 🧪 Verify Installation

Test that everything is working correctly:

```python
from blossom_ai import Blossom

def verify_installation():
    """Quick health check"""
    try:
        with Blossom() as ai:
            # Test image URL generation (V1 - no token needed)
            url = ai.image.generate_url("test")
            assert url.startswith("https://")
            
            # Test text generation
            text = ai.text.generate("Say hello in 3 words")
            assert len(text) > 0
            
            print("✅ Installation verified successfully!")
            print(f"Image URL: {url}")
            print(f"Text response: {text}")
            return True
            
    except Exception as e:
        print(f"❌ Installation verification failed: {e}")
        return False

verify_installation()
```

## 🔧 Development Setup

For contributors or advanced users who want to run tests:

### Install Test Dependencies

```bash
# Install package with test dependencies
pip install eclips-blossom-ai

# Install additional test tools
pip install pytest pytest-asyncio vcrpy

# Optional: install development tools
pip install black ruff mypy
```

### Run Tests

**v0.4.5+ includes integration tests:**

```bash
# Set API token for tests
export POLLINATIONS_API_KEY="your_token"

# Run integration tests
pytest tests/test_integration.py -v

# Run specific test
pytest tests/test_integration.py::test_text_generate_simple -v

# Run with coverage
pytest tests/test_integration.py --cov=blossom_ai
```

**First run:** Records API responses (cassettes)  
**Subsequent runs:** Uses cached responses (instant)

### Update Test Cassettes

```bash
# Re-record all API interactions
pytest tests/test_integration.py --record-mode=rewrite
```

## ⚙️ Configuration Options

### Basic Configuration

```python
from blossom_ai import Blossom

client = Blossom(
    api_version="v2",       # API version: "v1" or "v2"
    api_token="token",      # API token (optional)
    timeout=30,             # Request timeout in seconds
    debug=False             # Enable debug logging
)
```

### Advanced Configuration

```python
from blossom_ai import Blossom
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = Blossom(
    api_version="v2",
    api_token="token",
    timeout=60,             # Longer timeout for slow connections
    debug=True              # Detailed logging
)
```

## 🐍 Python Version Requirements

- **Minimum**: Python 3.9+
- **Recommended**: Python 3.10+
- **Tested on**: Python 3.9, 3.10, 3.11, 3.12, 3.13

```bash
# Check Python version
python --version
```

## 📦 Dependencies

Blossom AI has minimal dependencies:

- `requests` - HTTP library for synchronous requests
- `aiohttp` - HTTP library for async requests

**Optional (for testing):**
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `vcrpy` - HTTP interaction recording

## 🔍 Troubleshooting

### Import Error

```bash
ImportError: No module named 'blossom_ai'
```

**Solution:**
```bash
pip install eclips-blossom-ai
# Make sure you're in the correct virtual environment
```

### SSL Certificate Error

```python
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solution (v0.4.5+):**
SSL verification is enforced for security. If you're behind a corporate proxy:

```bash
# Update certificates (Linux/Mac)
pip install --upgrade certifi

# Or use system certificates
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

### Connection Timeout

```python
requests.exceptions.Timeout: HTTPSConnectionPool
```

**Solution:**
```python
# Increase timeout
client = Blossom(timeout=60)  # 60 seconds
```

### Rate Limit Error

```python
blossom_ai.core.errors.RateLimitError: Rate limit exceeded
```

**Solution:**
1. Get an API token for better limits
2. Wait for retry_after period
3. Implement exponential backoff

```python
from blossom_ai import Blossom, RateLimitError
import time

client = Blossom(api_token="token")

try:
    result = client.text.generate("test")
except RateLimitError as e:
    if e.retry_after:
        print(f"Waiting {e.retry_after}s...")
        time.sleep(e.retry_after)
```

### Memory Issues (v0.4.4 and earlier)

If using a version before v0.4.5:

```bash
# Upgrade to v0.4.5+ for memory leak fixes
pip install --upgrade eclips-blossom-ai
```

## 📚 Next Steps

Now that you have Blossom AI installed:

- **[Quick Start Guide](INDEX.md)** - Learn the basics
- **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)** - Upgrade to V2 API
- **[Examples](EXAMPLES.md)** - Practical code examples
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors properly
- **[Security Guide](../../SECURITY.md)** - Security best practices

## 💡 Tips

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install in virtual environment
pip install eclips-blossom-ai
```

### Docker

```dockerfile
FROM python:3.11-slim

# Install Blossom AI
RUN pip install eclips-blossom-ai

# Copy your code
COPY . /app
WORKDIR /app

# Set API token
ENV POLLINATIONS_API_KEY="your_token"

# Run your app
CMD ["python", "app.py"]
```

### Requirements File

```bash
# Create requirements.txt
echo "eclips-blossom-ai>=0.4.5" > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## 🆘 Getting Help

- 📖 [Documentation](INDEX.md)
- 🐛 [Report Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 [Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 [Security Policy](../../SECURITY.md)

---

<div align="center">

**Ready to start?** Check out the [Quick Start Guide](INDEX.md)!

Made with 🌸 by the Blossom AI Team

</div>