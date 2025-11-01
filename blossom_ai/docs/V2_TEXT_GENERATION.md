# 💬 V2 Text Generation Guide

> **Advanced text generation with OpenAI-compatible V2 API**

The V2 API brings OpenAI compatibility, function calling, structured outputs, and fine-grained control over text generation.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [New V2 Features](#-new-v2-features)
- [Advanced Parameters](#-advanced-parameters)
- [Function Calling](#-function-calling)
- [JSON Mode](#-json-mode)
- [Streaming](#-streaming)
- [Chat with History](#-chat-with-history)
- [Best Practices](#-best-practices)

---

## 🚀 Quick Start

```python
from blossom_ai import Blossom

# Initialize V2 client
client = Blossom(
    api_version="v2",
    api_token="your_token_here"
)

# Generate text with V2 features
response = client.text.generate(
    prompt="Explain quantum computing in simple terms",
    model="openai",
    max_tokens=200,  # NEW: Limit response length
    frequency_penalty=0.5,  # NEW: Reduce repetition
    presence_penalty=0.3  # NEW: Encourage diversity
)

print(response)
client.close_sync()
```

---

## ✨ New V2 Features

| Feature | Description | Example |
|---------|-------------|---------|
| **max_tokens** | Limit response length | `100`, `500`, `2000` |
| **frequency_penalty** | Reduce word repetition | `0.0` - `2.0` |
| **presence_penalty** | Encourage topic diversity | `0.0` - `2.0` |
| **top_p** | Nucleus sampling | `0.1` - `1.0` |
| **tools** | Function calling | Tool definitions |
| **tool_choice** | Control function use | `"auto"`, `"none"`, specific tool |
| **json_mode** | Structured output | `True` / `False` |
| **n** | Multiple completions | `1` - `128` |

---

## ⚙️ Advanced Parameters

### Max Tokens

Control the maximum length of the response.

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Short response
response = client.text.generate(
    "Explain AI",
    max_tokens=50  # ~50 words
)

# Medium response
response = client.text.generate(
    "Explain AI in detail",
    max_tokens=300  # ~300 words
)

# Long response
response = client.text.generate(
    "Write a comprehensive article about AI",
    max_tokens=2000  # ~2000 words
)

client.close_sync()
```

**Guidelines:**
- **50-100 tokens**: Short answers, summaries
- **200-500 tokens**: Paragraphs, explanations
- **1000+ tokens**: Articles, detailed content

---

### Frequency Penalty

Reduces repetition of words and phrases.

```python
# No penalty (may repeat words)
response = client.text.generate(
    "Write about the ocean",
    frequency_penalty=0.0
)

# Moderate penalty (balanced)
response = client.text.generate(
    "Write about the ocean",
    frequency_penalty=0.5  # Good default
)

# High penalty (very diverse vocabulary)
response = client.text.generate(
    "Write about the ocean",
    frequency_penalty=1.5
)
```

**Range:** `0.0` to `2.0`
- `0.0` - No penalty, may repeat
- `0.5` - Balanced (recommended)
- `1.0+` - Strong diversity

**Use Cases:**
- **Creative writing**: `0.5-1.0`
- **Technical docs**: `0.0-0.3`
- **Poetry**: `1.0-2.0`

---

### Presence Penalty

Encourages discussing new topics instead of repeating the same topic.

```python
# Focused on one topic
response = client.text.generate(
    "Tell me about space",
    presence_penalty=0.0
)

# Moderate diversity
response = client.text.generate(
    "Tell me about space",
    presence_penalty=0.5
)

# High topic diversity
response = client.text.generate(
    "Tell me about space",
    presence_penalty=1.5
)
```

**Range:** `0.0` to `2.0`
- `0.0` - Can repeat topics
- `0.5` - Balanced
- `1.5+` - Strong topic diversity

---

### Top-P (Nucleus Sampling)

Controls randomness by limiting word choices to top probability mass.

```python
# Very focused (deterministic)
response = client.text.generate(
    "Complete: The capital of France is",
    top_p=0.1  # Only most likely words
)

# Balanced
response = client.text.generate(
    "Write a story",
    top_p=0.9  # More creative
)

# Maximum creativity
response = client.text.generate(
    "Write a surreal poem",
    top_p=1.0  # All possibilities
)
```

**Range:** `0.1` to `1.0`
- `0.1-0.3` - Very focused, factual
- `0.7-0.9` - Balanced (default: `0.9`)
- `1.0` - Maximum creativity

---

### Temperature (Extended Range)

V2 extends temperature range to `0-2` (V1 was `0-1`).

```python
# Deterministic (factual)
response = client.text.generate(
    "What is 2+2?",
    temperature=0.0
)

# Balanced
response = client.text.generate(
    "Explain photosynthesis",
    temperature=0.7
)

# Creative (V2 extended range!)
response = client.text.generate(
    "Write a surreal story",
    temperature=1.5  # NEW in V2!
)
```

---

### Combined Parameters Example

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Generate creative, non-repetitive content
response = client.text.generate(
    prompt="Write a unique story about a robot",
    model="openai",
    max_tokens=500,
    temperature=0.9,
    frequency_penalty=0.8,  # Avoid repetition
    presence_penalty=0.6,  # Diverse topics
    top_p=0.95  # Creative but coherent
)

print(response)
client.close_sync()
```

---

## 🛠️ Function Calling

Enable AI to call functions in your application.

### Basic Function Calling

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

# Define available functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. London"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Chat with function calling
response = client.text.chat(
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ],
    model="openai",
    tools=tools,
    tool_choice="auto"  # AI decides when to call
)

print(response)
client.close_sync()
```

### Multiple Functions

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]

response = client.text.chat(
    messages=[
        {"role": "user", "content": "What is 15% of 200?"}
    ],
    tools=tools,
    tool_choice="auto"
)
```

### Tool Choice Options

```python
# Let AI decide when to use tools
tool_choice="auto"

# Never use tools (just chat)
tool_choice="none"

# Force specific tool
tool_choice={"type": "function", "function": {"name": "get_weather"}}
```

### Real-World Example: AI Assistant

```python
from blossom_ai import Blossom
import json

def get_weather(location, unit="celsius"):
    """Simulated weather API"""
    return {"temp": 22, "condition": "sunny", "location": location}

def search_web(query):
    """Simulated search API"""
    return {"results": f"Search results for: {query}"}

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

client = Blossom(api_version="v2", api_token="token")

# User asks a question
user_message = "What's the weather in London and search for London attractions"

response = client.text.chat(
    messages=[{"role": "user", "content": user_message}],
    tools=tools,
    tool_choice="auto"
)

print(f"AI Response: {response}")

# In real implementation, you'd parse tool calls and execute them
# Then send results back to the AI for final response

client.close_sync()
```

---

## 📋 JSON Mode

Force structured JSON output.

### Basic JSON Mode

```python
from blossom_ai import Blossom
import json

client = Blossom(api_version="v2", api_token="token")

response = client.text.generate(
    prompt="Generate a person with name, age, and city",
    model="openai",
    json_mode=True  # Force JSON output
)

# Parse JSON
data = json.loads(response)
print(data)
# {"name": "John Doe", "age": 30, "city": "New York"}

client.close_sync()
```

### Complex JSON Structures

```python
response = client.text.generate(
    prompt=(
        "Generate a company profile with: "
        "name, founded_year, employees (number), "
        "products (array of product names), "
        "headquarters (object with city and country)"
    ),
    json_mode=True,
    max_tokens=300
)

data = json.loads(response)
print(json.dumps(data, indent=2))
```

**Output:**
```json
{
  "name": "TechCorp",
  "founded_year": 2010,
  "employees": 500,
  "products": ["Widget A", "Service B", "Platform C"],
  "headquarters": {
    "city": "San Francisco",
    "country": "USA"
  }
}
```

### Validation Example

```python
from blossom_ai import Blossom
import json

client = Blossom(api_version="v2", api_token="token")

def generate_user_profile():
    response = client.text.generate(
        prompt=(
            "Generate a user profile JSON with: "
            "username (string), "
            "email (valid email format), "
            "age (integer 18-100), "
            "interests (array of 3-5 strings)"
        ),
        json_mode=True,
        max_tokens=200
    )
    
    try:
        data = json.loads(response)
        
        # Validate structure
        assert "username" in data
        assert "email" in data
        assert "@" in data["email"]
        assert isinstance(data["age"], int)
        assert 18 <= data["age"] <= 100
        assert isinstance(data["interests"], list)
        
        return data
    except (json.JSONDecodeError, AssertionError, KeyError) as e:
        print(f"Validation failed: {e}")
        return None

profile = generate_user_profile()
print(profile)

client.close_sync()
```

---

## 🌊 Streaming

Real-time text generation with chunks.

### Basic Streaming

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

print("AI: ", end="", flush=True)

for chunk in client.text.generate(
    "Tell me a short story about a robot",
    model="openai",
    stream=True
):
    print(chunk, end="", flush=True)

print()  # Newline at end
client.close_sync()
```

### Streaming with Error Handling

```python
from blossom_ai import Blossom, StreamError

client = Blossom(api_version="v2", api_token="token")

chunks = []

try:
    for chunk in client.text.generate(
        "Write a poem",
        stream=True,
        max_tokens=200
    ):
        print(chunk, end="", flush=True)
        chunks.append(chunk)
except StreamError as e:
    print(f"\nStream error: {e.message}")
finally:
    full_text = "".join(chunks)
    print(f"\n\nReceived {len(chunks)} chunks")
    print(f"Total: {len(full_text)} characters")
    client.close_sync()
```

### Streaming Chat

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Explain machine learning"}
]

print("Assistant: ", end="", flush=True)

for chunk in client.text.chat(
    messages=messages,
    model="openai",
    stream=True
):
    print(chunk, end="", flush=True)

print()
client.close_sync()
```

---

## 💬 Chat with History

Multi-turn conversations with context.

### Basic Chat

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

messages = [
    {"role": "user", "content": "Hi! My name is Alice"},
    {"role": "assistant", "content": "Hello Alice! Nice to meet you."},
    {"role": "user", "content": "What's my name?"}
]

response = client.text.chat(
    messages=messages,
    model="openai"
)

print(response)  # Should mention "Alice"
client.close_sync()
```

### Conversation Loop

```python
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")

messages = [
    {"role": "system", "content": "You are a helpful math tutor"}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        break
    
    # Add user message
    messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    response = client.text.chat(
        messages=messages,
        model="openai",
        max_tokens=200
    )
    
    # Add AI response to history
    messages.append({"role": "assistant", "content": response})
    
    print(f"AI: {response}\n")

client.close_sync()
```

### Context Management

```python
from blossom_ai import Blossom

MAX_HISTORY = 10  # Keep last 10 messages

client = Blossom(api_version="v2", api_token="token")

messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]

def add_message(role, content):
    messages.append({"role": role, "content": content})
    
    # Keep system message + last MAX_HISTORY messages
    if len(messages) > MAX_HISTORY + 1:
        # Keep system message (index 0) and recent messages
        messages[:] = [messages[0]] + messages[-(MAX_HISTORY):]

# Chat conversation
add_message("user", "Hello")
response = client.text.chat(messages=messages)
add_message("assistant", response)

add_message("user", "Tell me about AI")
response = client.text.chat(messages=messages)
add_message("assistant", response)

client.close_sync()
```

---

## ✅ Best Practices

### 1. Choose the Right Model

```python
# For general tasks
model = "openai"

# For faster responses
model = "openai-fast"

# For coding tasks
model = "qwen-coder"

# Check available models
models = client.text.models()
print(models)
```

### 2. Prompt Engineering

**✅ DO:**
```python
# Be specific
prompt = "Explain quantum computing in simple terms for a 10-year-old"

# Provide context
prompt = "You are a teacher. Explain photosynthesis to a 5th grade student"

# Use examples
prompt = "Translate to French:\n\nEnglish: Hello\nFrench: Bonjour\n\nEnglish: Goodbye\nFrench:"
```

**❌ DON'T:**
```python
# Too vague
prompt = "Tell me something"

# Too long (respect max_tokens)
prompt = "..." * 10000  # Will be truncated
```

### 3. Parameter Combinations

**For Factual Content:**
```python
response = client.text.generate(
    prompt,
    temperature=0.3,  # Low randomness
    top_p=0.8,
    frequency_penalty=0.0,
    presence_penalty=0.0
)
```

**For Creative Content:**
```python
response = client.text.generate(
    prompt,
    temperature=1.2,  # High creativity
    top_p=0.95,
    frequency_penalty=0.8,
    presence_penalty=0.6
)
```

**For Technical Writing:**
```python
response = client.text.generate(
    prompt,
    temperature=0.5,
    frequency_penalty=0.3,
    max_tokens=1000
)
```

### 4. Error Handling

```python
from blossom_ai import (
    Blossom, BlossomError, 
    RateLimitError, ValidationError
)

client = Blossom(api_version="v2", api_token="token")

try:
    response = client.text.generate(
        prompt="Test",
        max_tokens=100
    )
except RateLimitError as e:
    print(f"Rate limited. Wait {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid params: {e.message}")
except BlossomError as e:
    print(f"Error: {e.message}")
finally:
    client.close_sync()
```

### 5. Async Usage

```python
import asyncio
from blossom_ai import Blossom

async def generate_multiple():
    async with Blossom(api_version="v2", api_token="token") as client:
        # Generate multiple responses in parallel
        tasks = [
            client.text.generate(f"Topic {i}", max_tokens=100)
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            print(f"Result {i}: {result[:50]}...")

asyncio.run(generate_multiple())
```

---

## 🔗 Related Documentation

- **[V2 Migration Guide](V2_MIGRATION_GUIDE.md)** - Migrate from V1 to V2
- **[V2 Image Generation](V2_IMAGE_GENERATION.md)** - Advanced image features
- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API docs
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors properly

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>