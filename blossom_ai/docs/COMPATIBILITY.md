# Compatibility Guide - Blossom AI

> **Python versions, dependencies, platform support, and framework integration**

---

## Table of Contents

1. [Python Version Requirements](#python-version-requirements)
2. [Dependencies](#dependencies)
3. [Platform Support](#platform-support)
4. [Framework Integration](#framework-integration)
5. [Environment Compatibility](#environment-compatibility)
6. [API Version Migration](#api-version-migration)
7. [Testing Compatibility](#testing-compatibility)

---

## Python Version Requirements

### Supported Versions

```python
# Minimum Python version: 3.8+
# Recommended: Python 3.10+ for best performance

import sys
assert sys.version_info >= (3, 8), "Python 3.8+ required"
```

### Version-Specific Features

**Python 3.8:**
```python
# Basic sync/async support
from blossom_ai import Blossom

# Works with Python 3.8+
with Blossom(api_token="token") as client:
    response = client.text.generate("Hello")
```

**Python 3.9+:**
```python
# Type hints improvements
from blossom_ai import Blossom

def process(client: Blossom) -> str | None:  # 3.9+ union syntax
    return client.text.generate("test")
```

**Python 3.10+:**
```python
# Pattern matching (if you use it in your code)
match response:
    case str():
        print("Text response")
    case bytes():
        print("Binary response")
```

---

## Dependencies

### Core Dependencies

From the test files, the library requires:

```toml
[dependencies]
# HTTP client
httpx = ">=0.24.0"  # For sync/async HTTP requests
requests = ">=2.28.0"  # Fallback for sync requests

# Async support
aiohttp = ">=3.8.0"  # Alternative async HTTP client

# Type hints
typing-extensions = ">=4.5.0"  # For Python <3.11

# Optional: for VCR testing
vcrpy = ">=4.2.0"  # Only for testing
```

### Optional Dependencies

```python
# For file encoding detection
chardet = ">=5.0.0"  # or charset-normalizer

# For advanced caching
redis = ">=4.5.0"  # For distributed caching
msgpack = ">=1.0.0"  # For cache serialization

# For testing
pytest = ">=7.0.0"
pytest-asyncio = ">=0.21.0"
```

### Installation

```bash
# Minimal installation
pip install blossom-ai

# With all optional features
pip install blossom-ai[all]

# Development installation
pip install blossom-ai[dev]
```

---

## Platform Support

### Operating Systems

**Fully Supported:**
- ✅ Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- ✅ macOS (10.15+, including M1/M2 Apple Silicon)
- ✅ Windows 10/11

**Tested Configurations:**

```python
import platform

# Check platform
system = platform.system()
print(f"OS: {system}")
print(f"Version: {platform.version()}")
print(f"Architecture: {platform.machine()}")

# All should work
assert system in ["Linux", "Darwin", "Windows"]
```

### Architecture Support

- ✅ x86_64 (Intel/AMD)
- ✅ ARM64 (Apple Silicon, AWS Graviton)
- ✅ ARM (Raspberry Pi 4+)

---

## Framework Integration

### 1. FastAPI Integration

**From url_test.py patterns:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from blossom_ai import Blossom, BlossomError

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "openai"

class GenerateResponse(BaseModel):
    response: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text endpoint"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            response = await client.text.generate(
                request.prompt,
                model=request.model
            )
            return GenerateResponse(response=response)
    
    except BlossomError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )

@app.post("/image")
async def generate_image(request: GenerateRequest):
    """Generate image endpoint - returns URL"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            # Use URL generation for web apps
            url = await client.image.generate_url(
                request.prompt,
                nologo=True,
                private=True
            )
            return {"url": url}
    
    except BlossomError as e:
        raise HTTPException(status_code=500, detail=e.message)

# Run: uvicorn app:app --reload
```

**Dependency Injection:**

```python
from fastapi import Depends
from blossom_ai import Blossom

async def get_client():
    """Dependency for Blossom client"""
    async with Blossom(api_token=API_TOKEN) as client:
        yield client

@app.post("/generate")
async def generate(
    prompt: str,
    client: Blossom = Depends(get_client)
):
    """Generate with dependency injection"""
    response = await client.text.generate(prompt)
    return {"response": response}
```

### 2. Flask Integration

```python
from flask import Flask, request, jsonify
from blossom_ai import Blossom, BlossomError

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_text():
    """Synchronous generation endpoint"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt required'}), 400
    
    try:
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(prompt)
            return jsonify({'response': response})
    
    except BlossomError as e:
        return jsonify({'error': e.message}), e.status_code or 500

@app.route('/image', methods=['POST'])
def generate_image():
    """Image generation endpoint"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    try:
        with Blossom(api_token=API_TOKEN) as client:
            # Return URL for web display
            url = client.image.generate_url(
                prompt,
                nologo=True,
                private=True
            )
            return jsonify({'url': url})
    
    except BlossomError as e:
        return jsonify({'error': e.message}), 500

# Run: flask run
```

### 3. Django Integration

**views.py:**

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from blossom_ai import Blossom, BlossomError
from django.conf import settings

@csrf_exempt
@require_http_methods(["POST"])
def generate_text(request):
    """Django view for text generation"""
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        
        if not prompt:
            return JsonResponse({'error': 'Prompt required'}, status=400)
        
        with Blossom(api_token=settings.BLOSSOM_API_TOKEN) as client:
            response = client.text.generate(prompt)
            return JsonResponse({'response': response})
    
    except BlossomError as e:
        return JsonResponse({'error': e.message}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
```

**settings.py:**

```python
# Django settings
BLOSSOM_API_TOKEN = os.environ.get('BLOSSOM_API_TOKEN')

# For async views (Django 4.1+)
ASGI_APPLICATION = 'myproject.asgi.application'
```

**Async Django views (4.1+):**

```python
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from blossom_ai import Blossom

async def generate_text_async(request):
    """Async Django view"""
    import json
    data = json.loads(request.body)
    prompt = data.get('prompt')
    
    async with Blossom(api_token=settings.BLOSSOM_API_TOKEN) as client:
        response = await client.text.generate(prompt)
        return JsonResponse({'response': response})
```

### 4. Streamlit Integration

**From test_examples.py patterns:**

```python
import streamlit as st
from blossom_ai import Blossom, BlossomError
import os

# Page config
st.set_page_config(page_title="Blossom AI Demo", page_icon="🌸")

# Sidebar for API token
with st.sidebar:
    api_token = st.text_input(
        "API Token",
        type="password",
        value=os.getenv("BLOSSOM_API_TOKEN", "")
    )

st.title("🌸 Blossom AI Demo")

# Text generation tab
tab1, tab2 = st.tabs(["Text Generation", "Image Generation"])

with tab1:
    st.header("Text Generation")
    prompt = st.text_area("Enter your prompt:", height=100)
    
    if st.button("Generate", key="text"):
        if not api_token:
            st.error("Please enter your API token in the sidebar")
        elif not prompt:
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Generating..."):
                try:
                    with Blossom(api_token=api_token) as client:
                        response = client.text.generate(prompt)
                        st.success("Generated!")
                        st.write(response)
                except BlossomError as e:
                    st.error(f"Error: {e.message}")

with tab2:
    st.header("Image Generation")
    image_prompt = st.text_input("Describe the image:")
    
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Width", 256, 1024, 512, 64)
    with col2:
        height = st.number_input("Height", 256, 1024, 512, 64)
    
    if st.button("Generate Image", key="image"):
        if not api_token:
            st.error("Please enter your API token")
        elif not image_prompt:
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Generating image..."):
                try:
                    with Blossom(api_token=api_token) as client:
                        # Use URL for web display
                        url = client.image.generate_url(
                            image_prompt,
                            width=width,
                            height=height,
                            nologo=True
                        )
                        st.image(url, caption=image_prompt)
                except BlossomError as e:
                    st.error(f"Error: {e.message}")

# Run: streamlit run app.py
```

### 5. Discord Bot Integration

**From url_test.py Discord example:**

```python
import discord
from discord.ext import commands
from blossom_ai import Blossom, BlossomError
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

@bot.command(name='generate')
async def generate_text(ctx, *, prompt: str):
    """Generate text from prompt"""
    async with ctx.typing():
        try:
            async with Blossom(api_token=API_TOKEN) as client:
                response = await client.text.generate(prompt)
                # Discord has 2000 char limit
                if len(response) > 2000:
                    response = response[:1997] + "..."
                await ctx.send(response)
        except BlossomError as e:
            await ctx.send(f"Error: {e.message}")

@bot.command(name='image')
async def generate_image(ctx, *, prompt: str):
    """Generate image from prompt"""
    async with ctx.typing():
        try:
            async with Blossom(api_token=API_TOKEN) as client:
                # Use URL generation - Discord auto-embeds
                url = await client.image.generate_url(
                    prompt,
                    nologo=True,
                    private=True,
                    seed=hash(prompt) % 100000  # Deterministic
                )
                
                embed = discord.Embed(title=prompt, color=discord.Color.purple())
                embed.set_image(url=url)
                await ctx.send(embed=embed)
        
        except BlossomError as e:
            await ctx.send(f"Error: {e.message}")

# Run bot
bot.run(os.getenv("DISCORD_TOKEN"))
```

### 6. Gradio Integration

```python
import gradio as gr
from blossom_ai import Blossom, BlossomError
import os

API_TOKEN = os.getenv("BLOSSOM_API_TOKEN")

def generate_text(prompt, system_message=""):
    """Generate text with Gradio"""
    try:
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(
                prompt,
                system=system_message if system_message else None
            )
            return response
    except BlossomError as e:
        return f"Error: {e.message}"

def generate_image(prompt, width, height):
    """Generate image URL"""
    try:
        with Blossom(api_token=API_TOKEN) as client:
            url = client.image.generate_url(
                prompt,
                width=width,
                height=height,
                nologo=True
            )
            return url
    except BlossomError as e:
        return None

# Text generation interface
text_interface = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(label="Prompt", lines=3),
        gr.Textbox(label="System Message (optional)", lines=2)
    ],
    outputs=gr.Textbox(label="Response", lines=10),
    title="🌸 Blossom AI - Text Generation"
)

# Image generation interface
image_interface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(label="Prompt"),
        gr.Slider(256, 1024, 512, step=64, label="Width"),
        gr.Slider(256, 1024, 512, step=64, label="Height")
    ],
    outputs=gr.Image(label="Generated Image"),
    title="🌸 Blossom AI - Image Generation"
)

# Combine interfaces
demo = gr.TabbedInterface(
    [text_interface, image_interface],
    ["Text", "Image"]
)

# Launch
demo.launch()
```

---

## Environment Compatibility

### 1. Docker

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV BLOSSOM_API_TOKEN=""
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "app.py"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - BLOSSOM_API_TOKEN=${BLOSSOM_API_TOKEN}
    restart: unless-stopped
```

### 2. AWS Lambda

**lambda_handler.py:**

```python
import json
from blossom_ai import Blossom, BlossomError
import os

API_TOKEN = os.environ.get('BLOSSOM_API_TOKEN')

def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event
        prompt = body.get('prompt')
        
        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Prompt required'})
            }
        
        # Lambda runs sync code
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(prompt)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'response': response})
        }
    
    except BlossomError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': e.message})
        }
```

**requirements.txt for Lambda:**

```txt
blossom-ai>=0.5.0
```

### 3. Google Cloud Functions

**main.py:**

```python
import functions_framework
from blossom_ai import Blossom, BlossomError
import os

API_TOKEN = os.environ.get('BLOSSOM_API_TOKEN')

@functions_framework.http
def generate(request):
    """HTTP Cloud Function"""
    request_json = request.get_json(silent=True)
    
    if not request_json or 'prompt' not in request_json:
        return {'error': 'Prompt required'}, 400
    
    try:
        with Blossom(api_token=API_TOKEN) as client:
            response = client.text.generate(request_json['prompt'])
            return {'response': response}, 200
    
    except BlossomError as e:
        return {'error': e.message}, 500
```

### 4. Azure Functions

**__init__.py:**

```python
import azure.functions as func
from blossom_ai import Blossom, BlossomError
import json
import os

API_TOKEN = os.environ.get('BLOSSOM_API_TOKEN')

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function handler"""
    try:
        req_body = req.get_json()
        prompt = req_body.get('prompt')
        
        if not prompt:
            return func.HttpResponse(
                json.dumps({'error': 'Prompt required'}),
                status_code=400
            )
        
        # Use async
        async with Blossom(api_token=API_TOKEN) as client:
            response = await client.text.generate(prompt)
        
        return func.HttpResponse(
            json.dumps({'response': response}),
            status_code=200
        )
    
    except BlossomError as e:
        return func.HttpResponse(
            json.dumps({'error': e.message}),
            status_code=500
        )
```

### 5. Jupyter Notebooks

```python
# Install in notebook
!pip install blossom-ai

# Import
from blossom_ai import Blossom
import os

# Set token
API_TOKEN = os.getenv("BLOSSOM_API_TOKEN") or "your-token"

# Use synchronously in notebooks
with Blossom(api_token=API_TOKEN) as client:
    response = client.text.generate("Explain quantum computing")
    print(response)

# Display images
from IPython.display import Image, display

with Blossom(api_token=API_TOKEN) as client:
    url = client.image.generate_url("a beautiful sunset")
    display(Image(url=url))
```

**Async in Jupyter:**

```python
# Jupyter supports top-level await
from blossom_ai import Blossom

async with Blossom(api_token=API_TOKEN) as client:
    response = await client.text.generate("Hello")
    print(response)
```

---

## API Version Migration

### V1 to V2 Migration

**Key Changes:**

1. **Client initialization** - Same
2. **Method names** - Same (`.generate()`, `.save()`, etc.)
3. **Model parameter** - Now optional, defaults provided
4. **URL generation** - Security improved (token not in URL)

**Migration Checklist:**

```python
# ✅ No changes needed for basic usage
with Blossom(api_token=API_TOKEN) as client:
    response = client.text.generate("Hello")  # Works in V2

# ✅ Image generation - same
with Blossom(api_token=API_TOKEN) as client:
    image = client.image.generate("cat")  # Works in V2

# ⚠️ URL generation - improved security (V2)
with Blossom(api_token=API_TOKEN) as client:
    url = client.image.generate_url("test")
    # V2: Token NOT in URL (secure)
    # V1: Token might have been in URL
    assert API_TOKEN not in url  # V2 guarantee
```

**New in V2:**

```python
# 1. Vision support (v0.5.0+)
from blossom_ai import MessageBuilder

messages = [
    MessageBuilder.image(
        role="user",
        text="What's in this image?",
        image_url="https://example.com/image.jpg"
    )
]
response = client.text.chat(messages)

# 2. Native reasoning support
response = client.text.chat(
    messages=[{"role": "user", "content": "Solve this"}],
    thinking={"type": "enabled", "budget_tokens": 5000}
)

# 3. Audio output
response = client.text.chat(
    messages=[{"role": "user", "content": "Say hello"}],
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"}
)
```

---

## Testing Compatibility

### pytest Integration

**From test_integration.py:**

```python
import pytest
from blossom_ai import Blossom

# Mark tests that need API
pytestmark = pytest.mark.api

# Skip if no token
API_TOKEN = "your-token"
SKIP_IF_NO_TOKEN = pytest.mark.skipif(
    not API_TOKEN or API_TOKEN == "your-token",
    reason="No API token"
)

@SKIP_IF_NO_TOKEN
def test_text_generation():
    """Test with real API"""
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("Hello")
        assert response is not None

@pytest.mark.asyncio
@SKIP_IF_NO_TOKEN
async def test_async_generation():
    """Test async"""
    async with Blossom(api_token=API_TOKEN) as client:
        response = await client.text.generate("Hello")
        assert response is not None
```

### VCR.py for Recording

**From test_integration.py:**

```python
import vcr
from pathlib import Path

CASSETTES_DIR = Path(__file__).parent / "cassettes"
CASSETTES_DIR.mkdir(exist_ok=True)

vcr_config = vcr.VCR(
    cassette_library_dir=str(CASSETTES_DIR),
    record_mode="once",  # Record once, replay thereafter
    match_on=["method", "scheme", "host", "port", "path"],
    filter_headers=["authorization"],  # Hide token
    filter_query_parameters=["token"],  # Hide token in URL
)

@vcr_config.use_cassette("text_generate.yaml")
def test_with_vcr():
    """Test with VCR recording"""
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.generate("Hello")
        assert response is not None
    # First run: records to cassette
    # Subsequent runs: replays from cassette
```

### Mocking for Unit Tests

```python
from unittest.mock import Mock, patch
from blossom_ai import Blossom

def test_with_mock():
    """Unit test with mocking"""
    mock_client = Mock(spec=Blossom)
    mock_client.text.generate.return_value = "Mocked response"
    
    # Your code using mock
    response = mock_client.text.generate("test")
    assert response == "Mocked response"
    mock_client.text.generate.assert_called_once_with("test")
```

---

## Troubleshooting

### Common Issues

**1. Import Errors:**

```python
# If you get import errors
try:
    from blossom_ai import Blossom
except ImportError:
    print("Install: pip install blossom-ai")
```

**2. SSL Certificate Errors:**

```python
# For corporate proxies
import os
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/ca-bundle.crt'

# Or disable verification (not recommended)
import httpx
client = httpx.Client(verify=False)
```

**3. Timeout in Cloud Functions:**

```python
# Increase timeout for cloud functions
with Blossom(api_token=API_TOKEN, timeout=60) as client:
    response = client.text.generate(prompt)
```

**4. Memory Issues:**

```python
# Use streaming for large responses
with Blossom(api_token=API_TOKEN) as client:
    for chunk in client.text.generate(prompt, stream=True):
        process_chunk(chunk)  # Process incrementally
```

---

## Summary

### Compatibility Matrix

| Feature          | Python 3.8 | Python 3.9 | Python 3.10+ |
|------------------|------------|------------|--------------|
| Sync API         | ✅          | ✅          | ✅            |
| Async API        | ✅          | ✅          | ✅            |
| Type Hints       | ⚠️         | ✅          | ✅            |
| Pattern Matching | ❌          | ❌          | ✅            |

| Platform        | Support | Notes           |
|-----------------|---------|-----------------|
| Linux           | ✅       | Full support    |
| macOS           | ✅       | Including M1/M2 |
| Windows         | ✅       | Windows 10/11   |
| Docker          | ✅       | All platforms   |
| AWS Lambda      | ✅       | Sync mode       |
| Google Cloud    | ✅       | Sync/Async      |
| Azure Functions | ✅       | Sync/Async      |

### Best Practices

1. **Use Python 3.10+** for best experience
2. **Pin dependencies** in production
3. **Use context managers** always
4. **Test in target environment** before deploying
5. **Use VCR.py** for testing without API calls
6. **Set timeouts** appropriately for your environment

### Related Documentation

- [Error Handling](ERROR_HANDLING.md) - Error handling guide
- [Web App Guide](WEB_APP.md) - Web application patterns
- [API Reference](API_REFERENCE.md) - Complete API documentation