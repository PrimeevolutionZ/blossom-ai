"""
Blossom AI - Reasoning Module
Enhances prompts with reasoning capabilities for better AI responses
"""

from typing import Optional, Literal, Dict, Any, Union, List
from dataclasses import dataclass
from enum import Enum


class ReasoningLevel(str, Enum):
    """Reasoning complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ADAPTIVE = "adaptive"  # Automatically choose based on prompt complexity


@dataclass
class ReasoningConfig:
    """Configuration for reasoning enhancement"""
    level: ReasoningLevel = ReasoningLevel.MEDIUM
    max_reasoning_tokens: Optional[int] = None
    include_confidence: bool = False
    structured_thinking: bool = True
    chain_of_thought: bool = True

    # Advanced options
    self_critique: bool = False  # For HIGH level
    alternative_approaches: bool = False  # Consider multiple solutions
    step_verification: bool = False  # Verify each reasoning step


# Reasoning prompts for different levels
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

    Example:
        >>> enhancer = ReasoningEnhancer()
        >>> enhanced = enhancer.enhance(
        ...     "How do I optimize database queries?",
        ...     level="high"
        ... )
        >>> # Use enhanced prompt with your text generator
        >>> result = text_gen.generate(enhanced)
    """

    def __init__(self, default_config: Optional[ReasoningConfig] = None):
        self.default_config = default_config or ReasoningConfig()

    def enhance(
            self,
            prompt: str,
            level: Optional[Union[str, ReasoningLevel]] = None,
            config: Optional[ReasoningConfig] = None,
            context: Optional[str] = None,
            examples: Optional[List[str]] = None
    ) -> str:
        """
        Enhance a prompt with reasoning instructions

        Args:
            prompt: Original user prompt
            level: Reasoning level (low, medium, high, adaptive)
            config: Custom reasoning configuration
            context: Additional context to include
            examples: Example reasoning patterns

        Returns:
            Enhanced prompt with reasoning instructions
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

        # Build enhanced prompt
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
        if cfg.include_confidence and level in [ReasoningLevel.MEDIUM, ReasoningLevel.HIGH]:
            parts.append("\n[Please include confidence level: LOW/MEDIUM/HIGH]")

        if cfg.alternative_approaches and level == ReasoningLevel.HIGH:
            parts.append("[Consider at least 2-3 different approaches]")

        if cfg.self_critique and level == ReasoningLevel.HIGH:
            parts.append("[Critically evaluate your own reasoning]")

        if cfg.step_verification:
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
        Extract reasoning from AI response

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


class ReasoningChain:
    """
    Multi-step reasoning chain for complex problems

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
            level: ReasoningLevel = ReasoningLevel.HIGH
    ) -> Dict[str, Any]:
        """
        Solve problem through multi-step reasoning chain

        Args:
            problem: Problem to solve
            steps: Custom steps or None for automatic
            level: Reasoning level for each step

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
            enhanced = self.enhancer.enhance(step_prompt, level=level)

            # Generate response (handle both sync and async)
            if hasattr(self.generator, 'generate') and callable(self.generator.generate):
                import inspect
                if inspect.iscoroutinefunction(self.generator.generate):
                    response = await self.generator.generate(enhanced)
                else:
                    response = self.generator.generate(enhanced)
            else:
                raise ValueError("Invalid text generator")

            # Extract reasoning
            parsed = self.enhancer.extract_reasoning(response)

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

        if hasattr(self.generator, 'generate') and callable(self.generator.generate):
            import inspect
            if inspect.iscoroutinefunction(self.generator.generate):
                final = await self.generator.generate(synthesis_prompt)
            else:
                final = self.generator.generate(synthesis_prompt)

        results['final_answer'] = final

        return results


# Integration with Blossom client
def add_reasoning_to_blossom():
    """
    Monkey-patch to add reasoning to Blossom client

    Usage:
        >>> from blossom_ai.utils.reasoning import add_reasoning_to_blossom
        >>> add_reasoning_to_blossom()
        >>>
        >>> client = Blossom()
        >>> result = client.text.generate_with_reasoning(
        ...     "How to optimize Python code?",
        ...     level="high"
        ... )
    """
    from blossom_ai.generators.blossom import HybridTextGenerator

    def generate_with_reasoning(self, prompt: str, level="medium", **kwargs):
        """Generate text with reasoning enhancement"""
        enhancer = ReasoningEnhancer()
        enhanced_prompt = enhancer.enhance(prompt, level=level)
        response = self._call("generate", enhanced_prompt, **kwargs)
        return enhancer.extract_reasoning(response) if isinstance(response, str) else response

    # Add method to HybridTextGenerator
    HybridTextGenerator.generate_with_reasoning = generate_with_reasoning


# Convenience function
def create_reasoning_enhancer(
        level: str = "medium",
        **config_kwargs
) -> ReasoningEnhancer:
    """
    Create a reasoning enhancer with custom configuration

    Args:
        level: Default reasoning level
        **config_kwargs: Additional ReasoningConfig parameters

    Returns:
        Configured ReasoningEnhancer instance
    """
    config = ReasoningConfig(level=ReasoningLevel(level), **config_kwargs)
    return ReasoningEnhancer(default_config=config)