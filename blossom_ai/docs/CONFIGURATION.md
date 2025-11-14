# ⚙️ Configuration Guide

> **Configure the Blossom AI client for optimal performance and security**

Learn how to configure the Blossom AI client with API tokens, timeouts, custom settings, and environment variables.

---

## 📋 Table of Contents

- [Basic Configuration](#basic-configuration)
- [API Token](#api-token)
- [Client Settings](#client-settings)
- [Environment Variables](#environment-variables)
- [Advanced Configuration](#advanced-configuration)
- [Best Practices](#best-practices)

---

## 🚀 Basic Configuration

### Default Configuration

```python
from blossom_ai import Blossom

# Minimal configuration (no auth)
client = Blossom()

# With API token
client = Blossom(api_token="your_token_here")

# With timeout
client = Blossom(
    api_token="your_token",
    timeout=60  # seconds
)
```

### Context Manager (Recommended)

```python
from blossom_ai import Blossom

# Automatic resource cleanup
with Blossom(api_token="your_token") as client:
    response = client.text.generate("Hello")
    # Client automatically closed after block
```

### Manual Cleanup

```python
from blossom_ai import Blossom

client = Blossom(api_token="your_token")

try:
    response = client.text.generate("Hello")
finally:
    client.close_sync()  # Manual cleanup
```

---

## 🔑 API Token

### Getting Your Token

1. Visit [https://enter.pollinations.ai](https://enter.pollinations.ai)
2. Sign up or log in
3. Copy your API token

### Setting Token

**Method 1: Direct Parameter**

```python
from blossom_ai import Blossom

client = Blossom(api_token="your_token_here")
```

**Method 2: Environment Variable**

```bash
# In .env file or shell
export BLOSSOM_API_TOKEN="your_token_here"
```

```python
import os
from blossom_ai import Blossom

# Reads from environment
token = os.getenv("BLOSSOM_API_TOKEN")
client = Blossom(api_token=token)
```

**Method 3: Config File**

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BLOSSOM_CONFIG = {
    "api_token": os.getenv("BLOSSOM_API_TOKEN"),
    "timeout": 60,
}
```

```python
# main.py
from blossom_ai import Blossom
from config import BLOSSOM_CONFIG

client = Blossom(**BLOSSOM_CONFIG)
```

### Security Best Practices

```python
# ❌ DON'T hardcode tokens
client = Blossom(api_token="sk-1234567890abcdef")

# ✅ DO use environment variables
import os
client = Blossom(api_token=os.getenv("BLOSSOM_API_TOKEN"))

# ✅ DO use .env files (with .gitignore)
from dotenv import load_dotenv
load_dotenv()
client = Blossom(api_token=os.getenv("BLOSSOM_API_TOKEN"))
```

---

## 🔧 Client Settings

### Timeout Configuration

```python
from blossom_ai import Blossom

# Default timeout (30 seconds)
client = Blossom(api_token="token")

# Custom timeout
client = Blossom(
    api_token="token",
    timeout=120  # 2 minutes for large requests
)

# No timeout (wait forever - not recommended)
client = Blossom(
    api_token="token",
    timeout=None
)
```

### Per-Request Timeout

```python
from blossom_ai import Blossom

with Blossom(api_token="token", timeout=30) as client:
    # Use default timeout (30s)
    response1 = client.text.generate("Quick question")
    
    # Override for specific request
    # Note: Per-request timeout not directly supported
    # Set at client level instead
```

### Base URL Configuration

```python
from blossom_ai import Blossom

# Default V2 API
client = Blossom(api_token="token")
# Uses: https://text.pollinations.ai/v2

# Custom base URL (if needed)
# Note: This is handled internally by the library
```

---

## 🌍 Environment Variables

### Supported Variables

```bash
# API Token
BLOSSOM_API_TOKEN=your_token_here

# Timeout (optional)
BLOSSOM_TIMEOUT=60

# Cache directory (optional)
BLOSSOM_CACHE_DIR=./my_cache

# Log level (optional)
BLOSSOM_LOG_LEVEL=INFO
```

### .env File Example

```bash
# .env file
BLOSSOM_API_TOKEN=your_secret_token_here
BLOSSOM_TIMEOUT=60
BLOSSOM_CACHE_DIR=./cache
```

### Loading Environment

```python
from dotenv import load_dotenv
import os
from blossom_ai import Blossom

# Load .env file
load_dotenv()

# Use environment variables
client = Blossom(
    api_token=os.getenv("BLOSSOM_API_TOKEN"),
    timeout=int(os.getenv("BLOSSOM_TIMEOUT", "30"))
)
```

### .gitignore Setup

```bash
# .gitignore
.env
.env.local
*.env

# Cache directory
cache/
.cache/
```

---

## 🎯 Advanced Configuration

### Multi-Environment Setup

```python
# config/base.py
class Config:
    TIMEOUT = 30

# config/development.py
from .base import Config

class DevelopmentConfig(Config):
    API_TOKEN = "dev_token"
    TIMEOUT = 60  # Longer timeout for debugging

# config/production.py
from .base import Config
import os

class ProductionConfig(Config):
    API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
    TIMEOUT = 30
```

```python
# main.py
import os
from blossom_ai import Blossom

# Select config based on environment
env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    from config.production import ProductionConfig as Config
else:
    from config.development import DevelopmentConfig as Config

client = Blossom(
    api_token=Config.API_TOKEN,
    timeout=Config.TIMEOUT
)
```

### Configuration Class

```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class BlossomConfig:
    """Centralized configuration"""
    api_token: str
    timeout: int = 30
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    @classmethod
    def from_env(cls) -> "BlossomConfig":
        """Load from environment variables"""
        return cls(
            api_token=os.getenv("BLOSSOM_API_TOKEN", ""),
            timeout=int(os.getenv("BLOSSOM_TIMEOUT", "30")),
            cache_enabled=os.getenv("BLOSSOM_CACHE", "true").lower() == "true",
            cache_ttl=int(os.getenv("BLOSSOM_CACHE_TTL", "3600"))
        )
    
    def validate(self) -> None:
        """Validate configuration"""
        if not self.api_token:
            raise ValueError("API token is required")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")

# Usage
config = BlossomConfig.from_env()
config.validate()

from blossom_ai import Blossom
client = Blossom(
    api_token=config.api_token,
    timeout=config.timeout
)
```

### Async Configuration

```python
from blossom_ai import Blossom
import asyncio

async def configure_async_client():
    """Configure async client"""
    async with Blossom(
        api_token="your_token",
        timeout=60
    ) as client:
        response = await client.text.generate("Hello")
        return response

# Run
result = asyncio.run(configure_async_client())
```

### Retry Configuration

```python
from blossom_ai import Blossom
import time

def create_client_with_retry(max_retries: int = 3):
    """Create client with retry logic"""
    for attempt in range(max_retries):
        try:
            client = Blossom(api_token="your_token", timeout=30)
            # Test connection
            client.text.models()
            return client
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} in {wait}s...")
                time.sleep(wait)
            else:
                raise

# Usage
client = create_client_with_retry()
```

---

## ✅ Best Practices

### 1. Use Environment Variables

```python
import os
from blossom_ai import Blossom

# ✅ GOOD: Environment variables
client = Blossom(api_token=os.getenv("BLOSSOM_API_TOKEN"))

# ❌ BAD: Hardcoded token
client = Blossom(api_token="sk-hardcoded-token")
```

### 2. Always Use Context Managers

```python
from blossom_ai import Blossom

# ✅ GOOD: Auto cleanup
with Blossom(api_token="token") as client:
    response = client.text.generate("Hello")

# ❌ BAD: Manual cleanup required
client = Blossom(api_token="token")
response = client.text.generate("Hello")
client.close_sync()  # Easy to forget!
```

### 3. Set Appropriate Timeouts

```python
from blossom_ai import Blossom

# ✅ GOOD: Reasonable timeout
with Blossom(api_token="token", timeout=60) as client:
    # Large image generation
    image = client.image.generate("complex scene", width=1920, height=1080)

# ❌ BAD: Too short timeout
with Blossom(api_token="token", timeout=5) as client:
    image = client.image.generate("complex scene", width=1920, height=1080)
    # Will timeout!
```

### 4. Validate Configuration

```python
import os
from blossom_ai import Blossom

def create_validated_client():
    """Create client with validation"""
    token = os.getenv("BLOSSOM_API_TOKEN")
    
    if not token:
        raise ValueError(
            "BLOSSOM_API_TOKEN not set. "
            "Get token at https://enter.pollinations.ai"
        )
    
    if len(token) < 10:
        raise ValueError("Invalid API token format")
    
    return Blossom(api_token=token, timeout=30)

# Usage
try:
    client = create_validated_client()
except ValueError as e:
    print(f"Configuration error: {e}")
```

### 5. Separate Config from Code

```python
# ✅ GOOD: Separate config
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")
TIMEOUT = 60

# main.py
from blossom_ai import Blossom
from config import API_TOKEN, TIMEOUT

client = Blossom(api_token=API_TOKEN, timeout=TIMEOUT)
```

---

## 🏢 Production Configuration

### Production Checklist

```python
import os
import logging
from blossom_ai import Blossom

# ✅ 1. Load from environment
from dotenv import load_dotenv
load_dotenv()

# ✅ 2. Validate token
token = os.getenv("BLOSSOM_API_TOKEN")
if not token:
    raise ValueError("BLOSSOM_API_TOKEN not set")

# ✅ 3. Set appropriate timeout
timeout = int(os.getenv("BLOSSOM_TIMEOUT", "60"))

# ✅ 4. Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ 5. Create client with error handling
try:
    client = Blossom(api_token=token, timeout=timeout)
    logger.info("Blossom client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize client: {e}")
    raise

# ✅ 6. Use context manager
with client:
    response = client.text.generate("Hello")
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variable
ENV BLOSSOM_API_TOKEN=""

# Run application
CMD ["python", "main.py"]
```

```bash
# Run with token
docker run -e BLOSSOM_API_TOKEN="your_token" myapp
```

### Kubernetes Configuration

```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: blossom-secret
type: Opaque
stringData:
  api-token: your_token_here
```

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blossom-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: BLOSSOM_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: blossom-secret
              key: api-token
```

---

## 🔍 Configuration Examples

### Example 1: Development Setup

```python
# dev_config.py
import os
from dotenv import load_dotenv
from blossom_ai import Blossom

# Load development environment
load_dotenv(".env.development")

def get_dev_client():
    """Get configured development client"""
    return Blossom(
        api_token=os.getenv("BLOSSOM_API_TOKEN"),
        timeout=120  # Longer timeout for debugging
    )

# Usage
if __name__ == "__main__":
    with get_dev_client() as client:
        response = client.text.generate("Test")
        print(response)
```

### Example 2: Production Setup

```python
# prod_config.py
import os
import logging
from blossom_ai import Blossom

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProductionClient:
    """Production-ready client wrapper"""
    
    def __init__(self):
        self.token = os.getenv("BLOSSOM_API_TOKEN")
        if not self.token:
            raise ValueError("BLOSSOM_API_TOKEN not set")
        
        self.timeout = int(os.getenv("BLOSSOM_TIMEOUT", "30"))
        self.client = None
    
    def __enter__(self):
        logger.info("Initializing Blossom client")
        self.client = Blossom(
            api_token=self.token,
            timeout=self.timeout
        ).__enter__()
        return self.client
    
    def __exit__(self, *args):
        if self.client:
            logger.info("Closing Blossom client")
            self.client.__exit__(*args)

# Usage
with ProductionClient() as client:
    response = client.text.generate("Hello")
```

### Example 3: Multi-Service Configuration

```python
# services/config.py
import os
from typing import Dict, Any
from blossom_ai import Blossom

class ServiceConfig:
    """Configuration for multiple services"""
    
    SERVICES = {
        "text_generation": {
            "timeout": 30,
            "cache_ttl": 3600,
        },
        "image_generation": {
            "timeout": 120,
            "cache_ttl": 7200,
        },
        "analysis": {
            "timeout": 60,
            "cache_ttl": 1800,
        }
    }
    
    def __init__(self):
        self.api_token = os.getenv("BLOSSOM_API_TOKEN")
        if not self.api_token:
            raise ValueError("API token required")
    
    def get_client(self, service: str) -> Blossom:
        """Get configured client for service"""
        config = self.SERVICES.get(service, {})
        
        return Blossom(
            api_token=self.api_token,
            timeout=config.get("timeout", 30)
        )

# Usage
config = ServiceConfig()

# Text service
with config.get_client("text_generation") as client:
    response = client.text.generate("Hello")

# Image service
with config.get_client("image_generation") as client:
    image = client.image.generate("A cat")
```

---

## 🔗 Related Documentation

- [Quick Start](QUICKSTART.md) - Get started quickly
- [Error Handling](ERROR_HANDLING.md) - Handle configuration errors
- [Security](../../SECURITY.md) - Security best practices
- [API Reference](API_REFERENCE.md) - Complete API documentation

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Async Guide](ASYNC_GUIDE.md) | [Resource Management](RESOURCE_MANAGEMENT.md) →

</div>