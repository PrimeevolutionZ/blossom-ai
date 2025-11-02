# 🧠 Reasoning Module Guide

> **Enhance AI prompts with structured reasoning for better responses**

The Reasoning Module adds systematic thinking capabilities to your AI prompts, helping generate more thoughtful, accurate, and well-reasoned responses.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Reasoning Levels](#-reasoning-levels)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Advanced Features](#-advanced-features)
- [Best Practices](#-best-practices)

---

## 🚀 Quick Start

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

# Create reasoning enhancer
enhancer = ReasoningEnhancer()

# Enhance your prompt
enhanced = enhancer.enhance(
    "How do I optimize database queries?",
    level="high"
)

# Use with Blossom AI
with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced)
    print(response)
```

---

## 🎯 Reasoning Levels

The module offers four reasoning levels:

### 1. LOW - Quick Thinking

Best for: Simple questions, basic tasks

```python
from blossom_ai.utils import ReasoningLevel, ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "What is Python?",
    level=ReasoningLevel.LOW
)
```

**What it does:**
- Asks: "What is the core question?"
- Finds: "What's the most direct approach?"
- Provides quick, focused answer

**Example output structure:**
```
Before answering, briefly consider:
1. What is the core question?
2. What's the most direct approach?

Now provide your answer:

User question: What is Python?
```

---

### 2. MEDIUM - Systematic Thinking (Default)

Best for: General questions, explanations, analysis

```python
enhanced = enhancer.enhance(
    "How do I optimize database queries?",
    level=ReasoningLevel.MEDIUM
)
```

**What it does:**
- Understanding: Clarifies the question
- Key factors: Identifies important considerations
- Approach: Plans the solution method
- Potential issues: Anticipates problems

**Example output structure:**
```
Let's approach this systematically:

<reasoning>
1. Understanding: What exactly is being asked?
2. Key factors: What are the important considerations?
3. Approach: What's the best way to handle this?
4. Potential issues: What could go wrong?
</reasoning>

Based on this analysis, here's my response:

User question: How do I optimize database queries?
```

---

### 3. HIGH - Deep Reasoning

Best for: Complex problems, design decisions, architectural choices

```python
enhanced = enhancer.enhance(
    "Design a scalable microservices architecture",
    level=ReasoningLevel.HIGH
)
```

**What it does:**
- **Problem Analysis**: Core objectives, constraints, assumptions
- **Solution Exploration**: Multiple approaches with evaluation
- **Critical Evaluation**: Strengths, weaknesses, trade-offs
- **Verification**: Confidence scoring and validation
- **Final Synthesis**: Best approach with limitations

**Example output structure:**
```
Let me think through this carefully and thoroughly:

<deep_reasoning>
### Problem Analysis
- Core question and objectives
- Context and constraints
- Assumptions to validate

### Solution Exploration
- Approach 1: [describe and evaluate]
- Approach 2: [describe and evaluate]
- Approach 3: [describe and evaluate]

### Critical Evaluation
- Strengths and weaknesses of each approach
- Trade-offs and implications
- Edge cases and potential failures

### Verification
- Does this solution actually address the problem?
- What could go wrong?
- How confident am I? (1-10 scale)

### Final Synthesis
- Best approach and why
- Implementation considerations
- Limitations and caveats
</deep_reasoning>

Based on this thorough analysis, here's my detailed response:

User question: Design a scalable microservices architecture
```

---

### 4. ADAPTIVE - Automatic Selection

The system automatically chooses the best reasoning level based on prompt complexity.

```python
enhanced = enhancer.enhance(
    "Your question here",
    level=ReasoningLevel.ADAPTIVE
)
```

**Selection criteria:**
- **HIGH**: Complex indicators (explain, analyze, design, optimize)
- **LOW**: Simple indicators (what is, define, list)
- **MEDIUM**: Everything else

---

## ⚙️ Configuration

### Basic Configuration

```python
from blossom_ai.utils import ReasoningConfig, ReasoningLevel, ReasoningEnhancer

# Create custom config
config = ReasoningConfig(
    level=ReasoningLevel.MEDIUM,
    max_reasoning_tokens=None,
    include_confidence=False,
    structured_thinking=True,
    chain_of_thought=True
)

# Use config
enhancer = ReasoningEnhancer(default_config=config)
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `ReasoningLevel` | `MEDIUM` | Default reasoning level |
| `max_reasoning_tokens` | `Optional[int]` | `None` | Limit reasoning section length |
| `include_confidence` | `bool` | `False` | Request confidence scores |
| `structured_thinking` | `bool` | `True` | Use structured format |
| `chain_of_thought` | `bool` | `True` | Enable step-by-step reasoning |
| `self_critique` | `bool` | `False` | Enable self-evaluation (HIGH level) |
| `alternative_approaches` | `bool` | `False` | Consider multiple solutions |
| `step_verification` | `bool` | `False` | Verify each reasoning step |

### Advanced Configuration

```python
from blossom_ai.utils import ReasoningConfig, ReasoningLevel

config = ReasoningConfig(
    level=ReasoningLevel.HIGH,
    include_confidence=True,  # Ask for confidence scores
    self_critique=True,  # Request self-evaluation
    alternative_approaches=True,  # Consider 2-3 approaches
    step_verification=True  # Verify each step
)

enhancer = ReasoningEnhancer(default_config=config)
```

---

## 💡 Usage Examples

### Example 1: Simple Enhancement

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# Enhance prompt
enhanced = enhancer.enhance(
    "How does photosynthesis work?",
    level="medium"
)

# Generate response
with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced, max_tokens=500)
    print(response)
```

---

### Example 2: With Context

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    prompt="How can I improve this code?",
    level="high",
    context="The code is a Python web scraper that's running slowly",
    examples=[
        "Consider algorithmic complexity",
        "Look for unnecessary API calls",
        "Check for memory leaks"
    ]
)

# Use enhanced prompt...
```

---

### Example 3: Extract Reasoning

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Design a caching system",
    level="high"
)

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced, max_tokens=1000)
    
    # Extract reasoning and answer separately
    parsed = enhancer.extract_reasoning(response)
    
    print("=== REASONING ===")
    print(parsed['reasoning'])
    
    print("\n=== ANSWER ===")
    print(parsed['answer'])
    
    if parsed['confidence']:
        print(f"\n=== CONFIDENCE: {parsed['confidence']} ===")
```

---

### Example 4: Multi-Step Reasoning Chain

```python
import asyncio
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningChain

async def solve_complex_problem():
    # Initialize client
    client = Blossom(api_version="v2", api_token="token")
    
    # Create reasoning chain
    chain = ReasoningChain(client.text)
    
    # Solve step by step
    result = await chain.solve(
        problem="Design a scalable microservices architecture for e-commerce",
        steps=["analyze", "design", "validate", "optimize"],
        level="high"
    )
    
    # Access results
    print("=== PROBLEM ===")
    print(result['problem'])
    
    for step_result in result['steps']:
        print(f"\n=== STEP: {step_result['step'].upper()} ===")
        print(f"Reasoning: {step_result['reasoning']}")
        print(f"Output: {step_result['output']}")
    
    print("\n=== FINAL ANSWER ===")
    print(result['final_answer'])
    
    await client.close()

asyncio.run(solve_complex_problem())
```

---

### Example 5: Integration with Blossom Client

```python
from blossom_ai import Blossom
from blossom_ai.utils import add_reasoning_to_blossom

# Add reasoning capability to Blossom
add_reasoning_to_blossom()

# Now you can use generate_with_reasoning
with Blossom(api_version="v2", api_token="token") as client:
    result = client.text.generate_with_reasoning(
        "How to optimize Python code?",
        level="high"
    )
    
    # result is a dict with 'reasoning' and 'answer'
    print("Reasoning:", result['reasoning'])
    print("Answer:", result['answer'])
```

---

### Example 6: Convenience Factory

```python
from blossom_ai.utils import create_reasoning_enhancer

# Quick setup with custom config
enhancer = create_reasoning_enhancer(
    level="high",
    include_confidence=True,
    self_critique=True
)

# Use immediately
enhanced = enhancer.enhance("Your complex question")
```

---

## 🎓 Advanced Features

### Custom Reasoning Prompts

You can access and customize the built-in reasoning prompts:

```python
from blossom_ai.utils import REASONING_PROMPTS, ReasoningLevel

# View prompts
print(REASONING_PROMPTS[ReasoningLevel.LOW])
print(REASONING_PROMPTS[ReasoningLevel.MEDIUM])
print(REASONING_PROMPTS[ReasoningLevel.HIGH])

# Use in your own implementations
custom_prompt = REASONING_PROMPTS[ReasoningLevel.HIGH] + "\n\nAdditional instructions..."
```

---

### Adaptive Level Selection

The ADAPTIVE level uses heuristics to choose the right level:

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# These will automatically select appropriate levels
questions = [
    "What is Python?",  # → LOW
    "Explain how Python works",  # → MEDIUM
    "Design a Python web framework",  # → HIGH
]

for q in questions:
    enhanced = enhancer.enhance(q, level="adaptive")
    # Level chosen automatically
```

**Selection rules:**
- **HIGH**: 2+ complex keywords (explain, analyze, design, optimize, compare)
- **LOW**: Simple keywords (what is, define, list) + short prompt (<50 chars)
- **MEDIUM**: Everything else

---

### Confidence Scoring

Request confidence levels in responses:

```python
from blossom_ai.utils import ReasoningConfig, ReasoningEnhancer

config = ReasoningConfig(
    level="high",
    include_confidence=True
)

enhancer = ReasoningEnhancer(default_config=config)
enhanced = enhancer.enhance("Your question")

# The AI will include confidence level: LOW/MEDIUM/HIGH
# Can be extracted with extract_reasoning()
```

---

## ✅ Best Practices

### 1. Choose the Right Level

```python
# Simple facts → LOW
enhancer.enhance("What is the capital of France?", level="low")

# Explanations → MEDIUM
enhancer.enhance("How does encryption work?", level="medium")

# Complex design → HIGH
enhancer.enhance("Design a distributed system", level="high")

# Unsure → ADAPTIVE
enhancer.enhance("Your question", level="adaptive")
```

---

### 2. Provide Context

```python
# ❌ Without context
enhanced = enhancer.enhance("How to fix this?")

# ✅ With context
enhanced = enhancer.enhance(
    prompt="How to fix this performance issue?",
    context="Python web API with 10k requests/sec, database queries taking 2s"
)
```

---

### 3. Use Examples

```python
enhanced = enhancer.enhance(
    prompt="Analyze this error",
    examples=[
        "Check stack trace for root cause",
        "Look for recent code changes",
        "Consider environmental factors"
    ]
)
```

---

### 4. Extract Structured Output

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()
enhanced = enhancer.enhance("Your question", level="high")

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(enhanced)
    
    # Parse structured output
    parsed = enhancer.extract_reasoning(response)
    
    # Use separately
    reasoning = parsed['reasoning']  # The thinking process
    answer = parsed['answer']  # The final answer
    confidence = parsed['confidence']  # Confidence level (if requested)
```

---

### 5. Combine with V2 Features

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()
enhanced = enhancer.enhance(
    "Design a caching strategy",
    level="high"
)

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(
        enhanced,
        max_tokens=1500,  # V2: Control length
        frequency_penalty=0.3,  # V2: Reduce repetition
        temperature=0.7  # Balanced creativity
    )
    print(response)
```

---

### 6. Use with Caching

```python
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)  # Cache for 1 hour
def analyze_with_reasoning(question):
    enhanced = enhancer.enhance(question, level="high")
    # Generate response...
    return response

# First call: generates response
result1 = analyze_with_reasoning("Design microservices")

# Second call: returns cached result
result2 = analyze_with_reasoning("Design microservices")
```

---

## 🔗 Integration Examples

### With V2 API

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

with Blossom(api_version="v2", api_token="token") as client:
    # Enhance prompt
    enhanced = enhancer.enhance(
        "Optimize this SQL query",
        level="high",
        context="Query takes 5 seconds on 1M rows"
    )
    
    # Use V2 features
    response = client.text.generate(
        enhanced,
        max_tokens=1000,
        frequency_penalty=0.5
    )
    
    # Extract reasoning
    parsed = enhancer.extract_reasoning(response)
    print(parsed['answer'])
```

---

### With Streaming

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

with Blossom(api_version="v2", api_token="token") as client:
    enhanced = enhancer.enhance(
        "Write a detailed guide",
        level="medium"
    )
    
    # Stream response
    for chunk in client.text.generate(enhanced, stream=True):
        print(chunk, end="", flush=True)
```

---

### With Function Calling

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "Fetch data from database",
            "parameters": {...}
        }
    }
]

with Blossom(api_version="v2", api_token="token") as client:
    enhanced = enhancer.enhance(
        "Analyze user data and provide insights",
        level="high"
    )
    
    response = client.text.chat(
        messages=[{"role": "user", "content": enhanced}],
        tools=tools,
        tool_choice="auto"
    )
```

---

## 📊 Performance Tips

### 1. Cache Enhanced Prompts

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# Cache the enhancement
enhanced_cache = {}

def get_enhanced(prompt, level="medium"):
    key = f"{prompt}:{level}"
    if key not in enhanced_cache:
        enhanced_cache[key] = enhancer.enhance(prompt, level=level)
    return enhanced_cache[key]
```

---

### 2. Batch Processing

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

questions = [
    "Question 1",
    "Question 2",
    "Question 3"
]

# Enhance all at once
enhanced_questions = [
    enhancer.enhance(q, level="medium")
    for q in questions
]

# Process later
```

---

### 3. Adjust max_tokens Based on Level

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, ReasoningLevel

enhancer = ReasoningEnhancer()

level = ReasoningLevel.HIGH
enhanced = enhancer.enhance("Your question", level=level)

# Adjust max_tokens based on reasoning level
token_limits = {
    ReasoningLevel.LOW: 300,
    ReasoningLevel.MEDIUM: 800,
    ReasoningLevel.HIGH: 2000
}

with Blossom(api_version="v2", api_token="token") as client:
    response = client.text.generate(
        enhanced,
        max_tokens=token_limits[level]
    )
```

---

## 🔗 Related Documentation

- **[V2 Text Generation](V2_TEXT_GENERATION.md)** - Advanced text features
- **[Caching Guide](CACHING.md)** - Cache AI responses
- **[V2 API Reference](V2_API_REFERENCE.md)** - Complete API docs

---

<div align="center">

**Made with 🌸 by the Blossom AI Team**

[Documentation](INDEX.md) • [GitHub](https://github.com/PrimeevolutionZ/blossom-ai) • [PyPI](https://pypi.org/project/eclips-blossom-ai/)

</div>