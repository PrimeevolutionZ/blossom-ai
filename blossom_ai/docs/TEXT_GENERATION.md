# 💬 Text Generation Guide

Complete guide to generating text with Blossom AI V2 API (OpenAI-compatible).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [Generation Methods](#generation-methods)
- [Streaming](#streaming)
- [Chat Mode](#chat-mode)
- [System Messages](#system-messages)
- [Advanced Parameters](#advanced-parameters)
- [JSON Mode](#json-mode)
- [Function Calling](#function-calling)
- [Models](#models)
- [Temperature & Creativity](#temperature--creativity)
- [Token Control](#token-control)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## 🌟 Overview

Blossom AI v0.5.0 uses the Pollinations V2 API for text generation with OpenAI-compatible interface:

- 💬 **Multiple Models** - openai, deepseek, mistral, claude, and more
- 🌊 **Streaming** - Real-time response generation
- 🛠️ **Function Calling** - Tool use and API integration
- 📋 **JSON Mode** - Structured output guaranteed
- ⚙️ **Advanced Control** - Temperature, max_tokens, penalties
- 👁️ **Vision Support** - Analyze images (see [Vision Guide](VISION.md))
- 🔊 **Audio Support** - Audio input/output (see [Audio Guide](AUDIO.md))

### Supported Models

Common models (fetch dynamically for full list):
- `openai` (default) - GPT-based, versatile
- `openai-fast` - Faster responses
- `openai-large` - Maximum capability
- `openai-reasoning` - Enhanced reasoning
- `deepseek` - Alternative provider
- `mistral` - Mistral AI
- `claude` - Anthropic Claude
- And more...

---

## 🚀 Basic Usage

### Simplest Example

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Generate text
    response = client.text.generate(
        prompt="Explain quantum computing in simple terms"
    )
    print(response)
```

### With System Message

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a function to reverse a string",
        system="You are an expert Python programmer"
    )
    print(response)
```

### With Parameters

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a creative story",
        model="openai",
        temperature=0.8,      # More creative
        max_tokens=500,       # Limit length
        system="You are a creative writer"
    )
    print(response)
```

---

## 📦 Generation Methods

### 1. `generate()` - Simple Text

Convenience method for quick text generation.

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="What is Python?",
        model="openai",
        temperature=0.7
    )
    print(response)
```

**Use when:**
- Quick one-off generations
- Simple prompts
- Don't need conversation history

**Parameters:**
- `prompt` - Your text prompt (required)
- `system` - System message (optional)
- `model` - Model to use (default: "openai")
- `temperature` - Creativity level 0-2 (default: 1.0)
- `max_tokens` - Maximum response length (optional)
- `stream` - Enable streaming (default: False)
- `json_mode` - Force JSON output (default: False)
- `tools` - Function calling tools (optional)

### 2. `chat()` - Conversation

Full-featured chat with message history.

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What is Python?"}
    ]
    
    response = client.text.chat(
        messages=messages,
        model="openai",
        temperature=0.7
    )
    print(response)
```

**Use when:**
- Multi-turn conversations
- Need conversation context
- Complex interactions
- Function calling
- Vision/audio features

**Message Format:**
```python
messages = [
    {"role": "system", "content": "System instructions"},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Assistant response"},
    {"role": "user", "content": "Next user message"}
]
```

**Roles:**
- `system` - Instructions for the AI
- `user` - Messages from the user
- `assistant` - Responses from AI (for context)

---

## 🌊 Streaming

Stream responses in real-time for better UX.

### Basic Streaming

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    print("AI: ", end="", flush=True)
    
    for chunk in client.text.generate(
        prompt="Tell me a short story",
        stream=True
    ):
        print(chunk, end="", flush=True)
    
    print()  # New line at end
```

### Streaming with System Message

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    for chunk in client.text.generate(
        prompt="Explain machine learning",
        system="You are a teacher explaining to beginners",
        stream=True,
        max_tokens=300
    ):
        print(chunk, end="", flush=True)
```

### Streaming Chat

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain async programming"}
    ]
    
    print("Response: ", end="", flush=True)
    for chunk in client.text.chat(messages, stream=True):
        print(chunk, end="", flush=True)
    print()
```

### Collecting Streamed Response

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    chunks = []
    
    for chunk in client.text.generate("Count to 5", stream=True):
        chunks.append(chunk)
        print(chunk, end="", flush=True)
    
    full_response = "".join(chunks)
    print(f"\n\nFull length: {len(full_response)} chars")
```

### Async Streaming

```python
import asyncio
from blossom_ai import Blossom

async def stream_example():
    async with Blossom(api_token="your-token") as client:
        print("AI: ", end="", flush=True)
        
        # Get async generator
        stream = await client.text.generate(
            "Tell me about Python",
            stream=True
        )
        
        # Iterate async
        async for chunk in stream:
            print(chunk, end="", flush=True)
        
        print()

asyncio.run(stream_example())
```

---

## 💬 Chat Mode

Build multi-turn conversations with context.

### Basic Chat

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant"},
        {"role": "user", "content": "What is Python?"}
    ]
    
    response = client.text.chat(messages)
    print(response)
```

### Multi-Turn Conversation

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Initialize conversation
    conversation = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]
    
    # Turn 1
    conversation.append({"role": "user", "content": "What is Python?"})
    response1 = client.text.chat(conversation)
    conversation.append({"role": "assistant", "content": response1})
    print(f"AI: {response1}\n")
    
    # Turn 2 (with context from Turn 1)
    conversation.append({"role": "user", "content": "What are its main uses?"})
    response2 = client.text.chat(conversation)
    conversation.append({"role": "assistant", "content": response2})
    print(f"AI: {response2}\n")
    
    # Turn 3
    conversation.append({"role": "user", "content": "Show me a code example"})
    response3 = client.text.chat(conversation)
    print(f"AI: {response3}")
```

### Interactive Chat Loop

```python
from blossom_ai import Blossom

def chat_loop():
    with Blossom(api_token="your-token") as client:
        messages = [
            {"role": "system", "content": "You are a friendly assistant"}
        ]
        
        print("Chat started! Type 'quit' to exit.\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Add to conversation
            messages.append({"role": "user", "content": user_input})
            
            # Get response
            print("AI: ", end="", flush=True)
            response_chunks = []
            
            for chunk in client.text.chat(messages, stream=True):
                print(chunk, end="", flush=True)
                response_chunks.append(chunk)
            
            print("\n")
            
            # Add assistant response to history
            full_response = "".join(response_chunks)
            messages.append({"role": "assistant", "content": full_response})

chat_loop()
```

### Chat with Memory Limit

```python
from blossom_ai import Blossom

class ChatBot:
    def __init__(self, client, max_history=10):
        self.client = client
        self.max_history = max_history
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]
    
    def chat(self, user_message):
        # Add user message
        self.messages.append({"role": "user", "content": user_message})
        
        # Keep only recent history (system + last N messages)
        if len(self.messages) > self.max_history + 1:
            # Keep system message + recent messages
            self.messages = [self.messages[0]] + self.messages[-(self.max_history):]
        
        # Get response
        response = self.client.text.chat(self.messages)
        
        # Add assistant response
        self.messages.append({"role": "assistant", "content": response})
        
        return response

with Blossom(api_token="your-token") as client:
    bot = ChatBot(client, max_history=10)
    
    print(bot.chat("Hello!"))
    print(bot.chat("What can you help me with?"))
    print(bot.chat("Tell me about Python"))
```

---

## 🎯 System Messages

Control AI behavior with system messages.

### Basic System Message

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="Write a function to sort a list",
        system="You are an expert Python programmer. Write clean, efficient code."
    )
    print(response)
```

### Role-Based Systems

```python
from blossom_ai import Blossom

# Teacher
response = client.text.generate(
    "Explain recursion",
    system="You are a patient teacher explaining concepts to beginners. Use simple language and examples."
)

# Technical Writer
response = client.text.generate(
    "Document this API",
    system="You are a technical writer. Write clear, concise documentation with examples."
)

# Code Reviewer
response = client.text.generate(
    "Review this code: [code here]",
    system="You are a senior code reviewer. Focus on best practices, performance, and security."
)
```

### System Message Best Practices

```python
# ✅ Good: Specific, clear role
system = "You are a Python expert. Provide code examples with explanations."

# ✅ Good: Detailed instructions
system = """You are a helpful assistant that:
1. Answers questions clearly and concisely
2. Provides code examples when relevant
3. Explains complex concepts in simple terms
4. Always considers edge cases
"""

# ❌ Bad: Too vague
system = "Be helpful"

# ❌ Bad: Conflicting instructions
system = "Be brief but also very detailed"
```

---

## ⚙️ Advanced Parameters

### Complete Parameter List

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    response = client.text.chat(
        # Required
        messages=[{"role": "user", "content": "Hello"}],
        
        # Model Selection
        model="openai",              # Model to use
        
        # Creativity Control
        temperature=1.0,             # 0-2, higher = more creative
        top_p=1.0,                   # 0-1, nucleus sampling
        
        # Length Control
        max_tokens=None,             # Max response length
        
        # Repetition Control
        frequency_penalty=0.0,       # -2 to 2, penalize frequent tokens
        presence_penalty=0.0,        # -2 to 2, penalize repeated topics
        
        # Output Format
        stream=False,                # Enable streaming
        json_mode=False,             # Force JSON output
        n=1,                         # Number of completions
        
        # Advanced Features
        tools=None,                  # Function calling tools
        tool_choice=None,            # Tool selection strategy
        thinking=None,               # Native reasoning (V2)
        modalities=None,             # ["text", "audio"]
        audio=None                   # Audio output config
    )
```

### Parameter Details

#### `temperature`
Controls randomness and creativity.

```python
# Deterministic, focused (good for code, facts)
response = client.text.generate(
    "What is 2+2?",
    temperature=0.0
)

# Balanced (default, general use)
response = client.text.generate(
    "Write a story",
    temperature=1.0
)

# Creative, varied (good for creative writing)
response = client.text.generate(
    "Write a poem",
    temperature=1.5
)
```

**Range:** 0.0-2.0
- `0.0-0.3` - Very focused, deterministic
- `0.4-0.7` - Balanced, consistent
- `0.8-1.2` - Creative, varied (default: 1.0)
- `1.3-2.0` - Highly creative, unpredictable

#### `max_tokens`
Limit response length.

```python
# Short response
response = client.text.generate(
    "Explain Python",
    max_tokens=50  # ~50 tokens ≈ 30-40 words
)

# Medium response
response = client.text.generate(
    "Write a tutorial",
    max_tokens=500  # ~500 tokens ≈ 350-400 words
)

# Long response
response = client.text.generate(
    "Write a detailed guide",
    max_tokens=2000  # ~2000 tokens ≈ 1500 words
)
```

**Note:** 1 token ≈ 0.75 words (English)

#### `frequency_penalty`
Reduce repetition of tokens.

```python
# No penalty (may repeat)
response = client.text.generate(
    prompt,
    frequency_penalty=0.0
)

# Light penalty (default)
response = client.text.generate(
    prompt,
    frequency_penalty=0.3
)

# Strong penalty (avoid repetition)
response = client.text.generate(
    prompt,
    frequency_penalty=1.0
)
```

**Range:** -2.0 to 2.0
- Positive values reduce repetition
- Negative values encourage repetition
- `0.3-0.7` recommended for most use cases

#### `presence_penalty`
Encourage new topics and ideas.

```python
# Encourage diverse topics
response = client.text.generate(
    "Write about technology",
    presence_penalty=0.6
)
```

**Range:** -2.0 to 2.0
- Positive values encourage new topics
- Negative values stay on topic
- `0.3-0.6` good for creative writing

#### `top_p`
Nucleus sampling (alternative to temperature).

```python
# Focused (use most likely tokens)
response = client.text.generate(
    prompt,
    top_p=0.1
)

# Balanced
response = client.text.generate(
    prompt,
    top_p=0.9
)

# Diverse
response = client.text.generate(
    prompt,
    top_p=1.0  # Default
)
```

**Range:** 0.0-1.0
- Lower = more focused
- Higher = more diverse
- Use either `temperature` or `top_p`, not both

---

## 📋 JSON Mode

Force AI to return valid JSON.

### Basic JSON Mode

```python
from blossom_ai import Blossom
import json

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="List 3 programming languages with their use cases",
        json_mode=True
    )
    
    # Parse JSON
    data = json.loads(response)
    print(json.dumps(data, indent=2))
```

### Structured Data Extraction

```python
from blossom_ai import Blossom
import json

with Blossom(api_token="your-token") as client:
    response = client.text.generate(
        prompt="""Extract information from this text:
        "John Doe, age 30, lives in New York, works as a software engineer"
        
        Return JSON with fields: name, age, city, occupation""",
        json_mode=True
    )
    
    person = json.loads(response)
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    print(f"City: {person['city']}")
```

### JSON Schema Guidance

```python
from blossom_ai import Blossom
import json

with Blossom(api_token="your-token") as client:
    schema_prompt = """Return a JSON object with this schema:
    {
        "title": "string",
        "author": "string",
        "year": number,
        "genres": ["string"],
        "rating": number (1-5)
    }
    
    Create a book recommendation."""
    
    response = client.text.generate(
        schema_prompt,
        json_mode=True
    )
    
    book = json.loads(response)
    print(json.dumps(book, indent=2))
```

### JSON with Chat

```python
from blossom_ai import Blossom
import json

with Blossom(api_token="your-token") as client:
    messages = [
        {
            "role": "system",
            "content": "You return data in JSON format only. No markdown, no explanations."
        },
        {
            "role": "user",
            "content": "List 3 cities with population and country"
        }
    ]
    
    response = client.text.chat(messages, json_mode=True)
    cities = json.loads(response)
    print(json.dumps(cities, indent=2))
```

---

## 🛠️ Function Calling

**NEW in V2!** Let AI call functions/tools.

### Basic Function Calling

```python
from blossom_ai import Blossom
import json

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
                        "description": "City name, e.g., London"
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

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "user", "content": "What's the weather in London?"}
    ]
    
    response = client.text.chat(
        messages=messages,
        tools=tools,
        model="openai"
    )
    
    print(response)
```

### Complete Function Calling Example

```python
from blossom_ai import Blossom
import json

def get_weather(location, unit="celsius"):
    """Simulated weather API"""
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "condition": "sunny"
    }

def calculate(operation, a, b):
    """Calculator function"""
    ops = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b if b != 0 else "Error: Division by zero"
    }
    return ops.get(operation, lambda: "Unknown operation")()

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
            "name": "calculate",
            "description": "Perform calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]

# Function registry
functions = {
    "get_weather": get_weather,
    "calculate": calculate
}

with Blossom(api_token="your-token") as client:
    messages = [
        {"role": "user", "content": "What's 15 + 27?"}
    ]
    
    # Get AI response (may include tool calls)
    response = client.text.chat(
        messages=messages,
        tools=tools
    )
    
    # Check if AI wants to call a function
    # (Note: Response format may vary, check API docs)
    print(f"Response: {response}")
```

### Tool Choice Strategies

```python
# Auto (let AI decide)
response = client.text.chat(
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Default
)

# Force specific function
response = client.text.chat(
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)

# No functions (text only)
response = client.text.chat(
    messages=messages,
    tools=tools,
    tool_choice="none"
)
```

---

## 🎭 Models

### List Available Models

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    models = client.text.models()
    print(f"Available models: {models}")
```

### Common Models

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # OpenAI (default)
    client.text.generate("Hello", model="openai")
    
    # OpenAI Fast
    client.text.generate("Hello", model="openai-fast")
    
    # OpenAI Large
    client.text.generate("Complex task", model="openai-large")
    
    # OpenAI Reasoning
    client.text.generate("Solve this", model="openai-reasoning")
    
    # Deepseek
    client.text.generate("Hello", model="deepseek")
    
    # Mistral
    client.text.generate("Hello", model="mistral")
    
    # Claude
    client.text.generate("Hello", model="claude")
```

### Model Selection Guide

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `openai-fast` | ⚡⚡⚡⚡ | ⭐⭐⭐ | 💰 | Quick responses, chat |
| `openai` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | General use (default) |
| `openai-large` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Complex tasks |
| `openai-reasoning` | ⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Problem-solving |
| `deepseek` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | Alternative, coding |
| `mistral` | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | Multilingual |
| `claude` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Long context, analysis |

---

## 🌡️ Temperature & Creativity

### Understanding Temperature

Temperature controls randomness in responses:

```python
# Deterministic (same prompt = same output)
response = client.text.generate(
    "What is 2 + 2?",
    temperature=0.0
)

# Slightly varied
response = client.text.generate(
    "Explain Python",
    temperature=0.3
)

# Balanced (default)
response = client.text.generate(
    "Write a paragraph",
    temperature=1.0
)

# Creative
response = client.text.generate(
    "Write a creative story",
    temperature=1.5
)

# Highly creative/random
response = client.text.generate(
    "Generate ideas",
    temperature=2.0
)
```

### Use Cases by Temperature

**0.0-0.3: Factual, Consistent**
- Mathematical calculations
- Code generation
- Factual questions
- Data extraction
- Translations

**0.4-0.7: Balanced**
- Technical documentation
- Explanations
- Summaries
- General Q&A

**0.8-1.2: Moderate Creativity**
- Blog posts
- Marketing copy
- General writing
- Brainstorming

**1.3-2.0: High Creativity**
- Creative writing
- Poetry
- Experimental ideas
- Diverse variations

### Example: Temperature Comparison

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    prompt = "Complete this sentence: The future of AI is"
    
    for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
        response = client.text.generate(
            prompt,
            temperature=temp,
            max_tokens=30
        )
        print(f"Temperature {temp}: {response}\n")
```

---

## 🎯 Token Control

### Understanding Tokens

- **1 token ≈ 0.75 words** (English)
- **1000 tokens ≈ 750 words**
- Includes prompt + response

### Limiting Response Length

```python
from blossom_ai import Blossom

with Blossom(api_token="your-token") as client:
    # Very short (1-2 sentences)
    client.text.generate(
        "Explain Python",
        max_tokens=50
    )
    
    # Short paragraph
    client.text.generate(
        "Explain Python",
        max_tokens=150
    )
    
    # Medium (few paragraphs)
    client.text.generate(
        "Write a tutorial",
        max_tokens=500
    )
    
    # Long (article)
    client.text.generate(
        "Write a comprehensive guide",
        max_tokens=2000
    )
```

### Token Budgeting

```python
from blossom_ai import Blossom

def estimate_tokens(text):
    """Rough token estimation"""
    return len(text.split()) * 1.3  # Conservative estimate

with Blossom(api_token="your-token") as client:
    prompt = "Write about Python"
    prompt_tokens = estimate_tokens(prompt)
    
    # Reserve tokens for response
    max_response_tokens = 500
    
    response = client.text.generate(
        prompt,
        max_tokens=max_response_tokens
    )
    
    response_tokens = estimate_tokens(response)
    total_tokens = prompt_tokens + response_tokens
    
    print(f"Prompt: ~{prompt_tokens:.0f} tokens")
    print(f"Response: ~{response_tokens:.0f} tokens")
    print(f"Total: ~{total_tokens:.0f} tokens")
```

---

## ✅ Best Practices

### 1. Prompt Engineering

```python
# ❌ Bad: Vague
prompt = "Tell me about Python"

# ✅ Good: Specific
prompt = "Explain Python's main features for beginners in 3 paragraphs"

# ✅ Better: Very detailed
prompt = """Explain Python programming language:
1. What it is
2. Main features
3. Common use cases
4. Why it's popular

Target audience: Complete beginners
Format: Simple language, bullet points
Length: 200-300 words"""
```

### 2. Use System Messages

```python
# Set consistent behavior
system = """You are a helpful Python tutor.
- Explain concepts simply
- Provide code examples
- Use analogies
- Ask clarifying questions if needed"""

response = client.text.generate(
    "Explain variables",
    system=system
)
```

### 3. Control Output Length

```python
# Prevent overly long responses
response = client.text.generate(
    "Explain Python",
    max_tokens=200  # ~150 words
)

# Or specify in prompt
response = client.text.generate(
    "Explain Python in 2 paragraphs (max 100 words)"
)
```

### 4. Use Appropriate Temperature

```python
# Factual/code: Low temperature
code = client.text.generate(
    "Write a sorting function",
    temperature=0.2
)

# Creative writing: High temperature
story = client.text.generate(
    "Write a creative story",
    temperature=1.3
)
```

### 5. Stream for Better UX

```python
# Streaming provides instant feedback
for chunk in client.text.generate("Explain...", stream=True):
    print(chunk, end="", flush=True)
```

### 6. Handle Errors Gracefully

```python
from blossom_ai import Blossom, BlossomError

try:
    response = client.text.generate("Hello")
except BlossomError as e:
    print(f"Error: {e.message}")
    if e.suggestion:
        print(f"Suggestion: {e.suggestion}")
```

### 7. Use JSON Mode for Structured Data

```python
import json

response = client.text.generate(
    "List 3 cities with country",
    json_mode=True
)
data = json.loads(response)
```

### 8. Manage Conversation History

```python
# Limit history to avoid token limits
MAX_HISTORY = 10

if len(messages) > MAX_HISTORY + 1:  # +1 for system message
    messages = [messages[0]] + messages[-MAX_HISTORY:]
```

### 9. Test Different Models

```python
models = ["openai-fast", "openai", "deepseek"]

for model in models:
    response = client.text.generate("Test", model=model)
    print(f"{model}: {response[:50]}...")
```

### 10. Cache Common Responses

```python
from blossom_ai.utils import cached

@cached(ttl=3600)  # Cache for 1 hour
def get_explanation(topic):
    return client.text.generate(f"Explain {topic}")
```

---

## 🛡️ Error Handling

### Common Errors

#### ValidationError

```python
from blossom_ai import Blossom, ValidationError

with Blossom(api_token="your-token") as client:
    try:
        # Prompt too long
        client.text.generate("a" * 15000)
    except ValidationError as e:
        print(f"Invalid input: {e.message}")
```

#### AuthenticationError

```python
from blossom_ai import Blossom, AuthenticationError

try:
    client = Blossom(api_token="invalid-token")
    client.text.generate("Hello")
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

#### RateLimitError

```python
from blossom_ai import Blossom, RateLimitError
import time

with Blossom(api_token="your-token") as client:
    try:
        response = client.text.generate("Hello")
    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
        if e.retry_after:
            print(f"Waiting {e.retry_after}s...")
            time.sleep(e.retry_after)
            # Retry
            response = client.text.generate("Hello")
```

#### StreamError

```python
from blossom_ai import Blossom, StreamError

with Blossom(api_token="your-token") as client:
    try:
        for chunk in client.text.generate("Hello", stream=True):
            print(chunk, end="", flush=True)
    except StreamError as e:
        print(f"\nStream error: {e.message}")
```

### Complete Error Handling

```python
from blossom_ai import (
    Blossom,
    BlossomError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    StreamError,
    NetworkError,
    TimeoutError
)

with Blossom(api_token="your-token") as client:
    try:
        response = client.text.generate("Hello AI!")
        print(response)
        
    except ValidationError as e:
        print(f"❌ Invalid input: {e.message}")
        
    except AuthenticationError as e:
        print(f"❌ Auth failed: {e.message}")
        print(f"💡 {e.suggestion}")
        
    except RateLimitError as e:
        print(f"❌ Rate limited: {e.message}")
        if e.retry_after:
            print(f"⏳ Retry after {e.retry_after}s")
            
    except StreamError as e:
        print(f"❌ Stream error: {e.message}")
        
    except TimeoutError as e:
        print(f"❌ Timeout: {e.message}")
        
    except NetworkError as e:
        print(f"❌ Network error: {e.message}")
        
    except BlossomError as e:
        print(f"❌ Error: {e.message}")
```

---

## 📚 Examples

### Example 1: Code Generator

```python
from blossom_ai import Blossom

def generate_code(description, language="Python"):
    with Blossom(api_token="your-token") as client:
        system = f"""You are an expert {language} programmer.
Generate clean, well-commented code.
Include docstrings and type hints where appropriate."""

        response = client.text.generate(
            prompt=f"Write a {language} function: {description}",
            system=system,
            temperature=0.2,  # Low for consistent code
            max_tokens=500
        )
        return response

# Use it
code = generate_code("Sort a list of dictionaries by a key")
print(code)
```

### Example 2: Chatbot with Memory

```python
from blossom_ai import Blossom

class Chatbot:
    def __init__(self, api_token, personality="helpful"):
        self.client = Blossom(api_token=api_token)
        self.messages = [
            {"role": "system", "content": f"You are a {personality} assistant"}
        ]
    
    def chat(self, user_message, stream=False):
        self.messages.append({"role": "user", "content": user_message})
        
        if stream:
            chunks = []
            for chunk in self.client.text.chat(self.messages, stream=True):
                print(chunk, end="", flush=True)
                chunks.append(chunk)
            print()
            response = "".join(chunks)
        else:
            response = self.client.text.chat(self.messages)
        
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def reset(self):
        self.messages = [self.messages[0]]  # Keep system message
    
    def close(self):
        self.client.close_sync()

# Use it
bot = Chatbot(api_token="your-token", personality="friendly")

print("Bot:", bot.chat("Hello!"))
print("Bot:", bot.chat("What can you help me with?"))
print("Bot:", bot.chat("Tell me a joke", stream=True))

bot.close()
```

### Example 3: Document Summarizer

```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

def summarize_document(filepath, max_length=200):
    # Read file (respects API limits)
    content = read_file_for_prompt(filepath, max_length=5000)
    
    with Blossom(api_token="your-token") as client:
        prompt = f"""Summarize this document in {max_length} words or less:

{content}

Summary:"""
        
        response = client.text.generate(
            prompt,
            system="You are a professional summarizer. Create concise, accurate summaries.",
            max_tokens=max_length * 2,  # Rough token estimate
            temperature=0.3
        )
        
        return response

# Use it
summary = summarize_document("long_article.txt", max_length=150)
print(summary)
```

### Example 4: Batch Processing

```python
from blossom_ai import Blossom

def batch_generate(prompts, **kwargs):
    results = []
    
    with Blossom(api_token="your-token") as client:
        for i, prompt in enumerate(prompts):
            try:
                response = client.text.generate(prompt, **kwargs)
                results.append({"prompt": prompt, "response": response})
                print(f"✅ {i+1}/{len(prompts)} completed")
            except Exception as e:
                results.append({"prompt": prompt, "error": str(e)})
                print(f"❌ {i+1}/{len(prompts)} failed: {e}")
    
    return results

# Use it
prompts = [
    "Explain Python",
    "Explain JavaScript",
    "Explain Rust"
]

results = batch_generate(prompts, max_tokens=100, temperature=0.5)

for result in results:
    if "response" in result:
        print(f"\nPrompt: {result['prompt']}")
        print(f"Response: {result['response'][:100]}...")
```

### Example 5: Async Batch Processing

```python
import asyncio
from blossom_ai import Blossom

async def process_prompts(prompts):
    async with Blossom(api_token="your-token") as client:
        # Create tasks for parallel processing
        tasks = [
            client.text.generate(prompt, max_tokens=100)
            for prompt in prompts
        ]
        
        # Run all in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return list(zip(prompts, results))

# Use it
async def main():
    prompts = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
        "What is Go?",
        "What is Swift?"
    ]
    
    results = await process_prompts(prompts)
    
    for prompt, response in results:
        if isinstance(response, Exception):
            print(f"❌ {prompt}: {response}")
        else:
            print(f"✅ {prompt}: {response[:50]}...")

asyncio.run(main())
```

### Example 6: JSON Data Extractor

```python
from blossom_ai import Blossom
import json

def extract_info(text):
    with Blossom(api_token="your-token") as client:
        prompt = f"""Extract structured information from this text:

{text}

Return JSON with keys: name, age, city, occupation, hobbies (list)"""

        response = client.text.generate(
            prompt,
            json_mode=True,
            temperature=0.1
        )
        
        return json.loads(response)

# Use it
text = """
John Smith is a 32-year-old software engineer living in San Francisco.
He enjoys hiking, photography, and playing guitar in his free time.
"""

info = extract_info(text)
print(json.dumps(info, indent=2))
```

### Example 7: Translation System

```python
from blossom_ai import Blossom

class Translator:
    def __init__(self, api_token):
        self.client = Blossom(api_token=api_token)
    
    def translate(self, text, target_language, source_language="auto"):
        system = "You are a professional translator. Translate accurately while preserving meaning and tone."
        
        if source_language == "auto":
            prompt = f"Translate to {target_language}: {text}"
        else:
            prompt = f"Translate from {source_language} to {target_language}: {text}"
        
        return self.client.text.generate(
            prompt,
            system=system,
            temperature=0.3
        )
    
    def close(self):
        self.client.close_sync()

# Use it
translator = Translator(api_token="your-token")

print(translator.translate("Hello, how are you?", "Spanish"))
print(translator.translate("Bonjour", "English"))
print(translator.translate("こんにちは", "English"))

translator.close()
```

### Example 8: Content Moderator

```python
from blossom_ai import Blossom
import json

def moderate_content(text):
    with Blossom(api_token="your-token") as client:
        prompt = f"""Analyze this content for moderation:

{text}

Return JSON with:
- safe: boolean (true if content is safe)
- issues: list of any issues found
- severity: "none", "low", "medium", "high"
- category: type of content (if unsafe)"""

        response = client.text.generate(
            prompt,
            json_mode=True,
            temperature=0.1
        )
        
        return json.loads(response)

# Use it
result = moderate_content("This is a normal message about cooking")
print(f"Safe: {result['safe']}")
print(f"Severity: {result['severity']}")
```

### Example 9: Interactive Story Generator

```python
from blossom_ai import Blossom

class StoryGame:
    def __init__(self, api_token):
        self.client = Blossom(api_token=api_token)
        self.messages = [
            {
                "role": "system",
                "content": """You are an interactive story game master.
Create engaging narratives and present choices to the player.
Keep responses concise (2-3 paragraphs) and end with 2-3 choices."""
            },
            {
                "role": "user",
                "content": "Start a fantasy adventure story"
            }
        ]
        self.start_story()
    
    def start_story(self):
        print("\n=== Fantasy Adventure ===\n")
        response = self.client.text.chat(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        print(response)
    
    def make_choice(self, choice):
        self.messages.append({"role": "user", "content": choice})
        
        print("\n" + "="*50 + "\n")
        response = ""
        
        for chunk in self.client.text.chat(self.messages, stream=True):
            print(chunk, end="", flush=True)
            response += chunk
        
        print("\n")
        self.messages.append({"role": "assistant", "content": response})
    
    def close(self):
        self.client.close_sync()

# Use it
game = StoryGame(api_token="your-token")

while True:
    choice = input("\nYour choice (or 'quit'): ").strip()
    if choice.lower() in ['quit', 'exit', 'q']:
        break
    game.make_choice(choice)

game.close()
```

### Example 10: Code Reviewer

```python
from blossom_ai import Blossom

def review_code(code, language="Python"):
    with Blossom(api_token="your-token") as client:
        system = f"""You are a senior code reviewer specializing in {language}.
Review code for:
1. Bugs and errors
2. Performance issues
3. Security vulnerabilities
4. Best practices
5. Code style

Provide specific, actionable feedback."""

        prompt = f"""Review this {language} code:

```{language.lower()}
{code}
```

Provide a structured review."""

        response = client.text.generate(
            prompt,
            system=system,
            temperature=0.3,
            max_tokens=1000
        )
        
        return response

# Use it
code = """
def sort_list(items):
    for i in range(len(items)):
        for j in range(len(items)-1):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
    return items
"""

review = review_code(code)
print(review)
```

---

## 🔗 Related Documentation

- **[Image Generation](IMAGE_GENERATION.md)** - Generate images
- **[Vision Support](VISION.md)** - Analyze images with AI
- **[Audio Support](AUDIO.md)** - Audio input/output
- **[Reasoning Module](REASONING.md)** - Enhanced prompts
- **[API Reference](API_REFERENCE.md)** - Complete API docs
- **[Error Handling](ERROR_HANDLING.md)** - Handle errors

---

## 💡 Tips & Tricks

### Prompt Engineering

1. **Be specific** - Clear instructions yield better results
2. **Provide examples** - Show the format you want
3. **Set context** - Use system messages effectively
4. **Structure prompts** - Use sections, bullet points, numbering
5. **Iterate** - Test and refine your prompts

### Performance Optimization

1. **Stream responses** - Better UX for long generations
2. **Use async** - Parallel processing for multiple requests
3. **Cache results** - Avoid regenerating same content
4. **Choose right model** - Fast models for simple tasks
5. **Limit tokens** - Control response length

### Quality Control

1. **Use low temperature** - For consistent, factual output
2. **Set max_tokens** - Prevent overly long responses
3. **Add constraints** - Specify format, length, style in prompt
4. **Use JSON mode** - For structured data
5. **Test different models** - Find best for your use case

### Cost Optimization

1. **Cache common queries** - Use [Caching Module](CACHING.md)
2. **Use shorter prompts** - Be concise but clear
3. **Limit max_tokens** - Don't generate more than needed
4. **Choose appropriate model** - Fast models for simple tasks
5. **Batch similar requests** - Reuse context/parameters

---

## 🆘 Troubleshooting

### Issue: Response Too Short

**Solution:**
```python
# Increase max_tokens
response = client.text.generate(
    prompt,
    max_tokens=1000  # Increase limit
)

# Or specify in prompt
response = client.text.generate(
    "Write a detailed 500-word explanation of..."
)
```

### Issue: Response Too Generic

**Solution:**
```python
# Add more specific instructions
response = client.text.generate(
    prompt="Explain Python",
    system="You are an expert Python developer. Provide specific code examples and real-world use cases."
)

# Or lower temperature
response = client.text.generate(
    prompt,
    temperature=0.3  # More focused
)
```

### Issue: Inconsistent Results

**Solution:**
```python
# Use lower temperature for consistency
response = client.text.generate(
    prompt,
    temperature=0.0  # Deterministic
)
```

### Issue: Wrong Format

**Solution:**
```python
# Use JSON mode for structured data
response = client.text.generate(
    "Return data as JSON",
    json_mode=True
)

# Or be explicit in prompt
response = client.text.generate(
    """Return response in this format:
    1. First point
    2. Second point
    3. Third point"""
)
```

### Issue: Stream Timeout

**Solution:**
```python
# Increase timeout
client = Blossom(api_token="your-token", timeout=120)

# Or handle timeouts
from blossom_ai import TimeoutError

try:
    for chunk in client.text.generate(prompt, stream=True):
        print(chunk, end="", flush=True)
except TimeoutError:
    print("\n⏱️ Timeout - try shorter prompt or increase timeout")
```

---

## 📝 Summary

### Key Features

- 💬 **Multiple Models** - openai, deepseek, mistral, claude
- 🌊 **Streaming** - Real-time response generation
- 🛠️ **Function Calling** - Tool use and API integration (NEW)
- 📋 **JSON Mode** - Guaranteed structured output
- ⚙️ **Advanced Control** - Temperature, tokens, penalties
- 👁️ **Vision** - Analyze images (see [Vision Guide](VISION.md))
- 🔊 **Audio** - Audio I/O (see [Audio Guide](AUDIO.md))

### Best Practices

1. Use specific, detailed prompts
2. Set appropriate temperature for use case
3. Control output length with max_tokens
4. Stream for better UX
5. Use system messages for consistent behavior
6. Handle errors gracefully
7. Cache common responses
8. Choose right model for task

### Next Steps

1. 🎨 **[Image Generation](IMAGE_GENERATION.md)** - Generate images
2. 👁️ **[Vision Support](VISION.md)** - Analyze images
3. 🔊 **[Audio Support](AUDIO.md)** - Audio features
4. 🧠 **[Reasoning Module](REASONING.md)** - Enhanced thinking
5. ⚡ **[Caching Module](CACHING.md)** - Reduce costs
6. 📖 **[API Reference](API_REFERENCE.md)** - Complete docs

---

## 🆘 Need Help?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)
- 🔒 **Security:** [Security Policy](../../SECURITY.md)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Image Generation](IMAGE_GENERATION.md) | [Index](INDEX.md) | [Next: Vision Support →](VISION.md)

</div>