# Installation & Setup

This guide will help you install and set up the Blossom AI Python SDK.

## 📦 Installation

Blossom AI is available on PyPI and can be easily installed using `pip`.

```bash
pip install eclips-blossom-ai
```

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

For features like **Audio Generation**, you will need to provide an API token.

```python
from blossom_ai import Blossom

# Replace "YOUR_TOKEN" with your actual Pollinations.AI API token
ai = Blossom(api_token="YOUR_TOKEN")

# Now you can access token-required features
# ai.audio.save(...)
```
