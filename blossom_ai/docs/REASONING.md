# 🧠 Reasoning Guide

> **Enhance AI responses with structured thinking and multi-step problem solving**

The Reasoning module helps AI generate better responses by encouraging structured thinking, step-by-step analysis, and comprehensive problem-solving.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Reasoning Modes](#reasoning-modes)
- [Reasoning Levels](#reasoning-levels)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## 🌟 Overview

### Why Use Reasoning?

**Without Reasoning:**
- ❌ Direct, surface-level answers
- ❌ Misses edge cases
- ❌ No verification steps

**With Reasoning:**
- ✅ **Step-by-step thinking**
- ✅ **Better accuracy** for complex problems
- ✅ **Considers edge cases**
- ✅ **Shows work/logic**
- ✅ **Self-verification**

### Key Features

| Feature | Description |
|---------|-------------|
| **Two Modes** | Prompt engineering OR native API support |
| **Multiple Levels** | LOW, MEDIUM, HIGH, ADAPTIVE |
| **Auto-Detection** | Automatically chooses best mode |
| **Budget Control** | Token budget for reasoning (native mode) |
| **Universal** | Works with all models (prompt mode) |

---

## 🚀 Quick Start

### Basic Usage

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

# Create enhancer
enhancer = ReasoningEnhancer()

# Enhance your prompt
enhanced = enhancer.enhance(
    "How can I optimize database queries?",
    level="high"
)

# Generate with reasoning
with Blossom(api_token="your_token") as client:
    response = client.text.generate(enhanced)
    print(response)
```

### Quick Creation

```python
from blossom_ai.utils import create_reasoning_enhancer

# Create with defaults
enhancer = create_reasoning_enhancer(
    level="medium",
    mode="auto"  # Automatically choose best mode
)

# Use it
enhanced = enhancer.enhance("Explain recursion")
```

### With V2 Native Reasoning

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# Use native reasoning (V2 API + OpenAI)
enhanced = enhancer.enhance(
    "Design a microservices architecture",
    level="high",
    mode="native",
    api_version="v2",
    model="openai"
)

# Enhanced is now a dict with thinking parameter
with Blossom(api_token="your_token") as client:
    response = client.text.chat(
        messages=[{"role": "user", "content": enhanced["prompt"]}],
        thinking=enhanced["thinking"]  # Native reasoning
    )
    print(response)
```

---

## 🎭 Reasoning Modes

### 1. Prompt Mode (Universal)

Works with **all models** via prompt engineering.

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Solve this problem: ...",
    level="high",
    mode="prompt"  # Explicit prompt mode
)

# Returns enhanced prompt string
print(type(enhanced))  # <class 'str'>
```

**How it works:**
- Adds thinking instructions to prompt
- Encourages step-by-step reasoning
- Works with any model (OpenAI, Gemini, etc.)

**Best for:**
- Models without native reasoning support
- Maximum compatibility
- Fine-grained control over reasoning style

### 2. Native Mode (V2 API)

Uses built-in reasoning features of V2 API.

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Complex problem...",
    level="high",
    mode="native",
    api_version="v2",
    model="openai"
)

# Returns dict with thinking parameter
print(type(enhanced))  # <class 'dict'>
print(enhanced.keys())  # dict_keys(['prompt', 'thinking'])
```

**How it works:**
- Uses V2 API's `thinking` parameter
- Budget-based reasoning tokens
- More efficient than prompt engineering

**Best for:**
- V2 API with OpenAI models
- Maximum performance
- Token efficiency

### 3. Auto Mode (Smart Selection)

Automatically chooses the best mode.

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# Auto-detects based on API version and model
enhanced = enhancer.enhance(
    "Question...",
    level="medium",
    mode="auto",
    api_version="v2",
    model="openai"
)

# Automatically chose native mode (V2 + OpenAI)
if isinstance(enhanced, dict):
    print("Native mode selected")
else:
    print("Prompt mode selected")
```

**Selection Logic:**
- V2 API + OpenAI → Native mode
- Other combinations → Prompt mode

---

## 📊 Reasoning Levels

### Level: LOW

**Quick, focused reasoning for simple problems.**

```python
enhanced = enhancer.enhance(
    "What is the capital of France?",
    level="low"
)
```

**Characteristics:**
- Minimal reasoning overhead
- Fast responses
- Good for straightforward questions
- Budget: 1,000-2,000 tokens (native mode)

**Use when:**
- Simple factual questions
- Quick lookups
- Clear-cut problems

### Level: MEDIUM (Default)

**Balanced reasoning for moderate complexity.**

```python
enhanced = enhancer.enhance(
    "How do I implement a binary search?",
    level="medium"
)
```

**Characteristics:**
- Structured approach
- Considers alternatives
- Verifies logic
- Budget: 5,000-8,000 tokens (native mode)

**Use when:**
- Technical problems
- Design decisions
- Moderate complexity tasks

### Level: HIGH

**Deep, thorough reasoning for complex problems.**

```python
enhanced = enhancer.enhance(
    "Design a scalable distributed system",
    level="high"
)
```

**Characteristics:**
- Extensive analysis
- Multiple perspectives
- Edge case consideration
- Self-verification steps
- Budget: 10,000-15,000 tokens (native mode)

**Use when:**
- Complex architecture decisions
- Critical problem-solving
- Research tasks
- Need highest accuracy

### Level: ADAPTIVE

**Dynamic adjustment based on problem complexity.**

```python
enhanced = enhancer.enhance(
    "Your question here",
    level="adaptive"
)
```

**Characteristics:**
- Analyzes problem complexity
- Adjusts reasoning depth automatically
- Efficient token usage
- Budget: varies (native mode)

**Use when:**
- Mixed complexity questions
- Want automatic optimization
- Unsure of required depth

---

## 🔧 Advanced Usage

### Custom Reasoning Patterns

```python
from blossom_ai.utils import ReasoningEnhancer, ReasoningMode

enhancer = ReasoningEnhancer()

# Custom reasoning instructions
custom_pattern = """
Think through this step-by-step:
1. Identify key requirements
2. List constraints
3. Propose solutions
4. Evaluate trade-offs
5. Recommend best approach

Problem: {prompt}
"""

enhanced = enhancer.enhance(
    "Design a caching system",
    level="high",
    mode="prompt",
    custom_pattern=custom_pattern
)
```

### Token Budget Control (Native Mode)

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Complex problem",
    level="high",
    mode="native",
    api_version="v2",
    model="openai"
)

# Check assigned budget
print(f"Thinking budget: {enhanced['thinking']['budget_tokens']} tokens")

# Manually set budget
enhanced["thinking"]["budget_tokens"] = 20000  # Custom budget
```

### Combine with Caching

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)
def reason_and_cache(question: str, level: str = "medium") -> str:
    """Cached reasoning results"""
    enhanced = enhancer.enhance(
        question,
        level=level,
        mode="auto",
        api_version="v2",
        model="openai"
    )
    
    with Blossom(api_token="your_token") as client:
        if isinstance(enhanced, dict):
            # Native mode
            return client.text.chat(
                messages=[{"role": "user", "content": enhanced["prompt"]}],
                thinking=enhanced.get("thinking")
            )
        else:
            # Prompt mode
            return client.text.generate(enhanced)

# First call: generates with reasoning and caches
result1 = reason_and_cache("Explain distributed systems")

# Second call: instant from cache
result2 = reason_and_cache("Explain distributed systems")
```

### Multi-Step Reasoning

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

def multi_step_analysis(problem: str) -> dict:
    """Break down problem into steps with reasoning"""
    enhancer = ReasoningEnhancer()
    
    with Blossom(api_token="your_token") as client:
        # Step 1: Understand the problem
        step1 = enhancer.enhance(
            f"Analyze this problem and identify key challenges: {problem}",
            level="medium"
        )
        understanding = client.text.generate(step1)
        
        # Step 2: Generate solutions
        step2 = enhancer.enhance(
            f"Based on: {understanding}\n\nPropose 3 solution approaches",
            level="high"
        )
        solutions = client.text.generate(step2)
        
        # Step 3: Evaluate solutions
        step3 = enhancer.enhance(
            f"Evaluate these solutions:\n{solutions}\n\nRank by feasibility",
            level="high"
        )
        evaluation = client.text.generate(step3)
        
        return {
            "understanding": understanding,
            "solutions": solutions,
            "evaluation": evaluation
        }

# Usage
result = multi_step_analysis("Design a real-time chat system")
print(result["evaluation"])
```

### Domain-Specific Reasoning

```python
from blossom_ai.utils import ReasoningEnhancer

class CodeReasoningEnhancer(ReasoningEnhancer):
    """Specialized reasoning for code problems"""
    
    def enhance_for_code(self, code_problem: str, language: str = "Python"):
        """Enhance with code-specific reasoning"""
        enhanced_prompt = f"""
Analyze this {language} problem with systematic reasoning:

1. Understand requirements
2. Identify data structures needed
3. Consider time/space complexity
4. Think about edge cases
5. Propose solution
6. Verify correctness

Problem:
{code_problem}
"""
        return self.enhance(
            enhanced_prompt,
            level="high",
            mode="auto"
        )

# Usage
code_enhancer = CodeReasoningEnhancer()
enhanced = code_enhancer.enhance_for_code(
    "Implement LRU cache",
    language="Python"
)
```

---

## ✅ Best Practices

### 1. Choose Right Level

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# ❌ Don't use high reasoning for simple questions
enhanced = enhancer.enhance(
    "What is 2+2?",
    level="high"  # Overkill!
)

# ✅ Match level to complexity
simple = enhancer.enhance("What is 2+2?", level="low")
medium = enhancer.enhance("Implement binary search", level="medium")
complex = enhancer.enhance("Design distributed system", level="high")
```

### 2. Use Auto Mode for Flexibility

```python
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

# ✅ Auto mode adapts to environment
enhanced = enhancer.enhance(
    "Your question",
    level="medium",
    mode="auto",  # Automatically chooses best mode
    api_version="v2",
    model="openai"
)
```

### 3. Cache Reasoning Results

```python
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

# ✅ Cache expensive reasoning
@cached(ttl=7200)  # 2 hours
def expensive_reasoning(problem: str) -> str:
    enhanced = enhancer.enhance(problem, level="high")
    # ... generate response ...
    return response

# Subsequent calls are instant
result = expensive_reasoning("Complex problem")
```

### 4. Monitor Token Usage (Native Mode)

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

enhancer = ReasoningEnhancer()

enhanced = enhancer.enhance(
    "Problem...",
    level="high",
    mode="native",
    api_version="v2",
    model="openai"
)

# Check budget before calling API
budget = enhanced.get("thinking", {}).get("budget_tokens", 0)
print(f"Will use ~{budget} reasoning tokens")

if budget > 15000:
    print("⚠️ High token usage - consider lower level")
```

### 5. Combine with Other Features

```python
from blossom_ai import Blossom, MessageBuilder
from blossom_ai.utils import ReasoningEnhancer, cached

enhancer = ReasoningEnhancer()

@cached(ttl=3600)
def analyze_with_vision_and_reasoning(image_url: str, question: str) -> str:
    """Vision + Reasoning + Caching"""
    
    # Enhance question with reasoning
    enhanced = enhancer.enhance(
        f"Analyze image and {question}",
        level="high",
        mode="native",
        api_version="v2",
        model="openai"
    )
    
    # Build vision message
    messages = [
        MessageBuilder.image_message(
            role="user",
            text=enhanced["prompt"],
            image_url=image_url
        )
    ]
    
    with Blossom(api_token="your_token") as client:
        return client.text.chat(
            messages,
            thinking=enhanced.get("thinking")
        )

# Usage: Vision + Reasoning + Cached
result = analyze_with_vision_and_reasoning(
    "https://example.com/diagram.jpg",
    "identify potential security vulnerabilities"
)
```

---

## 📚 Examples

### Example 1: Code Review with Reasoning

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, read_file_for_prompt

def review_code_with_reasoning(file_path: str) -> str:
    """Deep code review with structured reasoning"""
    
    # Read code file
    code = read_file_for_prompt(file_path, truncate_if_needed=True)
    
    # Enhance with reasoning
    enhancer = ReasoningEnhancer()
    enhanced = enhancer.enhance(
        f"""Review this code:

{code}

Provide:
1. Code quality assessment
2. Potential bugs
3. Security concerns
4. Performance optimization suggestions
5. Best practices violations""",
        level="high",
        mode="auto",
        api_version="v2",
        model="openai"
    )
    
    # Generate review
    with Blossom(api_token="your_token") as client:
        if isinstance(enhanced, dict):
            return client.text.chat(
                messages=[{"role": "user", "content": enhanced["prompt"]}],
                thinking=enhanced.get("thinking")
            )
        else:
            return client.text.generate(enhanced)

# Usage
review = review_code_with_reasoning("app.py")
print(review)
```

### Example 2: Architecture Design Assistant

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

def design_architecture(requirements: str) -> dict:
    """Design system architecture with multi-step reasoning"""
    
    enhancer = ReasoningEnhancer()
    
    with Blossom(api_token="your_token") as client:
        # Step 1: Analyze requirements
        step1 = enhancer.enhance(
            f"Analyze these requirements:\n{requirements}\n\nIdentify key challenges",
            level="high"
        )
        analysis = client.text.generate(step1)
        
        # Step 2: Design components
        step2 = enhancer.enhance(
            f"Based on:\n{analysis}\n\nDesign system components",
            level="high"
        )
        design = client.text.generate(step2)
        
        # Step 3: Identify risks
        step3 = enhancer.enhance(
            f"For this design:\n{design}\n\nIdentify risks and mitigation",
            level="high"
        )
        risks = client.text.generate(step3)
        
        return {
            "analysis": analysis,
            "design": design,
            "risks": risks
        }

# Usage
requirements = """
Build a real-time collaborative document editor:
- Support 1000+ concurrent users
- Sub-100ms latency
- Conflict resolution
- Mobile support
"""

architecture = design_architecture(requirements)
print("Design:", architecture["design"])
print("\nRisks:", architecture["risks"])
```

### Example 3: Problem Solver

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer, cached

@cached(ttl=3600)
def solve_problem(problem: str, complexity: str = "medium") -> dict:
    """Solve problem with reasoning and caching"""
    
    enhancer = ReasoningEnhancer()
    
    # Map complexity to reasoning level
    level_map = {
        "simple": "low",
        "medium": "medium",
        "complex": "high"
    }
    
    enhanced = enhancer.enhance(
        problem,
        level=level_map.get(complexity, "medium"),
        mode="auto",
        api_version="v2",
        model="openai"
    )
    
    with Blossom(api_token="your_token") as client:
        if isinstance(enhanced, dict):
            solution = client.text.chat(
                messages=[{"role": "user", "content": enhanced["prompt"]}],
                thinking=enhanced.get("thinking")
            )
        else:
            solution = client.text.generate(enhanced)
        
        return {
            "problem": problem,
            "complexity": complexity,
            "solution": solution,
            "cached": False  # First call
        }

# Usage
problems = [
    ("Design a URL shortener", "medium"),
    ("Implement LRU cache", "medium"),
    ("Design a URL shortener", "medium"),  # Cached!
]

for problem, complexity in problems:
    result = solve_problem(problem, complexity)
    print(f"\nProblem: {result['problem']}")
    print(f"Solution: {result['solution'][:200]}...")
```

### Example 4: Research Assistant

```python
from blossom_ai import Blossom
from blossom_ai.utils import ReasoningEnhancer

def research_topic(topic: str, depth: str = "medium") -> dict:
    """Research topic with structured reasoning"""
    
    enhancer = ReasoningEnhancer()
    
    with Blossom(api_token="your_token") as client:
        # Overview
        overview_prompt = enhancer.enhance(
            f"Provide comprehensive overview of: {topic}",
            level=depth
        )
        overview = client.text.generate(overview_prompt)
        
        # Key concepts
        concepts_prompt = enhancer.enhance(
            f"Based on:\n{overview}\n\nExplain 5 key concepts",
            level=depth
        )
        concepts = client.text.generate(concepts_prompt)
        
        # Applications
        apps_prompt = enhancer.enhance(
            f"For topic: {topic}\nList practical applications",
            level=depth
        )
        applications = client.text.generate(apps_prompt)
        
        # Future directions
        future_prompt = enhancer.enhance(
            f"For topic: {topic}\nPredict future developments",
            level=depth
        )
        future = client.text.generate(future_prompt)
        
        return {
            "topic": topic,
            "overview": overview,
            "key_concepts": concepts,
            "applications": applications,
            "future_directions": future
        }

# Usage
research = research_topic("Quantum Computing", depth="high")

print(f"Topic: {research['topic']}\n")
print(f"Overview:\n{research['overview']}\n")
print(f"Key Concepts:\n{research['key_concepts']}\n")
print(f"Applications:\n{research['applications']}\n")
print(f"Future:\n{research['future_directions']}")
```

---

## 🎯 Use Cases

### When to Use Reasoning

**Perfect for:**
- 🏗️ Architecture and design decisions
- 🐛 Complex debugging
- 📊 Data analysis
- 🔒 Security audits
- 📝 Technical documentation
- 🧪 Research tasks
- 💡 Problem-solving

**Not needed for:**
- Simple factual questions
- Quick lookups
- Straightforward tasks
- When speed is critical

---

## ⚠️ Limitations

### Current Limitations

1. **Native Mode**: Only works with V2 API + OpenAI models
2. **Token Usage**: High-level reasoning uses more tokens
3. **Response Time**: Reasoning adds processing time
4. **Cost**: More tokens = higher cost

### Mitigation Strategies

```python
# Use appropriate level
enhancer.enhance(prompt, level="low")  # For simple tasks

# Cache results
@cached(ttl=3600)
def reason_once(prompt):
    return enhancer.enhance(prompt, level="high")

# Monitor costs
if complexity == "high":
    print("⚠️ This will use significant tokens")
```

---

## 🔗 Related Documentation

- [Text Generation](TEXT_GENERATION.md) - Generate with reasoning
- [Caching Guide](CACHING.md) - Cache reasoning results
- [File Reader](FILE_READER.md) - Analyze files with reasoning
- [Performance Guide](PERFORMANCE.md) - Optimize reasoning usage

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Caching Guide](CACHING.md) | [File Reader](FILE_READER.md) →

</div>