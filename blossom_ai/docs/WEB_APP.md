# 🌐 Web Application Guide

> **Build production-ready web applications with Blossom AI v0.5.0**

This guide shows you how to build web applications with Blossom AI, including REST APIs, real-time streaming, and multimodal features (text, images, vision, and audio).

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [FastAPI Applications](#-fastapi-applications)
- [Flask Applications](#-flask-applications)
- [Streaming Endpoints](#-streaming-endpoints)
- [Vision & Multimodal](#-vision--multimodal)
- [Authentication & Security](#-authentication--security)
- [Production Deployment](#-production-deployment)
- [Error Handling](#-error-handling)
- [Performance Optimization](#-performance-optimization)

---

## 🚀 Quick Start

### Installation

```bash
# Install Blossom AI
pip install eclips-blossom-ai

# For web frameworks
pip install fastapi uvicorn  # FastAPI
# OR
pip install flask            # Flask
```

### Minimal Example (FastAPI)

```python
from fastapi import FastAPI
from blossom_ai import Blossom
import os

app = FastAPI()
API_TOKEN = os.getenv('POLLINATIONS_API_KEY')

@app.get("/generate")
async def generate_text(prompt: str):
    async with Blossom(api_token=API_TOKEN) as client:
        response = await client.text.generate(prompt)
        return {"response": response}

# Run: uvicorn main:app --reload
```

---

## ⚡ FastAPI Applications

FastAPI is recommended for production applications due to its async support and automatic documentation.

### Complete FastAPI Application

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from blossom_ai import Blossom, MessageBuilder, BlossomError
import os
from typing import Optional, List
import asyncio

# ============================================================================
# CONFIGURATION
# ============================================================================

app = FastAPI(
    title="Blossom AI API",
    description="AI-powered text, image, and vision API",
    version="0.5.0"
)

API_TOKEN = os.getenv('POLLINATIONS_API_KEY')
if not API_TOKEN:
    raise ValueError("POLLINATIONS_API_KEY environment variable required")

# ============================================================================
# REQUEST MODELS
# ============================================================================

class TextGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)
    model: str = Field(default="openai")
    max_tokens: Optional[int] = Field(default=None, ge=1, le=4000)
    temperature: Optional[float] = Field(default=None, ge=0, le=2)
    stream: bool = False

class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=250)
    model: str = Field(default="flux")
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    seed: Optional[int] = None
    quality: Optional[str] = Field(default="high", pattern="^(low|medium|high|hd)$")

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = Field(default="openai")
    stream: bool = False

class VisionRequest(BaseModel):
    image_url: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=1)
    model: str = Field(default="openai")
    detail: str = Field(default="auto", pattern="^(low|auto|high)$")

# ============================================================================
# TEXT GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/text/generate")
async def generate_text(request: TextGenerateRequest):
    """Generate text from prompt"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            if request.stream:
                # Return streaming response
                async def stream_generator():
                    stream = await client.text.generate(
                        request.prompt,
                        model=request.model,
                        max_tokens=request.max_tokens,
                        temperature=request.temperature,
                        stream=True
                    )
                    async for chunk in stream:
                        yield f"data: {chunk}\n\n"
                
                return StreamingResponse(
                    stream_generator(),
                    media_type="text/event-stream"
                )
            else:
                # Non-streaming response
                response = await client.text.generate(
                    request.prompt,
                    model=request.model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                )
                return {"response": response}
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail={
            "error": e.error_type,
            "message": e.message,
            "suggestion": e.suggestion
        })

@app.post("/api/text/chat")
async def chat(request: ChatRequest):
    """Multi-turn chat completion"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            messages = [{"role": msg.role, "content": msg.content} 
                       for msg in request.messages]
            
            if request.stream:
                async def stream_generator():
                    stream = await client.text.chat(
                        messages,
                        model=request.model,
                        stream=True
                    )
                    async for chunk in stream:
                        yield f"data: {chunk}\n\n"
                
                return StreamingResponse(
                    stream_generator(),
                    media_type="text/event-stream"
                )
            else:
                response = await client.text.chat(messages, model=request.model)
                return {"response": response}
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail={
            "error": e.error_type,
            "message": e.message
        })

# ============================================================================
# IMAGE GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/image/generate")
async def generate_image(request: ImageGenerateRequest):
    """Generate image from prompt"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            # Return URL for fast response
            url = await client.image.generate_url(
                request.prompt,
                model=request.model,
                width=request.width,
                height=request.height,
                seed=request.seed,
                quality=request.quality,
                nologo=True
            )
            return {"url": url}
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail={
            "error": e.error_type,
            "message": e.message
        })

@app.post("/api/image/download")
async def download_image(request: ImageGenerateRequest):
    """Generate and download image"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            image_bytes = await client.image.generate(
                request.prompt,
                model=request.model,
                width=request.width,
                height=request.height,
                seed=request.seed,
                quality=request.quality
            )
            
            return StreamingResponse(
                iter([image_bytes]),
                media_type="image/png",
                headers={
                    "Content-Disposition": f"attachment; filename=generated.png"
                }
            )
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail={
            "error": e.error_type,
            "message": e.message
        })

# ============================================================================
# VISION ENDPOINTS (NEW in v0.5.0)
# ============================================================================

@app.post("/api/vision/analyze")
async def analyze_image(request: VisionRequest):
    """Analyze image with vision model"""
    try:
        async with Blossom(api_token=API_TOKEN) as client:
            messages = [
                MessageBuilder.image(
                    role="user",
                    text=request.prompt,
                    image_url=request.image_url,
                    detail=request.detail
                )
            ]
            
            response = await client.text.chat(messages, model=request.model)
            return {"analysis": response}
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail={
            "error": e.error_type,
            "message": e.message
        })

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/api/models/text")
async def list_text_models():
    """List available text models"""
    async with Blossom(api_token=API_TOKEN) as client:
        models = await client.text.models()
        return {"models": models}

@app.get("/api/models/image")
async def list_image_models():
    """List available image models"""
    async with Blossom(api_token=API_TOKEN) as client:
        models = await client.image.models()
        return {"models": models}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.5.0"}

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(BlossomError)
async def blossom_error_handler(request, exc: BlossomError):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "suggestion": exc.suggestion
        }
    )

@app.exception_handler(Exception)
async def general_error_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": str(exc)
        }
    )

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run FastAPI Application

```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🌶️ Flask Applications

Flask is a simpler alternative if you don't need async features.

### Complete Flask Application

```python
from flask import Flask, request, jsonify, Response, stream_with_context
from blossom_ai import Blossom, MessageBuilder, BlossomError
import os
from functools import wraps
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__)
API_TOKEN = os.getenv('POLLINATIONS_API_KEY')

if not API_TOKEN:
    raise ValueError("POLLINATIONS_API_KEY required")

# ============================================================================
# DECORATORS
# ============================================================================

def handle_errors(f):
    """Error handling decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BlossomError as e:
            return jsonify({
                "error": e.error_type,
                "message": e.message,
                "suggestion": e.suggestion
            }), 400
        except Exception as e:
            return jsonify({
                "error": "internal_error",
                "message": str(e)
            }), 500
    return decorated_function

# ============================================================================
# TEXT GENERATION ENDPOINTS
# ============================================================================

@app.route('/api/text/generate', methods=['POST'])
@handle_errors
def generate_text():
    """Generate text from prompt"""
    data = request.get_json()
    
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    
    model = data.get('model', 'openai')
    stream = data.get('stream', False)
    
    with Blossom(api_token=API_TOKEN) as client:
        if stream:
            def generate():
                for chunk in client.text.generate(prompt, model=model, stream=True):
                    yield f"data: {chunk}\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream'
            )
        else:
            response = client.text.generate(prompt, model=model)
            return jsonify({"response": response})

@app.route('/api/text/chat', methods=['POST'])
@handle_errors
def chat():
    """Multi-turn chat"""
    data = request.get_json()
    
    messages = data.get('messages')
    if not messages:
        return jsonify({"error": "messages required"}), 400
    
    model = data.get('model', 'openai')
    
    with Blossom(api_token=API_TOKEN) as client:
        response = client.text.chat(messages, model=model)
        return jsonify({"response": response})

# ============================================================================
# IMAGE GENERATION ENDPOINTS
# ============================================================================

@app.route('/api/image/generate', methods=['POST'])
@handle_errors
def generate_image():
    """Generate image URL"""
    data = request.get_json()
    
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    
    with Blossom(api_token=API_TOKEN) as client:
        url = client.image.generate_url(
            prompt,
            model=data.get('model', 'flux'),
            width=data.get('width', 1024),
            height=data.get('height', 1024),
            seed=data.get('seed'),
            nologo=True
        )
        return jsonify({"url": url})

@app.route('/api/image/download', methods=['POST'])
@handle_errors
def download_image():
    """Generate and download image"""
    data = request.get_json()
    
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    
    with Blossom(api_token=API_TOKEN) as client:
        image_bytes = client.image.generate(
            prompt,
            model=data.get('model', 'flux'),
            width=data.get('width', 1024),
            height=data.get('height', 1024)
        )
        
        return Response(
            image_bytes,
            mimetype='image/png',
            headers={
                'Content-Disposition': 'attachment; filename=generated.png'
            }
        )

# ============================================================================
# VISION ENDPOINTS (NEW in v0.5.0)
# ============================================================================

@app.route('/api/vision/analyze', methods=['POST'])
@handle_errors
def analyze_image():
    """Analyze image with vision"""
    data = request.get_json()
    
    image_url = data.get('image_url')
    prompt = data.get('prompt')
    
    if not image_url or not prompt:
        return jsonify({"error": "image_url and prompt required"}), 400
    
    with Blossom(api_token=API_TOKEN) as client:
        messages = [
            MessageBuilder.image(
                role="user",
                text=prompt,
                image_url=image_url,
                detail=data.get('detail', 'auto')
            )
        ]
        
        response = client.text.chat(messages, model=data.get('model', 'openai'))
        return jsonify({"analysis": response})

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.route('/api/models/text')
@handle_errors
def list_text_models():
    """List text models"""
    with Blossom(api_token=API_TOKEN) as client:
        models = client.text.models()
        return jsonify({"models": models})

@app.route('/api/models/image')
@handle_errors
def list_image_models():
    """List image models"""
    with Blossom(api_token=API_TOKEN) as client:
        models = client.image.models()
        return jsonify({"models": models})

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "version": "0.5.0"})

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```

### Run Flask Application

```bash
# Development
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 🌊 Streaming Endpoints

Real-time streaming for better user experience.

### Server-Sent Events (SSE)

**FastAPI:**

```python
from fastapi.responses import StreamingResponse

@app.post("/api/stream")
async def stream_text(prompt: str):
    async def event_generator():
        async with Blossom(api_token=API_TOKEN) as client:
            stream = await client.text.generate(prompt, stream=True)
            async for chunk in stream:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

**Flask:**

```python
from flask import stream_with_context

@app.route('/api/stream', methods=['POST'])
def stream_text():
    prompt = request.json.get('prompt')
    
    def generate():
        with Blossom(api_token=API_TOKEN) as client:
            for chunk in client.text.generate(prompt, stream=True):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream'
    )
```

### Client-Side JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>Streaming Example</title>
</head>
<body>
    <textarea id="prompt" rows="4" cols="50"></textarea>
    <button onclick="streamGenerate()">Generate</button>
    <div id="output"></div>

    <script>
        function streamGenerate() {
            const prompt = document.getElementById('prompt').value;
            const output = document.getElementById('output');
            output.textContent = '';

            const eventSource = new EventSource('/api/stream?prompt=' + encodeURIComponent(prompt));

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                output.textContent += data.chunk;
            };

            eventSource.onerror = function() {
                eventSource.close();
            };
        }
    </script>
</body>
</html>
```

---

## 👁️ Vision & Multimodal

Handle images and vision requests.

### Vision Analysis Endpoint

```python
from fastapi import UploadFile, File

@app.post("/api/vision/analyze-upload")
async def analyze_uploaded_image(
    file: UploadFile = File(...),
    prompt: str = "What's in this image?"
):
    """Analyze uploaded image"""
    try:
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        async with Blossom(api_token=API_TOKEN) as client:
            messages = [
                MessageBuilder.image(
                    role="user",
                    text=prompt,
                    image_path=tmp_path,
                    detail="high"
                )
            ]
            
            response = await client.text.chat(messages, model="openai")
        
        # Cleanup
        os.unlink(tmp_path)
        
        return {"analysis": response}
    
    except BlossomError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Multiple Images

```python
@app.post("/api/vision/compare")
async def compare_images(
    image_url1: str,
    image_url2: str,
    question: str = "Compare these images"
):
    """Compare two images"""
    async with Blossom(api_token=API_TOKEN) as client:
        messages = [
            MessageBuilder.image(
                role="user",
                text=question,
                image_url=image_url1,
                detail="high"
            ),
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "And this second image:"},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url2, "detail": "high"}
                    }
                ]
            }
        ]
        
        response = await client.text.chat(messages, model="openai")
        return {"comparison": response}
```

---

## 🔐 Authentication & Security

Protect your API endpoints.

### API Key Authentication

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key"""
    valid_keys = os.getenv("API_KEYS", "").split(",")
    if x_api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/api/text/generate")
async def generate_text(
    request: TextGenerateRequest,
    api_key: str = Depends(verify_api_key)
):
    # Your endpoint logic
    pass
```

### Rate Limiting

```python
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import time
from collections import defaultdict

# Simple in-memory rate limiter
request_counts = defaultdict(lambda: {"count": 0, "reset_time": time.time() + 60})

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    
    current_time = time.time()
    client_data = request_counts[client_ip]
    
    # Reset if time window passed
    if current_time > client_data["reset_time"]:
        client_data["count"] = 0
        client_data["reset_time"] = current_time + 60
    
    # Check limit (e.g., 100 requests per minute)
    if client_data["count"] >= 100:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )
    
    client_data["count"] += 1
    response = await call_next(request)
    return response

app.middleware("http")(rate_limit_middleware)
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Production Deployment

### Environment Configuration

```bash
# .env file
POLLINATIONS_API_KEY=your_api_token_here
API_KEYS=key1,key2,key3
ALLOWED_ORIGINS=https://yourdomain.com
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pollinations_api_key: str
    api_keys: str
    allowed_origins: str = "*"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POLLINATIONS_API_KEY=${POLLINATIONS_API_KEY}
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # For streaming
        proxy_buffering off;
        proxy_cache off;
    }
}
```

---

## ⚠️ Error Handling

Comprehensive error handling for production.

```python
from blossom_ai.core.errors import (
    BlossomError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    ModelNotFoundError
)

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": exc.message,
            "suggestion": exc.suggestion
        }
    )

@app.exception_handler(AuthenticationError)
async def auth_error_handler(request, exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content={
            "error": "authentication_error",
            "message": "Invalid API token"
        }
    )

@app.exception_handler(RateLimitError)
async def rate_limit_handler(request, exc: RateLimitError):
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_error",
            "message": exc.message,
            "retry_after": exc.retry_after
        },
        headers={"Retry-After": str(exc.retry_after)}
    )
```

---

## ⚡ Performance Optimization

### Connection Pooling

Blossom AI automatically handles connection pooling. Use context managers:

```python
# ✅ Good - Automatic cleanup
async with Blossom(api_token=API_TOKEN) as client:
    result = await client.text.generate(prompt)

# ❌ Bad - Manual cleanup required
client = Blossom(api_token=API_TOKEN)
result = await client.text.generate(prompt)
await client.close()  # Easy to forget!
```

### Caching

```python
from blossom_ai.utils import CacheManager, cached

cache = CacheManager()

@cached(ttl=3600)
async def generate_cached(prompt: str):
    async with Blossom(api_token=API_TOKEN) as client:
        return await client.text.generate(prompt)

@app.post("/api/cached/generate")
async def generate_with_cache(prompt: str):
    result = await generate_cached(prompt)
    return {"response": result}
```

### Background Tasks

```python
from fastapi import BackgroundTasks

def process_generation(prompt: str, user_id: str):
    """Process generation in background"""
    with Blossom(api_token=API_TOKEN) as client:
        result = client.text.generate(prompt)
        # Save to database, send notification, etc.
        save_result(user_id, result)

@app.post("/api/generate-async")
async def generate_async(
    prompt: str,
    user_id: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_generation, prompt, user_id)
    return {"status": "processing", "message": "Generation started"}
```

---

## 📚 Complete Example Projects

### 1. AI Chat Application

```python
# See full example at:
# https://github.com/PrimeevolutionZ/blossom-ai/examples/web/chat_app.py
```

### 2. Image Generation Service

```python
# See full example at:
# https://github.com/PrimeevolutionZ/blossom-ai/examples/web/image_service.py
```

### 3. Vision Analysis API

```python
# See full example at:
# https://github.com/PrimeevolutionZ/blossom-ai/examples/web/vision_api.py
```

---

## 🔗 Related Documentation

- [**API Reference**](API_REFERENCE.md) - Complete API documentation
- [**Vision Guide**](VISION.md) - Vision and multimodal features
- [**Error Handling**](ERROR_HANDLING.md) - Error handling patterns
- [**Security Policy**](../../SECURITY.md) - Security best practices
- [**Async Guide**](ASYNC_GUIDE.md) - Async programming patterns

---

## ❓ Troubleshooting

### Common Issues

**1. Connection pool exhausted**

```python
# Use context managers to ensure cleanup
async with Blossom(api_token=API_TOKEN) as client:
    # Your code
    pass
```

**2. Streaming not working**

```python
# Disable buffering in Nginx
proxy_buffering off;
proxy_cache off;
```

**3. High memory usage**

```python
# Don't store large responses in memory
# Stream or save to disk immediately
```

---

## 💡 Best Practices

✅ **Do:**
- Use environment variables for secrets
- Implement rate limiting
- Use async for FastAPI
- Enable CORS selectively
- Cache frequent requests
- Use context managers
- Handle errors gracefully
- Validate user input

❌ **Don't:**
- Hardcode API tokens
- Allow unlimited requests
- Block event loop with sync code
- Enable CORS for all origins in production
- Store sensitive data in logs
- Ignore resource cleanup
- Trust user input blindly

---

<div align="center">

**Made with 🌸 by [Eclips Team](https://github.com/PrimeevolutionZ)**

[PyPI Package](https://pypi.org/project/eclips-blossom-ai/) • [GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai) • [Report Issue](https://github.com/PrimeevolutionZ/blossom-ai/issues)

</div>