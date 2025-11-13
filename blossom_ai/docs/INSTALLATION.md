# 🔧 Installation & Setup

Complete guide to installing and configuring Blossom AI v0.5.0.

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [API Token Setup](#api-token-setup)
- [Verify Installation](#verify-installation)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Upgrade Guide](#upgrade-guide)
- [Uninstallation](#uninstallation)

---

## 💻 System Requirements

### Python Version

- **Python 3.8 or higher** (recommended: Python 3.10+)
- Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12

### Operating Systems

- ✅ **Linux** (Ubuntu, Debian, CentOS, Fedora, etc.)
- ✅ **macOS** (10.14+ / Mojave or later)
- ✅ **Windows** (10, 11)

### Dependencies

Blossom AI automatically installs these dependencies:

- `requests>=2.31.0` - HTTP client for sync operations
- `aiohttp>=3.9.0` - HTTP client for async operations

All dependencies are automatically managed by pip.

---

## 📦 Installation Methods

### Method 1: Install from PyPI (Recommended)

The easiest way to install Blossom AI:

```bash
pip install eclips-blossom-ai
```

**For specific version:**

```bash
pip install eclips-blossom-ai==0.5.0
```

**Upgrade to latest:**

```bash
pip install --upgrade eclips-blossom-ai
```

### Method 2: Install from GitHub

Install the latest development version:

```bash
pip install git+https://github.com/PrimeevolutionZ/blossom-ai.git
```

**Install specific branch:**

```bash
pip install git+https://github.com/PrimeevolutionZ/blossom-ai.git@main
```

### Method 3: Install from Source

Clone and install manually:

```bash
# Clone repository
git clone https://github.com/PrimeevolutionZ/blossom-ai.git
cd blossom-ai

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Method 4: Using Poetry (for developers)

If you use Poetry for dependency management:

```bash
poetry add eclips-blossom-ai
```

### Method 5: Using Requirements File

Add to your `requirements.txt`:

```text
eclips-blossom-ai>=0.5.0
```

Then install:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Token Setup

### Get Your API Token

1. Visit [Pollinations.AI](https://enter.pollinations.ai)
2. Sign up or log in
3. Navigate to your dashboard
4. Copy your API token

> **Note:** The V2 API requires authentication for most features. Some basic features may work without a token, but you'll have rate limits.

### Configure API Token

You have three options to provide your API token:

#### Option 1: Environment Variable (Recommended)

Set the environment variable in your terminal:

**Linux/macOS:**

```bash
export POLLINATIONS_API_KEY="your-api-token-here"
```

**Windows (Command Prompt):**

```cmd
set POLLINATIONS_API_KEY=your-api-token-here
```

**Windows (PowerShell):**

```powershell
$env:POLLINATIONS_API_KEY="your-api-token-here"
```

**Persistent (Linux/macOS) - Add to `~/.bashrc` or `~/.zshrc`:**

```bash
echo 'export POLLINATIONS_API_KEY="your-api-token-here"' >> ~/.bashrc
source ~/.bashrc
```

**Persistent (Windows) - System Environment Variables:**

1. Open System Properties → Environment Variables
2. Add new User Variable:
   - Name: `POLLINATIONS_API_KEY`
   - Value: `your-api-token-here`

#### Option 2: `.env` File

Create a `.env` file in your project root:

```bash
# .env
POLLINATIONS_API_KEY=your-api-token-here
```

**Load with python-dotenv:**

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()

from blossom_ai import Blossom

# Token is automatically loaded from environment
client = Blossom()
```

#### Option 3: Pass Directly in Code

```python
from blossom_ai import Blossom

client = Blossom(api_token="your-api-token-here")
```

> ⚠️ **Security Warning:** Never commit API tokens to version control. Use environment variables or `.env` files (and add `.env` to `.gitignore`).

### Alternative Token Variable

You can also use `BLOSSOM_API_KEY` instead of `POLLINATIONS_API_KEY`:

```bash
export BLOSSOM_API_KEY="your-api-token-here"
```

The library checks both variables automatically.

---

## ✅ Verify Installation

### Quick Test

Run this simple test to verify everything works:

```python
from blossom_ai import Blossom

# Check version
import blossom_ai
print(f"Blossom AI version: {blossom_ai.__version__}")

# Test basic functionality
with Blossom(api_token="your-token") as client:
    # Test text generation
    response = client.text.generate("Say hello!")
    print(f"✅ Text generation works: {response[:50]}...")
    
    # Test image URL generation (no download)
    url = client.image.generate_url("a test image", width=256, height=256)
    print(f"✅ Image generation works: {url[:50]}...")

print("🎉 Installation successful!")
```

### Run Test Suite

Blossom AI includes a comprehensive test suite:

```bash
# Download test file from repository
wget https://raw.githubusercontent.com/PrimeevolutionZ/blossom-ai/main/blossom_ai/test_examples.py

# Run all tests
python test_examples.py --token YOUR_TOKEN

# Run only sync tests
python test_examples.py --sync --token YOUR_TOKEN

# Run only async tests
python test_examples.py --async --token YOUR_TOKEN

# Run v0.5.0 feature tests (Vision & Audio)
python test_examples.py --v050 --token YOUR_TOKEN
```

### Test CLI Interface

Test the command-line interface:

```bash
# Interactive mode
python -m blossom_ai.utils.cli

# Quick test
python -m blossom_ai.utils.cli --text "Hello world"
```

---

## ⚙️ Configuration

### Global Configuration

Configure default settings globally:

```python
from blossom_ai import Blossom
from blossom_ai.core import Config, Defaults

# Create custom configuration
config = Config()
config.api_token = "your-token"
config.debug = True  # Enable debug logging

# Update defaults
config.defaults = Defaults(
    IMAGE_MODEL="flux",
    TEXT_MODEL="openai",
    IMAGE_WIDTH=1024,
    IMAGE_HEIGHT=1024,
    TEMPERATURE=0.7
)

# Use configuration
client = Blossom(api_token=config.api_token)
```

### Environment Variables

Configure via environment variables:

```bash
# API Configuration
export POLLINATIONS_API_KEY="your-token"
export BLOSSOM_API_KEY="your-token"  # Alternative

# Default Models
export BLOSSOM_IMAGE_MODEL="flux"
export BLOSSOM_TEXT_MODEL="openai"

# Default Parameters
export BLOSSOM_IMAGE_WIDTH=1024
export BLOSSOM_IMAGE_HEIGHT=1024
export BLOSSOM_TEMPERATURE=0.8

# Debug Mode
export BLOSSOM_DEBUG=true
```

### Timeout Settings

Configure timeouts for requests:

```python
from blossom_ai import Blossom

# Custom timeout (in seconds)
client = Blossom(
    api_token="your-token",
    timeout=60  # 60 seconds timeout
)

# For long-running generations
client = Blossom(
    api_token="your-token",
    timeout=120  # 2 minutes
)
```

### Debug Mode

Enable debug logging:

```python
from blossom_ai import Blossom

client = Blossom(
    api_token="your-token",
    debug=True  # Enable debug output
)
```

Or via environment:

```bash
export BLOSSOM_DEBUG=1
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: `ModuleNotFoundError: No module named 'blossom_ai'`

**Solution:**

```bash
# Verify installation
pip list | grep blossom

# Reinstall if needed
pip uninstall eclips-blossom-ai
pip install eclips-blossom-ai
```

#### Issue 2: `ImportError: cannot import name 'Blossom'`

**Possible causes:**
- Old version installed
- Conflicting package name

**Solution:**

```bash
# Uninstall all versions
pip uninstall blossom-ai eclips-blossom-ai -y

# Install latest
pip install eclips-blossom-ai==0.5.0

# Verify
python -c "from blossom_ai import Blossom; print('OK')"
```

#### Issue 3: Authentication Errors

**Error:** `AuthenticationError: Invalid or missing API token`

**Solution:**

1. Check your API token is correct
2. Verify environment variable is set:

```bash
echo $POLLINATIONS_API_KEY
```

3. Try passing token directly:

```python
client = Blossom(api_token="your-token-here")
```

#### Issue 4: SSL/Certificate Errors

**Error:** `SSLError: certificate verify failed`

**Solution:**

```bash
# Update certificates
pip install --upgrade certifi

# Update pip and dependencies
pip install --upgrade pip requests aiohttp
```

#### Issue 5: Timeout Errors

**Error:** `TimeoutError: Request timed out`

**Solution:**

```python
# Increase timeout
client = Blossom(api_token="your-token", timeout=120)

# Or for specific request
client.image.generate("prompt", timeout=60)
```

#### Issue 6: Rate Limit Errors

**Error:** `RateLimitError: Rate limit exceeded`

**Solution:**

- Wait for the specified `retry_after` time
- Upgrade your API plan at [enter.pollinations.ai](https://enter.pollinations.ai)
- Implement caching to reduce requests (see [Caching Guide](CACHING.md))

### Version Conflicts

If you have multiple Python versions:

```bash
# Use specific Python version
python3.10 -m pip install eclips-blossom-ai

# Verify which Python is used
which python
python --version

# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install eclips-blossom-ai
```

### Firewall/Proxy Issues

If you're behind a corporate firewall:

```bash
# Install with proxy
pip install --proxy http://proxy.company.com:8080 eclips-blossom-ai

# Or set environment
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### Getting Help

If issues persist:

1. **Check documentation:** [Error Handling Guide](ERROR_HANDLING.md)
2. **Search issues:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
3. **Report new issue:** [Create Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues/new)
4. **Security issues:** See [Security Policy](../../SECURITY.md)

---

## 🔄 Upgrade Guide

### Upgrading from v0.4.x to v0.5.0

> ⚠️ **Breaking Changes:** v0.5.0 removes V1 API support and introduces breaking changes. See [V1 to V2 Migration Guide](V1_TO_V2_MIGRATION.md).

**Upgrade command:**

```bash
pip install --upgrade eclips-blossom-ai
```

**Key changes:**
- ❌ V1 API removed (`api_version="v1"` no longer works)
- ✅ V2 API is now the default and only option
- ✅ New features: Vision, Audio, Function Calling
- ✅ Improved streaming and error handling

**Migration steps:**

1. **Backup your code:**
   ```bash
   git commit -am "Before upgrading to v0.5.0"
   ```

2. **Upgrade:**
   ```bash
   pip install --upgrade eclips-blossom-ai
   ```

3. **Update imports (if needed):**
   ```python
   # Old (v0.4.x)
   from blossom_ai import Blossom
   client = Blossom(api_version="v1")  # ❌ Will fail
   
   # New (v0.5.0)
   from blossom_ai import Blossom
   client = Blossom()  # ✅ V2 by default
   ```

4. **Test your code:**
   ```bash
   python test_examples.py --token YOUR_TOKEN
   ```

5. **Read migration guide:** [V1 to V2 Migration](V1_TO_V2_MIGRATION.md)

### Upgrading within v0.5.x

For minor updates (e.g., v0.5.0 → v0.5.1):

```bash
pip install --upgrade eclips-blossom-ai
```

No breaking changes expected within minor versions.

---

## 🗑️ Uninstallation

To completely remove Blossom AI:

```bash
# Uninstall package
pip uninstall eclips-blossom-ai

# Remove cache (optional)
rm -rf ~/.blossom_cache

# Remove environment variables (optional)
# Edit ~/.bashrc, ~/.zshrc, or Windows Environment Variables
# and remove POLLINATIONS_API_KEY / BLOSSOM_API_KEY
```

---

## 📚 Next Steps

Now that you have Blossom AI installed:

1. 🚀 **[Quick Start Guide](QUICKSTART.md)** - Your first generation in 5 minutes
2. 🎨 **[Image Generation](IMAGE_GENERATION.md)** - Generate stunning images
3. 💬 **[Text Generation](TEXT_GENERATION.md)** - Generate text with AI
4. 👁️ **[Vision Support](VISION.md)** - Analyze images with AI
5. 📖 **[API Reference](API_REFERENCE.md)** - Complete API documentation

---

## 🆘 Support

Need help with installation?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Next: Quick Start →](QUICKSTART.md)

</div>