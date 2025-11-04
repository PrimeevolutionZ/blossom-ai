"""
Blossom AI - Reasoning Module (V2 Native Support)
Enhances prompts with reasoning capabilities for better AI responses
Supports both prompt-based (universal) and native V2 reasoning
"""

from typing import Optional, Literal, Dict, Any, Union, List
from dataclasses import dataclass
from enum import Enum


class ReasoningLevel(str, Enum):
    """Reasoning complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ADAPTIVE = "adaptive"


class ReasoningMode(str, Enum):
    """Reasoning implementation mode"""
    PROMPT = "prompt"      # Through prompt engineering (works for all models)
    NATIVE = "native"      # Built-in reasoning (V2 OpenAI models only)
    AUTO = "auto"          # Automatic selection based on API version and model


@dataclass
class ReasoningConfig:
    """Configuration for reasoning enhancement"""
    level: ReasoningLevel = ReasoningLevel.MEDIUM
    mode: ReasoningMode = ReasoningMode.AUTO  # ✅ NEW: Auto-detect best mode

    # Native reasoning params (V2 only)
    budget_tokens: Optional[int] = None  # ✅ NEW: Token budget for native reasoning

    # Prompt-based reasoning params
    max_reasoning_tokens: Optional[int] = None
    include_confidence: bool = False
    structured_thinking: bool = True
    chain_of_thought: bool = True

    # Advanced options
    self_critique: bool = False
    alternative_approaches: bool = False
    step_verification: bool = False


# Models that support native reasoning (V2 API)
NATIVE_REASONING_MODELS = {
    "openai",
    "openai-large",
    "openai-fast",
    # Add more as OpenAI releases them
}


# Reasoning prompts for different levels (PROMPT mode)
REASONING_PROMPTS = {
    ReasoningLevel.LOW: """Before answering, briefly consider:
1. What is the core question?
2. What's the most direct approach?

Now provide your answer:""",

    ReasoningLevel.MEDIUM: """Let's approach this systematically:

<reasoning>
1. Understanding: What exactly is being asked?
2. Key factors: What are the important considerations?
3. Approach: What's the best way to handle this?
4. Potential issues: What could go wrong?
</reasoning>

Based on this analysis, here's my response:""",

    ReasoningLevel.HIGH: """Let me think through this carefully and thoroughly:

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

Based on this thorough analysis, here's my detailed response:"""
}


class ReasoningEnhancer:
    """
    Enhances prompts with reasoning capabilities

    Supports two modes:
    - PROMPT: Universal, works with all models (adds reasoning to prompt)
    - NATIVE: V2 API only, uses built-in thinking parameter (more efficient)
    - AUTO: Automatically chooses best mode

    Example:
        >>> enhancer = ReasoningEnhancer()
        >>>
        >>> # Auto mode - chooses best approach
        >>> result = enhancer.enhance(
        ...     "How to optimize code?",
        ...     level="high",
        ...     api_version="v2",
        ...     model="openai"
        ... )
        >>>
        >>> # Use with V2 API
        >>> if result.get("thinking"):
        ...     client.text.chat(
        ...         messages=[{"role": "user", "content": result["prompt"]}],
        ...         thinking=result["thinking"]
        ...     )
        ... else:
        ...     client.text.generate(result["prompt"])
    """

    def __init__(self, default_config: Optional[ReasoningConfig] = None):
        self.default_config = default_config or ReasoningConfig()

    def enhance(
            self,
            prompt: str,
            level: Optional[Union[str, ReasoningLevel]] = None,
            mode: Optional[Union[str, ReasoningMode]] = None,
            api_version: str = "v1",
            model: Optional[str] = None,
            config: Optional[ReasoningConfig] = None,
            context: Optional[str] = None,
            examples: Optional[List[str]] = None
    ) -> Union[str, Dict[str, Any]]:
        """
        Enhance a prompt with reasoning instructions

        Args:
            prompt: Original user prompt
            level: Reasoning level (low, medium, high, adaptive)
            mode: Reasoning mode (prompt, native, auto)
            api_version: API version ("v1" or "v2")
            model: Model name (for native reasoning detection)
            config: Custom reasoning configuration
            context: Additional context to include
            examples: Example reasoning patterns

        Returns:
            - PROMPT mode: Enhanced prompt string
            - NATIVE mode: Dict with {"prompt": str, "thinking": dict}
        """
        # Use provided config or default
        cfg = config or self.default_config

        # Determine reasoning level
        if level is None:
            level = cfg.level
        elif isinstance(level, str):
            level = ReasoningLevel(level.lower())

        # For adaptive level, analyze prompt complexity
        if level == ReasoningLevel.ADAPTIVE:
            level = self._determine_adaptive_level(prompt)

        # Determine reasoning mode
        if mode is None:
            mode = cfg.mode
        elif isinstance(mode, str):
            mode = ReasoningMode(mode.lower())

        # Auto-detect best mode
        if mode == ReasoningMode.AUTO:
            mode = self._auto_detect_mode(api_version, model)

        # NATIVE mode - use V2 built-in reasoning
        if mode == ReasoningMode.NATIVE:
            if api_version != "v2":
                raise ValueError(
                    "Native reasoning only available in V2 API. "
                    "Use mode='prompt' for V1 or switch to api_version='v2'"
                )

            if model and model not in NATIVE_REASONING_MODELS:
                raise ValueError(
                    f"Model '{model}' doesn't support native reasoning. "
                    f"Supported models: {', '.join(NATIVE_REASONING_MODELS)}. "
                    f"Use mode='prompt' as fallback."
                )

            return self._create_native_reasoning(prompt, level, cfg, context, examples)

        # PROMPT mode - enhance prompt text
        return self._create_prompt_reasoning(prompt, level, cfg, context, examples)

    def _auto_detect_mode(self, api_version: str, model: Optional[str]) -> ReasoningMode:
        """
        Automatically detect best reasoning mode

        Logic:
        - V2 API + OpenAI model → NATIVE (more efficient)
        - V2 API + other model → PROMPT (fallback)
        - V1 API → PROMPT (only option)
        """
        if api_version == "v2" and model in NATIVE_REASONING_MODELS:
            return ReasoningMode.NATIVE
        return ReasoningMode.PROMPT

    def _create_native_reasoning(
        self,
        prompt: str,
        level: ReasoningLevel,
        config: ReasoningConfig,
        context: Optional[str],
        examples: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Create native reasoning configuration for V2 API

        Returns dict with prompt and thinking config
        """
        # Build enhanced prompt (but lighter than PROMPT mode)
        parts = []

        if context:
            parts.append(f"Context: {context}\n")

        if examples:
            parts.append("Consider these approaches:")
            for i, example in enumerate(examples, 1):
                parts.append(f"{i}. {example}")
            parts.append("")

        parts.append(prompt)

        enhanced_prompt = "\n".join(parts)

        # Map reasoning level to token budget
        budget_mapping = {
            ReasoningLevel.LOW: 500,
            ReasoningLevel.MEDIUM: 1500,
            ReasoningLevel.HIGH: 3000
        }

        budget_tokens = config.budget_tokens or budget_mapping.get(level, 1500)

        return {
            "prompt": enhanced_prompt,
            "thinking": {
                "type": "enabled",
                "budget_tokens": budget_tokens
            },
            "mode": "native",
            "level": level.value
        }

    def _create_prompt_reasoning(
        self,
        prompt: str,
        level: ReasoningLevel,
        config: ReasoningConfig,
        context: Optional[str],
        examples: Optional[List[str]]
    ) -> str:
        """
        Create prompt-based reasoning enhancement

        Returns enhanced prompt string
        """
        parts = []

        # Add context if provided
        if context:
            parts.append(f"Context: {context}\n")

        # Add examples if provided
        if examples:
            parts.append("Example reasoning patterns:")
            for i, example in enumerate(examples, 1):
                parts.append(f"Example {i}: {example}")
            parts.append("")

        # Add reasoning prompt
        parts.append(REASONING_PROMPTS[level])
        parts.append("")

        # Add original prompt
        parts.append(f"User question: {prompt}")

        # Add special instructions based on config
        if config.include_confidence and level in [ReasoningLevel.MEDIUM, ReasoningLevel.HIGH]:
            parts.append("\n[Please include confidence level: LOW/MEDIUM/HIGH]")

        if config.alternative_approaches and level == ReasoningLevel.HIGH:
            parts.append("[Consider at least 2-3 different approaches]")

        if config.self_critique and level == ReasoningLevel.HIGH:
            parts.append("[Critically evaluate your own reasoning]")

        if config.step_verification:
            parts.append("[Verify each logical step]")

        return "\n".join(parts)

    def _determine_adaptive_level(self, prompt: str) -> ReasoningLevel:
        """
        Automatically determine reasoning level based on prompt complexity

        Factors considered:
        - Length and complexity of prompt
        - Presence of technical terms
        - Question complexity indicators
        """
        prompt_lower = prompt.lower()

        # Indicators for high-level reasoning
        high_indicators = [
            'explain', 'analyze', 'compare', 'evaluate', 'design',
            'architecture', 'optimize', 'debug', 'algorithm',
            'trade-off', 'consider', 'pros and cons', 'best practice',
            'why', 'how does', 'what if'
        ]

        # Indicators for low-level reasoning (simple queries)
        low_indicators = [
            'what is', 'define', 'list', 'name',
            'when was', 'who is', 'where is'
        ]

        # Count indicators
        high_count = sum(1 for ind in high_indicators if ind in prompt_lower)
        low_count = sum(1 for ind in low_indicators if ind in prompt_lower)

        # Decision logic
        if high_count >= 2 or (len(prompt) > 200 and high_count >= 1):
            return ReasoningLevel.HIGH
        elif low_count >= 1 and high_count == 0 and len(prompt) < 50:
            return ReasoningLevel.LOW
        else:
            return ReasoningLevel.MEDIUM

    def extract_reasoning(self, response: str) -> Dict[str, Any]:
        """
        Extract reasoning from AI response (PROMPT mode only)

        Note: NATIVE mode reasoning is internal and not returned in response

        Returns:
            Dictionary with 'reasoning' and 'answer' parts
        """
        result = {
            'reasoning': None,
            'answer': response,
            'confidence': None
        }

        # Extract reasoning section
        if '<reasoning>' in response:
            try:
                start = response.index('<reasoning>') + len('<reasoning>')
                end = response.index('</reasoning>')
                result['reasoning'] = response[start:end].strip()
                result['answer'] = response[end + len('</reasoning>'):].strip()
            except ValueError:
                pass

        if '<deep_reasoning>' in response:
            try:
                start = response.index('<deep_reasoning>') + len('<deep_reasoning>')
                end = response.index('</deep_reasoning>')
                result['reasoning'] = response[start:end].strip()
                result['answer'] = response[end + len('</deep_reasoning>'):].strip()
            except ValueError:
                pass

        # Extract confidence if present
        for conf_level in ['HIGH', 'MEDIUM', 'LOW']:
            if f'confidence: {conf_level}' in response.upper():
                result['confidence'] = conf_level
                break

        return result

    def supports_native_reasoning(self, model: str) -> bool:
        """
        Check if model supports native reasoning

        Args:
            model: Model name

        Returns:
            True if model supports native reasoning
        """
        return model in NATIVE_REASONING_MODELS


def get_native_reasoning_models() -> List[str]:
    """
    Get list of models that support native reasoning

    Returns:
        List of model names
    """
    return list(NATIVE_REASONING_MODELS)


class ReasoningChain:
    """
    Multi-step reasoning chain for complex problems

    Automatically uses native reasoning for V2 API

    Example:
        >>> chain = ReasoningChain(text_generator)
        >>> result = await chain.solve(
        ...     "Design a scalable microservices architecture",
        ...     steps=["analyze", "design", "validate"]
        ... )
    """

    def __init__(self, text_generator):
        """
        Args:
            text_generator: TextGenerator or AsyncTextGenerator instance
        """
        self.generator = text_generator
        self.enhancer = ReasoningEnhancer()

    async def solve(
            self,
            problem: str,
            steps: Optional[List[str]] = None,
            level: ReasoningLevel = ReasoningLevel.HIGH,
            api_version: str = "v1",
            model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Solve problem through multi-step reasoning chain

        Args:
            problem: Problem to solve
            steps: Custom steps or None for automatic
            level: Reasoning level for each step
            api_version: API version ("v1" or "v2")
            model: Model name

        Returns:
            Dictionary with step-by-step reasoning and final answer
        """
        if steps is None:
            steps = ["understand", "plan", "execute", "verify"]

        results = {
            'problem': problem,
            'steps': [],
            'final_answer': None
        }

        context = problem

        for step in steps:
            # Create step-specific prompt
            step_prompt = f"""
Step: {step.upper()}
Previous context: {context}

Please complete this reasoning step.
"""

            # Enhance with reasoning
            enhanced = self.enhancer.enhance(
                step_prompt,
                level=level,
                api_version=api_version,
                model=model
            )

            # Generate response (handle both sync and async)
            if hasattr(self.generator, 'generate') and callable(self.generator.generate):
                import inspect
                if inspect.iscoroutinefunction(self.generator.generate):
                    if isinstance(enhanced, dict):
                        # Native mode
                        response = await self.generator.chat(
                            messages=[{"role": "user", "content": enhanced["prompt"]}],
                            thinking=enhanced.get("thinking")
                        )
                    else:
                        # Prompt mode
                        response = await self.generator.generate(enhanced)
                else:
                    if isinstance(enhanced, dict):
                        # Native mode
                        response = self.generator.chat(
                            messages=[{"role": "user", "content": enhanced["prompt"]}],
                            thinking=enhanced.get("thinking")
                        )
                    else:
                        # Prompt mode
                        response = self.generator.generate(enhanced)
            else:
                raise ValueError("Invalid text generator")

            # Extract reasoning (only for prompt mode)
            if isinstance(enhanced, str):
                parsed = self.enhancer.extract_reasoning(response)
            else:
                parsed = {'reasoning': None, 'answer': response}

            results['steps'].append({
                'step': step,
                'reasoning': parsed['reasoning'],
                'output': parsed['answer']
            })

            # Update context for next step
            context = f"{context}\n\nStep '{step}' output:\n{parsed['answer']}"

        # Final synthesis
        synthesis_prompt = f"""
Based on all previous reasoning steps, provide a comprehensive final answer to:
{problem}

Previous reasoning:
{context}
"""

        final_enhanced = self.enhancer.enhance(
            synthesis_prompt,
            level=level,
            api_version=api_version,
            model=model
        )

        if hasattr(self.generator, 'generate') and callable(self.generator.generate):
            import inspect
            if inspect.iscoroutinefunction(self.generator.generate):
                if isinstance(final_enhanced, dict):
                    final = await self.generator.chat(
                        messages=[{"role": "user", "content": final_enhanced["prompt"]}],
                        thinking=final_enhanced.get("thinking")
                    )
                else:
                    final = await self.generator.generate(final_enhanced)
            else:
                if isinstance(final_enhanced, dict):
                    final = self.generator.chat(
                        messages=[{"role": "user", "content": final_enhanced["prompt"]}],
                        thinking=final_enhanced.get("thinking")
                    )
                else:
                    final = self.generator.generate(final_enhanced)

        results['final_answer'] = final

        return results


# Convenience function
def create_reasoning_enhancer(
        level: str = "medium",
        mode: str = "auto",
        **config_kwargs
) -> ReasoningEnhancer:
    """
    Create a reasoning enhancer with custom configuration

    Args:
        level: Default reasoning level
        mode: Reasoning mode ("prompt", "native", "auto")
        **config_kwargs: Additional ReasoningConfig parameters

    Returns:
        Configured ReasoningEnhancer instance

    Example:
        >>> # Auto mode - best for most cases
        >>> enhancer = create_reasoning_enhancer(level="high", mode="auto")
        >>>
        >>> # Force prompt mode (universal)
        >>> enhancer = create_reasoning_enhancer(level="high", mode="prompt")
        >>>
        >>> # Force native mode (V2 only)
        >>> enhancer = create_reasoning_enhancer(
        ...     level="high",
        ...     mode="native",
        ...     budget_tokens=2000
        ... )
    """
    config = ReasoningConfig(
        level=ReasoningLevel(level),
        mode=ReasoningMode(mode),
        **config_kwargs
    )
    return ReasoningEnhancer(default_config=config)